import cv2
import numpy as np
import pyrealsense2 as rs

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        param['mouse_coords'] = (x,y)
cap=cv2.VideoCapture(2)
ret, frame=cap.read()
"""pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color,640,480,rs.format.z16,30)
mouse_param = {'mouse_coords':None}
pipeline.start(config)

cv2.namedWindow('Camera')
frames = pipeline.wait_for_frames() # Wait for a second to get frames
depth_frame = frames.get_color_frames() 
depth_image = np.asanyarray(depth_frame.get_data())
cv2.setMouseCallback('Camera',mouse_callback,mouse_param)
mouse_coords = mouse_param['mouse_coords']
if mouse_coords:
    cv2.putText(depth_image,f'Coordonnes (x,y):{mouse_coords}',(10,30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

cv2.waitKey(1)
pipeline.stop()

cv2.destroyWindow('Camera')"""

hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
lower_green = np.array([40, 60, 150])
upper_green = np.array([60, 80, 180])
mask = cv2.inRange(hsv,lower_green,upper_green)

rose = np.array([250, 192, 203], dtype=np.uint8)  
blanc = np.array([255, 255, 255], dtype=np.uint8)  

borne_inf_rose = np.array([150, 40, 100])
borne_sup_rose = np.array([200, 100, 220])

borne_inf_blanc = np.array([30, 0, 120])
borne_sup_blanc = np.array([80, 60, 255])

masque_rose = cv2.inRange(hsv, borne_inf_rose, borne_sup_rose)
masque_blanc = cv2.inRange(hsv, borne_inf_blanc, borne_sup_blanc)

photo_rose = cv2.bitwise_and(frame, frame, mask=masque_rose)
photo_blanc = cv2.bitwise_and(frame, frame, mask=masque_blanc)

img_g = cv2.bitwise_and(frame,frame, mask=mask)
cv2.imshow('mask',img_g)    
cv2.imshow("Rose", photo_rose)
cv2.imshow("White", photo_blanc)
if cv2.waitKey(0)&0xFF==ord('s'):
    cv2.imwrite('image_cam.jpg',frame)
cap.release()
cv2.destroyAllWindows()