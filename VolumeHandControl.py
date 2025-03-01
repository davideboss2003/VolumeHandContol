import time
from operator import length_hint

import cv2
import numpy as np
import HandTrakingModule as htm
from HandTrakingModule import handDetector
import math
import pyautogui



from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

####################AICI PARAMETRII###########
wCam,hCam=1280,720
##############################################
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime =0

detector = htm.handDetector(detectionCon=0.7)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volumeRange= volume.GetVolumeRange()

minVol=volumeRange[0]
maxVol=volumeRange[1]

vol=0
volBar=400 #ca este minimul adica 0 la volum
volProcent=0


def fingersUp(lmList):
    if len(lmList) == 0:  # Verifica daca lista este goala
        return [0, 0, 0, 0, 0]  # Returneaza o lista cu toate degetele coborate

    fingers = []
    # Thumb (degetul mare)
    if lmList[4][1] > lmList[3][1]:  # Daca x-ul degetului mare e mai mare decat al bazei
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers (index, middle, ring, pinky)
    for id in [8, 12, 16, 20]:  # Top tips of fingers
        if lmList[id][2] < lmList[id - 2][2]:  # Daca y-ul extremitatii e mai mic decat al bazei
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers




while True:
    success,img=cap.read()
#cautam mana si desenam pe ea si gasim pozitiaac
    detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)

    if len(lmList)!=0:


        x1,y1=lmList[4][1],lmList[4][2] #indexul 4 este degetul mare primu param si al doilea
        x2,y2=lmList[8][1],lmList[8][2] #la fel

        #ne trebuie centrul liniei aceleia
        cx, cy=(x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3) #linie intre cele 2 degete

        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

        lungime=math.hypot(x2-x1,y2-y1)
        #print(lungime)



        #hand range 50 - 300
        #volume range -65 - 0

        vol=np.interp(lungime,[50,300], [minVol, maxVol])
        volBar=np.interp(lungime,[50,300], [400, 150])
        volProcent=np.interp(lungime,[50,300], [0, 100])
        #vol cand e 400 e min si cand e 150 e max in bara
        print(int(lungime),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if lungime<50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        #o sa ne trebuiasca sa aflam lungimea liniei dintre cele 2 degete

    fingers = fingersUp(lmList)
    # Control Media
    if fingers == [1, 1, 1, 1, 1]:  # Play/Pause (doar degetul mare ridicat)
        pyautogui.press('playpause')
    elif fingers == [0, 0, 1, 1, 1]:  # Next Track (degetul mare + index)
        pyautogui.press('nexttrack')
    elif fingers == [0, 0, 0, 0, 1]:  # Previous Track (degetul mare + mijlociu)
        pyautogui.press('prevtrack')

    cv2.rectangle(img,(50,150), (85,400), (0,255,0),3)
    cv2.rectangle(img,(50,int(volBar)), (85,400), (0,255,0),cv2.FILLED)
    cv2.putText(img,f'{int(volProcent)}%',(40,450),cv2.FONT_HERSHEY_PLAIN,3,(0,250,0),3)


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    cv2.waitKey(1)