import cv2
import mediapipe as mp
import time
cap = cv2.VideoCapture(0)

pTime = 0
while True:
    success, img = cap.read()



    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70,50),cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,0))

    cv2.imshow("Image",img)
    cv2.waitKey(1)