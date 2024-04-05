import cv2
import numpy as np
import quaternion as q
#q.quaternion(1,0,0,0)
def trouver_centre_contour(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
    return [cX, cY]

def trouver_coordonnees(contour):
    coord_x = []
    coord_y = []
    for point in contour:
        x, y = point[0]
        coord_x.append(x)
        coord_y.append(y)
    return coord_x, coord_y

def trouver_centres_et_coordonnees(image_path):
    # Lire l'image en niveaux de gris
    image = cv2.imread(image_path)
    gris = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binariser l'image pour obtenir le fond noir
    _, seuil = cv2.threshold(gris, 1, 255, cv2.THRESH_BINARY)

    # Trouver les contours des formes
    contours, _ = cv2.findContours(seuil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Garder les centres de gravité, les coordonnées x et y de chaque forme
    centres = []
    coord_x_listes = []
    coord_y_listes = []

    for contour in contours:
        centre = trouver_centre_contour(contour)
        coord_x, coord_y = trouver_coordonnees(contour)
        centres.append(centre)
        coord_x_listes.append(coord_x)
        coord_y_listes.append(coord_y)

    return centres, coord_x_listes, coord_y_listes

# Exemple d'utilisation
image_path = "crop_diff.jpg"  # Remplacer "image.jpg" par le chemin de votre image
centres, coord_x_listes, coord_y_listes = trouver_centres_et_coordonnees(image_path)

#print("Informations pour chaque forme :")
for i in range(len(centres)):
    print(f"Forme {i+1}:")
    print(f"Centre de gravité : {centres[i]}")
    print(f"Coordonnées x : {coord_x_listes[i]}")
    print(f"Coordonnées y : {coord_y_listes[i]}")
    print()

def transposer_matrice(matrice):
    return list(zip(*matrice))

def matrice_C(centre, coordx, coordy):
    M= []
    for i in range(len(coordx)):
        x_tilde = centre[0]-coordx[i]
        y_tilde = centre[0]-coordy[i]
        M.append([x_tilde, y_tilde])

    Mt = transposer_matrice(M)
    C = np.dot(Mt, M)
    return C

def orientation(C):
    valeurs_propres, vecteurs_propres = np.linalg.eig(C)
    indice_max_valeur_propre = np.argmax(valeurs_propres)
    vecteur_propre_max = vecteurs_propres[:, indice_max_valeur_propre]
    #print(vecteur_propre_max)
    vecteur_propre_max_transforme = np.array([vecteur_propre_max[0], vecteur_propre_max[1], 0])
    return vecteur_propre_max_transforme

# Exemple d'utilisation
centre = [5, 5]
coordx = [1, 2, 3]  
coordy = [4, 5, 6]


C = matrice_C(centre, coordx, coordy)
vecteur_propre_max = orientation(C)

print("C:")
print(C)
print("--------------------")
print("Vecteur propre associé à la plus grande valeur propre:")
print(vecteur_propre_max)

#qt = q.quaternion(0, vecteur_propre_max[0], vecteur_propre_max[1], vecteur_propre_max[2])
#qt = q.as_quat_array(vecteur_propre_max)
#qt = q.as_rotation_vector(vecteur_propre_max)

rotation_vector = vecteur_propre_max
angle = np.arctan2(vecteur_propre_max[1],vecteur_propre_max[0])

axis = rotation_vector / angle if angle != 0 else np.zeros(3)

s = np.sin(angle / 2)
pose_objet = np.array([np.cos(angle / 2), axis[0] * s, axis[1] * s, axis[2] * s])

print(pose_objet)
#print("Le quaternion correspondant au vecteur u dans le plan xy est :", qt)