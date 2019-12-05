#!/usr/bin/env python3
# File name   : move.py
# Description : Control Motor
# Product     : PiCar-C
# Website     : www.adeept.com
# Author      : William
# Date        : 2019/11/21
import time
import RPi.GPIO as GPIO

# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN    = 4
Motor_B_EN    = 17

Motor_A_Pin1  = 14
Motor_A_Pin2  = 15
Motor_B_Pin1  = 27
Motor_B_Pin2  = 18

Dir_forward   = 0
Dir_backward  = 1

pwn_A = 0
pwm_B = 0

def motorStop():#Motor stops
	GPIO.output(Motor_A_Pin1, GPIO.LOW)
	GPIO.output(Motor_A_Pin2, GPIO.LOW)
	GPIO.output(Motor_B_Pin1, GPIO.LOW)
	GPIO.output(Motor_B_Pin2, GPIO.LOW)
	GPIO.output(Motor_A_EN, GPIO.LOW)
	GPIO.output(Motor_B_EN, GPIO.LOW)


def setup():#Motor initialization
	global pwm_A, pwm_B
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(Motor_A_EN, GPIO.OUT)
	GPIO.setup(Motor_B_EN, GPIO.OUT)
	GPIO.setup(Motor_A_Pin1, GPIO.OUT)
	GPIO.setup(Motor_A_Pin2, GPIO.OUT)
	GPIO.setup(Motor_B_Pin1, GPIO.OUT)
	GPIO.setup(Motor_B_Pin2, GPIO.OUT)

	motorStop()
	try:
		pwm_A = GPIO.PWM(Motor_A_EN, 1000)
		pwm_B = GPIO.PWM(Motor_B_EN, 1000)
	except:
		pass


def motor_A(direction, speed):#Motor 2 positive and negative rotation
	if direction == Dir_backward:
		GPIO.output(Motor_B_Pin1, GPIO.HIGH)
		GPIO.output(Motor_B_Pin2, GPIO.LOW)
		pwm_A.start(100)
		pwm_A.ChangeDutyCycle(speed)
	elif direction == Dir_forward:
		GPIO.output(Motor_B_Pin1, GPIO.LOW)
		GPIO.output(Motor_B_Pin2, GPIO.HIGH)
		pwm_A.start(100)
		pwm_A.ChangeDutyCycle(speed)


def motor_B(direction, speed):#Motor 1 positive and negative rotation
	if direction == Dir_forward:#
		GPIO.output(Motor_A_Pin1, GPIO.HIGH)
		GPIO.output(Motor_A_Pin2, GPIO.LOW)
		pwm_B.start(100)
		pwm_B.ChangeDutyCycle(speed)
	elif direction == Dir_backward:
		GPIO.output(Motor_A_Pin1, GPIO.LOW)
		GPIO.output(Motor_A_Pin2, GPIO.HIGH)
		pwm_B.start(0)
		pwm_B.ChangeDutyCycle(speed)


def move(speed, direction):   # 0 < radius <= 1
	if direction == 'forward':
		motor_A(0, speed)
		motor_B(1, speed)
	elif direction == 'backward':
		motor_A(1, speed)
		motor_B(0, speed)
	elif direction == 'no':
		motorStop()
	else:
		pass


def destroy():
	motorStop()
	GPIO.cleanup()             # Release resource


if __name__ == '__main__':
	try:
		setup()
		move(100, 'forward')
		time.sleep(1.3)
		motorStop()
		destroy()
	except KeyboardInterrupt:
		destroy()

