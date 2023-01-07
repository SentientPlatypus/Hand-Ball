import sys
import random
import time
sys.path.insert(1, r'W:\Code\Visions\Advanced AI Visions\Hand tracker')
from HandTrackingModule import HandDetector
import cv2
from PIL import Image, ImageChops
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pandas as pd
import csv
import datetime
import time


print("we out")
def writeScore(score):
    with open(r"C:\Users\trexx\Documents\PYTHON CODE LOL\Advanced AI Visions\Hand tracker\catchBall\scores.csv", "a",newline='\n', encoding='utf-8') as f:
        w = csv.writer(f)
        date = str(datetime.datetime.date(datetime.datetime.now()))
        w.writerow([score, date])

def getHighScore():
    dataframe = pd.read_csv(r"scores.csv")
    dataframe = dataframe.sort_values(["score"], ascending=False ,key= lambda x: x)
    firstRow = dataframe.head(1)
    score = firstRow["score"]
    return score[1]

seconds = 300
cap = cv2.VideoCapture(0)
detector = HandDetector()
generateNewCircle = True
score = 0
displaySeconds = f"{seconds/10}"
while True:
    score = int(score)
    sucess, img = cap.read()
    img = cv2.flip(img, 1)
    if seconds <= 0:
        if score > getHighScore():
            cv2.putText(img, f"NEW HIGH SCORE: {score}", (10,h-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.putText(img, f"Game complete! Score: {score}", (10,h-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        writeScore(score=score)
        cv2.imshow("Image", img)
        time.sleep(5)
        break

    h, w, c = img.shape
    img = detector.findHands(img)
    LandMarks = detector.find_Landmarks(img, draw=False)
    cv2.putText(img, f"Score: {score}", (10,70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
    if seconds % 10 == 0:
        displaySeconds = seconds/10
    cv2.putText(img, f"Time left: {displaySeconds}", (10,h-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        


    if generateNewCircle:
        center = (random.randint(50, w-50), random.randint(50, h-50))
        generateNewCircle = False
        start = time.time()
    
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
        centroidEdges = list(zip(xValues,yValues))

        handpoint = (int(sum(xValues)/len(centroidEdges)), int(sum(yValues)/len(centroidEdges)))
        if Polygon(centroidEdges).contains(Point(center)):
            generateNewCircle = True
            end = time.time()
            score += 100-(end-start)*10

        #print(LandMarks[0], center[1])
    cv2.circle(img, center, 25, (255,0,0), cv2.FILLED)
    cv2.imshow("Image", img)
    seconds-=1
    cv2.waitKey(1)
print("done")
