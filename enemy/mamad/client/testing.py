import numpy as np
import math


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


def best_shoot(ball, player):

    target = [(7, 1.15), (7, -1.15)]
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
    r = 1.5
    inter = intersection_line_circle(p1, p2, q, r)
    print(inter)
    player_slope_range = (get_slope((x1, y1), inter[0]), get_slope((x1, y1), (inter[1])))
    print(player_slope_range)
    ball_slope_range = (get_slope(inter[0], (x2, y2)), get_slope(inter[1], (x2, y2)))
    print(ball_slope_range)
    print(get_ball_ang(player_slope_range, ball_slope_range, 32))
    target_slope_range = (get_slope((x2, y2), target[1]), get_slope((x2, y2), target[0]))

    if player_slope_range[1] < player_slope_range[0]:
        player_slope_range = (player_slope_range[1], player_slope_range[0])
    if ball_slope_range[1] < ball_slope_range[0]:
        ball_slope_range = (ball_slope_range[1], ball_slope_range[0])
    if target_slope_range[1] < target_slope_range[0]:
        target_slope_range = (target_slope_range[1], target_slope_range[0])
    print(target_slope_range)
    final_angle = 1000
    # fitter = (player_slope_range[1] - player_slope_range[0]) / 6
    # player_slope_range = (player_slope_range[0] + fitter, player_slope_range[1] - fitter)
    print(player_slope_range)
    for ang in range(int(player_slope_range[0]), int(player_slope_range[1])):
        if target_slope_range[0] < get_ball_ang(player_slope_range, ball_slope_range, ang) < target_slope_range[1]:
            final_angle = ang
            break

    return final_angle


def defence(player, ball):
    my_gate = (-7, 0)
    target = tuple((np.array(my_gate) + np.array(ball))/2)
    print(target)
    print(math.radians(get_slope(player, target)))
    slope = math.tan(math.radians(get_slope(player, target)))
    print(slope)

# print("final angle : ", best_shoot((5, 3), (-2, 0)))
defence((2, -1), (2, -2))