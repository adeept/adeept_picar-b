#!/usr/bin/env/python
# File name   : server.py
# Production  : PiCar-C
# Website	 : www.adeept.com
# Author	  : William
# Date		: 2019/11/21
import servo
servo.servo_init()
import socket
import time
import threading
import GUImove as move
import Adafruit_PCA9685
import os
import FPV
import info

import LED
import GUIfindline as findline
import switch
import ultra
import PID

import random

SR_dect = 0
appConnection = 1
Blockly = 0

if SR_dect:
	try:
		import SR
		SR_dect = 1
	except:
		SR_dect = 0
		pass
SR_mode = 0


if appConnection:
	try:
		import appserver
		AppConntect_threading=threading.Thread(target=appserver.app_ctrl)		 #Define a thread for app ctrl
		AppConntect_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
		AppConntect_threading.start()									 #Thread starts
	except:
		pass


MPU_connection = 1

servo_speed  = 5
functionMode = 0
dis_keep = 0.35
goal_pos = 0
tor_pos  = 1
mpu_speed = 1
init_get = 0

range_min = 0.55

R_set = 0
G_set = 0
B_set = 0


def start_blockly():
	os.system("cd //home/pi/Blockly_picar-c && sudo python3 server.py")


if Blockly:
	try:
		blockly_threading=threading.Thread(target=start_blockly)     #Define a thread for Blockly
		blockly_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
		blockly_threading.start()									 #Thread starts
	except:
		pass


def autoDect(speed):
	move.motorStop()
	servo.ahead()
	time.sleep(0.3)
	getMiddle = ultra.checkdist()
	print('M%f'%getMiddle)

	servo.ahead()
	servo.lookleft(100)
	time.sleep(0.3)
	getLeft = ultra.checkdist()
	print('L%f'%getLeft)

	servo.ahead()
	servo.lookright(100)
	time.sleep(0.3)
	getRight = ultra.checkdist()
	print('R%f'%getRight)

	if getMiddle < range_min and min(getLeft, getRight) > range_min:
		if random.randint(0,1):
			servo.turnLeft()
		else:
			servo.turnRight()
		move.move(speed,'forward')
		time.sleep(0.5)
		move.motorStop()
	elif getLeft < range_min and min(getMiddle, getRight) > range_min:
		servo.turnRight(0.7)
		move.move(speed,'forward')
		time.sleep(0.5)
		move.motorStop()
	elif getRight < range_min and min(getMiddle, getLeft) > range_min:
		servo.turnLeft(0.7)
		move.move(speed,'forward')
		time.sleep(0.5)
		move.motorStop()
	elif max(getLeft, getMiddle) < range_min and getRight > range_min:
		servo.turnRight()
		move.move(speed,'forward')
		time.sleep(0.5)
		move.motorStop()
	elif max(getMiddle, getRight) < range_min and getLeft >range_min:
		servo.turnLeft()
		move.move(speed, 'forward')
		time.sleep(0.5)
		move.motorStop()
	elif max(getLeft, getMiddle, getRight) < range_min:
		move.move(speed,'backward')
		time.sleep(0.5)
		move.motorStop()
	else:
		servo.turnMiddle()
		move.move(speed,'forward')
		time.sleep(0.5)
		move.motorStop()


class Servo_ctrl(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(Servo_ctrl, self).__init__(*args, **kwargs)
		self.__flag = threading.Event()
		self.__flag.set()
		self.__running = threading.Event()
		self.__running.set()

	def run(self):
		global goal_pos, servo_command, init_get, functionMode
		while self.__running.isSet():
			self.__flag.wait()
			if functionMode != 6:
				if servo_command == 'lookleft':
					servo.lookleft(servo_speed)
				elif servo_command == 'lookright':
					servo.lookright(servo_speed)
				elif servo_command == 'up':
					servo.up(servo_speed)
				elif servo_command == 'down':
					servo.down(servo_speed)
				else:
					pass

			if functionMode == 4:
				servo.ahead()
				findline.run()
				if not functionMode:
					move.motorStop()
			elif functionMode == 5:
				autoDect(50)
				if not functionMode:
					move.motorStop()
			elif functionMode == 6:
				if MPU_connection:
					accelerometer_data = sensor.get_accel_data()
					X_get = accelerometer_data['x']
					if not init_get:
						goal_pos = X_get
						init_get = 1
					if servo_command == 'up':
						servo.up(servo_speed)
						time.sleep(0.2)
						accelerometer_data = sensor.get_accel_data()
						X_get = accelerometer_data['x']
						goal_pos = X_get
					elif servo_command == 'down':
						servo.down(servo_speed)
						time.sleep(0.2)
						accelerometer_data = sensor.get_accel_data()
						X_get = accelerometer_data['x']
						goal_pos = X_get
					if abs(X_get-goal_pos)>tor_pos:
						if X_get > goal_pos:
							servo.down(int(mpu_speed*abs(X_get - goal_pos)))
						elif X_get < goal_pos:
							servo.up(int(mpu_speed*abs(X_get - goal_pos)))
						time.sleep(0.03)
						continue
				else:
					functionMode = 0
					try:
						self.pause()
					except:
						pass

			time.sleep(0.03)

	def pause(self):
		self.__flag.clear()

	def resume(self):
		self.__flag.set()

	def stop(self):
		self.__flag.set()
		self.__running.clear()


class SR_ctrl(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(SR_ctrl, self).__init__(*args, **kwargs)
		self.__flag = threading.Event()
		self.__flag.set()
		self.__running = threading.Event()
		self.__running.set()

	def run(self):
		global goal_pos, servo_command, init_get, functionMode
		while self.__running.isSet():
			self.__flag.wait()
			if SR_mode:
				voice_command = SR.run()
				if voice_command == 'forward':
					turn.turnMiddle()
					move.move(speed_set, 'forward')
					time.sleep(1)
					move.motorStop()

				elif voice_command == 'backward':
					turn.turnMiddle()
					move.move(speed_set, 'backward')
					time.sleep(1)
					move.motorStop()

				elif voice_command == 'left':
					servo.turnLeft()
					move.move(speed_set, 'forward')
					time.sleep(1)
					turn.turnMiddle()
					move.motorStop()

				elif voice_command == 'right':
					servo.turnRight()
					move.move(speed_set, 'forward')
					time.sleep(1)
					turn.turnMiddle()
					move.motorStop()

				elif voice_command == 'stop':
					turn.turnMiddle()
					move.motorStop()
			else:
				self.pause()

	def pause(self):
		self.__flag.clear()

	def resume(self):
		self.__flag.set()

	def stop(self):
		self.__flag.set()
		self.__running.clear()


def info_send_client():
	SERVER_IP = addr[0]
	SERVER_PORT = 2256   #Define port serial 
	SERVER_ADDR = (SERVER_IP, SERVER_PORT)
	Info_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Set connection value for socket
	Info_Socket.connect(SERVER_ADDR)
	print(SERVER_ADDR)
	while 1:
		try:
			Info_Socket.send((info.get_cpu_tempfunc()+' '+info.get_cpu_use()+' '+info.get_ram_info()+' '+str(servo.get_direction())).encode())
			time.sleep(1)
		except:
			time.sleep(10)
			pass


def FPV_thread():
	global fpv
	fpv=FPV.FPV()
	fpv.capture_thread(addr[0])


def  ap_thread():
	os.system("sudo create_ap wlan0 eth0 Groovy 12345678")


def run():
	global servo_move, speed_set, servo_command, functionMode, init_get, R_set, G_set, B_set, SR_mode
	servo.servo_init()
	move.setup()
	findline.setup()
	direction_command = 'no'
	turn_command = 'no'
	servo_command = 'no'
	speed_set = 100
	rad = 0.5

	info_threading=threading.Thread(target=info_send_client)	#Define a thread for FPV and OpenCV
	info_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
	info_threading.start()									 #Thread starts


	servo_move = Servo_ctrl()
	servo_move.start()
	servo_move.pause()
	findline.setup()
	while True: 
		data = ''
		data = str(tcpCliSock.recv(BUFSIZ).decode())
		if not data:
			continue

		elif 'forward' == data:
			direction_command = 'forward'
			move.move(speed_set, direction_command)
		
		elif 'backward' == data:
			direction_command = 'backward'
			move.move(speed_set, direction_command)

		elif 'DS' in data:
			direction_command = 'no'
			move.move(speed_set, direction_command)

		elif 'left' == data:
			# turn_command = 'left'
			servo.turnLeft()

		elif 'right' == data:
			# turn_command = 'right'
			servo.turnRight()

		elif 'TS' in data:
			# turn_command = 'no'
			servo.turnMiddle()


		elif 'Switch_1_on' in data:
			switch.switch(1,1)
			tcpCliSock.send(('Switch_1_on').encode())

		elif 'Switch_1_off' in data:
			switch.switch(1,0)
			tcpCliSock.send(('Switch_1_off').encode())

		elif 'Switch_2_on' in data:
			switch.switch(2,1)
			tcpCliSock.send(('Switch_2_on').encode())

		elif 'Switch_2_off' in data:
			switch.switch(2,0)
			tcpCliSock.send(('Switch_2_off').encode())

		elif 'Switch_3_on' in data:
			switch.switch(3,1)
			tcpCliSock.send(('Switch_3_on').encode())

		elif 'Switch_3_off' in data:
			switch.switch(3,0)
			tcpCliSock.send(('Switch_3_off').encode())


		elif 'function_1_on' in data:
			servo.ahead()
			time.sleep(0.2)
			tcpCliSock.send(('function_1_on').encode())
			radar_send = servo.radar_scan()
			tcpCliSock.sendall(radar_send.encode())
			print(radar_send)
			time.sleep(0.3)
			tcpCliSock.send(('function_1_off').encode())


		elif 'function_2_on' in data:
			functionMode = 2
			fpv.FindColor(1)
			tcpCliSock.send(('function_2_on').encode())

		elif 'function_3_on' in data:
			functionMode = 3
			fpv.WatchDog(1)
			tcpCliSock.send(('function_3_on').encode())

		elif 'function_4_on' in data:
			functionMode = 4
			servo_move.resume()
			tcpCliSock.send(('function_4_on').encode())

		elif 'function_5_on' in data:
			functionMode = 5
			servo_move.resume()
			tcpCliSock.send(('function_5_on').encode())

		elif 'function_6_on' in data:
			if MPU_connection:
				functionMode = 6
				servo_move.resume()
				tcpCliSock.send(('function_6_on').encode())


		#elif 'function_1_off' in data:
		#	tcpCliSock.send(('function_1_off').encode())

		elif 'function_2_off' in data:
			functionMode = 0
			fpv.FindColor(0)
			switch.switch(1,0)
			switch.switch(2,0)
			switch.switch(3,0)
			tcpCliSock.send(('function_2_off').encode())

		elif 'function_3_off' in data:
			functionMode = 0
			fpv.WatchDog(0)
			tcpCliSock.send(('function_3_off').encode())

		elif 'function_4_off' in data:
			functionMode = 0
			servo_move.pause()
			move.motorStop()
			tcpCliSock.send(('function_4_off').encode())

		elif 'function_5_off' in data:
			functionMode = 0
			servo_move.pause()
			move.motorStop()
			tcpCliSock.send(('function_5_off').encode())

		elif 'function_6_off' in data:
			functionMode = 0
			servo_move.pause()
			move.motorStop()
			init_get = 0
			tcpCliSock.send(('function_6_off').encode())


		elif 'lookleft' == data:
			servo_command = 'lookleft'
			servo_move.resume()

		elif 'lookright' == data:
			servo_command = 'lookright'
			servo_move.resume()

		elif 'up' == data:
			servo_command = 'up'
			servo_move.resume()

		elif 'down' == data:
			servo_command = 'down'
			servo_move.resume()

		elif 'stop' == data:
			if not functionMode:
				servo_move.pause()
			servo_command = 'no'
			pass

		elif 'home' == data:
			servo.ahead()

		elif 'CVrun' == data:
			if not FPV.CVrun:
				FPV.CVrun = 1
				tcpCliSock.send(('CVrun_on').encode())
			else:
				FPV.CVrun = 0
				tcpCliSock.send(('CVrun_off').encode())

		elif 'wsR' in data:
			try:
				set_R=data.split()
				R_set = int(set_R[1])
				led.colorWipe(R_set, G_set, B_set)
			except:
				pass

		elif 'wsG' in data:
			try:
				set_G=data.split()
				G_set = int(set_G[1])
				led.colorWipe(R_set, G_set, B_set)
			except:
				pass

		elif 'wsB' in data:
			try:
				set_B=data.split()
				B_set = int(set_B[1])
				led.colorWipe(R_set, G_set, B_set)
			except:
				pass

		elif 'pwm0' in data:
			try:
				set_pwm0=data.split()
				pwm0_set = int(set_pwm0[1])
				servo.setPWM(0, pwm0_set)
			except:
				pass

		elif 'pwm1' in data:
			try:
				set_pwm1=data.split()
				pwm1_set = int(set_pwm1[1])
				servo.setPWM(1, pwm1_set)
			except:
				pass

		elif 'pwm2' in data:
			try:
				set_pwm2=data.split()
				pwm2_set = int(set_pwm2[1])
				servo.setPWM(2, pwm2_set)
			except:
				pass

		elif 'Speed' in data:
			try:
				set_speed=data.split()
				speed_set = int(set_speed[1])
			except:
				pass

		elif 'Save' in data:
			try:
				servo.saveConfig()
			except:
				pass

		elif 'CVFL' in data:
			if not FPV.FindLineMode:
				FPV.FindLineMode = 1
				tcpCliSock.send(('CVFL_on').encode())
			else:
				move.motorStop()
				FPV.FindLineMode = 0
				tcpCliSock.send(('CVFL_off').encode())

		elif 'Render' in data:
			if FPV.frameRender:
				FPV.frameRender = 0
			else:
				FPV.frameRender = 1

		elif 'WBswitch' in data:
			if FPV.lineColorSet == 255:
				FPV.lineColorSet = 0
			else:
				FPV.lineColorSet = 255

		elif 'lip1' in data:
			try:
				set_lip1=data.split()
				lip1_set = int(set_lip1[1])
				FPV.linePos_1 = lip1_set
			except:
				pass

		elif 'lip2' in data:
			try:
				set_lip2=data.split()
				lip2_set = int(set_lip2[1])
				FPV.linePos_2 = lip2_set
			except:
				pass

		elif 'err' in data:
			try:
				set_err=data.split()
				err_set = int(set_err[1])
				FPV.findLineError = err_set
			except:
				pass

		elif 'FCSET' in data:
				FCSET = data.split()
				fpv.colorFindSet(int(FCSET[1]), int(FCSET[2]), int(FCSET[3]))

		elif 'setEC' in data:#Z
			ECset = data.split()
			try:
				fpv.setExpCom(int(ECset[1]))
			except:
				pass

		elif 'defEC' in data:#Z
			fpv.defaultExpCom()

		elif 'police' in data:
			if LED.ledfunc != 'police':
				tcpCliSock.send(('rainbow_off').encode())
				LED.ledfunc = 'police'
				ledthread.resume()
				tcpCliSock.send(('police_on').encode())
			elif LED.ledfunc == 'police':
				LED.ledfunc = ''
				ledthread.pause()
				tcpCliSock.send(('police_off').encode())

		elif 'rainbow' in data:
			if LED.ledfunc != 'rainbow':
				tcpCliSock.send(('police_off').encode())
				LED.ledfunc = 'rainbow'
				ledthread.resume()
				tcpCliSock.send(('rainbow_on').encode())
			elif LED.ledfunc == 'rainbow':
				LED.ledfunc = ''
				ledthread.pause()
				tcpCliSock.send(('rainbow_off').encode())

		elif 'sr' in data:
			if not SR_mode:
				if SR_dect:
					SR_mode = 1
					tcpCliSock.send(('sr_on').encode())
					sr.resume()

			elif SR_mode:
				SR_mode = 0
				sr.pause()
				move.motorStop()
				tcpCliSock.send(('sr_off').encode())

		else:
			pass

		print(data)


def wifi_check():
	try:
		s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(("1.1.1.1",80))
		ipaddr_check=s.getsockname()[0]
		s.close()
		print(ipaddr_check)
	except:
		ap_threading=threading.Thread(target=ap_thread)   #Define a thread for data receiving
		ap_threading.setDaemon(True)						  #'True' means it is a front thread,it would close when the mainloop() closes
		ap_threading.start()								  #Thread starts

		led.colorWipe(0,16,50)
		time.sleep(1)
		led.colorWipe(0,16,100)
		time.sleep(1)
		led.colorWipe(0,16,150)
		time.sleep(1)
		led.colorWipe(0,16,200)
		time.sleep(1)
		led.colorWipe(0,16,255)
		time.sleep(1)
		led.colorWipe(35,255,35)



if __name__ == '__main__':
	servo.servo_init()
	switch.switchSetup()
	switch.set_all_switch_off()

	HOST = ''
	PORT = 10223							  #Define port serial 
	BUFSIZ = 1024							 #Define buffer size
	ADDR = (HOST, PORT)

	# try:
	led  = LED.LED()
	led.colorWipe(255,16,0)
	ledthread = LED.LED_ctrl()
	ledthread.start()
	# except:
	#	 print('Use "sudo pip3 install rpi_ws281x" to install WS_281x package')
	#	 pass

	if SR_dect:
		sr = SR_ctrl()
		sr.start()

	while  1:
		wifi_check()
		try:
			tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
			tcpSerSock.bind(ADDR)
			tcpSerSock.listen(5)					  #Start server,waiting for client
			print('waiting for connection...')
			tcpCliSock, addr = tcpSerSock.accept()
			print('...connected from :', addr)

			# fpv=FPV.FPV()
			# fps_threading=threading.Thread(target=FPV_thread)		 #Define a thread for FPV and OpenCV
			# fps_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
			# fps_threading.start()									 #Thread starts
			break
		except:
			led.colorWipe(0,0,0)

		try:
			led.colorWipe(0,80,255)
		except:
			pass
			fpv=FPV.FPV()
	fps_threading=threading.Thread(target=FPV_thread)		 #Define a thread for FPV and OpenCV
	fps_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
	fps_threading.start()									 #Thread starts
	run()
	try:
		run()
	except:
		servo_move.stop()
		led.colorWipe(0,0,0)
		servo.clean_all()
		move.destroy()
