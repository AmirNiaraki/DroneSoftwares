#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 17:44:09 2021

@author: filet
"""


#First run a grep on the USB port to create a txt log file of all GPS locations
#i.e. sudo cat /dev/ttyACM0 | grep -i GNGLL > GPSlog.txt


import pynmea2
from datetime import datetime
import time
import subprocess

def shell_call():
   result = subprocess.run('ls', stdout=subprocess.PIPE).stdout.decode('UTF-8')
   print(result)
   script = "cat /dev/ttyACM0 | grep -i GNGLL & sleep 5; kill $!"
#    GNGLL=subprocess.call(script, shell=True)
#    print("itis",GNGLL)
    
#    return GNGLL



def main():
    while True:
            
        with open('GPSlog.txt', 'r') as f:
            last_line = f.readlines()[-2]
        print(last_line)
        #nmea = '$GNGLL,4201.21700,N,09340.84216,W,003933.00,A,A*6B'
        nmea=last_line
#        nmea=shell_call()
        nmeaobj = pynmea2.parse(nmea)
        print("latitude:",nmeaobj.latitude)
        print("longitude", nmeaobj.longitude)
    #    print("Time stamp:"+str(datetime.today())+"\n"+str(nmeaobj.timestamp.hour+20)+":"+str(nmeaobj.timestamp.minute)+":"+str(nmeaobj.timestamp.second))
        print("Time stamp:",datetime.now().time())
        time.sleep(5)





if __name__ == '__main__':
    main()