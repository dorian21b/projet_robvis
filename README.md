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
