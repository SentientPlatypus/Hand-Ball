import sys
import random
sys.path.insert(1, r'C:\Users\trexx\Documents\PYTHON CODE LOL\Advanced AI Visions\Hand tracker')
from HandTrackingModule import HandDetector
import cv2
from PIL import Image, ImageChops
import numpy as np


cap = cv2.VideoCapture(0)
detector = HandDetector()
generateNewCircle = True
while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    LandMarks = detector.find_Landmarks(img, draw=False)
    h, w, c = img.shape


    if generateNewCircle:
        center = (random.randint(50, w), random.randint(50, h))
        generateNewCircle = False
    
    if LandMarks:
        centroidEdges = [
            LandMarks[0],
            LandMarks[5],
            LandMarks[9],
            LandMarks[13],
            LandMarks[17]
        ]
        xValues = [x[1] for x in centroidEdges]
        yValues = [x[2] for x in centroidEdges]

        handpoint = (int(sum(xValues)/len(centroidEdges)), int(sum(yValues)/len(centroidEdges)))
        if LandMarks[0][2] > center[1]:
            print("satisfied1")
            if LandMarks[5][1] < center[0] and LandMarks[5][2]<center[1]:
                print("satisfied2")
                if LandMarks[17][1] > center[0] and LandMarks[17][2]<center[1]:
                    print("satisfied3")
                    generateNewCircle = True

        print(LandMarks[0], center[1])
    cv2.circle(img, center, 25, (255,0,0), cv2.FILLED)


    cv2.imshow("Image", img)
    cv2.waitKey(1)