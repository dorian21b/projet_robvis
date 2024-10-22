# Readme: Projet ROBVIS

This project, named ROBVIS, was a school project aimed at establishing a connection between the ABB YuMi robot and a depth camera. It involves capturing images, processing them to extract information, and sending this data to RobotStudio for robot control.

## Tutorial

To use our program, follow these steps:

1. Capture images of the shapes for template matching using the *rec_temp.py* program.
2. Run the *template_match.py* program to obtain the necessary variables for the robot.
3. Use the *socket.py* program to send the variables to RobotStudio.

## Project Workflow Overview

![Description de l'image 1](robot_yumi.jpeg)
![Description de l'image 2](Intel.jpeg)

The project can be broken down into several key stages:

1. **Image Acquisition**
2. **Image Processing**
3. **Communication with RobotStudio**
4. **Robot Actuation**

### Image Acquisition

We mounted an Intel camera above the YuMi robot, allowing us to capture top-down images of the objects.

![Description de l'image](image_cam.jpg)

### Image Processing

Once the image is processed, we can first retrieve the centroid $(\bar{x},\bar{y})$ of the shapes. This allows us to determine their position in millimeters in the camera's coordinate system.

Since the camera plane and the interaction plane (where the objects are placed) are parallel, this establishes a linear relationship between the coordinates of the objects in the camera's coordinate system and the robot's coordinate system.

**Coordinate Transformation**

The transformation between the source and destination coordinates is defined as follows:

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

Where :

- $(x, y, z)$ are the coordinates of the source point,
- $(x', y', z')$ are the coordinates of the transformed point (destination),
- $(a, b, c, d, e, f, g, h, i)$ are the coefficients of the affine transformation,
- $(t_x, t_y, t_z)$ are the translation components in the $x, y$ and $z$ directions, respectively.

In this context, the matrix

$$ 
\begin{bmatrix} 
a & b & c & t_x \\ 
d & e & f & t_y \\ 
g & h & i & t_z \\ 
0 & 0 & 0 & 1 
\end{bmatrix} 
$$

is called an affine transformation matrix, where the coefficients of this matrix correspond to the parameters of the affine transformation. This matrix is obtained by performing a linear resolution using four points with known coordinates in both reference frames. We then find the coordinates of the object in the robot's coordinate system.

Next, we calculate the orientation of the object. To do this, we take the coordinates $(x_i,y_i)$ of each pixel. We calculate

$$\bar{x}_i = \bar{x} - x_i$$
$$\bar{y}_i = \bar{y} - y_i$$

We then create a matrix $C$ such that

$$ C = M^TM $$

Where:

$$ M = \begin{bmatrix} \bar{x}_1 & \bar{y}_1\\
\bar{x}_2 & \bar{y}_2 \\ 
\vdots & \vdots\\
\bar{x}_n& \bar{y}_n  \end{bmatrix}$$

We extract the eigenvector associated with the largest eigenvalue of matrix $C$, which corresponds to the orientation of the object. We then convert this vector into a quaternion.

### Communication of Information to RobotStudio

We communicate with RobotStudio via the TCP/IP protocol, transmitting the coordinates $(x,y,z)$ of the shape, a quaternion, and whether the object is upright or inverted. The variables are received by the Robot_R_Harm program.

### Robot Actuation

We then use the acquired variables to run the program on the robot's right arm.
