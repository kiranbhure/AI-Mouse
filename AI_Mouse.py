import cv2
import numpy as np
import HandTrackingModule as htm
import time
import pyautogui as autopy

wCam,hCam=640,480
frameR=150
smoothning=3

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
pTime=0
plocX,plocY=0,0
clocX,clocY=0,0

detector=htm.handDetector(maxHands=1)
wScr,hScr=autopy.size()
# print(wScr,hScr)


while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img)
    if len(lmList)!=0:
        x1,y1=lmList[8][1:]
        x2,y2=lmList[12][1:]
        # print(x1,y1,x2,y2)

        fingers=detector.fingersUp()
        # print(fingers)

        cv2.rectangle(img,(frameR,frameR),(wCam-frameR,hCam-frameR),(255,0,255),2)


        if fingers[1]==1 and fingers[2]==0:
            
           

            x3=np.interp(x1,(frameR,wCam-frameR),(0,wScr))
            y3=np.interp(y1,(frameR,hCam-frameR),(0,hScr))


            clocX=plocX+(x3-plocX)/smoothning
            clocY=plocY+(y3-plocY)/smoothning

            autopy.moveTo(wScr-clocX,clocY)

            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
            plocX,plocY=clocX,clocY


        if fingers[1]==1 and fingers[2]==1:
            length,img,_=detector.findDistance(8,12,img)
            print(length)
            #clicking length(length betn two fingers)
            if length<30:
                 cv2.circle(img,(x1,y1),15,(0,255,0),cv2.FILLED)
                 autopy.click()


        


    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

    cv2.imshow("image",img)
    cv2.waitKey(1)

