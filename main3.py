import cv2
import time
import numpy as np
import module as htm
import math 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam,hCam = 640,480

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7,maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(0, None)

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255,0,0)

while True:
    success,img = cap.read()

    # Find hand
    img = detector.findHands(img)
    lmList,bbox = detector.findPosition(img,draw=True)
    if len(lmList)!=0:

        # Filter based on size 
        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]) // 100
        if 250 < area < 1000:

            # Distane between index and Thumb
            length, img, lineInfo = detector.findDistance(4,8,img)
            # Convert volume from length to actual volume
            # Linear scale instead of logarithm scale 
            #vol = np.interp(length,[50,180],[minVol,maxVol])
            volBar = np.interp(length,[50,200],[400,150])
            volPer = np.interp(length,[50,200],[0,100])
            #print(int(length),vol)
            #volume.SetMasterVolumeLevel(vol,None)
        
            # Reduce resolution to make it smoother 
            smoothness = 10
            volPer = smoothness * round(volPer/smoothness)
            # Check fingers up 
            fingers = detector.fingersUp()
            print(fingers)
            # Set volume with pinky down
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer/100,None)
                cv2.circle(img,(lineInfo[4],lineInfo[5]),15,(0,255,0),cv2.FILLED)
                colorVol = (0,255,0)
                time.sleep(0.1)
            else:
                colorVol = (255,0,0)
           
            

            # Hand range is 50 - 300
            # Volume range -65 to 0

    
    # Drawings 
    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(255,0,0),cv2.FILLED)
    cv2.putText(img,f'{int(volPer)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img,f'Volume Set {int(cVol)}%',(300,50),cv2.FONT_HERSHEY_COMPLEX,1,colorVol,3)
    
     # Frame rate 
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)