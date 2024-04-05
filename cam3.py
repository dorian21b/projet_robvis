import cv2
import numpy as np


back = cv2.imread('image_camq.jpg')
video = cv2.VideoCapture(2)
ret,frame = video.read()
#frame = cv2.imread('image_cam.jpg')


r = cv2.selectROI(frame)
imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
back_crop = back[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

grey_crop = cv2.cvtColor(imCrop,cv2.COLOR_BGR2GRAY)
grey_back = cv2.cvtColor(back_crop,cv2.COLOR_BGR2GRAY)

n1 = cv2.normalize(grey_back,None,0,255,cv2.NORM_MINMAX)
n2 = cv2.normalize(grey_crop,None,0,255,cv2.NORM_MINMAX)
diff_crop = cv2.absdiff(back_crop,imCrop)
coins = [[r[0],r[1]],
         [r[0]+r[2],r[1]],
         [r[0]+r[2],r[1]+r[3]],
         [r[0],r[1]+r[3]]]

print("coordonnées des quatres coins de l'image rognée :", coins)
cv2.imshow('imcrop',imCrop)
cv2.imshow('back_crop',back_crop)
cv2.imshow('diff', diff_crop)
#cv2.imwrite('crop_diff.jpg',diff_crop)
cv2.waitKey(0)
cv2.destroyAllWindows()