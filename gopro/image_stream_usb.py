# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 11:59:17 2020

@author: amire
"""

import cv2
import numpy as np
from goprocam import GoProCamera
from goprocam import constants
#cascPath="/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
#faceCascade = cv2.CascadeClassifier(cascPath)
gpCam = GoProCamera.GoPro()
print("here0")

#cap = cv2.VideoCapture("udp://127.0.0.1:10000")
#cap = cv2.VideoCapture(0)
  # Set UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 12345
fs = FrameSegment(s, port)
 
cap = cv2.VideoCapture(0)
print("here1")
while True:
    ret, frame = cap.read()
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#    faces = faceCascade.detectMultiScale(
#        gray,
#        scaleFactor=1.1,
#        minNeighbors=5,
#        minSize=(30, 30),
#        flags=cv2.CASCADE_SCALE_IMAGE
#    )
#    for (x, y, w, h) in faces:
#        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow("GoPro OpenCV", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()