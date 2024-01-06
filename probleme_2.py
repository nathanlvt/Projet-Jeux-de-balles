##Dans le probleme2 on a repris les routines d'intersection,
import random
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import scipy.integrate
import time
import matplotlib.animation as animation

## données initiales du problème
FLAG = 0
X = [32]
Y = [20]
vx = 5
vy = 2
R_part = 0.1
larg = 60
haut = 50
delta = 5
larg = larg + R_part
haut = haut + R_part

###
def ligne(X, Y, **kwargs):
    """fonction qui crée les lignes de la boite"""
    plt.plot([X[0],X[1]],[Y[0],Y[1]], **kwargs)


def creer_boite(larg, haut, delta):
    """fonction qui crée la boite"""
    plt.plot([delta, larg - delta], [0,0], color='black')
    plt.plot([delta, larg - delta], [haut, haut], color='black')
    plt.plot([0, 0], [delta, haut - delta], color='black')
    plt.plot([larg, larg], [delta, haut - delta], color='black')
    plt.axis("off")
    #plt.title("MOUVEMENT D'UNE PARTICULE DANS UNE BOITE")


### Routine pour trouver les intersections
def intersection_segment_droite(a1, b1, a2, b2, point1, point2, x, y, vx, vy):
    """prend en argument le coeff directeur, l'ordonner à l'origine de deux droites ainsi que les point d'extremité du segment et renvoie True s'ils s'intersect"""
    intersec = (b2 - b1) / a1 - a2
    if vx < 0 and vy > 0:
        return intersec > point1[0] and intersec < point2[0] and y < b2
    elif vx > 0 and vy > 0:
        return intersec > point1[0] and intersec < point2[0] and y < b2
    elif vx > 0 and vy < 0:
        return intersec > point1[0] and intersec < point2[0] and y > b2
    else :
        return intersec > point1[0] and intersec < point2[0] and y > b2

def intersection_segmentVerticale_droite(a, b, x, point1, point2, vx, vy):
    """prend en argument le coeff directeur, l'ordonner à l'origine de deux droites ainsi que les point d'extremité du segment et renvoie True s'ils s'intersect"""
    intersec = a * x + b
    if vx < 0 and vy > 0:
        return intersec > point1[1] and intersec < point2[1] and x == 0
    elif vx < 0 and vy < 0:
        return intersec > point1[1] and intersec < point2[1] and x == 0
    elif vx > 0 and vy > 0:
        return intersec > point1[1] and intersec < point2[1] and x == larg
    else:
        return intersec > point1[1] and intersec < point2[1] and x == larg

### Implémentation
def trouver_intersec_composante_billard(larg, haut, delta, X, Y, vx, vy, FLAG):
    """fonction qui permet de trouver l'intersection entre la trajectoire des particles et les contours de la boite"""
    a = vy / vx
    b = Y[-1] - a * X[-1]
    #pour  la face inférieur
    if intersection_segment_droite(a, b, 0, 0, [0 + delta, 0], [larg - delta, 0], X[-1], Y[-1], vx, vy):
        vy = -vy
        X.append(-b / a)
        Y.append(0)
    #pour la face supérieur
    elif intersection_segment_droite(a, b, 0, haut, [0 + delta, haut], [larg - delta, haut], X[-1], Y[-1], vx, vy):
        vy = -vy
        X.append((haut - b) / a)
        Y.append(haut)
    #pour la face gauche
    elif  intersection_segmentVerticale_droite(a, b, 0, [0, 0 + delta], [0, haut - delta], vx, vy):
        vx = -vx
        X.append(0)
        Y.append(b)
    #pour la face droite
    elif intersection_segmentVerticale_droite(a, b, larg, [larg, 0 + delta], [larg, haut - delta], vx, vy):
        vx = -vx
        X.append(larg)
        Y.append(a * larg + b)
    #dans les coins
    else:
        if abs(vx) == abs(vy) and (b == 0 or b == haut and b == haut - a * larg and b == -a * larg):
            vx = -vx
            vy = -vy
            if b == 0 or b == haut:     #coins haut et bas gauche
                X.append(0)
                Y.append(b)
            elif b == haut - a * larg:  #coin haut droit
                X.append(larg)
                Y.append(haut)
            else:                       #coin bas droite
                X.append(larg)
                Y.append(0)
        #face inférieur dans la zone delta
        elif intersection_segment_droite(a, b, 0, 0, [0, 0], [delta, 0], X[-1], Y[-1], vx, vy) or intersection_segment_droite(a, b, 0, 0, [larg - delta, 0], [larg, 0], X[-1], Y[-1], vx, vy):
            X.append(-b / a)
            Y.append(0)
        #face supérieur dans la zone delta
        elif intersection_segment_droite(a, b, 0, haut, [0, haut], [delta, haut], X[-1], Y[-1], vx, vy) or intersection_segment_droite(a, b, 0, haut, [larg - delta, haut], [larg, haut], X[-1], Y[-1], vx, vy):
            X.append((haut - b) / a)
            Y.append(haut)
        #face de gauche dans la zone delta
        elif intersection_segmentVerticale_droite(a, b, 0, [0, 0], [0, delta], vx, vy) or intersection_segmentVerticale_droite(a, b, 0, [0, haut - delta], [0, haut], vx, vy):
            X.append(0)
            Y.append(b)
        #face de droite dans la zone delta
        else:
            X.append(larg)
            Y.append(a * larg + b)
        FLAG = 1
    return vx, vy, FLAG


def trajectoire(larg, haut, delta, X, Y, vx, vy):
       """prend en argument, les dimension de la boîte, la liste des position de la particule et les composantes de la vitesse et return le nombre de choc entre la particule et les parois et deux listes qui permette d'avoir les toutes les position de la particule pendant la simulation"""
    global FLAG
    count = 0
    while FLAG != 1:
        vx, vy, FLAG = trouver_intersec_composante_billard(larg, haut, delta, X, Y, vx, vy, FLAG)
        count += 1
    return (count - 1), X, Y

#### Animation de la particule
nb_collisions, X, Y = trajectoire(larg, haut, delta, X, Y, vx, vy)
diviseur = 4 #nombre de fois où l'on divise le segment
"""cette partie permet d'obtenir plusieur points qui permetterons de tracer la trajectoire"""
for j in range(diviseur):
    liste_inter_X = []
    liste_inter_Y = []
    liste_finale_X = []
    liste_finale_Y = []
    for i in range(len(X) - 1):
        x = (X[i] + X[i+1]) / 2
        y = (Y[i] + Y[i+1]) / 2
        liste_inter_X.append(x)
        liste_inter_Y.append(y)
    for i in range( len(liste_inter_X) ):
        liste_finale_X.append(X[i])
        liste_finale_X.append(liste_inter_X[i])
        liste_finale_Y.append(Y[i])
        liste_finale_Y.append(liste_inter_Y[i])
    liste_finale_X.append(X[-1])
    liste_finale_Y.append(Y[-1])
    X = liste_finale_X
    Y = liste_finale_Y

#Créer une liste d'indice pour l'animation
Tmps = []
for i in range (len(liste_finale_X)):
    Tmps.append(i)

###Animation/représentation
fig, ax = plt.subplots()
scat = ax.scatter(liste_finale_X, liste_finale_Y, c='r',s=100*R_part)
creer_boite(larg,haut,delta)
plt.text(5, -5, "Le nombre de collisions contre les parois est de " + str(nb_collisions)) #affiche le nombre de collisions total de la particule avant sa sortie

def animate(i):
    """fonction qui permet l'animation de la particule"""
    scat.set_offsets((liste_finale_X[i], liste_finale_Y[i]))
ani = animation.FuncAnimation(fig, animate, frames=len(Tmps), interval=50, repeat=False)

plt.plot(X, Y, "--", color="k")
plt.show()


