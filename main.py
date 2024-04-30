# Packages Required - mediapipe & opencv-python
# Minimum code for hand tracking

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) # webcam

mpHands = mp.solutions.hands
hands = mpHands.Hands() # Default paramaters - static_image_mode, max_num_hands,min_detection_confidence,min_tracking_confidence
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) # hands only used RGB image
    results = hands.process(imgRGB)
    #Extract Landmarks for each hand
    # results.multi_hand_landmarks - If hand detected else none
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # Each hand
            #Landmark info is x,y and ID number
            # ID is like 0 for bottom, 1 for thumb, 2 for index midpoint....
            for id,lm in enumerate(handLms.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h) # x and y coordinate
                print(id,cx,cy)
                #if id==0:
                #    cv2.circle(img,(cx,cy),25,(255,0,255),cv2.FILLED) # draw circle at 0 landmark 
                #Values are decimal rations so multiply with height and width to get pixel value 
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS) # On img draw the points 
            # hand connections gives lines between points 
    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
    # text, position, font, scale, color, thickness
    cv2.imshow("Image",img)
    cv2.waitKey(1) # Frame interval 


