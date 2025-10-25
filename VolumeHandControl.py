import cv2 # type: ignore
import time
import numpy as np # type: ignore
import HandTrack as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL # type: ignore
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume # type: ignore


##########################
w,h=640,480
##########################




cap=cv2.VideoCapture(0)
cap.set(3,w)
cap.set(4,h)
ptime=0

detector=htm.handDetector()


devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL ,None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-20.0,None)
minVol = volRange[0]
#print(minVol)
maxVol = volRange[1]
#print(maxVol)
vol=0
volBar=400
volPer=0



while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len((lmList))!= 0:
        #print(lmList[4],lmList[8])


        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2 ,(y1+y2)//2

        cv2.circle(img,(x1,y1),12,(0,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),12,(255,255,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,200,0),3)
        cv2.circle(img,(cx,cy),12,(255,0,255),cv2.FILLED)

        l=math.hypot(x2-x1,y2-y1)
        #print(l)

        #hand range 25-150
        #volume range -63 to 0

        vol=np.interp(l,[0,180],[minVol,maxVol]) #minVol=-65.25 #maxVol=0
        volBar=np.interp(l,[100,200],[400,200])
        volPer=np.interp(l,[100,200],[0,100])
        vol = np.clip(vol, -65.25, 0.0)
        #print(int(l),vol)
        volume.SetMasterVolumeLevel(vol,None)



        
        if l<80:
            cv2.circle(img,(cx,cy),12,(255,100,0),cv2.FILLED)
            

    cv2.rectangle(img ,(30,200) ,(85,400),(255,0,0) ,3)
    cv2.rectangle(img ,(30,int(volBar)) ,(85,400),(0,255,0) ,cv2.FILLED)
    cv2.putText(img,f'VOLUME: {int(volPer)} %',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),3)
    
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime

    cv2.putText(img,f'FPS: {int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(0, 0,255 ),3)
    
    cv2.imshow("img",img)
    cv2.waitKey(1)
