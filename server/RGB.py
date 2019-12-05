#!/usr/bin/python3
# File name   : motor.py
# Description : Control LEDs 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12
import RPi.GPIO as GPIO
import time

left_R = 22
left_G = 23
left_B = 24

right_R = 10
right_G = 9
right_B = 25

on  = GPIO.LOW
off = GPIO.HIGH

def both_on():
    GPIO.output(left_R, on)
    GPIO.output(left_G, on)
    GPIO.output(left_B, on)

    GPIO.output(right_R, on)
    GPIO.output(right_G, on)
    GPIO.output(right_B, on)

def setup():#initialization
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(left_R, GPIO.OUT)
    GPIO.setup(left_G, GPIO.OUT)
    GPIO.setup(left_B, GPIO.OUT)
    GPIO.setup(right_R, GPIO.OUT)
    GPIO.setup(right_G, GPIO.OUT)
    GPIO.setup(right_B, GPIO.OUT)
    both_off()

def both_off():
    GPIO.output(left_R, off)
    GPIO.output(left_G, off)
    GPIO.output(left_B, off)

    GPIO.output(right_R, off)
    GPIO.output(right_G, off)
    GPIO.output(right_B, off)

def side_on(side_X):
    GPIO.output(side_X, on)

def side_off(side_X):
    GPIO.output(side_X, off)

def police(police_time):
    for i in range (1,police_time):
        for i in range (1,3):
            side_on(left_R)
            side_on(right_B)
            time.sleep(0.1)
            both_off()
            side_on(left_B)
            side_on(right_R)
            time.sleep(0.1)
            both_off()
        for i in range (1,5):
            side_on(left_R)
            side_on(right_B)
            time.sleep(0.3)
            both_off()
            side_on(left_B)
            side_on(right_R)
            time.sleep(0.3)
            both_off()

def red():
    side_on(right_R)
    side_on(left_R)

def green():
    side_on(right_G)
    side_on(left_G)

def blue():
    side_on(right_B)
    side_on(left_B)

def yellow():
    red()
    green()    

def pink():
    red()
    blue()

def cyan():
    blue()
    green()

def side_color_on(side_X,side_Y):
    GPIO.output(side_X, on)
    GPIO.output(side_Y, on)

def side_color_off(side_X,side_Y):
    GPIO.output(side_X, off)
    GPIO.output(side_Y, off)

def turn_left(times):
    for i in range(0,times):
        both_off()
        side_on(left_G)
        side_on(left_R)
        time.sleep(0.5)
        both_off()
        time.sleep(0.5)

def turn_right(times):
    for i in range(1,times):
        both_off()
        side_on(right_G)
        side_on(right_R)
        time.sleep(0.5)
        both_off()
        time.sleep(0.5)

if __name__ == '__main__':
    setup()
    police(4)
    both_on()
    time.sleep(1)
    both_off()
    yellow()
    time.sleep(5)
    both_off()
    pink()
    time.sleep(5)
    both_off()
    cyan()
    time.sleep(5)
    both_off()
