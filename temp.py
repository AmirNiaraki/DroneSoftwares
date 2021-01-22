# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from datetime import datetime
import time
from image_capturer import capturer
from multiprocessing import Process
from threading import Thread



def helloer():
    while True:
        print("hello", datetime.now())
        time.sleep(1)


if __name__ == '__main__':
    
    p2 = Process(target = capturer)
    p2.start() 
    
    p1 = Process(target = helloer)
#    p1=Thread(target=helloer)
    p1.start()
#    p2=Thread(target=capturer)

    
    time.sleep(10)
    print("over")
    p1.terminate()
    p2.terminate()
   