#!/usr/bin/python3
# File name   : Ultrasonic.py
# Description : Detection distance and tracking with ultrasonic
# Website     : www.adeept.com
# Author      : William
# Date        : 2019/11/21
import RPi.GPIO as GPIO
import time

Tr = 11
Ec = 8

GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
# GPIO.setup(Ec, GPIO.IN)
GPIO.setmode(GPIO.BCM)
GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(Ec, GPIO.IN)

def checkdist():       #Reading distance
    GPIO.output(Tr, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Tr, GPIO.LOW)
    while not GPIO.input(Ec):
        pass
    t1 = time.time()
    while GPIO.input(Ec):
        pass
    t2 = time.time()
    return round((t2-t1)*340/2,2)

# def checkdist():       #Reading distance
#     GPIO.output(Tr, GPIO.HIGH)
#     time.sleep(0.000015)
#     GPIO.output(Tr, GPIO.LOW)
#     while not GPIO.input(Ec):
#         pass
#     t1 = time.time()
#     while GPIO.input(Ec):
#         t3 = time.time()
#         if ((t3-t1)*340/2)>=2:
#             break
#         pass
#     t2 = time.time()
#     return round((t2-t1)*340/2,2)

if __name__ == '__main__':
    while 1:
        print(checkdist())
        time.sleep(1)
