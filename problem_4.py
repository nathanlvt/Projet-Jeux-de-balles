
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from math import *



### données initiales du problème, X,Y coordonnées des points au fur et à mesure
""" vx et vy composantes de la vitesse, ouv = ouverture de la boite , larg et haut sont les dimensions de la boite , R : rayon cercle et xc,yc coordonnées du cercle"""
X = [35]
Y = [30]
vx = 1
vy = 3
R_part = 0.1
C = [[0,0,0],[30, 20, 2], [30, 30, 2], [ 30, 40, 2], [40 , 20, 2], [40, 30, 2 ],[40 ,40 ,2 ]]
larg = 60
haut = 50
ouv = 20

larg = larg + R_part
haut = haut + R_part
R = 2 #rayon du cercle
xc = 20
yc = 20

count_face_gauche = 0




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
    plt.title("MOUVEMENT D'UNE PARTICULE DANS UNE BOITE")

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
    global count_face_gauche    #variable global 
    a = vy / vx                 #coefficient directeur
    b = Y[-1] - a * X[-1]       #ordonnée à l'origine
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
        count_face_gauche += 1
    #pour la face droite
    elif intersection_segmentVerticale_droite(a, b, larg, [larg, 0], [larg, (haut - ouv) / 2], vx, vy) or intersection_segmentVerticale_droite(a, b, larg, [larg, (haut + ouv) / 2], [larg, haut], vx, vy):
        vx = -vx
        X.append(larg)
        Y.append(a * larg + b)

    #si on est dans les coins
    elif abs(vx) == abs(vy) and (b == 0 or b == haut and b == haut - a * larg and b == -a * larg):
        vx = -vx
        vy = -vy
        if b == 0 or b == haut: #coins haut et bas gauche
            X.append(0)
            Y.append(b)
        elif b == haut - a * larg: #coin haut droit
            X.append(larg)
            Y.append(haut)
        else:   #coin bas droite
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
def creer_vecteur(X,Y,A):
    return[A[0]-X[-1],A[1]-Y[-1]]
def prod_scal(a, b):
    """prend en argument deux vecteurs et retourne le preoduit scalaire"""
    return a[0] * b[0] + a[1] * b[1]

def mult_scalaire_vec(alpha, x):
    """renvoie la multiplication d'un scalaire par un vecteur"""
    return [alpha * x[0], alpha * x[1]]

def norme(x):
    """norme le vecteur a"""
    return sqrt((x[0])**2 + (x[1])**2)

###
def detect(xc, yc, R, X, Y, vx, vy):
    """prend en argument origine du cercle, le rayon, les listes de coordonnées et les composantes de vitesse 
    et return True s'il y a intersection entre le cercle et la trajectoire"""
    alpha = vx ** 2 + vy ** 2
    b = 2 * (vx * (X[-1] - xc) + vy * (Y[-1] - yc))
    c = xc ** 2 + yc ** 2 + X[-1] ** 2 + Y[-1] ** 2 - 2 * (xc * X[-1] + yc * Y[-1]) - R ** 2
    discriminant = b ** 2 - 4 * alpha * c
    t1 = (- b + sqrt(abs(discriminant))) / (2 * alpha)
    t2 = (- b - sqrt(abs(discriminant))) / (2 * alpha)
    if (discriminant < 0):
        return False
    elif t1<=0 and t2<=0:
        return False
    else :
        return True


def detect_general(X, Y, C, vx, vy):
    """fonction qui prend en arguments X,Y , C (les différents cercles) et les composantes vx,vy et elle retourne soit l'indice avec lequel il y a intersection ou non"""
    n=len(C)
    L=np.ones(n)
    indices = [i for i in range(len(L))]
    for i in range(len(C)):
        L[i]=sqrt((C[i][0]-X[-1])**2+(C[i][1]-Y[-1])**2)       #calcule de la distance avec les cercles et le point précédent
    indice_triee= [i for _, i in sorted(zip(L, indices))]
    j=0
    for j in indice_triee :
        if detect(C[j][0], C[j][1],C[j][2], X, Y, vx, vy)==True:
            return j    #donne l'indice du cercle de la liste, 
                        #le premier cercle a pour paramètres [0,0,0] pour faciliter la fonction trajectoire
    return False

###
def intersection_circle_halfline(xc, yc, R, X, Y, vx, vy):
    """prend en argument origine du cercle, le rayon, les listes de coordonnées
    et les composantes de vitesse et détermine le point d'intersection avec le cercle et l'ajoute dans X et Y"""
    a = vx ** 2 + vy ** 2
    b = 2 * (vx * (X[-1] - xc) + vy * (Y[-1] - yc))
    c = xc ** 2 + yc ** 2 + X[-1] ** 2 + Y[-1] ** 2 - 2 * (xc * X[-1] + yc * Y[-1]) - R ** 2
    discriminant = b ** 2 - 4 * a * c
    t1 = (- b + sqrt(abs(discriminant))) / (2 * a)
    t2 = (- b - sqrt(abs(discriminant))) / (2 * a)
    if t1 >=0 and t2 >=0:
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
        if t1>0:
            x1 = X[-1] + t1 * vx
            y1 = Y[-1] + t1 * vy
            X.append(x1)
            Y.append(y1)
        elif t2>0:
            x2 = X[-1]+ t2 * vx
            y2 = Y[-1] + t2 * vy
            X.append(x2)
            Y.append(y2)


###
def vec_normal_cercle(xc, yc, R, X, Y, vx, vy):
    """prend en argument origine du cercle, le rayon, les listes de coordonnées 
    et les composantes de vitesse et retourne le vecteur normal à la droite tangante au cercle du point d'intersection"""
    intersection_circle_halfline(xc, yc, R, X, Y, vx, vy)
    vec_directeur = [ X[-1] - xc, Y[-1] - yc]
    return [(1 / norme(vec_directeur)) * vec_directeur[0] , (1 / norme(vec_directeur)) * vec_directeur[1]]

def symetrique(xc, yc, R, X, Y, vx, vy):
    """prend en argument l'origine du cercle, le rayon, les listes de coordonnées et les composantes de vitesse
    et retourne le symétrique du vecteur incident """
    omega = vec_normal_cercle(xc, yc, R, X, Y, vx, vy)
    moins_v = [X[-2] - X[-1],Y[-2] - Y[-1]]
    prod = prod_scal(moins_v, omega)
    res =mult_scalaire_vec(2 * prod, omega)
    return [res[0] - moins_v[0], res[1] - moins_v[1]]


def after_rebond(vec, vx, vy):
    """retourne vx_rebond et vy_rebond en fonction du coeff directeur et de l'ordonné à l'origine de la droite"""
    V=(vx**2+vy**2)**(1/2)
    if vec[0] == 0 :
        return 1,np.copysign(V, vec[1])
    else :
        a= vec[1] / vec[0]
        V = sqrt(vx**2 + vy**2)
        vx = np.copysign(V * sqrt(1 / (1 + a**2)), vec[0])
        vy = np.copysign(V * sqrt(1 / (1 + (1/ a**2))), vec[1])
        return vx,vy


def trajectoire(larg, haut, ouv, X, Y, vx, vy, C):
    """prend en arguments, les dimensions de la boîte, la liste des positions de la particule,la liste des cercles et les composantes de la vitesse les paramètres du cercle et return le nombre de choc entre la particule et les parois et deux listes qui permettent d'avoir toutes les positions de la particule pendant la simulation"""
    FLAG = 0
    count = 0
    while FLAG != 1:
            while detect_general(X, Y, C , vx, vy)!= False:     #detecte si il y intersection avec des cercles
                    k = detect_general(X, Y, C , vx, vy)
                    vec = symetrique(C[k][0],C[k][1],C[k][2],X, Y, vx, vy)
                    vx,vy = after_rebond(vec, vx, vy)
                    X[-1]=X[-1] + R_part*vx
                    Y[-1]=Y[-1] +R_part*vy
            vx, vy, FLAG = trouver_intersec_composante(larg, haut, ouv, X, Y, vx, vy, FLAG)
            count += 1
    return X, Y

###

X,Y = trajectoire(larg, haut, ouv, X, Y, vx, vy, C)     #actualise les liste X,Y avec les points de collisions


def distance_points(X,Y):
    """fonction qui prends en arguments X et Y et qui retourne une liste des distances entre les points"""
    D = []
    for i in range (len(X) - 1):
        D.append(sqrt((X[i+1] - X[i]) ** 2 + (Y[i+1] - Y[i]) ** 2))
    return D

D = distance_points(X,Y)
D = np.array(D)
D = np.round(D).astype(int)     #nécessité d'avoir des entiers 

def liste_anim(X,Y):
    """fonction qui prend en arguments X,Y c'est à dire les différents points de collisions et 
    calcule des points intermédiaires pour l'animation """
    longueur = len(X)
    X_tmp, Y_tmp = np.copy(X), np.copy(Y)   #on copie les listes X,Y sinon on utilisera des noouveaux points de la liste
    for i in range(longueur - 1):
        index = longueur - i - 2
        for j in range(D[index] - 1, 0, -1):
            X_int = X_tmp[index] + j * (X_tmp[index + 1] - X_tmp[index]) / D[index]
            Y_int = Y_tmp[index] + j * (Y_tmp[index + 1] - Y_tmp[index]) / D[index]
            X.insert(index + 1, X_int)
            Y.insert(index + 1, Y_int)

liste_anim(X,Y)                     #actualise les listes X,Y

def creation_fig(larg,haut,ouv,C):
    creer_boite(larg,haut,ouv)      #on utilise la fonction creer_boite pour faire le cadre 
    for i in range(len(C)):
        plot_circle_halfline(C[i][0],C[i][1],C[i][2] )  #permet de tracer les différents cercles

def frames(X):
    """fonction qui prend en argument la liste X actualisée et retourne une liste"""
    T = []
    for i in range (len(X)):
        T.append(i)
    return T 

Tmps = frames(X) #la longueur de cette liste nous donnera le nombre de frames 

fig, ax = plt.subplots()    
scat = ax.scatter(X, Y, c='r',s=100*R_part)

def animate(i):
    """"fonction qui permet de mettre en place les points sur la figure, fonctionne avec FuncAnimation """
    scat.set_offsets((X[i], Y[i]))

creation_fig(larg,haut,ouv,C)
    
ani = animation.FuncAnimation(fig, animate, frames=len(Tmps), interval=40, repeat=False)

plt.text(5,-5, "La particule heurte la paroi de gauche " + str(count_face_gauche) + " fois")

plt.show()

