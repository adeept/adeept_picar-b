#!/usr/bin/python3
# File name   : findline.py
# Description : line tracking 
# Website     : www.adeept.com
# Author      : William
# Date        : 2019/11/21
import RPi.GPIO as GPIO
import time
import move
import servo

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)
    #motor.setup()

def run():
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    #print('R%d   M%d   L%d'%(status_right,status_middle,status_left))
    if status_middle == 1:
        move.move(100, 'forward')
    elif status_left == 1:
        servo.turnRight()
        move.move(100, 'forward')
    elif status_right == 1:
        servo.turnLeft()
        move.move(100, 'forward')
    else:
        move.move(100, 'backward')

if __name__ == '__main__':
    try:
        setup()
        move.setup()
        while 1:
            run()
        pass
    except KeyboardInterrupt:
        move.destroy()
