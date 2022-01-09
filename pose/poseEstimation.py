import cv2
import mediapipe as mp
import time


class poseDetector():
    def __init__(self, mode=False, upperBodyOnly=False, smooth=True, complexity=1,
        min_detection_conf = 0.5, min_tracking_conf = 0.5) -> None:

        self.mode = mode
        self.upperBodyOnly = upperBodyOnly
        self.smooth = smooth
        self.complexity = complexity
        self.min_detection_confidence = min_detection_conf
        self.min_tracking_confidence = min_tracking_conf

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upperBodyOnly,self.complexity, self.smooth,
            self.min_detection_confidence, self.min_tracking_confidence)
        
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if draw:
            if self.results.pose_landmarks:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img


    def find_Landmarks(self, img, draw=True):
        Landmarks = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                Landmarks.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 15, (255,0,0), cv2.FILLED)
            return Landmarks









def main():
    cap = cv2.VideoCapture(0)
    detector = poseDetector()
    pTime = 0
    while True:
        success, img = cap.read()
        detector.findPose(img)
        LandMarks = detector.find_Landmarks(img)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70,50),cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,0))

        cv2.imshow("Image",img)
        cv2.waitKey(1)
if __name__ == '__main__':
    main()