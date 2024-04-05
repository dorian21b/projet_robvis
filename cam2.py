import cv2

back = cv2.imread('background_img.jpg')
img = cv2.imread('image_cam.jpg') #

diff = cv2.absdiff(back, img) 
cv2.imshow('back',back)
cv2.imshow('img',img)
cv2.imshow('difference', diff)
cv2.waitKey(0)
cv2.destroyAllWindows()