import cv2
import mediapipe as mp
import time





class HandDetector():
    def __init__(self, mode = False, max_hands=2, modelComplexity=1, detectionConfidence = 0.5, trackConfidence = 0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detectionConfidence = detectionConfidence
        self.modelComplexity = modelComplexity
        self.trackConfidence = trackConfidence
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.max_hands, self.modelComplexity, self.detectionConfidence, self.trackConfidence)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLM in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLM, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_Landmarks(self, img, handNumber = 0, draw = True):
        #print(results.multi_hand_landmarks)
        #[
        # landmark {
        #   x:###
        #   y:###
        #   z:###
        # }
        # ]
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNumber]
            for id, lm in enumerate(myHand.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)      
        return lmList

            

def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img=img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        LandMarks = detector.find_Landmarks(img=img, draw=True)

        if LandMarks:
            print(LandMarks[0])
        



        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
if __name__ == "__main__":
    main()