import time

import cv2
import mediapipe as mp


# check frame rate
# mediapipe ne ajuta sa desenam punctele de pe mana ai 21 de puncte
# pentru a desena punctele pe mana avem o metroda mpDraw


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # pentru ca obj hands foloseste numai imagini RGB
        self.results = self.hands.process(imgRGB)
        # ne asiguram ca avem cv in  results si verificam daca ceva e detectat sau nu
        # print(results.multi_hand_landmarks)
        # trebuie verificat daca e o mana sau mai multe

        if self.results.multi_hand_landmarks:
            for handLmk in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLmk, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape  # high,width,channel
                cx, cy = int(lm.x * w), int(lm.y * h)  # pozitia centerului
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    # if id == 4:
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            # deseneasza punctele pe mana si muchile dintre ele
        return lmList


def main():
    ptime = 0
    cTime = 0
    detector = handDetector()
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList=detector.findPosition(img)


        if len(lmList)!=0:
            print(lmList)

        cTime = time.time()
        fps = 1 / (cTime - ptime)
        ptime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
    cv2.waitKey(1)


if __name__ == '__main__':
    main()
