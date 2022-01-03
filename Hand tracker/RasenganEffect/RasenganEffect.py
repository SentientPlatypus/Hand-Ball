import sys
sys.path.insert(1, r'C:\Users\trexx\Documents\PYTHON CODE LOL\Advanced AI Visions\Hand tracker')
from HandTrackingModule import HandDetector
import cv2
from PIL import Image, ImageChops
import numpy as np
cap = cv2.VideoCapture(0)
detector = HandDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img, True)
    LandMarks = detector.find_Landmarks(img, 0, False)

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


        center = (int(sum(xValues)/len(centroidEdges)), int(sum(yValues)/len(centroidEdges)))


        areaofpolygonlist = []
        for x in range(len(yValues)):
            areaofpolygonlist.append(yValues[x]*xValues[x-1]-yValues[x-1]*xValues[x])
        totalArea = abs((1/2)*sum(areaofpolygonlist))


        def determineRadius(area):
            return 25+4*int(area/1000)

        radius = determineRadius(totalArea)
        rasengan_img = Image.open(r"C:\Users\trexx\Documents\PYTHON CODE LOL\Advanced AI Visions\Hand tracker\RasenganEffect\rasengan.png").convert("RGB")
        rasengan_img = rasengan_img.resize((radius*2, radius*2))
        rasengan_img = ImageChops.invert(rasengan_img)
        img_pil = Image.fromarray(img)
        #toPasteAt = (center[0]-radius, center[1]+radius)
        toPasteAt = (center[0]-radius, center[1]-radius)
        img_pil.paste(rasengan_img, toPasteAt)


        img = np.asarray(img_pil)
        

        print(center, radius)






    cv2.imshow("Image", img)
    cv2.waitKey(1)