import cv2
import numpy as np
import os
# chargement d'une image
path_blanc = 'template_blanc/'
path_rose = 'template_rose/'


def parcours_dossier(path,image):
    copy_image = image.copy()
    copy_image = image[250:370,250:440]
    copy_image2 = image.copy()
    seuil = 0.8
    l = []
    for file in  os.listdir(path):
        if file.endswith('png'):
            image_path =  os.path.join(path,file)
            temp = cv2.imread(image_path,0)
            w1,h1 = temp.shape[::-1]
            r = cv2.matchTemplate(img_gray,temp,cv2.TM_CCOEFF_NORMED)
            loc = np.where(r>=seuil)
            if len(loc[0])>0:
                l.append([image_path,len(loc[0])])
    p = []
    for j in range(len(l)):
        p.append(l[j][1])
    best = max(p)
    best_im = ""
    angle_rot = 0
    for x in l:
        if x[1]==best:
            best_im=x[0]
    num_image = (best_im[23:25])
    if num_image[1]=='.':
        num_image = num_image[0]
    num_image = int(num_image)
    sens = 0
    if path==path_blanc:
        if num_image in [i for i in range(1,10)] : # si le nombre est entre 
            sens = 0
        else:
            sens = 1
    templ = cv2.imread(best_im,0)
    im_gray = cv2.cvtColor(copy_image,cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(im_gray,templ,cv2.TM_CCOEFF_NORMED)
    locate = np.where(res >= seuil)
    #locate2 = np.where(res>=seuil)
    w2,h2 = templ.shape[::-1]
    for pt in zip(*locate[::-1]):
        cv2.rectangle(copy_image2, (pt[0]+250,pt[1]+250), (pt[0]+250 + w2, pt[1]+250 + h2), (0,255,255), 2)
    x1 = list(zip(*locate[::-1]))[0][0]+125
    y1 = list(zip(*locate[::-1]))[0][1]+125
    x2 = x1+ w2+250
    y2 = y1 + h2+250

    x = int((x1+x2)/2)
    y = int((y1+y2)/2)

    x1_c = list(zip(*locate[::-1]))[0][0]
    y1_c = list(zip(*locate[::-1]))[0][1]
    x2_c = x1_c+ w2
    y2_c = y1_c + h2
    x_c = int((x1_c+x2_c)/2)
    y_c = int((y1_c+y2_c)/2)
    cv2.circle(copy_image2,(x,y),5,[0,0,255],-1)
    #cv2.imshow("Result", copy_image)
    #cv2.imshow('2', copy_image2)
    #cv2.waitKey(0)
    return ([x_c,y_c],sens)
            


def difference(background,image):
    sens = parcours_dossier(path_blanc,image)
    img_back = cv2.imread(background)
    copy = image.copy()
    back_copy =img_back.copy()
    kernel = np.ones((7,7),np.uint8)
    #img = cv2.imread(copy)
    crop_back = back_copy[250:370-5,250:440-5]
    crop_img = copy[250:370-5,250:440-5]
    diff = cv2.absdiff(crop_back,crop_img)
    _,bin = cv2.threshold(diff,80,255,cv2.THRESH_BINARY)
    bin_closed = cv2.morphologyEx(bin,cv2.MORPH_CLOSE,kernel)
    dim = bin_closed.shape
    couleurs = []
    xlist = []
    ylist = []
    for i in range((dim[0])):
        for j in range((dim[1])):
            couleurs.append(bin_closed[i][j])
            if  (couleurs[-1][0]==255 and couleurs[-1][1]==255 and couleurs[-1][2]==255):
                xlist.append(i)
                ylist.append(j)
                cv2.circle(bin_closed,(i,j),1,[0,0,255],-1)
    x = int(sum(xlist)/len(xlist))
    y = int(sum(ylist)/len(ylist))
    centre_g = (y,x)
    cv2.circle(bin_closed,(y,x),5,[0,0,255],-1)
    cv2.imshow('diff',diff)
    cv2.imshow('bin',bin_closed[0:120-5,0:190-5])
    cv2.waitKey(0)
    
    return(centre_g,xlist,ylist,dim)



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







video = cv2.VideoCapture(2)
ret,frame = video.read()
p = frame[220:400,200:500]
cv2.imshow("Vidéo", frame)


# conversio en niveau de gris (un seul canal)
img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#print(parcours_dossier(path_blanc,frame))
centre,xlist,ylist,referentiel = difference('image_cam.jpg',frame)
print(referentiel)
centre_mm = [centre[0]*350/referentiel[1]+20,centre[1]*250/referentiel[0]+25]
print(centre_mm,'mm')
C = matrice_C(centre,xlist,ylist)
vecteur_centre = np.array([centre[0], centre[1],0, 1])

longueur_x = 350
largeur_y = 250

vecteur_propre_max = orientation(C)
#depart-repere de la camera
x1, y1, z1 = 0,0,0
x2, y2, z2 = 0,350,0
x3, y3, z3 = 250,0,0
x4, y4, z4 = 250,350,0

#destination-repere du robot
x1_prime, y1_prime, z1_prime = -46.46,236.83,0
x2_prime, y2_prime, z2_prime = 286.38,236.55,0
x3_prime, y3_prime, z3_prime = -44,3,0
x4_prime, y4_prime, z4_prime = 286.98,3,0


points_src = np.array([[x1, y1, z1, 1],
                       [x2, y2, z2, 1],
                       [x3, y3, z3, 1],
                       [x4, y4, z4, 1]])

points_dst = np.array([[x1_prime, y1_prime, z1_prime,1],
                       [x2_prime, y2_prime, z2_prime,1],
                       [x3_prime, y3_prime, z3_prime,1],
                       [x4_prime, y4_prime, z4_prime,1]])



affine_transformation = np.transpose(np.linalg.lstsq(points_src, points_dst, rcond=None)[0])
print(affine_transformation)
coord_a_atteindre = np.dot(affine_transformation, np.transpose(vecteur_centre))
print('coordonnes',coord_a_atteindre)

print("Matrice de transformation affine :\n", affine_transformation)





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
#print(parcours_dossier(path_blanc,frame))
#ima = cv2.imread(parcours_dossier(path_blanc))
# chargement de l'image template à rechercher

# seuil de décision qui valide ou non le matching


