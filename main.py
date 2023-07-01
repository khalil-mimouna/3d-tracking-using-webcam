import cv2
from cvzone.HandTrackingModule import HandDetector
import socket
width , height = 1280 , 720

cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

detector = HandDetector(maxHands=1,detectionCon=0.8)

#com with unity (broadcasting)
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverAdressPort = ("localhost",5052)
while True:
    succes , img =cap.read()
    hands, img =detector.findHands(img)
    data =[]
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        #print(lmList)
        for lm in lmList:
            #need to change the y because in opencv and unity the direction are opposite
            data.extend([lm[0],height - lm[1],lm[2]])
        #print(data)     
        sock.sendto(str.encode(str(data)),serverAdressPort)
    img = cv2.resize(img,(0,0),None,0.5,0.5)
    cv2.imshow("Image",img)
    cv2.waitKey(1)



