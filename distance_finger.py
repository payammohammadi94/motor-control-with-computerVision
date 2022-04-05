import math
from numpy import interp
from cvzone.HandTrackingModule import HandDetector
from cvzone.SerialModule import SerialObject
import cv2


arduino = SerialObject("/dev/tty.usbserial-1410")

cap = cv2.VideoCapture(0)
cap.set(3,500)
cap.set(4,500)

detector = HandDetector(detectionCon=0.8)
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        bbox = hand["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand['center']  # center of the hand cx,cy
        handType = hand["type"]  # Handtype Left or Right
        fingers = detector.fingersUp(hand)
        
        x1 , y1 = lmList[4][0],lmList[4][1]
        x2 , y2 = lmList[8][0],lmList[8][1]
        
        cx,cy = (x2+x1)//2,(y1+y2)//2
        
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x1,y1),15,(205,0,255),cv2.FILLED)
        cv2.line(img,(x2,y2),(x1,y1),(255,255,0),3 )
        cv2.circle(img,(cx,cy),15,(205,0,255),cv2.FILLED)
        
        length = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        
        val = interp(int(length),[20,200],[0,255])
        print(int(val))
        arduino.sendData([int(val)])
        
        if 0<int(val)<255:
            arduino.sendData([int(val)])
            
        # Find Distance between two Landmarks. Could be same hand or different hands
        #length, info,img = detector.findDistance(lmList[8][2], lmList[6][2], img)  # with draw
        
        
            # length, info = detector.findDistance(lmList1[8], lmList2[8])  # with draw
    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()