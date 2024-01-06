import matplotlib.pyplot as plt
import matplotlib.animation as animation

### données initiales du problème
X = [10]
Y = [25.13]
vx = -6
vy = 2
larg = 60
haut = 50
ouv = 15
R_part = 0.1
larg = larg + R_part
haut = haut + R_part

### Construction boite
def ligne(X, Y, **kwargs):
    """fonction qui crée les lignes de la boite"""
    plt.plot([X[0],X[1]],[Y[0],Y[1]], **kwargs)


def creer_boite(larg, haut, ouv):
    """fonction qui crée la boite"""
    ligne([0, larg], [0, 0], color='black')
    ligne([0, 0], [0, haut], color='black')
    ligne([0, larg], [haut, haut], color='black')
    ligne([larg, larg], [0, (haut - ouv) / 2], color='black')
    ligne([larg, larg], [(haut + ouv) / 2, haut], color='black')
    plt.axis("off")
    plt.title("MOUVEMENT D'UNE PARTICULE DANS UNE BOITE")


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
def trouver_intersec_composante(larg, haut, ouv, X, Y, vx, vy, FLAG):
    """prend un argument les dimension de la boîte, la position  des chocs entre la particule et les parois, les composante de la vitesse et return les nouvelles composante de la vitesse après le rebond, les liste X et Y sont actualisé avec les coordonner du nouveau choc"""
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
        if b == 0 or b == haut:             #coins haut et bas gauche
            X.append(0)
            Y.append(b)
        elif b == haut - a * larg:          #coin haut droit
            X.append(larg)
            Y.append(haut)
        else:                               #coin bas droite
            X.append(larg)
            Y.append(0)
    #pour l'ouverture
    else :
        X.append(larg)
        Y.append(a * larg + b)
        FLAG = 1
    return vx, vy, FLAG

###Animation de la particule
def trajectoire(larg, haut, ouv, X, Y, vx, vy):
    """prend en argument, les dimension de la boîte, la liste des position de la particule et les composantes de la vitesse et return le nombre de choc entre la particule et les parois et deux listes qui permette d'avoir les toutes les position de la particule pendant la simulation"""
    FLAG = 0
    count = 0
    while FLAG != 1:
        vx, vy, FLAG = trouver_intersec_composante(larg, haut, ouv, X, Y, vx, vy, FLAG)
        count += 1
    return (count - 1), X, Y

#On cherche le nombre de collisions que la particule fait
nb_collisions, X, Y = trajectoire(larg, haut, ouv, X, Y, vx, vy)
diviseur = 6 #nombre de fois où l'on divise le segment
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
for i in range (len(liste_finale_X)):
    Tmps.append(i)

def animate(i):
    """fonction qui permet l'animation de la particule"""
    scat.set_offsets((liste_finale_X[i], liste_finale_Y[i]))
fig, ax = plt.subplots()
scat = ax.scatter(liste_finale_X, liste_finale_Y, c='r',s=100*R_part)
creer_boite(larg,haut,ouv)
ani = animation.FuncAnimation(fig, animate, frames=len(Tmps), interval=10, repeat=False)
plt.text(5,-5, "Le nombre de collisions contre les parois est de " + str(nb_collisions)) #affiche le nombre de collisions total de la particule avant sa sortie
plt.show()