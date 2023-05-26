import cv2
import numpy as np
import HandTrackingModule as htm
import facetracking as ft
import autopy
import os

from pynput.keyboard import Key, Controller
######################
wCam, hCam = 1280, 720
frameR = 200     #Frame Reduction
smoothening = 7  #random value
######################

keyboard = Controller()

######################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=2)
wScr, hScr = autopy.screen.size()
facet = ft.faceTrack()
# print(wScr, hScr)
flag = 0
while True:
    success, img = cap.read()
    dect = facet.findFace(img)
    os.system("rundll32.exe user32.dll,LockWorkStation")
    if dect:
        if flag == 0:
            print("key pressed")
            keyboard.press(Key.space)
            flag = 1
        while True:
            # Step1: Find the landmarks
            success, img = cap.read()
            dector = facet.findFace(img)
            if not dector:
                break
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)
    
            # Step2: Get the tip of the index and middle finger
            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
    
                # Step3: Check which fingers are up
                fingers = detector.fingersUp()
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                              (255, 0, 255), 2)
    
                # Step8: Both Index and middle are up: Clicking Mode
                if fingers[1] == 1 and fingers[2] == 1:
                    x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
    
                    # Step6: Smooth Values
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening
    
                    # Step7: Move Mouse
                    autopy.mouse.move(wScr - clocX, clocY)
                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY
    
                    # Step9: Find distance between fingers
                    length, img, lineInfo = detector.findDistance(8, 12, img)
    
                    # Step10: Click mouse if distance short
                    if length > 60:
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                        autopy.mouse.click()
    
                if fingers.count(1) == 5:
                
                    if plocY < (hCam/2):
                        keyboard.press(Key.up)
                    else:
                        keyboard.press(Key.down)
    
                    if plocX > (wCam/2):
                        keyboard.press(Key.left)
                    else:
                        keyboard.press(Key.right)
    
            # Step12: Display
            cv2.imshow("Image", img)
            cv2.waitKey(1)
    else:
        if flag == 1:
            print("lock")
            os.system("rundll32.exe user32.dll,LockWorkStation")
            flag = 0
            
    cv2.imshow("Image", img)
    cv2.waitKey(1)
