import math
import random

from client import *


def init_players():
    '''
    Here you can set each of your player's name and your team formation.
    In case of setting wrong position, server will set default formation for your team.
    '''

    players = [Player(name="ali-biro", first_pos=Pos(-5.8, 0)),
               Player(name="sed jalal", first_pos=Pos(-6.5, 1.1)),
               Player(name="shoja", first_pos=Pos(-6.5, -1.1)),
               Player(name="kamal", first_pos=Pos(-1, 1)),
               Player(name="alipour", first_pos=Pos(-3, -0))]
    return players

def shootPreciseAngle(player, ball, angle):

    if  player.getPosition().getX() - ball.getPosition().getX() > -6  :
        print('hello')
        if 3 > player.getPosition().getY() - ball.getPosition().getY() >= 0.5 and ball.getPosition().getY() >= 0:
            print("1")
            return angle - abs(player.getPosition().getY() - ball.getPosition().getY()) * 3.5 + abs(
                player.getPosition().getX() - ball.getPosition().getX()) / 3

        if -3 <= player.getPosition().getY() - ball.getPosition().getY() <= -0.5 and ball.getPosition().getY() <= 0:
            print("2")
            return angle + abs(player.getPosition().getY() - ball.getPosition().getY()) * 3.5 - abs(
                player.getPosition().getX() - ball.getPosition().getX()) / 3

        if 3 >= ball.getPosition().getY() - player.getPosition().getY() >= 0.5 and ball.getPosition().getY() >= 0:
            print("3")
            return angle + abs(player.getPosition().getY() - ball.getPosition().getY()) * 3.5 + abs(
                player.getPosition().getX() - ball.getPosition().getX()) / 3

        if 3 < ball.getPosition().getY() - player.getPosition().getY() <= -0.5 and ball.getPosition().getY() <= 0:
            print("4")
            return angle - abs(player.getPosition().getY() - ball.getPosition().getY()) * 3.5 - abs(
                player.getPosition().getX() - ball.getPosition().getX()) / 3
        else:
            print("not in ifs")
            return angle
    else:
        return angle

def gobackPower(player):

            if player.getPosition().getX() > 0:
                disX = 7 + player.getPosition().getX()
            else:
                disX = 7 - abs(player.getPosition().getX())
            dis = abs(math.sqrt(disX ** 2 + abs(player.getPosition().getY()) ** 2))
            print(player.getPosition().getX())
            return 10 * dis

def shootball(game,k):
    '''
    selectplayer=[]
    for i in range(0,5):
        if game.getMyTeam().getPlayer(i).getPosition().getX() < game.getBall().getPosition().getX():
            selectplayer.append(game.getMyTeam().getPlayer(i))
    a1 = selectplayer[0]

    for j in range(0,selectplayer.__len__()):
        if selectplayer[j].getPosition().getX() > a1.getPosition().getX():
            a1 = selectplayer[j]

    '''

    xb = game.getBall().getPosition().getX()
    yb = game.getBall().getPosition().getY()
    xp = game.getMyTeam().getPlayer(k).getPosition().getX()
    yp = game.getMyTeam().getPlayer(k).getPosition().getY()
    angle = math.fabs(math.degrees(math.atan((yb - yp) / (xb - xp))))
    if xb > xp:
        if yb < yp:
            angle = 360 - angle
    else:
        if yb < yp:
            angle += 180
        else:
            angle = 180 - angle

    return angle



#defence

#harif defaee ye  ya na?
def isOpponentInDefenceMode(game):

    defenceCount = 0
    for i in range(5):
        opponent = game.getOppTeam().getPlayer(i)
        opX = opponent.getPosition().getX()
        opY = opponent.getPosition().getY()

        if -1.4 <= opY < 1.4 and opX > 5:
            defenceCount +=1

    if defenceCount >=2:
        return 1
    else:
        return 0



def shouldGotoDefence(game):
    defencecount = 0
    for i in range(0,5):
        x = game.getMyTeam().getPlayer(i).getPosition().getX()
        y = game.getMyTeam().getPlayer(i).getPosition().getY()
        if x < -2.5 :
            if y > -2 and y < 2:
                defencecount = defencecount + 1
    if defencecount >= 3:
        return 0
    else:
        return 1



def shouldGotoDefence1(game):
    defencecount1 = 0
    for i in range(0,5):
        x = game.getMyTeam().getPlayer(i).getPosition().getX()
        y = game.getMyTeam().getPlayer(i).getPosition().getY()
        if x < -2.5 :
            if y > -2 and y < 2:
                defencecount1 = defencecount1 + 1
    if defencecount1 >= 2:
        return 0
    else:
        return 1


def zaviyeBazgashtBeDefa(game,player):
    xd = -7
    yd = 0
    xp = player.getPosition().getX()
    yp = player.getPosition().getY()
    angle = math.fabs(math.degrees(math.atan((yd - yp) / (xd - xp))))
    if xd > xp:
        if yd < yp:
            angle = 360 - angle
    else:
        if yd < yp:
            angle += 180
        else:
            angle = 180 - angle
    return angle



# zaviyeBazgashtBeDefa vaghti hameye bazikonan jelotar az top hastand
def zaviyeBazgashtBeDefa1111(game,player):
    xd = -2.5
    yd = 3.8
    xp = player.getPosition().getX()
    yp = player.getPosition().getY()
    angle = math.fabs(math.degrees(math.atan((yd - yp) / (xd - xp))))
    if xd > xp:
        if yd < yp:
            angle = 360 - angle
    else:
        if yd < yp:
            angle += 180
        else:
            angle = 180 - angle
    return angle



# zaviyeBazgashtBeDefa vaghti top dar nahiye 4 ast
def zaviyeBazgashtBeDefa2222(game,player):
    xd = -3.5
    yd = 0
    xp = player.getPosition().getX()
    yp = player.getPosition().getY()
    angle = math.fabs(math.degrees(math.atan((yd - yp) / (xd - xp))))
    if xd > xp:
        if yd < yp:
            angle = 360 - angle
    else:
        if yd < yp:
            angle += 180
        else:
            angle = 180 - angle
    return angle


def zaviyeBazgashtBeDefa3333(game,player):
    xd = -7
    yd = 0
    xp = player.getPosition().getX()
    yp = player.getPosition().getY()
    angle = math.fabs(math.degrees(math.atan((yd - yp) / (xd - xp))))
    if xd > xp:
        if yd < yp:
            angle = 360 - angle
    else:
        if yd < yp:
            angle += 180
        else:
            angle = 180 - angle
    return angle



def zaviyeBazgashtBeDefaBalatarinY(game,player):
    xd = -7
    yd = 0.85
    xp = player.getPosition().getX()
    yp = player.getPosition().getY()
    angle = math.fabs(math.degrees(math.atan((yd - yp) / (xd - xp))))
    if xd > xp:
        if yd < yp:
            angle = 360 - angle
    else:
        if yd < yp:
            angle += 180
        else:
            angle = 180 - angle
    return angle


def zaviyeBazgashtBeDefaPaeentarinY(game,player):
    xd = -7
    yd = -0.85
    xp = player.getPosition().getX()
    yp = player.getPosition().getY()
    angle = math.fabs(math.degrees(math.atan((yd - yp) / (xd - xp))))
    if xd > xp:
        if yd < yp:
            angle = 360 - angle
    else:
        if yd < yp:
            angle += 180
        else:
            angle = 180 - angle
    return angle


def zaviyeBazgashtBeDefa1000(game,player):
    xd = -4.5
    yd = 0
    xp = player.getPosition().getX()
    yp = player.getPosition().getY()
    angle = math.fabs(math.degrees(math.atan((yd - yp) / (xd - xp))))
    if xd > xp:
        if yd < yp:
            angle = 360 - angle
    else:
        if yd < yp:
            angle += 180
        else:
            angle = 180 - angle
    return angle



#takhrib
def takhrib1(game, player1):

    xd = 7
    yd = 0
    xp = player1.getPosition().getX()
    yp = player1.getPosition().getY()
    angle = math.fabs(math.degrees(math.atan((yd - yp) / (xd - xp))))
    if xd > xp:
        if yd < yp:
            angle = 360 - angle
    else:
        if yd < yp:
            angle += 180
        else:
            angle = 180 - angle
    return angle

def do_turn(game):
    try:
        act = Triple()
        '''
        Write your code here
        At the end you have to set 3 parameter:
            player id -> act.setPlyerID()
            angle -> act.setAngle()
            power -> act.setPower()
        '''

        '''
        #jelotarin vs aghab tarin bazikonan ghabl top
    
        selectp=[]
        selectp.append(game.getMyTeam().getPlayer(1))
        for i in range(0,5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() < game.getBall().getPosition().getX():
                selectp.append(game.getMyTeam().getPlayer(i))
        print(selectp)
    
        global a
        a = selectp[0]
        global k
        k = 1
        # jelotarin bazikon ghabl top
        for j in range(0,selectp.__len__()):
            if selectp[j].getPosition().getX() > a.getPosition().getX():
                a = selectp[j]
    
                print("a",a)
    
                k = selectp[j].getId()
                print("k",k)
                print(selectp[j].getId())
    
    
    
        global b
        b=selectp[0]
        global k1
        k1 = 2
        for j in range(0,selectp.__len__()):
            if selectp[j].getPosition().getX() < b.getPosition().getX():
                b = selectp[j]
                #aghabtarin bazikon ghabl top
                k1=selectp[j].getId()
                print("k1",k1)
        print("aghabtarin bazikon ghabl top", b, k1)
    
        '''

        # jelotarin vs aghab tarin bazikonan bad top
        selectp2=[]
        selectp2.append(game.getMyTeam().getPlayer(4))
        for i in range(0,5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() > game.getBall().getPosition().getX():
                selectp2.append(game.getMyTeam().getPlayer(i))
        print(selectp2)
        global a1
        a1 = selectp2[0]
        global k2
        k2 = 4
        for j in range(0, selectp2.__len__()):
            if selectp2[j].getPosition().getX() > a1.getPosition().getX():
                a1 = selectp2[j]
                # jelotarin bazikon bad top
                k2= selectp2[j].getId()
                print("k2 ",k2)
        print("jelotarin bazikon bad top", a1, k2)

        # aghabtarin bazikon bad top
        global k3
        k3 = 3
        global bbbbbb
        bbbbbb= selectp2[0]

        for j in range(0, selectp2.__len__()):
            if selectp2[j].getPosition().getX() < bbbbbb.getPosition().getX():
                bbbbbb = selectp2[j]
                k3 = bbbbbb.getId()
                print("k3",k3)
        print("aghabtarin bazikon bad top", bbbbbb, k3)


        # bazikonanam dar zamin harif
        selectp3=[]
        selectp3.append(game.getMyTeam().getPlayer(4))
        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() > -2.5:
                selectp3.append(game.getMyTeam().getPlayer(i))



        # bazikonanam dar zamin khodam
        selectp4 = []
        #selectp4.append(game.getMyTeam().getPlayer(0))
        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() <= -2.5:
                selectp4.append(game.getMyTeam().getPlayer(i))

        # bazikon dar zamin khodam 2
        selectp5 = []
        #selectp5.append(game.getMyTeam().getPlayer(0))
        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() <= 1:
                selectp5.append(game.getMyTeam().getPlayer(i))

        #jelotarin bazikon man

        global jelotarinBazikonMan
        jelotarinBazikonMan= game.getMyTeam().getPlayer(0)
        global k4
        k4 = 4
        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() > jelotarinBazikonMan.getPosition().getX():
                jelotarinBazikonMan = game.getMyTeam().getPlayer(i)

                k4 = jelotarinBazikonMan.getId()
                print("k4",k4)
        print("jelotarin bazikon man", jelotarinBazikonMan, k4)



        #aghab tarin bazikon man

        global aghabtarinBazikonMan
        aghabtarinBazikonMan= game.getMyTeam().getPlayer(0)
        global k5
        k5 = 0

        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() < aghabtarinBazikonMan.getPosition().getX():
                aghabtarinBazikonMan = game.getMyTeam().getPlayer(i)

                k5= aghabtarinBazikonMan.getId()
                print("k5",k5)
        print("aghab tarin bazikon man ", aghabtarinBazikonMan, k5)


        #bala tarin bazikon man az nazar Y

        global balaTarinBazikonManY
        balaTarinBazikonManY = game.getMyTeam().getPlayer(0)
        global k6
        k6 = 3
        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getY() > balaTarinBazikonManY.getPosition().getY():
                balaTarinBazikonManY = game.getMyTeam().getPlayer(i)
                k6 = balaTarinBazikonManY.getId()
                print("k6",k6)
        print("bala tarin bazikon man az nazar Y ", balaTarinBazikonManY, k6)


         # paeen tarin bazikon man az nazar Y

        global paeenTarinBazikonManY
        paeenTarinBazikonManY = game.getMyTeam().getPlayer(0)
        global k7
        k7 = 2
        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getY() < paeenTarinBazikonManY.getPosition().getY():
                paeenTarinBazikonManY = game.getMyTeam().getPlayer(i)

                k7 = paeenTarinBazikonManY.getId()
                print("k7",k7)
        print(" paeen tarin bazikon man az nazar Y ", paeenTarinBazikonManY, k7)

        # paeen tarin bazikon man az nazar Y dar zamin khodam

        global paeenTarinBazikonManY1
        paeenTarinBazikonManY1 = game.getMyTeam().getPlayer(0)
        global k8
        k8 = 2
        for i in range(0, len(selectp5)):
            if selectp5[i].getPosition().getY() < paeenTarinBazikonManY1.getPosition().getY():
                paeenTarinBazikonManY1 = selectp5[i]
                k8 = paeenTarinBazikonManY1.getId()
                print("k8",k8)
        print(" paeen tarin bazikon man az nazar Y dar zamin khodam ", paeenTarinBazikonManY1, k8)

        # bala tarin bazikon man az nazar Y dar zamin khodam

        global balaTarinBazikonManY1
        balaTarinBazikonManY1 = game.getMyTeam().getPlayer(0)
        global k9
        k9 = 2
        for i in range(0, len(selectp5)):
            if selectp5[i].getPosition().getY() > balaTarinBazikonManY1.getPosition().getY():
                balaTarinBazikonManY1 = selectp5[i]
                k9 = balaTarinBazikonManY1.getId()
                print("k9",k9)
        print(" bala tarin bazikon man az nazar Y dar zamin khodam ", balaTarinBazikonManY1, k9)



        #bazikonan ghabl top man
        bazikonanGhablTopMan = []
        bazikonanGhablTopMan.append(game.getMyTeam().getPlayer(0))
        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() <= game.getBall().getPosition().getX():
                bazikonanGhablTopMan.append(game.getMyTeam().getPlayer(i))

        # bazikonan bad top man
        bazikonanBadTopMan = []
        bazikonanBadTopMan.append(game.getMyTeam().getPlayer(0))
        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() <= game.getBall().getPosition().getX():
                bazikonanBadTopMan.append(game.getMyTeam().getPlayer(i))

            # jelotarin vs aghab tarin bazikonan ghabl top

        selectp = []
        selectp.append(game.getMyTeam().getPlayer(k5))
        for i in range(0, 5):
            if game.getMyTeam().getPlayer(i).getPosition().getX() < game.getBall().getPosition().getX():
                selectp.append(game.getMyTeam().getPlayer(i))
        print(selectp)

        global a
        a = selectp[0]
        global k
        k = k5
        # jelotarin bazikon ghabl top
        for j in range(0, selectp.__len__()):
            if selectp[j].getPosition().getX() > a.getPosition().getX():
                a = selectp[j]

                print("a", a)

                k = selectp[j].getId()
                print("k", k)
                print(selectp[j].getId())

        global b
        b = selectp[0]
        global k1
        k1 = 2
        for j in range(0, selectp.__len__()):
            if selectp[j].getPosition().getX() < b.getPosition().getX():
                b = selectp[j]
                # aghabtarin bazikon ghabl top
                k1 = selectp[j].getId()
                print("k1", k1)
        print("aghabtarin bazikon ghabl top", b, k1)





        print("......................................")







        if game.getBall().getPosition().getX() >= 0:
            if game.getBall().getPosition().getY() <= 2.3 and game.getBall().getPosition().getY() >= -2.3:
                print("hala",k)
                act.setPlayerID(k)
                act.setAngle(shootPreciseAngle(game.getMyTeam().getPlayer(k),game.getBall(),shootball(game,k)))
                act.setPower(100)
                return act
            elif game.getBall().getPosition().getY() > 2.3 or game.getBall().getPosition().getY() < -2.3:
                true1 = shouldGotoDefence(game)
                print("true= ",true1)
                if true1 == 0:

                    #3ta to defa khodemon
                    global aa
                    aa = game.getMyTeam().getPlayer(4)
                    global s
                    s = 4
                    for j in range(0,len(selectp3)):
                        if selectp3[j].getPosition().getX() > aa.getPosition().getX():
                            aa = selectp3[j]
                            s = selectp3[j].getId()
                    true3 = isOpponentInDefenceMode(game)
                    if true3 == 1:
                        act.setPlayerID(s)
                        act.setAngle(takhrib1(game, aa))
                        act.setPower(100)
                        return act
                    else:
                        act.setPlayerID(k4)
                        act.setAngle(zaviyeBazgashtBeDefa1000(game,jelotarinBazikonMan))
                        act.setPower(35)



                else:
                    global  a11
                    a11 = game.getMyTeam().getPlayer(4)
                    #bazgasht be defa az x<1  y>2.3 or x<1 y < -2.3

                    global defendbazgashtiID
                    defendbazgashtiID = 4
                    print("naaaaaaaaaaaaaaaaaa")
                    for i in range(0,len(selectp5)):
                        if selectp5[i].getPosition().getY() > 2.3 or selectp5[i].getPosition().getY() < -2.3 :
                            a11 = selectp5[i]


                            defendbazgashtiID = a11.getId()

                    if a11.getPosition().getX() > -3.5 :
                        act.setPlayerID(defendbazgashtiID)
                        act.setAngle(zaviyeBazgashtBeDefa(game,a11))
                        act.setPower(gobackPower(game.getMyTeam().getPlayer(defendbazgashtiID)))
                        return act

                    if a11.getPosition().getX() <= -3.5:
                        act.setPlayerID(defendbazgashtiID)
                        act.setAngle(zaviyeBazgashtBeDefa(game,a11))
                        act.setPower(gobackPower(game.getMyTeam().getPlayer(defendbazgashtiID)))
                        return act

        if game.getBall().getPosition().getX() < 0 :
            if game.getBall().getPosition().getX() > -2.5 :
                if game.getBall().getPosition().getY() > -2.3 and  game.getBall().getPosition().getY() < 2.3 :
                    if game.getMyTeam().getPlayer(k).getPosition().getX() <= game.getBall().getPosition().getX():
                        act.setPlayerID(k)
                        act.setAngle(shootPreciseAngle(game.getMyTeam().getPlayer(k), game.getBall(), shootball(game, k)))
                        act.setPower(100)
                        return act

                    if game.getMyTeam().getPlayer(k).getPosition().getX() > game.getBall().getPosition().getX():
                        if game.getMyTeam().getPlayer(k3).getPosition().getY() >= 2 or game.getMyTeam().getPlayer(k3).getPosition().getY() <= -2 :
                            act.setPlayerID(k3)
                            act.setAngle(shootPreciseAngle(game.getMyTeam().getPlayer(k3), game.getBall(), shootball(game, k3)))
                            act.setPower(30)
                            return act
                        else:
                            act.setPlayerID(k3)
                            act.setAngle(zaviyeBazgashtBeDefa1111(game, bbbbbb))
                            act.setPower(gobackPower(game.getMyTeam().getPlayer(k3)))
                            return act

                if game.getBall().getPosition().getY() >= 2.3 or game.getBall().getPosition().getY() <= -2.3 :
                    true2 = shouldGotoDefence1(game)
                    if true2 == 0 :
                        act.setPlayerID(k4)
                        act.setAngle(takhrib1(game,jelotarinBazikonMan))
                        act.setPower(100)
                        return act
                    else:
                        #shoot bayad aram bashad
                        if game.getBall().getPosition().getY() >= 2.3 :
                            for i in range(0,len(bazikonanGhablTopMan)):
                                if bazikonanGhablTopMan[i].getPosition().getY() >= 2.3 and bazikonanGhablTopMan[i].getPosition().getX() < game.getBall().getPosition().getX():
                                    ll = bazikonanGhablTopMan[i].getId()
                                    act.setPlayerID(ll)
                                    act.setAngle(shootPreciseAngle(game.getMyTeam().getPlayer(ll), game.getBall(),shootball(game, ll)))
                                    act.setPower(30)
                                    return act

                            act.setPlayerID(k3)
                            act.setAngle(zaviyeBazgashtBeDefa2222(game, bbbbbb))
                            act.setPower(gobackPower(game.getMyTeam().getPlayer(k3)))
                            return act



                        # shoot bayad aram bashad
                        if game.getBall().getPosition().getY() < -2.3 :
                            for i in range(0,len(bazikonanGhablTopMan)):
                                if bazikonanGhablTopMan[i].getPosition().getY() < -2.3 and bazikonanGhablTopMan[i].getPosition().getX() < game.getBall().getPosition().getX():
                                    ll = bazikonanGhablTopMan[i].getId()
                                    act.setPlayerID(ll)
                                    act.setAngle(shootPreciseAngle(game.getMyTeam().getPlayer(ll), game.getBall(), shootball(game, ll)))
                                    act.setPower(30)
                                    return act

                            act.setPlayerID(k3)
                            act.setAngle(zaviyeBazgashtBeDefa2222(game, bbbbbb))
                            act.setPower(gobackPower(game.getMyTeam().getPlayer(k3)))
                            return act

            if game.getBall().getPosition().getX() <= -2.5 :
                 if game.getBall().getPosition().getY() <= 2.3 and game.getBall().getPosition().getY() >= -2.3 :
                     #a = jelotarin bazikon ghabl top
                     if a.getPosition().getX() <= game.getBall().getPosition().getX():
                         act.setPlayerID(k)
                         act.setAngle(shootPreciseAngle(game.getMyTeam().getPlayer(k), game.getBall(), shootball(game, k)))
                         act.setPower(100)
                         return act
                     else:

                         if game.getBall().getPosition().getY() >= 0:
                             act.setPlayerID(k8)
                             act.setAngle(zaviyeBazgashtBeDefaPaeentarinY(game,paeenTarinBazikonManY1))
                             act.setPower(gobackPower(game.getMyTeam().getPlayer(k8)))
                             return act

                         if game.getBall().getPosition().getY() < 0:
                             act.setPlayerID(k9)
                             act.setAngle(zaviyeBazgashtBeDefaBalatarinY(game,balaTarinBazikonManY1))
                             act.setPower(gobackPower(game.getMyTeam().getPlayer(k9)))
                             return act

                 if game.getBall().getPosition().getY() > 2.3 or game.getBall().getPosition().getY() < -2.3 :
                     if a.getPosition().getX() <= game.getBall().getPosition().getX():
                         act.setPlayerID(k)
                         act.setAngle(shootball(game, k))
                         act.setPower(100)
                         return act

                     else:
                         if game.getBall().getPosition().getY() > 2.3:
                             if bbbbbb.getPosition().getY() < game.getBall().getPosition().getY():
                                 act.setPlayerID(k3)
                                 act.setAngle(zaviyeBazgashtBeDefa3333(game,bbbbbb))
                                 act.setPower(gobackPower(game.getMyTeam().getPlayer(k3)))
                                 return act

                             else:
                                 act.setPlayerID(4)
                                 act.setAngle(zaviyeBazgashtBeDefa3333(game, game.getMyTeam().getPlayer(4)))
                                 act.setPower(gobackPower(game.getMyTeam().getPlayer(4)))
                                 return act

                         if game.getBall().getPosition().getY() < -2.3:
                             if bbbbbb.getPosition().getY() > game.getBall().getPosition().getY():
                                 act.setPlayerID(k3)
                                 act.setAngle(zaviyeBazgashtBeDefa3333(game,bbbbbb))
                                 act.setPower(gobackPower(game.getMyTeam().getPlayer(k3)))
                                 return act

                             else:
                                 act.setPlayerID(4)
                                 act.setAngle(zaviyeBazgashtBeDefa3333(game, game.getMyTeam().getPlayer(4)))
                                 act.setPower(gobackPower(game.getMyTeam().getPlayer(4)))
                                 return act
        print("nooooooooooooooooooooooooooooooo ifffffffffffffffffffffffff")
        act.setPlayerID(0)
        act.setAngle(0)
        act.setPower(0)
        return act
    except Exception as e:
        print("cause")
        print(e.__cause__)
        act = Triple()
        act.setPlayerID(0)
        act.setAngle(0)
        act.setPower(0)
        return act












