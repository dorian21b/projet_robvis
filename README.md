# Readme: Projet ROBVIS

## Tutoriel

Pour utiliser notre programme, il faut tout d'abord enregistrer des images des formes pour le template matching avec le programme *rec_temp.py*. Ensuite, on peut lancer le programme *template_match.py* pour obtenir les variables à envoyer au robot. Enfin, on utilise le programme *socket.py* pour envoyer les variables sur RobotStudio.

## Détails sur la démarche

![Description de l'image 1](robot_yumi.jpeg)
![Description de l'image 2](Intel.jpeg)

Notre projet était d'établir une connexion entre le robot YuMi de ABB et une caméra de profondeur. Il peut se hiérarchiser en différentes étapes :
1. Acquisition de l'image
2. Traitement de l'image
3. Communication des informations à RobotStudio
4. Actionnement du robot

### Acquisition de l'image

Nous avons fixé une caméra Intel au-dessus du robot YuMi, nous permettant de capturer des images en vue du dessus des objets.

![Description de l'image](image_cam.jpg)

### Traitement de l'image

Une fois l'image traitée, on peut récupérer tout d'abord le centre de gravité $(\bar{x},\bar{y})$ des formes. Ceci nous permet de trouver leur position en $mm$ dans le repère de la caméra.

Comme les plans de la caméra et d'interaction (celui où les objets sont disposés) sont parallèles, cela permet d'établir une relation linéaire entre les coordonnées des objets dans le repère de la caméra et le repère du robot.

**Changement de repère**

$$  \begin{bmatrix} 
x' \\ 
y' \\ 
z' \\ 
1 
\end{bmatrix} = \begin{bmatrix} 
a & b & c & t_x \\ 
d & e & f & t_y \\ 
g & h & i & t_z \\ 
0 & 0 & 0 & 1 
\end{bmatrix} 
\begin{bmatrix} 
x \\
y \\ 
z \\ 
1 
\end{bmatrix}$$

Où :

- $(x, y, z)$ sont les coordonnées du point source,
- $(x', y', z')$ sont les coordonnées du point transformé (destination),
- $(a, b, c, d, e, f, g, h, i)$ sont les coefficients de la transformation affine,
- $(t_x, t_y, t_z)$ sont les composantes de la translation dans les directions $x, y$ et $z$ respectivement.

Dans ce contexte, la matrice 

$$ \begin{bmatrix} a & b & c & t_x \\ d & e & f & t_y \\ g & h & i & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}$$  

est dite de transformation affine où les coefficients de cette matrice correspondent aux paramètres de la transformation affine. On trouve cette matrice en faisant une résolution linéaire en choisissant 4 points dont on connaît les coordonnées dans les deux repères. On trouve ensuite les coordonnées de l'objet dans le repère du robot.

Ensuite, on calcule l'orientation de l'objet. Pour ce faire, on prend les coordonnées $(x_i,y_i)$ de chaque pixel. On calcule
$$\bar{x}_i = \bar{x} - x_i$$
$$\bar{y}_i = \bar{y} - y_i$$

On crée alors une matrice C telle que

$$ C = M^TM $$

Où 

$$ M = \begin{bmatrix} \bar{x}_1 & \bar{y}_1\\
\bar{x}_2 & \bar{y}_2 \\ 
\vdots & \vdots\\
\bar{x}_n& \bar{y}_n  \end{bmatrix}$$

On extrait le vecteur propre associé à la valeur propre maximale de la matrice C, ce qui correspond à l'orientation de l'objet. On convertit ensuite ce vecteur en quaternion.

### Communication des informations à RobotStudio

Nous communiquons avec RobotStudio par protocole TCP/IP, nous transmettons les coordonnées $(x,y,z)$ de la forme, un quaternion et si l'objet est à l'endroit ou à l'envers. Les variables sont acquises par le programme Robot_R_Harm.

### Actionnement du robot

Nous utilisons alors les variables acquises pour lancer le programme sur le bras droit.

# Readme: ROBVIS Project

## Introduction

This project, named ROBVIS, was a school project aimed at establishing a connection between the ABB YuMi robot and a depth camera. It involves capturing images, processing them to extract information, and sending this data to RobotStudio for robot control.

## How to Use the Program

To use our program, follow these steps:

1. **Template Creation:** First, capture images of the shapes for template matching using the program `rec_temp.py`.
2. **Template Matching:** Next, run `template_match.py` to extract the variables needed for robot control.
3. **Sending Data to Robot:** Finally, use the program `socket.py` to send the variables to RobotStudio.

## Project Workflow Overview

Our project follows a structured process involving multiple stages:

1. **Image Acquisition**
2. **Image Processing**
3. **Communication with RobotStudio**
4. **Robot Control**

Below is a detailed explanation of each stage.

### Image Acquisition

We installed an Intel depth camera above the YuMi robot to capture top-down images of the objects. This setup allows us to get a clear view of the workspace and objects.

![YuMi Robot Setup](robot_yumi.jpeg)
![Intel Camera Setup](Intel.jpeg)

![Camera View](image_cam.jpg)

### Image Processing

Once the image is captured, we calculate the centroid \((\bar{x}, \bar{y})\) of the shapes, which gives us their position in millimeters in the camera's coordinate system. Since the camera plane and the robot’s workspace are parallel, we can establish a linear relationship between the camera and robot coordinate systems.

#### Coordinate Transformation

We use an affine transformation to convert the object's position from the camera’s coordinates to the robot’s coordinates:

\[
\begin{bmatrix} 
x' \\ 
y' \\ 
z' \\ 
1 
\end{bmatrix} = 
\begin{bmatrix} 
a & b & c & t_x \\ 
d & e & f & t_y \\ 
g & h & i & t_z \\ 
0 & 0 & 0 & 1 
\end{bmatrix}
\begin{bmatrix} 
x \\
y \\ 
z \\ 
1 
\end{bmatrix}
\]

Where:

- \((x, y, z)\) are the original coordinates,
- \((x', y', z')\) are the transformed coordinates,
- \((a, b, c, d, e, f, g, h, i)\) are the affine transformation coefficients,
- \((t_x, t_y, t_z)\) are the translation components.

The matrix is calculated by solving a linear system using four points with known coordinates in both reference frames.

#### Object Orientation

We then compute the object’s orientation using the coordinates \((x_i, y_i)\) of each pixel:

\[
\bar{x}_i = \bar{x} - x_i
\]
\[
\bar{y}_i = \bar{y} - y_i
\]

We construct matrix \(C\) as follows:

\[
C = M^T M
\]

Where:

\[
M = \begin{bmatrix} \bar{x}_1 & \bar{y}_1\\
\bar{x}_2 & \bar{y}_2 \\ 
\vdots & \vdots\\
\bar{x}_n & \bar{y}_n  \end{bmatrix}
\]

The principal eigenvector of matrix \(C\) corresponds to the object's orientation, which we then convert into a quaternion.

### Communication with RobotStudio

We communicate with RobotStudio via the TCP/IP protocol, transmitting the coordinates \((x, y, z)\) of the object, a quaternion for its orientation, and whether the object is facing up or down. The variables are received by the `Robot_R_Harm` program in RobotStudio.

### Robot Control

The acquired variables are then used to execute the program on the robot’s right arm for object manipulation.

