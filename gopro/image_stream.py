# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 14:07:32 2020

@author: amir niaraki
please refer to https://github.com/konradit/gopro-py-api for details on API
"""

from goprocam import GoProCamera, constants
import time
#goproCamera = GoProCamera.GoPro()
#
#
##Shooting video for 10 seconds
#goproCamera.shoot_video(10)
#
#
##taking 1 pic after waiting for 10 seconds
#import time
#gpCam = GoProCamera.GoPro()
#
#print(gpCam.take_photo(10))
#
##download the pic after 4 seconds
#gpCam = GoProCamera.GoPro()
#TIMER=4
#gpCam.downloadLastMedia(gpCam.take_photo(TIMER)) #take a photo in 4 seconds and download it.
#

#test for printing current time, taking a pic, and download it to pc
#gpCam = GoProCamera.GoPro()
#gpCam.take_photo(1)
#
#from datetime import datetime
#
#now = datetime.now()
#
#current_time = now.strftime("%H:%M:%S")
#print("Current Time =", current_time)
#
##wait(4)
#time.sleep(5)
#gpCam.downloadLastMedia()
# 



######################################################################
import cv2
from time import time
import socket
from goprocam import GoProCamera, constants

WRITE = False
gpCam = GoProCamera.GoPro()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
t=time()
gpCam.livestream("start")
gpCam.video_settings(res='1080p', fps='30')
gpCam.gpControlSet(constants.Stream.WINDOW_SIZE, constants.Stream.WindowSize.R720)
#cap = cv2.VideoCapture("udp://10.5.5.9:8554", cv2.CAP_FFMPEG)
cap = cv2.VideoCapture("udp://127.0.0.1:10000", cv2.CAP_FFMPEG)

counter = 0
while True:
    nmat, frame = cap.read()
    cv2.imshow("GoPro OpenCV", frame)
    if WRITE == True:
        cv2.imwrite(str(counter)+".jpg", frame)
        counter += 1
        if counter >= 10:
            break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if time() - t >= 2.5:
        sock.sendto("_GPHD_:0:0:2:0.000000\n".encode(), ("10.5.5.9", 8554))
        t=time()
# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()