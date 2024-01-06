import random
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import matplotlib.animation as animation
from math import *

### données initiales du problème, X,Y coordonnées des points au fur et à mesure
""" vx et vy composantes de la vitesse, ouv = ouverture de la boite , larg et haut sont les dimensions de la boite , R : rayon cercle et xc,yc coordonnées du cercle"""
FLAG = 0
X = [15]
Y = [10]
vx = 1
vy = -3
larg = 60
haut = 50
ouv = 15
R_part = 0.1
larg = larg + R_part
haut = haut + R_part
R = 5 #rayon du cercle
xc = 30
yc = 25



### Construction boite
def ligne(X, Y, **kwargs):
    """fonction qui crée les lignes de la boite"""
    plt.plot([X[0],X[1]],[Y[0],Y[1]], **kwargs)


def creer_boite( larg, haut, ouv):
    """fonction qui crée la boite"""
    ligne([0, larg], [0, 0], color='black')
    ligne([0, 0], [0, haut], color='black')
    ligne([0, larg], [haut, haut], color='black')
    ligne([larg, larg], [0, (haut - ouv) / 2], color='black')
    ligne([larg, larg], [(haut + ouv) / 2, haut], color='black')
    plt.axis("off")
    #plt.title("MOUVEMENT D'UNE PARTICULE DANS UNE BOITE")

def plot_circle_halfline(xc, yc, R):
    # Génération des points du cercle
    t = np.linspace(0, 2 * np.pi, 100)
    x = xc + R * np.cos(t)
    y = yc + R * np.sin(t)
    # Affichage du cercle
    plt.plot(x, y, 'b-')
    plt.axis("off")

###
"""
#initialisation de la boite avec ouverture
#demande type de boite
haut = float(input("quelle hauteur de boite désirez vous?"))
larg = float(input("quelle largeur de boite désirez vous?"))
ouv = float(input("quelle taille d'ouverture désirez vous 0 et "+ str(haut) + "?"))
r_part = float(input("quel est le rayon de la particule?"))

#haut_coision: hauteur du centre particule ou rentre en colision avec paroi du haut
haut_col = haut  -r_part
"""

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

### Implémentation pour collision sur une droite
def trouver_intersec_composante(larg, haut, ouv, X, Y, vx, vy, FLAG):
    """fonction qui permet de trouver l'intersection entre la trajectoire des particules et les contours de la boite"""
    a = vy / vx             #coefficient directeur
    b = Y[-1] - a * X[-1]   #ordonnée à l'origine
    #pour  la face inférieur
    if intersection_segment_droite(a, b, 0, 0, [0, 0], [larg, 0], X[-1], Y[-1], vx, vy):
        vy = -vy
        X.append(-b / a)
        Y.append(0)
    #pour la face supérieur
    elif intersection_segment_droite(a, b, 0, haut, [0, haut], [larg, haut], X[-1], Y[-1], vx, vy):
        vy = -vy
        X.append((haut - b) / a)
        Y.append(haut)
    #pour la face gauche
    elif  intersection_segmentVerticale_droite(a, b, 0, [0, 0], [0, haut], vx, vy):
        vx = -vx
        X.append(0)
        Y.append(b)
    #pour la face droite
    elif intersection_segmentVerticale_droite(a, b, larg, [larg, 0], [larg, (haut - ouv) / 2], vx, vy) or intersection_segmentVerticale_droite(a, b, larg, [larg, (haut + ouv) / 2], [larg, haut], vx, vy):
        vx = -vx
        X.append(larg)
        Y.append(a * larg + b)
    #si on est dans les coins
    elif abs(vx) == abs(vy) and (b == 0 or b == haut and b == haut - a * larg and b == -a * larg):
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
    #pour l'ouverture
    else :
        X.append(larg)
        Y.append(a * larg + b)
        FLAG = 1
    return vx, vy, FLAG

#pour un cercle
#X,Y coordonnées des différents points au fil des avancées

###

def prod_scal(a, b):
    """prend en argument deux vecteurs et retourne le preoduit scalaire"""
    return a[0] * b[0] + a[1] * b[1]

def mult_scalaire_vec(alpha, x):
    """renvoie la multiplication d'un scalaire par un vecteur"""
    return [alpha * x[0], alpha * x[1]]

def norme(x):
    """norme le vecteur x"""
    return sqrt((x[0])**2 + (x[1])**2)


###
def detect(xc, yc, R, X, Y, vx, vy):
    """prend en argument origine du cercle, le rayon, les listes de coordonnées et les composantes de vitesse et return True s'il y a intersection entre le cercle et la trajectoir"""
    alpha = vx**2 + vy**2
    b = 2 * (vx * (X[-1] - xc) + vy * (Y[-1] - yc))
    c = xc**2 + yc**2 + X[-1]**2 + Y[-1]**2 - 2 * (xc * X[-1] + yc * Y[-1]) - R ** 2
    discriminant = b**2 - 4 * alpha * c
    t1 = (- b + sqrt(abs(discriminant))) / (2 * alpha)
    t2 = (- b - sqrt(abs(discriminant))) / (2 * alpha)
    if (discriminant < 0):
        return False
    elif t1<0 and t2<0:
        return False
    else :
        return True

def intersection_circle_halfline(xc, yc, R, X, Y, vx, vy):
    """prend en argument origine du cercle, le rayon, les listes de coordonnées et les composantes de vitesse et détermine le point d'intersection avec le cercle et l'ajoute dans X et Y"""
    a = vx**2 + vy**2
    b = 2 * (vx * (X[-1] - xc) + vy * (Y[-1] - yc))
    c = xc**2 + yc**2 + X[-1] ** 2 + Y[-1]**2 - 2 * (xc * X[-1] + yc * Y[-1]) - R**2
    discriminant = b**2 - 4 * a * c
    t1 = (-b + sqrt(abs(discriminant))) / (2 * a)
    t2 = (-b - sqrt(abs(discriminant))) / (2 * a)
    if t1 >= 0 and t2 >= 0:
        x1 = X[-1] + t1 * vx
        y1 = Y[-1] + t1 * vy
        x2 = X[-1] + t2 * vx
        y2 = Y[-1] + t2 * vy
        d1 = sqrt((x1 - X[-1])** 2 + (y1 - Y[-1]) ** 2)
        d2 = sqrt((x2 - X[-1])** 2 + (y2 - Y[-1]) ** 2)
        if d1 < d2:
            X.append(x1)
            Y.append(y1)
        else:
            X.append(x2)
            Y.append(y2)
    else:
        if t1>=0:
            x1 = X[-1] + t1 * vx
            y1 = Y[-1] + t1 * vy
            X.append(x1)
            Y.append(y1)
        else:
            x2 = X[-1]+ t2 * vx
            y2 = Y[-1] + t2 * vy
            X.append(x2)
            Y.append(y2)

###
def vec_normal_cercle(xc, yc, R, X, Y, vx, vy):
    """prend en argument origine du cercle, le rayon, les listes de coordonnées et les composantes de vitesse et retourne le vecteur normal à la droite tangante au cercle du point d'intersection"""
    intersection_circle_halfline(xc, yc, R, X, Y, vx, vy)
    vec_directeur = [ X[-1] - xc, Y[-1] - yc]
    return [(1 / norme(vec_directeur)) * vec_directeur[0] , (1 / norme(vec_directeur)) * vec_directeur[1]]

def symetrique(xc, yc, R, X, Y, vx, vy):
    """prend en argument l'origine du cercle, le rayon, les listes de coordonnées et les composantes de vitesse
    et retourne le symètrique du vecteur incident """
    omega = vec_normal_cercle(xc, yc, R, X, Y, vx, vy)
    moins_v = [X[-2] - X[-1],Y[-2] - Y[-1]]
    prod = prod_scal(moins_v, omega)
    res = mult_scalaire_vec(2 * prod, omega)
    return [res[0] - moins_v[0], res[1] - moins_v[1]]

def trouve_composante_vitesse(vec, vx, vy):
    """retourne vx_rebond et vy_rebond en fonction de la norme de la vitesse"""
    if vec[0] == 0 :
        return 0,np.copysign(V, vec[1])
    else :
        a= vec[1] / vec[0]
        V = sqrt(vx**2 + vy**2)
        vx = np.copysign(V * sqrt(1 / (1 + a**2)), vec[0])   #la fonction copysign permet de donner le signe du deuxième argument
        vy = np.copysign(V * sqrt(1 / (1 + (1/ a**2))), vec[1])
        return vx,vy

def after_rebond(xc, yc, R, X, Y, vx, vy):
    """prend en argument origine du cercle, le rayon, les listes de coordonnées et les composantes de vitesse et retourne les nouvelles composantes ou non si il y a intersection"""
    if detect(xc, yc, R, X, Y, vx, vy):
        vec = symetrique(xc, yc, R, X, Y, vx, vy)
        vx, vy = trouve_composante_vitesse(vec, vx, vy)
        return vx, vy
    else :
        return vx,vy

def trajectoire(larg, haut, ouv, X, Y, vx, vy, xc, yc, R):
    """prend en arguments, les dimensions de la boîte, la liste des positions de la particule et les composantes de la vitesse les paramètres du cercle et return le nombre de choc entre la particule et les parois et deux listes qui permettent d'avoir toutes les positions de la particule pendant la simulation"""
    global FLAG
    count = 0
    while FLAG != 1:
        vx, vy =after_rebond(xc, yc, R, X, Y, vx, vy)
        vx, vy, FLAG = trouver_intersec_composante(larg, haut, ouv, X, Y, vx, vy, FLAG)
        count += 1
    return (count - 1), X, Y


###

nb_collisions, X, Y = trajectoire(larg, haut, ouv, X, Y, vx, vy, xc, yc, R)
diviseur = 4 #nombre de fois où l'on divise le segment

#code qui permet d'avoir plus de points pour l'animation

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

    for i in range(len(liste_inter_X)):
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
for i in range (len(X)):
    Tmps.append(i)

def animate(i):
    scat.set_offsets((liste_finale_X[i], liste_finale_Y[i]))


fig, ax = plt.subplots()

scat = ax.scatter(liste_finale_X, liste_finale_Y, c='r',s=100*R_part)

creer_boite(larg,haut,ouv)

plot_circle_halfline(xc, yc, R)


ani = animation.FuncAnimation(fig, animate, frames=len(Tmps), interval=75, repeat=False)

plt.plot(X, Y, "--", color="k")

plt.show()