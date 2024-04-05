import cv2

video = cv2.VideoCapture(2)
ret,frame = video.read()
cv2.imshow('frame',frame)
if cv2.waitKey(0)&0xff == ord('s'):
    cv2.imwrite('vackground_img.jpg',frame)
video.release()
cv2.destroyAllWindows()