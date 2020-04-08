#!/usr/bin/env python3
# File name   : servo.py
# Description : Control Servos
# Author      : William
# Date        : 2019/11/21
from __future__ import division
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685
import ultra
import RGB

'''
change this form 1 to 0 to reverse servos
'''
pwm0_direction = -1
pwm1_direction = 1
pwm2_direction = 1

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

pwm0_init = 300
pwm0_range = 100
pwm0_max  = 500
pwm0_min  = 100
pwm0_pos  = pwm0_init

pwm1_init = 300
pwm1_range = 150
pwm1_max  = 450
pwm1_min  = 150
pwm1_pos  = pwm1_init

pwm2_init = 300
pwm2_range = 150
pwm2_max  = 450
pwm2_min  = 150
pwm2_pos  = pwm2_init

RGB.setup()
RGB.cyan()

def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
	newline=""
	str_num=str(new_num)
	with open("%s/servo.py"%sys.path[0],"r") as f:
		for line in f.readlines():
			if(line.find(initial) == 0):
				line = initial+"%s\n"%(str_num)
			newline += line
	with open("%s/servo.py"%sys.path[0],"w") as f:
		f.writelines(newline)	#Call this function to replace data in '.txt' file


def turnLeft(coe=1):
	global pwm2_pos
	pwm2_pos = pwm2_init + int(coe*pwm2_range*pwm2_direction)
	pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, pwm2_min)
	RGB.both_off()
	RGB.yellow()
	pwm.set_pwm(2, 0, pwm2_pos)


def turnRight(coe=1):
	global pwm2_pos
	pwm2_pos = pwm2_init - int(coe*pwm2_range*pwm2_direction)
	pwm2_pos = ctrl_range(pwm2_pos, pwm2_max, pwm2_min)
	RGB.both_off()
	RGB.yellow()
	pwm.set_pwm(2, 0, pwm2_pos)


def turnMiddle():
	global pwm2_pos
	pwm2_pos = pwm2_init
	RGB.both_on()
	pwm.set_pwm(2, 0, pwm2_pos)


def setPWM(num, pos):
	global pwm0_init, pwm1_init, pwm2_init, pwm0_pos, pwm1_pos, pwm2_pos
	pwm.set_pwm(num, 0, pos)
	if num == 0:
		pwm0_init = pos
		pwm0_pos = pos
	elif num == 1:
		pwm1_init = pos
		pwm1_pos = pos
	elif num == 2:
		pwm2_init = pos
		pwm2_pos = pos


def saveConfig():
	RGB.pink()
	replace_num('pwm0_init = ',pwm0_init)
	replace_num('pwm1_init = ',pwm1_init)
	replace_num('pwm2_init = ',pwm2_init)
	RGB.cyan()


def radar_scan():
	global pwm1_pos
	RGB.cyan()
	scan_result = 'U: '
	scan_speed = 1
	if pwm1_direction:
		pwm1_pos = pwm1_max
		pwm.set_pwm(1, 0, pwm1_pos)
		time.sleep(0.5)
		scan_result += str(ultra.checkdist())
		scan_result += ' '
		while pwm1_pos>pwm1_min:
			pwm1_pos-=scan_speed
			pwm.set_pwm(1, 0, pwm1_pos)
			scan_result += str(ultra.checkdist())
			scan_result += ' '
		pwm.set_pwm(1, 0, pwm1_init)
		pwm1_pos = pwm1_init
	else:
		pwm1_pos = pwm1_min
		pwm.set_pwm(1, 0, pwm1_pos)
		time.sleep(0.5)
		scan_result += str(ultra.checkdist())
		scan_result += ' '
		while pwm1_pos<pwm1_max:
			pwm1_pos+=scan_speed
			pwm.set_pwm(1, 0, pwm1_pos)
			scan_result += str(ultra.checkdist())
			scan_result += ' '
		pwm.set_pwm(1, 0, pwm1_init)
		pwm1_pos = pwm1_init
	RGB.both_on()
	return scan_result


def ctrl_range(raw, max_genout, min_genout):
	if raw > max_genout:
		raw_output = max_genout
	elif raw < min_genout:
		raw_output = min_genout
	else:
		raw_output = raw
	return int(raw_output)


def lookleft(speed):
	global pwm1_pos
	pwm1_pos += speed*pwm1_direction
	pwm1_pos = ctrl_range(pwm1_pos, pwm1_max, pwm1_min)
	pwm.set_pwm(1, 0, pwm1_pos)


def lookright(speed):
	global pwm1_pos
	pwm1_pos -= speed*pwm1_direction
	pwm1_pos = ctrl_range(pwm1_pos, pwm1_max, pwm1_min)
	pwm.set_pwm(1, 0, pwm1_pos)


def up(speed):
	global pwm0_pos
	pwm0_pos -= speed*pwm0_direction
	pwm0_pos = ctrl_range(pwm0_pos, pwm0_max, pwm0_min)
	pwm.set_pwm(0, 0, pwm0_pos)


def down(speed):
	global pwm0_pos
	pwm0_pos += speed*pwm0_direction
	pwm0_pos = ctrl_range(pwm0_pos, pwm0_max, pwm0_min)
	pwm.set_pwm(0, 0, pwm0_pos)


def servo_init():
	try:
		pwm.set_all_pwm(0, 300)
	except:
		pass
	pwm.set_pwm(0, 0, pwm0_init)
	pwm.set_pwm(1, 0, pwm1_init)
	pwm.set_pwm(2, 0, pwm2_init)


def clean_all():
	global pwm
	pwm = Adafruit_PCA9685.PCA9685()
	pwm.set_pwm_freq(50)
	pwm.set_all_pwm(0, 0)


def ahead():
	global pwm1_pos, pwm0_pos
	pwm.set_pwm(1, 0, pwm1_init)
	pwm.set_pwm(0, 0, pwm0_init)
	pwm1_pos = pwm1_init
	pwm0_pos = pwm0_init


def get_direction():
	return (pwm1_pos - pwm1_init)


if __name__ == '__main__':
	print('%s/servo.py'%sys.path[0])
	# radar_scan()
	# turnRight()
	# time.sleep(1)
	# turnLeft()
	# time.sleep(1)
	# turnMiddle()
	# pwm.set_pwm(0, 0, 370)
	# for i in range(0,100):
	# 	up(1)
	# 	time.sleep(0.1)
	# 	print('1')
	pass
