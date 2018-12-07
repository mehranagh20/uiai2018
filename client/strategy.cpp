#include <assert.h>
#include <algorithm>
#include "strategy.h"
#include "game.h"

Strategy::Strategy() {

}

Player *Strategy::init_players() {
    Player *players = new Player[5];
    /*
    Here you can set each of your player's name and your team formation.
    In case of setting wrong position, server will set default formation for your team.
     */

    /* TODO later
     *     players = [Player(name="player_1", first_pos=Pos(-6.5, .6)),
               Player(name="player_2", first_pos=Pos(-6.5, -.6)),
               Player(name="player_3", first_pos=Pos(-4, 0)),
               Player(name="player_4", first_pos=Pos(-3, -2)),
               Player(name="player_5", first_pos=Pos(-3, 2))]

     */

    players[0] = Player("Mehran", Pos(-6.5, 1.2), 0);
    players[1] = Player("Mamad", Pos(-6, 0), 1);
    players[2] = Player("Alireza.Koochooloo", Pos(-6.5, -1.2), 2);
    players[3] = Player("The Alireza", Pos(-1, 0), 3);
    players[4] = Player("Nokhodi", Pos(-2.5, 0), 4);

    return players;

}

#define VERBOSITY 1
double OPP_GOAL_X = 7;
double OUR_GOAL_X = -7;
double OPP_GOAL_Y_BEG = 1.4;
double OPP_GOAL_Y_END = -1.4;
double eps = 1e-7;
double DANGOR_ZONE_X = -1;
double DANGOR_ZONE_Y = 2.5;
double CORNER_TRESHOLD = 2.5;
#define inf 1e7
#define BID -100

double BALL_R = .25;
double PLAYER_R = 0.5;
double pi = acos(-1);

struct point {
    double x, y;
    bool valid = false;

    point(double x, double y, bool valid = true) {
        this->x = x, this->y = y, this->valid = valid;
    }
};

struct obj {
    double x, y, r;
    int id;
    bool mine = true;
    bool valid = true;

    obj(double x, double y, double r, int id, bool mine = true, bool valid = true) {
        this->x = x, this->y = y, this->r = r, this->id = id, this->mine = mine, this->valid = valid;
    }

    bool operator<(const obj &a) const {
        return x < a.x;
    }
};

struct candidate {
    int id;
    double diff, deg;
    bool valid = false;
    int power;
    double x, y;
    double ballDeg;

    candidate(int id, double deg, double ballDeg, bool valid, double x = -1, double y = -1, int power = 100) {
        this->x = x, this->y = y, this->id = id, this->deg = deg, this->diff = fabs(deg - ballDeg), this->valid = valid, this->power = power;
        this->ballDeg = ballDeg;
    }

    bool operator<(const candidate &can) {
        return this->diff < can.diff;
    }
};

struct line {
    double a, b, c;
    bool valid = true;

    line(double a, double b, double c, bool valid = true) {
        this->a = a, this->b = b, this->c = c, this->valid = valid;
    }
};


line point_slop_to_line(double x, double y, double m) {
    double a = -m;
    double b = 1;
    double c = -((a * x) + (b * y));
    return line(a, b, c);
}

vector<obj> mirro(vector<obj> &basic) {
    vector<obj> mir = basic;
    for (auto &e: mir) e.x *= -1, e.y *= -1;
    return mir;
}

int getNeededPower(double dis) {
    return (int) floor((dis * 50) / 4.720186);
}

double get_x(line l, double y) {
    return (-l.b * y - l.c) / l.a;
}

double get_y(line l, double x) {
    return (-l.a * x - l.c) / l.b;
}

double shortest_distance(double x, double y, line l) {
    return abs((l.a * x + l.b * y + l.c)) / (sqrt(l.a * l.a + l.b * l.b));
}

double radians(double theta) { return theta * pi / 180.0; }

double degrees(double theta) { return theta * 180.0 / pi; }

obj first_colid(double deg, obj check, vector<obj> others) {
    double m = tan(radians(deg));
    line l = point_slop_to_line(check.x, check.y, m);
    vector<obj> good;
    for (auto &e: others)
        if (e.x > check.x && e.id != check.id)
            good.push_back(e);

    sort(good.begin(), good.end());
    for (auto &e: good)
        if (e.x > check.x) {
            double shortest_dis = shortest_distance(e.x, e.y, l);
            if (shortest_dis - (check.r + e.r) < -eps)
                return e;
        }
    return obj(-1, -1, -1, -1, false, false);
}

double point_dist(double x1, double y1, double x2, double y2) {
    return sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2));
}

bool do_colide(obj f, obj s) {
    return point_dist(f.x, f.y, s.x, s.y) - f.r + s.r < eps;
}

point line_circle_intersection(line l, obj ball, int bullshit = 2, double remR = PLAYER_R) {
    double p = ball.x, q = ball.y, r = ball.r + remR + eps;
    double m = -l.a;
    double c = -l.c;
    double A = m * m + 1;
    double B = 2 * (m * c - m * q - p);
    double C = q * q - r * r + p * p - 2 * c * q + c * c;
    double delta = B * B - (4 * A * C);
    if (delta < -eps)
        return point(-1, -1, false);
    double x = (-B - bullshit * sqrt(delta)) / (2 * A); // todo bullshit!
    double y = m * x + c;
    return point(x, y);
}

bool in_goal(double y, double r) {
    return (OPP_GOAL_Y_BEG - r - y > eps && y - (OPP_GOAL_Y_END + r) > eps);
}

bool canScore(double deg, obj ball, vector<obj> al, int id = -1) {
    obj col = first_colid(deg, ball, al);
    if (!col.valid) {
        double m = tan(radians(deg));
        line cur_line = point_slop_to_line(ball.x, ball.y, m);
        double y = get_y(cur_line, OPP_GOAL_X);
        if (in_goal(y, ball.r)) {
            return true;
        }
    }
    return false;
}

vector<candidate> scoreCandidates(obj ball, vector<obj> mine, vector<obj> al) { // returns id, deg
    sort(mine.begin(), mine.end());
    vector<candidate> candidates;
    for (auto &e: mine)
        if (e.x < ball.x) {
            for (double i = 75; i >= -75; i -= .5) {
                obj f_col = first_colid(i, e, al);
                if (f_col.valid && f_col.id == ball.id) {
                    double m = tan(radians(i));
                    line cur_line = point_slop_to_line(e.x, e.y, m);
                    point p = line_circle_intersection(cur_line, ball);
                    if (p.valid && p.x > e.x) {
                        double radian_angle = abs(atan((ball.y - p.y) / (ball.x - p.x)));
                        if (p.y > ball.y) radian_angle *= -1;
                        if(e.id == 4 && i == 17) printf("%lf, %lf done\n", p.x, p.y);
                        double deg = degrees(radian_angle);
//                        if(e.id == 0) printf("found for 0: %lf\n", deg);
                        if (canScore(deg, ball, al, e.id))
                            candidates.push_back(candidate(e.id, i, deg, true, e.x, e.y));
                    }
                }
            }
        }
    return candidates;
}

candidate tryToScore(obj ball, vector<obj> mine, vector<obj> al) {
    vector<candidate> candidates = scoreCandidates(ball, mine, al);
    printf("found %d chances to score, trying to find the best one...\n", (int) candidates.size());
    random_shuffle(candidates.begin(), candidates.end());
    if (candidates.size() == 0) return candidate(0, 0, 0, false);
    vector<candidate> real;
    for(int i = 0; i < 3; i++) {
        int x = random() % candidates.size();
        real.push_back(candidates[x]);
    }
    candidate best(-1, -1, -1, false);
    double cur_x = -inf;
    for(auto &e: real) if(e.x > cur_x)
            cur_x = e.x, best = e;
    return best;
}

candidate getBehindTheBall(obj ball, obj bestMine, double m, double dist = 3.8) {
    double radian_angle = fabs(atan(m));
    double y = dist * sin(radian_angle);
    double x = dist * cos(radian_angle);
    double good_x = ball.x - x, good_y = ball.y;
    if (m < 0) good_y += y;
    else good_y -= y;
    radian_angle = abs(atan((good_y - bestMine.y) / (good_x - bestMine.x)));
    int degree_angle = (int) round(degrees(radian_angle));
    double x1 = bestMine.x, x2 = good_x, y1 = bestMine.y, y2 = good_y;
    if (x2 > x1) {
        if (y2 < y1)
            degree_angle = 360 - degree_angle;
    } else {
        if (y2 < y1)
            degree_angle += 180;
        else
            degree_angle = 180 - degree_angle;
    }
    double dis = point_dist(good_x, good_y, bestMine.x, bestMine.y);
    if(dis < .6)
        return candidate(-1, -1, -1, false);
    int pow = getNeededPower(dis);
    return candidate(bestMine.id, degree_angle, -1, true, good_x, good_y, pow);
}

candidate tryGettingBehindTheBall(obj ball, vector<obj> mine, vector<obj> al, bool notCare = false, double dist = 2.8, double xx = OUR_GOAL_X, double yy = 0) {
    double m = (ball.y - yy) / (ball.x - xx);
    line l = point_slop_to_line(ball.x, ball.y, m);
    bool isOk = false;
    for (auto &e: al)
        if (e.x - ball.x < -eps) {
            double dis = shortest_distance(e.x, e.y, l);
            if (dis <= e.r) {
                if (point_dist(e.x, e.y, ball.x, ball.y) <= dist + 2) { // todo 4?
                    isOk = true;
                    printf("There are players blocking the ball dir to our goal in pos %lf, %lf\n", e.x, e.y);
                    break;
                }
            }
        }
    if (!isOk || notCare) {
        printf("trying to find a player to get behind the ball\n");
        obj bestMine(-1, -1, -1, -1, true, false);
        double curDis = inf;
        for (auto &e: mine) {
            double radian_angle = abs(atan((ball.y - e.y) / (ball.x - e.x)));
            double deg = degrees(radian_angle);
            if (e.x < ball.x || deg >= 45) {
                if (point_dist(e.x, e.y, ball.x, ball.y) < curDis) {
                    curDis = point_dist(e.x, e.y, ball.x, ball.y);
                    bestMine = e;
                }
            }
        }
        if (!bestMine.valid) {
            printf("WE ARE FUCKED DUDE :))))\n");
        } else {
            return getBehindTheBall(ball, bestMine, m, dist);
        }
    }
    return candidate(-1, -1, -1, false, -1);
}

candidate makeBallGoAway(obj ball , vector<obj> mine, vector<obj> al) {
    sort(mine.begin(), mine.end());
    vector<candidate> cands;
    vector<candidate> colCands;
    for(auto &e: mine) if(e.x < ball.x) {
            for (double i = 60; i >= -60; i -= .5) {
                obj f_col = first_colid(i, e, al);
                if (f_col.valid && f_col.id == ball.id) {
                    double m = tan(radians(i));
                    line cur_line = point_slop_to_line(e.x, e.y, m);
                    point p = line_circle_intersection(cur_line, ball);
                    if (p.valid && p.x > e.x) {
                        double radian_angle = abs(atan((ball.y - p.y) / (ball.x - p.x)));
                        if (p.y > ball.y) radian_angle *= -1;
                        double deg = degrees(radian_angle);
                        if(deg > 55 || deg < -55) // todo
                            continue;
                        f_col = first_colid(deg, ball, al);
                        if(f_col.valid) colCands.push_back(candidate(e.id, i, deg, true,
                            f_col.x, f_col.y, 100));
                        else cands.push_back(candidate(e.id, i, deg, true, 0, 0, 100));
                    }
                }
            }
        }
    if(cands.size()) {
        sort(cands.begin(), cands.end());
        int sz = cands.size() - 1, rnd = random() % 3;
        int x = min(sz, rnd);
        return cands[x];
    }
//    if(colCands.size()) {
//        int id = 0;
//        for(int i = 0; i < colCands.size(); i++) if(colCands[i].x > colCands[id].x)
//                id = i;
//        return colCands[id];
//    }mehranagh200
    return candidate(-1, -1, -1, false);
}

candidate handleDangerZone(obj ball, vector<obj> mine, vector<obj> al) {
    candidate cand = makeBallGoAway(ball, mine, al);
    if(cand.valid)
        return cand;

    cand = tryGettingBehindTheBall(ball, mine, al, false, .8);
    if(!cand.valid)
        return cand;
    auto p = mine[0];
    for(auto &e: mine) if(e.id == cand.id)
            p = e;
    double dist = point_dist(p.x, p.y, cand.x, cand.y);
    if(dist <= .8)
        return candidate(-1, -1, -1, false);
    return cand;
}

candidate handleCornerPlayers(obj ball, vector<obj> mine, vector<obj> al) {
    vector<obj> better;
    for(auto &e: mine) if(e.x < ball.x && (e.y > CORNER_TRESHOLD || e.y < -CORNER_TRESHOLD)) {
            better.push_back(e);
        }
    if(!better.size()) return candidate(-1, -1, -1, false);
    obj worst_best = better[0];
    for(auto &e: better) if(e.x < worst_best.x)
            worst_best = e;
    vector<obj> fakeMine = {worst_best};
    return tryGettingBehindTheBall(ball, fakeMine, al, true, 2);
}

candidate handleDumbPlayers(obj ball, vector<obj> mine, vector<obj> al) {
    vector<obj> dumbs;
    for(auto &e: mine) if(e.x > ball.x && e.x > 0)
            dumbs.push_back(e);
    if(!dumbs.size())
        return candidate(-1, -1, -1, false);
    int x = random() % dumbs.size();
    obj rnd = dumbs[x];
    double xx = ball.x - fabs(OUR_GOAL_X - ball.x) / 2, yy = ball.y;
    if(ball.y > 0) {
        // below wall
        double wy = -4, wx = (xx + rnd.x) / 2;
        double dist = point_dist(rnd.x, rnd.y, wx, wy) * 2.1; // todo
        int pow = getNeededPower(dist);
        double radian_angle = abs(atan((rnd.y - wy) / (rnd.x - wx)));
        int degree_angle = (int) round(degrees(radian_angle));
        double x1 = rnd.x, x2 = wx, y1 = rnd.y, y2 = wy;
        if (x2 > x1) {
            if (y2 < y1)
                degree_angle = 360 - degree_angle;
        } else {
            if (y2 < y1)
                degree_angle += 180;
            else
                degree_angle = 180 - degree_angle;
        }
        return candidate(rnd.id, degree_angle, -1, true, -1, -1, pow);
    } else {
        // above wall
        double wy = 4, wx = (xx + rnd.x) / 2;
        double dist = point_dist(rnd.x, rnd.y, wx, wy) * 2.1; // todo
        int pow = getNeededPower(dist);
        double radian_angle = abs(atan((rnd.y - wy) / (rnd.x - wx)));
        int degree_angle = (int) round(degrees(radian_angle));
        double x1 = rnd.x, x2 = wx, y1 = rnd.y, y2 = wy;
        if (x2 > x1) {
            if (y2 < y1)
                degree_angle = 360 - degree_angle;
        } else {
            if (y2 < y1)
                degree_angle += 180;
            else
                degree_angle = 180 - degree_angle;
        }
        return candidate(rnd.id, degree_angle, -1, true, -1, -1, pow);
    }

}

candidate handleBlokcers(obj ball, vector<obj> mine, vector<obj> al) {
    for(auto &e: mine) if(e.x > ball.x) {
            if(point_dist(ball.x, ball.y, e.x, e.y) <= 2 * (ball.r + e.r)) {
                double radian_angle = abs(atan((ball.y - e.y) / (ball.x - e.x)));
                double deg = degrees(radian_angle);
                if(deg <= 30) {
                    return candidate(e.id, 45, -1, true, -1, -1, 40);
                }
            }
        }
    return candidate(-1, -1, -1, false);
}

candidate handleBulshitly(obj ball, vector<obj> mine, vector<obj> al) {
    vector<obj> maybe;
    vector<candidate> idk;
    for(auto &e: mine) if(e.x - ball.x > 1.5) {
            double radian_angle = abs(atan((ball.y - e.y) / (ball.x - e.x)));
            if(e.y > ball.y) radian_angle *= -1;
            double deg = degrees(radian_angle);
            obj col = first_colid(deg, e, al);
            if(col.valid && col.id == -100) {
                maybe.push_back(e);
                col = first_colid(deg, ball, al);
                if(!col.valid) idk.push_back(candidate(e.id, deg, deg, true, -1, -1, 100));
            }
        }
    if(idk.size()) {
        int x = random() % idk.size();
        return idk[x];
    }
    if(maybe.size()) {
        auto id = maybe[0];
        for(auto &e: maybe) {
            if(fabs(e.y - ball.y) < fabs(id.y - ball.y))
                id =  e;
        }
        double radian_angle = abs(atan((ball.y - id.y) / (ball.x - id.x)));
        if(id.y > ball.y) radian_angle *= -1;
        double deg = degrees(radian_angle);
        return candidate(id.id, deg, -1, true, -1, -1, 100);
    }
    double dis = inf;
    obj mi = mine[0];
    random_shuffle(mine.begin(), mine.end());
    for(auto &e: mine) {
        if(point_dist(ball.x, ball.y, e.x, e.y) < dis) {
            dis = point_dist(ball.x, ball.y, e.x, e.y);
            mi = e;
        }
    }
    double radian_angle = abs(atan((ball.y - mi.y) / (ball.x - mi.x)));
    if(mi.y > ball.y) radian_angle *= -1;
    double deg = degrees(radian_angle);
    return candidate(mi.id, deg, deg, -1, -1, 40);
}

Triple getAct(int id, int deg, int pow) {
    Triple act;
    act.setPower(pow);
    if (deg < 0) deg += 360;
    act.setAngle(deg);
    act.setPlayerID(id);
    return act;
}

Triple Strategy::do_turn(Game *game) {
    /**
     * try to get the ball away? how? for example in our goal line!
     * Handle wall hits! (just in first_collide?)
     *
     * Main strategy:
     * KEEP IT SIMPLE STUPID!!!
     * Score if you can (of course!)
     * if ball.x < DANGER_ZONE then get as near as fucking possible!
     * else get behind the wall if necessary
     * get players in the corner near goal
     * get players in our field behind the wall!
     * Get behind the ball if none of above is possible
     * Defend our goal in the line!
     */
    srand(time(NULL));

//    auto p = game->get_myTeam()->get_players()[0];
//    printf("%lf, %lf\n", p.get_pos().get_x(), p.get_pos().get_y());
//    printf("%lf\n", point_dist(p.get_pos().get_x(), p.get_pos().get_y(), -6, 2.5));
//    return getAct(0, 0, 50);


    // Some initialization
    double ball_x = game->get_ball()->get_Position().get_x();
    double ball_y = game->get_ball()->get_Position().get_y();
    obj ball = {ball_x, ball_y, BALL_R, -100};
    vector<obj> mine, al, hers, alMir;
    for (int i = 0; i < 5; i++) {
        Player p = game->get_myTeam()->get_players()[i];
        al.push_back({p.get_pos().get_x(), p.get_pos().get_y(), PLAYER_R, i});
        mine.push_back({p.get_pos().get_x(), p.get_pos().get_y(), PLAYER_R, i});
    }
    for (int i = 0; i < 5; i++) {
        Player p = game->get_oppTeam()->get_players()[i];
        al.push_back({p.get_pos().get_x(), p.get_pos().get_y(), PLAYER_R, i, false});
        hers.push_back({p.get_pos().get_x(), p.get_pos().get_y(), PLAYER_R, i, false});
    }
    al.push_back(ball);
    alMir = mirro(al);

    printf("trying to score...\n");
    candidate can = tryToScore(ball, mine, al);
    if (can.valid) {
        printf("found %d %lf to score\n", can.id, can.deg);
        printf("Shooting\n");
        if(can.y > 3.4 || can.y < -3.4) { // todo
            auto m = mine[0];
            for(auto &e: mine) if(e.id == can.id)
                    m = e;
            double radian_angle = abs(atan((ball.y - m.y) / (ball.x - m.x)));
            if(m.y > ball.y) radian_angle *= -1;
            double deg = degrees(radian_angle);
            can.deg = deg;
        }
        return getAct(can.id, can.deg, can.power);
    }

    printf("Applying second strategy\n");
    if ((ball.x < DANGOR_ZONE_X) && (ball.y < DANGOR_ZONE_Y && ball.y > -DANGOR_ZONE_Y)) {
        printf("we are in danger zone\n");
        candidate cand = handleDangerZone(ball, mine ,al);
        if(cand.valid)
            return getAct(cand.id, cand.deg, cand.power);

    } else {
        printf("Try to get behind the wall if necessary\n");
        candidate candidate = tryGettingBehindTheBall(ball, mine, al);
        if (candidate.valid) {
            return getAct(candidate.id, candidate.deg, candidate.power);
        }
    }

    printf("Trying to get players in corner near ball\n");
    candidate cand = handleCornerPlayers(ball, mine, al);
    if(cand.valid)
        return getAct(cand.id, cand.deg, cand.power);

    printf("Trying to remove our blockers\n");
    cand = handleBlokcers(ball, mine, al);
    if(cand.valid)
        return getAct(cand.id, cand.deg, cand.power);


    printf("Trying to get the dumb players to our field!\n");
    cand = handleDumbPlayers(ball, mine, al);
    if(cand.valid) {
        int x = random();
        if(x % 2) return getAct(cand.id, cand.deg, cand.power);
    }

    printf("Hit the ball\n");
    cand = handleBulshitly(ball, mine, al);

    return getAct(cand.id, cand.deg, cand.power);
}
