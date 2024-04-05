import cv2

video = cv2.VideoCapture(2)
ret,frame = video.read()
i = 0
while ret:
    crop = frame[300:350,300:350]
    cv2.imshow('vid',frame)
    cv2.imshow('crop',crop)
    if cv2.waitKey(0)&0xFF == ord('s'):
        cv2.imwrite(f'template_blanc/template16.png',crop)
        i += 1
    elif cv2.waitKey(0)&0xFF == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
