import math
import random

from client import *
import numpy as np

cycle_num = 0

def init_players():
    '''
    Here you can set each of your player's name and your team formation.
    In case of setting wrong position, server will set default formation for your team.
    '''

    players = [Player(name="0", first_pos=Pos(-6.5, 1.1)),
               Player(name="1", first_pos=Pos(-6.5, -0)),
               Player(name="2", first_pos=Pos(-6.5, -1.1)),
               Player(name="3", first_pos=Pos(-5, 0)),
               Player(name="4", first_pos=Pos(-2, 0))]
    return players


def dist_two_point(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def conflict(x1, y1, ang, players):
    m = math.tan(math.radians(ang))
    x2 = 10
    y2 = m * (x2 - x1) + y1
    p1 = np.array([x2, y2])
    p2 = np.array([x1, y1])
    closest_obj = -1
    closest_dist = 1000
    for pid in players:
        b1 = pid.getPosition().getX()
        b2 = pid.getPosition().getY()
        p3 = np.array([b1, b2])
        d = abs(np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1))
        if d < .75 and isinstance(pid, Ball) and dist_two_point(x1, y1, b1, b2) < closest_dist:
            # print("ball in ", pid.getPosition().getX(), " ", pid.getPosition().getY(), "is conflicted:")
            # print("d is: ", d)
            # print("type of ball : ", type(pid))
            closest_dist = dist_two_point(x1, y1, b1, b2)
            closest_obj = pid
        elif d < 1 and dist_two_point(x1, y1, b1, b2) < closest_dist:
            # print("player in ", pid.getPosition().getX(), " ", pid.getPosition().getY(), "is conflicted:")
            # print("d is: ", d)
            closest_dist = dist_two_point(x1, y1, b1, b2)
            closest_obj = pid
    if closest_obj == -1:
        return False
    else:
        return True


def get_needed_power(dis):
    return (dis * 50) / 4.720186


def get_slope(p1, p2):
    return math.degrees(math.atan2(p2[1] - p1[1], p2[0] - p1[0]))


def get_ball_ang(p_slope, b_slope, ang):
    if p_slope[1] < p_slope[0]:
        p_slope = (p_slope[1], p_slope[0])
    if b_slope[1] < b_slope[0]:
        b_slope = (b_slope[1], b_slope[0])
    coef = 180 / (p_slope[1] - p_slope[0])
    return b_slope[1] - coef * (ang - p_slope[0])


def intersection_line_circle(p1, p2, q, r):
    p1 = np.array(p1)
    p2 = np.array(p2)
    q = np.array(q)
    v = p2 - p1
    a = np.dot(v, v)
    b = 2 * (np.dot(v, (p1 - q)))
    c = np.dot(p1, p1) + np.dot(q, q) - (2 * np.dot(p1, q)) - (r * r)
    disc = b ** 2 - 4 * a * c
    if disc < 0:
        return -1
    sqrt_disc = math.sqrt(disc)
    t1 = (-b + sqrt_disc) / (2 * a)
    t2 = (-b - sqrt_disc) / (2 * a)
    if not (0 <= t1 <= 1 or 0 <= t2 <= 1):
        return -1
    pans1 = p1 + t1 * v
    pans1 = tuple(pans1)
    pans2 = p1 + t2 * v
    pans2 = tuple(pans2)
    return [pans1, pans2]

def bullshit_to_be_added(p_slope, diff):
    bull = 10
    return (bull * diff * (p_slope[1] - p_slope[0])) / 180


def best_shoot(ball, player):

    target = [(7, 1.1), (7, -1.1)]
    x1 = player[0]
    y1 = player[1]
    x2 = ball[0]
    y2 = ball[1]

    q = [x2, y2]
    slope = (y2 - y1) / (x2 - x1)
    if -0.001 < slope < 0.001:
        slope = 0.001
    slope = (1 / slope) * -1
    p1 = [10, (slope * (10 - x2) + y2)]
    p2 = [-10, (slope * (-10 - x2) + y2)]
    r = .75
    inter = intersection_line_circle(p1, p2, q, r)
    # print(inter)
    player_slope_range = (get_slope((x1, y1), inter[0]), get_slope((x1, y1), (inter[1])))
    # print(player_slope_range)
    ball_slope_range = (get_slope(inter[0], (x2, y2)), get_slope(inter[1], (x2, y2)))
    # print(ball_slope_range)
    # print(get_ball_ang(player_slope_range, ball_slope_range, 32))
    target_slope_range = (get_slope((x2, y2), target[1]), get_slope((x2, y2), target[0]))

    if player_slope_range[1] < player_slope_range[0]:
        player_slope_range = (player_slope_range[1], player_slope_range[0])
    if ball_slope_range[1] < ball_slope_range[0]:
        ball_slope_range = (ball_slope_range[1], ball_slope_range[0])
    if target_slope_range[1] < target_slope_range[0]:
        target_slope_range = (target_slope_range[1], target_slope_range[0])
    # print(target_slope_range)
    final_angle = 1000
    fitter = (player_slope_range[1] - player_slope_range[0]) / 5
    player_slope_range2 = (player_slope_range[0] + fitter, player_slope_range[1] - fitter)
    # print(player_slope_range)
    best_slope = get_slope((x2, y2), (7, 0))
    for ang in range(int(player_slope_range2[0]), int(player_slope_range2[1])):
        if target_slope_range[0] < get_ball_ang(player_slope_range, ball_slope_range, ang) < target_slope_range[1]:
            if final_angle == 1000:
                final_angle = ang
            elif abs(get_ball_ang(player_slope_range, ball_slope_range, final_angle) - best_slope) > abs(get_ball_ang(player_slope_range, ball_slope_range, ang) - best_slope):
                final_angle = ang
    diff_from_expected = abs(get_ball_ang(player_slope_range, ball_slope_range, final_angle) - best_slope)
    # print("diff slope from expected", diff_from_expected)
    bullshit_added = bullshit_to_be_added(player_slope_range, diff_from_expected)
    # print("bull aded :", bullshit_added)
    if best_slope > get_ball_ang(player_slope_range, ball_slope_range, final_angle) and final_angle != 1000:
        final_angle += bullshit_added
    elif final_angle != 1000:
        final_angle -= bullshit_added
    return [final_angle, get_ball_ang(player_slope_range, ball_slope_range, final_angle)]


def do_turn(game):
    act = Triple()
    global cycle_num
    cycle_num +=1
    opp_gate_pos = [(7, 1.4), (7, -1.4)]
    player_id = -1
    opp_players = []
    opp_and_baal = []
    my_players = []
    angle = 0
    for pid in range(0, 5):
        opp_players.append(game.getOppTeam().getPlayer(pid))
        opp_and_baal.append(game.getOppTeam().getPlayer(pid))
        my_players.append(game.getMyTeam().getPlayer(pid))
    opp_and_baal.append(game.getBall())


    final_angle = 0
    found = -1
    for pid in range(0, 5):
        x1 = game.getMyTeam().getPlayer(pid).getPosition().getX()
        y1 = game.getMyTeam().getPlayer(pid).getPosition().getY()
        if x1 > game.getBall().getPosition().getX():
            continue

        x2 = game.getBall().getPosition().getX()
        y2 = game.getBall().getPosition().getY()
        if get_needed_power(dist_two_point(x1, y1, x2, y2)) > 95:
            continue

        if best_shoot((x2, y2), (x1, y1))[0] != 1000:
            angle_of_this_shoot = best_shoot((x2, y2), (x1, y1))[0]
            best_slope = get_slope((x2, y2), (7, 0))
            dist_last_from_ball = dist_two_point(game.getMyTeam().getPlayer(player_id).getPosition().getX(), game.getMyTeam().getPlayer(player_id).getPosition().getY(), x2, y2)
            if found == -1:
                player_id = pid
                final_angle = angle_of_this_shoot
                print("eccured by best function - 1")
            elif dist_last_from_ball > dist_two_point(x1, y1, x2, y2): #and abs(dist_last_from_ball - dist_two_point(x1, y1, x2, y2)) > 2.5:
                player_id = pid
                final_angle = angle_of_this_shoot
                print("eccured by best function - 2")
            # elif abs(best_slope - final_angle) > abs(best_slope - angle_of_this_shoot): #BUGGGG
            #     player_id = pid
            #     final_angle = angle_of_this_shoot
            #     print("eccured by best function - 3")

            found = 1
    if found == -1:
        final_angle = 180
        for pid in range(0, 5):
            x1 = game.getMyTeam().getPlayer(pid).getPosition().getX()
            y1 = game.getMyTeam().getPlayer(pid).getPosition().getY()
            if x1 > game.getBall().getPosition().getX():
                continue
            x2 = game.getBall().getPosition().getX()
            y2 = game.getBall().getPosition().getY()
            if x2 > 3 and x1 > 0:
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
                if abs(angle) < abs(final_angle):
                    final_angle = angle
                    player_id = pid
                    print("eccured by second")
                    found = 1
    if found == -1:
        final_angle = 180
        for pid in range(0, 5):
            x1 = game.getMyTeam().getPlayer(pid).getPosition().getX()
            y1 = game.getMyTeam().getPlayer(pid).getPosition().getY()
            if x1 > game.getBall().getPosition().getX():
                continue
            x2 = game.getBall().getPosition().getX()
            y2 = game.getBall().getPosition().getY()
            if get_needed_power(dist_two_point(x1, y1, x2, y2)) > 95:
                continue
            angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
            if abs(angle) < abs(final_angle):
                final_angle = angle
                player_id = pid
                print("accured by smallest angle")
                found = 1
    print("round : ", cycle_num)
    if found == -1:
        print("here")
        final_angle = 180
        for pid in range(0, 5):
            x1 = game.getMyTeam().getPlayer(pid).getPosition().getX()
            y1 = game.getMyTeam().getPlayer(pid).getPosition().getY()
            if x1 < game.getBall().getPosition().getX():
                continue
            for ang in range(-85, 85):
                if ang < 0:
                    ang -= 90
                else:
                    ang += 90
                if not conflict(x1, y1, ang, opp_and_baal):
                    final_angle = ang # bug -> chose the closest player to the ball
                    player_id = pid
                    print("eccured by tokhm")

    act.setPlayerID(player_id)
    if final_angle < 0:
        final_angle += 360
    act.setAngle(final_angle)

    act.setPower(100)

    return act
