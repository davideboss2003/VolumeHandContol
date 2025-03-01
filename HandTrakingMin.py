import cv2
import mediapipe as mp
import time
#check frame rate
# mediapipe ne ajuta sa desenam punctele de pe mana ai 21 de puncte
#pentru a desena punctele pe mana avem o metroda mpDraw

cap=cv2.VideoCapture(0)

mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
ptime=0
cTime=0

while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #pentru ca obj hands foloseste numai imagini RGB
    results=hands.process(imgRGB)
   #ne asiguram ca avem cv in  results si verificam daca ceva e detectat sau nu
    #print(results.multi_hand_landmarks)
    # trebuie verificat daca e o mana sau mai multe

    if results.multi_hand_landmarks:
        for handLmk in results.multi_hand_landmarks:
            for id, lm in enumerate(handLmk.landmark):
                #print(id,lm)
                h,w,c=img.shape #high,width,channel
                cx,cy = int(lm.x*w),int(lm.y*h) #pozitia centerului
                print(id,cx,cy)
                if id==4:
                    cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)
            mpDraw.draw_landmarks(img,handLmk, mpHands.HAND_CONNECTIONS)
            #deseneasza punctele pe mana si muchile dintre ele


    cTime=time.time()
    fps=1/(cTime-ptime)
    ptime= cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)
#facem asta tot timpul sa damm run la webcam


