#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 10:39:25 2021
@author: amir niaraki

The script camputres images and shows them every second and names them with the timestamp.png   
in order to stop the process tap 'q' on keyboard when the image preview screen is open. 
"""

import cv2
from datetime import datetime

# Open the device at the ID 0 
cap = cv2.VideoCapture(0)
c=0
#determines the second interval for image capture and save

interval=1
#Check whether user selected camera is opened successfully.

if not (cap.isOpened()):

    print('Could not open video device')
    


#To set the resolution 
#cap.set(cv2.CV_CAP_PROP_FRAME_WIDTH, 640)
#
#cap.set(cv2.CV_CAP_PROP_FRAME_HEIGHT, 480)

while(True): 
# Capture frame-by-frame

    ret, frame = cap.read()

# Display the resulting frame

#    cv2.imshow("preview",frame)
#    if ret:
##        cv2.imwrite('frame{:d}.jpg'.format(count), frame)
#        cv2.imwrite('./images/'+str(datetime.now())+'.png',frame)
#        count += 30 # i.e. at 30 fps, this advances one second
#        cap.set(1, count)
    
#    cv2.imwrite('./images/'+str(datetime.now())+'.png',frame)
##    cv2.imwrite('./images/'+str(datetime.now.replace(microsecond=0))+'.png',frame)
#    
##Waits for a user input to quit the application

    if c%(interval*5)==0:
        cv2.imshow('Frame',frame)
        cv2.imwrite('./images/'+str(datetime.now())+'.png',frame)

        cv2.waitKey(1)

        if  cv2.waitKey(1) & 0xFF == ord("q"):
            break
    c+=1


#vs.release()    
#    elif cv2.waitKey(10) & 0xFF == ord("q"):
#
#        break
#      
#    else:
#        cap.release()
#        break
  
    
# When everything done, release the capture 
cap.release()

cv2.destroyAllWindows()