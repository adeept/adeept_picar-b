#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# File name   : client.py
# Description : client  
# Website	 : www.adeept.com
# Author	  : William
# Date		: 2019/11/21

from socket import *
import sys
import time
import threading as thread
import tkinter as tk
import math
import os

try:
	import cv2
	import zmq
	import base64
	import numpy as np
except:
	print("Couldn't import OpenCV, you need to install it first.")


def global_init():
	global DS_stu, TS_stu, color_bg, color_text, color_btn, color_line, color_can, color_oval, target_color
	global speed, ip_stu, Switch_3, Switch_2, Switch_1, servo_stu, function_stu
	DS_stu = 0
	TS_stu = 0

	color_bg='#000000'		#Set background color
	color_text='#E1F5FE'	  #Set text color
	color_btn='#0277BD'	   #Set button color
	color_line='#01579B'	  #Set line color
	color_can='#212121'	   #Set canvas color
	color_oval='#2196F3'	  #Set oval color
	target_color='#FF6D00'
	speed = 1
	ip_stu=1

	Switch_3 = 0
	Switch_2 = 0
	Switch_1 = 0

	servo_stu = 0
	function_stu = 0


global_init()

########>>>>>VIDEO<<<<<########
def RGB_to_Hex(r, g, b):
	return ('#'+str(hex(r))[-2:]+str(hex(g))[-2:]+str(hex(b))[-2:]).replace('x','0').upper()


def rgb2hsv(r, g, b):
	r, g, b  = r/255.0, g/255.0, b/255.0
	mx = max(r, g, b)
	mn = min(r, g, b)
	df = mx-mn
	if mx == mn:
		h = 0
	elif mx == r:
		h = (60*((g-b)/df) + 360) % 360
	elif mx == g:
		h = (60*((b-r)/df) + 120) % 360
	elif mx == b:
		h = (60*((r-g)/df) + 240) % 360
	if mx == 0:
		s = 0
	else:
		s = (df/mx)*100
	v = mx*100
	h=h/360*255
	return str(int(h))+' '+str(int(s))+' '+str(int(v))

def video_thread():
	global footage_socket, font, frame_num, fps
	context = zmq.Context()
	footage_socket = context.socket(zmq.SUB)
	footage_socket.bind('tcp://*:5555')
	footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

	font = cv2.FONT_HERSHEY_SIMPLEX

	frame_num = 0
	fps = 0

def getposBgr(event, x, y, flags, param):
	if event==cv2.EVENT_LBUTTONDOWN:
		getBGR = source[y, x]
		var_R.set(getBGR[2])
		var_G.set(getBGR[1])
		var_B.set(getBGR[0])
		# tcpClicSock.send(('FCSET %s'%rgb2hsv(int(var_R.get()), int(var_G.get()), int(var_B.get()))).encode())
		canvas_show.config(bg = RGB_to_Hex(int(var_R.get()), int(var_G.get()), int(var_B.get())))
		print("Bgr is", getBGR)
		print("HSV is", HSVimg[y, x])
		tcpClicSock.send(('FCSET %s %s %s'%(HSVimg[y, x][0], HSVimg[y, x][1], HSVimg[y, x][2])).encode())
		# print("HSV genOut is", rgb2hsv(int(var_R.get()), int(var_G.get()), int(var_B.get())))


def getposHsv(event, x, y, flags, param):
	if event==cv2.EVENT_LBUTTONDOWN:
		print("HSV is", HSVimg[y, x])
		tcpClicSock.send(('FCSET %s %s %s'%(HSVimg[y, x][0], HSVimg[y, x][1], HSVimg[y, x][2])).encode())
		getBGR = source[y, x]
		var_R.set(getBGR[2])
		var_G.set(getBGR[1])
		var_B.set(getBGR[0])
		canvas_show.config(bg = RGB_to_Hex(int(var_R.get()), int(var_G.get()), int(var_B.get())))

def get_FPS():
	global frame_num, fps
	while 1:
		try:
			time.sleep(1)
			fps = frame_num
			frame_num = 0
		except:
			time.sleep(1)

def opencv_r():
	global frame_num, source, HSVimg
	while True:
		try:
			frame = footage_socket.recv_string()
			img = base64.b64decode(frame)
			npimg = np.frombuffer(img, dtype=np.uint8)
			source = cv2.imdecode(npimg, 1)
			cv2.putText(source,('PC FPS: %s'%fps),(40,20), font, 0.5,(255,255,255),1,cv2.LINE_AA)

			
			try:
				cv2.putText(source,('CPU Temperature: %s'%CPU_TEP),(370,350), font, 0.5,(128,255,128),1,cv2.LINE_AA)
				cv2.putText(source,('CPU Usage: %s'%CPU_USE),(370,380), font, 0.5,(128,255,128),1,cv2.LINE_AA)
				cv2.putText(source,('RAM Usage: %s'%RAM_USE),(370,410), font, 0.5,(128,255,128),1,cv2.LINE_AA)

				cv2.rectangle(source, (167, 320), (473, 330), (255,255,255))

				DIR_show = int(CAR_DIR)
				if DIR_show > 0:
					cv2.rectangle(source, ((320-DIR_show), 323), (320, 327), (255,255,255))
				elif DIR_show < 0:
					cv2.rectangle(source, (320, 323), ((320-DIR_show), 327), (255,255,255))


				#cv2.line(source,(320,240),(260,300),(255,255,255),1)
				#cv2.line(source,(210,300),(260,300),(255,255,255),1)

				#cv2.putText(source,('%sm'%ultra_data),(210,290), font, 0.5,(255,255,255),1,cv2.LINE_AA)
			except:
				pass
			
			#cv2.putText(source,('%sm'%ultra_data),(210,290), font, 0.5,(255,255,255),1,cv2.LINE_AA)
			cv2.imshow("Stream", source)
			cv2.setMouseCallback("Stream", getposBgr)

			HSVimg = cv2.cvtColor(source, cv2.COLOR_BGR2HSV)
			cv2.imshow("StreamHSV", HSVimg)
			cv2.setMouseCallback("StreamHSV", getposHsv)
			
			frame_num += 1
			cv2.waitKey(1)

		except:
			time.sleep(0.5)
			break

fps_threading=thread.Thread(target=get_FPS)		 #Define a thread for FPV and OpenCV
fps_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
fps_threading.start()									 #Thread starts

video_threading=thread.Thread(target=video_thread)		 #Define a thread for FPV and OpenCV
video_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
video_threading.start()									 #Thread starts

########>>>>>VIDEO<<<<<########


def replace_num(initial,new_num):   #Call this function to replace data in '.txt' file
	newline=""
	str_num=str(new_num)
	with open("ip.txt","r") as f:
		for line in f.readlines():
			if(line.find(initial) == 0):
				line = initial+"%s" %(str_num)
			newline += line
	with open("ip.txt","w") as f:
		f.writelines(newline)	#Call this function to replace data in '.txt' file


def num_import(initial):			#Call this function to import data from '.txt' file
	with open("ip.txt") as f:
		for line in f.readlines():
			if(line.find(initial) == 0):
				r=line
	begin=len(list(initial))
	snum=r[begin:]
	n=snum
	return n	


def connection_thread():
	global Switch_3, Switch_2, Switch_1, function_stu
	while 1:
		car_info = (tcpClicSock.recv(BUFSIZ)).decode()
		if not car_info:
			continue
		elif 'Switch_3_on' in car_info:
			Switch_3 = 1
			Btn_Switch_3.config(bg='#4CAF50')

		elif 'Switch_2_on' in car_info:
			Switch_2 = 1
			Btn_Switch_2.config(bg='#4CAF50')

		elif 'Switch_1_on' in car_info:
			Switch_1 = 1
			Btn_Switch_1.config(bg='#4CAF50')

		elif 'Switch_3_off' in car_info:
			Switch_3 = 0
			Btn_Switch_3.config(bg=color_btn)

		elif 'Switch_2_off' in car_info:
			Switch_2 = 0
			Btn_Switch_2.config(bg=color_btn)

		elif 'Switch_1_off' in car_info:
			Switch_1 = 0
			Btn_Switch_1.config(bg=color_btn)

		elif 'U:' in car_info:
			print('ultrasonic radar')
			new_number2view(30,290,car_info)


		elif 'function_1_on' in car_info:
			function_stu = 1
			Btn_function_1.config(bg='#4CAF50')

		elif 'function_2_on' in car_info:
			function_stu = 1
			Btn_function_2.config(bg='#4CAF50')

		elif 'function_3_on' in car_info:
			function_stu = 1
			Btn_function_3.config(bg='#4CAF50')

		elif 'function_4_on' in car_info:
			function_stu = 1
			Btn_function_4.config(bg='#4CAF50')

		elif 'function_5_on' in car_info:
			function_stu = 1
			Btn_function_5.config(bg='#4CAF50')

		elif 'function_6_on' in car_info:
			function_stu = 1
			Btn_function_6.config(bg='#4CAF50')

		elif 'CVFL_on' in car_info:
			function_stu = 1
			Btn_CVFL.config(bg='#4CAF50')

		elif 'CVFL_off' in car_info:
			function_stu = 0
			Btn_CVFL.config(bg='#212121')

		elif 'function_1_off' in car_info:
			function_stu = 0
			Btn_function_1.config(bg=color_btn)

		elif 'function_2_off' in car_info:
			function_stu = 0
			Btn_function_2.config(bg=color_btn)

		elif 'function_3_off' in car_info:
			function_stu = 0
			Btn_function_3.config(bg=color_btn)

		elif 'function_4_off' in car_info:
			function_stu = 0
			Btn_function_4.config(bg=color_btn)

		elif 'function_5_off' in car_info:
			function_stu = 0
			Btn_function_5.config(bg=color_btn)

		elif 'function_6_off' in car_info:
			function_stu = 0
			Btn_function_6.config(bg=color_btn)

		elif 'CVrun_on' in car_info:
			Btn_SR.config(bg='#4CAF50')

		elif 'CVrun_off' in car_info:
			Btn_SR.config(bg=color_btn)

		elif 'police_on' in car_info:
			Btn_Police.config(bg='#4CAF50')

		elif 'police_off' in car_info:
			Btn_Police.config(bg=color_btn)

		elif 'rainbow_on' in car_info:
			Btn_Rainbow.config(bg='#4CAF50')

		elif 'rainbow_off' in car_info:
			Btn_Rainbow.config(bg=color_btn)

		elif 'sr_on' in car_info:
			Btn_3.config(bg='#4CAF50')

		elif 'sr_off' in car_info:
			Btn_3.config(bg=color_btn)


def Info_receive():
	global CPU_TEP,CPU_USE,RAM_USE,CAR_DIR
	HOST = ''
	INFO_PORT = 2256							#Define port serial 
	ADDR = (HOST, INFO_PORT)
	InfoSock = socket(AF_INET, SOCK_STREAM)
	InfoSock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	InfoSock.bind(ADDR)
	InfoSock.listen(5)					  #Start server,waiting for client
	InfoSock, addr = InfoSock.accept()
	print('Info connected')
	while 1:
		try:
			info_data = ''
			info_data = str(InfoSock.recv(BUFSIZ).decode())
			info_get = info_data.split()
			CPU_TEP,CPU_USE,RAM_USE,CAR_DIR= info_get
			CPU_TEP_lab.config(text='CPU Temp: %s℃'%CPU_TEP)
			CPU_USE_lab.config(text='CPU Usage: %s'%CPU_USE)
			RAM_lab.config(text='RAM Usage: %s'%RAM_USE)
		except:
			pass


def socket_connect():	 #Call this function to connect with the server
	global ADDR,tcpClicSock,BUFSIZ,ip_stu,ipaddr
	ip_adr=E1.get()	   #Get the IP address from Entry

	if ip_adr == '':	  #If no input IP address in Entry,import a default IP
		ip_adr=num_import('IP:')
		l_ip_4.config(text='Connecting')
		l_ip_4.config(bg='#FF8F00')
		l_ip_5.config(text='Default:%s'%ip_adr)
		pass
	
	SERVER_IP = ip_adr
	SERVER_PORT = 10223   #Define port serial 
	BUFSIZ = 1024		 #Define buffer size
	ADDR = (SERVER_IP, SERVER_PORT)
	tcpClicSock = socket(AF_INET, SOCK_STREAM) #Set connection value for socket

	for i in range (1,6): #Try 5 times if disconnected
		#try:
		if ip_stu == 1:
			print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
			print("Connecting")
			tcpClicSock.connect(ADDR)		#Connection with the server
		
			print("Connected")
		
			l_ip_5.config(text='IP:%s'%ip_adr)
			l_ip_4.config(text='Connected')
			l_ip_4.config(bg='#558B2F')

			replace_num('IP:',ip_adr)
			E1.config(state='disabled')	  #Disable the Entry
			Btn14.config(state='disabled')   #Disable the Entry
			
			ip_stu=0						 #'0' means connected

			connection_threading=thread.Thread(target=connection_thread)		 #Define a thread for FPV and OpenCV
			connection_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
			connection_threading.start()									 #Thread starts

			info_threading=thread.Thread(target=Info_receive)		 #Define a thread for FPV and OpenCV
			info_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
			info_threading.start()									 #Thread starts

			video_threading=thread.Thread(target=opencv_r)		 #Define a thread for FPV and OpenCV
			video_threading.setDaemon(True)							 #'True' means it is a front thread,it would close when the mainloop() closes
			video_threading.start()									 #Thread starts

			break
		else:
			print("Cannot connecting to server,try it latter!")
			l_ip_4.config(text='Try %d/5 time(s)'%i)
			l_ip_4.config(bg='#EF6C00')
			print('Try %d/5 time(s)'%i)
			ip_stu=1
			time.sleep(1)
			continue

	if ip_stu == 1:
		l_ip_4.config(text='Disconnected')
		l_ip_4.config(bg='#F44336')


def connect(event):	   #Call this function to connect with the server
	if ip_stu == 1:
		sc=thread.Thread(target=socket_connect) #Define a thread for connection
		sc.setDaemon(True)					  #'True' means it is a front thread,it would close when the mainloop() closes
		sc.start()							  #Thread starts


def servo_buttons(x,y):
	global Btn_SR, Btn_Police, Btn_Rainbow, Btn_3
	def call_up(event):
		global servo_stu
		if servo_stu == 0:
			tcpClicSock.send(('up').encode())
			servo_stu = 1

	def call_down(event):
		global servo_stu
		if servo_stu == 0:
			tcpClicSock.send(('down').encode())
			servo_stu = 1

	def call_lookleft(event):
		global servo_stu
		if servo_stu == 0:
			tcpClicSock.send(('lookleft').encode())
			servo_stu = 1

	def call_lookright(event):
		global servo_stu
		if servo_stu == 0:
			tcpClicSock.send(('lookright').encode())
			servo_stu = 1

	def call_police(event):
		tcpClicSock.send(('police').encode())

	def call_rainbow(event):
		tcpClicSock.send(('rainbow').encode())

	def call_sr(event):
		tcpClicSock.send(('sr').encode())

	def call_CVrun(event):
		tcpClicSock.send(('CVrun').encode())

	def call_stop(event):
		global servo_stu
		tcpClicSock.send(('stop').encode())
		servo_stu = 0

	def call_home(event):
		tcpClicSock.send(('home').encode())
		time.sleep(0.15)

	Btn_0 = tk.Button(root, width=8, text='Left',fg=color_text,bg=color_btn,relief='ridge')
	Btn_0.place(x=x,y=y+35)
	Btn_0.bind('<ButtonPress-1>', call_lookleft)
	Btn_0.bind('<ButtonRelease-1>', call_stop)
	root.bind('<KeyPress-j>', call_lookleft)
	root.bind('<KeyRelease-j>', call_stop)

	Btn_1 = tk.Button(root, width=8, text='Up',fg=color_text,bg=color_btn,relief='ridge')
	Btn_1.place(x=x+70,y=y)
	Btn_1.bind('<ButtonPress-1>', call_up)
	Btn_1.bind('<ButtonRelease-1>', call_stop)
	root.bind('<KeyPress-i>', call_up)
	root.bind('<KeyRelease-i>', call_stop) 

	Btn_1 = tk.Button(root, width=8, text='Down',fg=color_text,bg=color_btn,relief='ridge')
	Btn_1.place(x=x+70,y=y+35)
	Btn_1.bind('<ButtonPress-1>', call_down)
	Btn_1.bind('<ButtonRelease-1>', call_stop)
	root.bind('<KeyPress-k>', call_down)
	root.bind('<KeyRelease-k>', call_stop)

	Btn_2 = tk.Button(root, width=8, text='Right',fg=color_text,bg=color_btn,relief='ridge')
	Btn_2.place(x=x+140,y=y+35)
	Btn_2.bind('<ButtonPress-1>', call_lookright)
	Btn_2.bind('<ButtonRelease-1>', call_stop)
	root.bind('<KeyPress-l>', call_lookright) 
	root.bind('<KeyRelease-l>', call_stop)

	Btn_3 = tk.Button(root, width=8, text='SpeechR',fg=color_text,bg=color_btn,relief='ridge')
	Btn_3.place(x=x+140,y=y)
	Btn_3.bind('<ButtonPress-1>', call_sr)
	root.bind('<KeyPress-o>', call_sr) 

	Btn_SR = tk.Button(root, width=8, text='CV Run',fg=color_text,bg=color_btn,relief='ridge')
	Btn_SR.place(x=x,y=y)
	Btn_SR.bind('<ButtonPress-1>', call_CVrun)
	root.bind('<KeyPress-u>', call_CVrun) 

	Btn_Police = tk.Button(root, width=8, text='Police',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Police.place(x=x,y=y-55)
	Btn_Police.bind('<ButtonPress-1>', call_police)
	root.bind('<KeyPress-g>', call_police) 

	Btn_Rainbow = tk.Button(root, width=8, text='Rainbow',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Rainbow.place(x=x,y=y-55-35)
	Btn_Rainbow.bind('<ButtonPress-1>', call_rainbow)
	root.bind('<KeyPress-y>', call_rainbow)

	root.bind('<KeyPress-h>', call_home)


def motor_buttons(x,y):
	def call_left(event):
		global TS_stu
		if TS_stu == 0:
			tcpClicSock.send(('left').encode())
			TS_stu = 1

	def call_right(event):
		global TS_stu
		if TS_stu == 0:
			tcpClicSock.send(('right').encode())
			TS_stu = 1

	def call_forward(event):
		global DS_stu
		if DS_stu == 0:
			tcpClicSock.send(('forward').encode())
			DS_stu = 1

	def call_backward(event):
		global DS_stu
		if DS_stu == 0:
			tcpClicSock.send(('backward').encode())
			DS_stu = 1

	def call_DS(event):
		global DS_stu
		tcpClicSock.send(('DS').encode())
		DS_stu = 0

	def call_TS(event):
		global TS_stu
		tcpClicSock.send(('TS').encode())
		TS_stu = 0

	Btn_0 = tk.Button(root, width=8, text='Left',fg=color_text,bg=color_btn,relief='ridge')
	Btn_0.place(x=x,y=y+35)
	Btn_0.bind('<ButtonPress-1>', call_left)
	Btn_0.bind('<ButtonRelease-1>', call_TS)
	root.bind('<KeyPress-a>', call_left)
	root.bind('<KeyRelease-a>', call_TS)

	Btn_1 = tk.Button(root, width=8, text='Forward',fg=color_text,bg=color_btn,relief='ridge')
	Btn_1.place(x=x+70,y=y)
	Btn_1.bind('<ButtonPress-1>', call_forward)
	Btn_1.bind('<ButtonRelease-1>', call_DS)
	root.bind('<KeyPress-w>', call_forward)
	root.bind('<KeyRelease-w>', call_DS) 

	Btn_1 = tk.Button(root, width=8, text='Backward',fg=color_text,bg=color_btn,relief='ridge')
	Btn_1.place(x=x+70,y=y+35)
	Btn_1.bind('<ButtonPress-1>', call_backward)
	Btn_1.bind('<ButtonRelease-1>', call_DS)
	root.bind('<KeyPress-s>', call_backward)
	root.bind('<KeyRelease-s>', call_DS)

	Btn_2 = tk.Button(root, width=8, text='Right',fg=color_text,bg=color_btn,relief='ridge')
	Btn_2.place(x=x+140,y=y+35)
	Btn_2.bind('<ButtonPress-1>', call_right)
	Btn_2.bind('<ButtonRelease-1>', call_TS)
	root.bind('<KeyPress-d>', call_right) 
	root.bind('<KeyRelease-d>', call_TS) 


def information_screen(x,y):
	global CPU_TEP_lab, CPU_USE_lab, RAM_lab, l_ip_4, l_ip_5
	CPU_TEP_lab=tk.Label(root,width=18,text='CPU Temp:',fg=color_text,bg='#212121')
	CPU_TEP_lab.place(x=x,y=y)						 #Define a Label and put it in position

	CPU_USE_lab=tk.Label(root,width=18,text='CPU Usage:',fg=color_text,bg='#212121')
	CPU_USE_lab.place(x=x,y=y+30)						 #Define a Label and put it in position

	RAM_lab=tk.Label(root,width=18,text='RAM Usage:',fg=color_text,bg='#212121')
	RAM_lab.place(x=x,y=y+60)						 #Define a Label and put it in position

	l_ip_4=tk.Label(root,width=18,text='Disconnected',fg=color_text,bg='#F44336')
	l_ip_4.place(x=x,y=y+95)						 #Define a Label and put it in position

	l_ip_5=tk.Label(root,width=18,text='Use default IP',fg=color_text,bg=color_btn)
	l_ip_5.place(x=x,y=y+130)						 #Define a Label and put it in position


def connent_input(x,y):
	global E1, Btn14
	E1 = tk.Entry(root,show=None,width=16,bg="#37474F",fg='#eceff1')
	E1.place(x=x+5,y=y+25)							 #Define a Entry and put it in position

	l_ip_3=tk.Label(root,width=10,text='IP Address:',fg=color_text,bg='#000000')
	l_ip_3.place(x=x,y=y)						 #Define a Label and put it in position

	Btn14= tk.Button(root, width=8,height=2, text='Connect',fg=color_text,bg=color_btn,relief='ridge')
	Btn14.place(x=x+130,y=y)						  #Define a Button and put it in position

	root.bind('<Return>', connect)
	Btn14.bind('<ButtonPress-1>', connect)


def switch_button(x,y):
	global Btn_Switch_1, Btn_Switch_2, Btn_Switch_3
	def call_Switch_1(event):
		if Switch_1 == 0:
			tcpClicSock.send(('Switch_1_on').encode())
		else:
			tcpClicSock.send(('Switch_1_off').encode())


	def call_Switch_2(event):
		if Switch_2 == 0:
			tcpClicSock.send(('Switch_2_on').encode())
		else:
			tcpClicSock.send(('Switch_2_off').encode())


	def call_Switch_3(event):
		if Switch_3 == 0:
			tcpClicSock.send(('Switch_3_on').encode())
		else:
			tcpClicSock.send(('Switch_3_off').encode())

	Btn_Switch_1 = tk.Button(root, width=8, text='Port 1',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Switch_2 = tk.Button(root, width=8, text='Port 2',fg=color_text,bg=color_btn,relief='ridge')
	Btn_Switch_3 = tk.Button(root, width=8, text='Port 3',fg=color_text,bg=color_btn,relief='ridge')

	Btn_Switch_1.place(x=x,y=y)
	Btn_Switch_2.place(x=x+70,y=y)
	Btn_Switch_3.place(x=x+140,y=y)

	Btn_Switch_1.bind('<ButtonPress-1>', call_Switch_1)
	Btn_Switch_2.bind('<ButtonPress-1>', call_Switch_2)
	Btn_Switch_3.bind('<ButtonPress-1>', call_Switch_3)


def scale(x,y,w):
	def speed_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('Speed %s'%var_Speed.get()).encode())

	Scale_Speed = tk.Scale(root,label=None,
	from_=60,to=100,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=10,variable=var_Speed,troughcolor='#448AFF',command=speed_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_Speed.place(x=x,y=y)							#Define a Scale and put it in position

	canvas_cover=tk.Canvas(root,bg=color_bg,height=30,width=510,highlightthickness=0)
	canvas_cover.place(x=x,y=y+30)


def scale_RGB(x,y,w):
	def R_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('wsR %s'%var_R_L.get()).encode())

	def G_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('wsG %s'%var_G_L.get()).encode())

	def B_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('wsB %s'%var_B_L.get()).encode())

	Scale_R = tk.Scale(root,label=None,
	from_=0,to=255,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_R_L,troughcolor='#F44336',command=R_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_R.place(x=x,y=y)							#Define a Scale and put it in position

	Scale_G = tk.Scale(root,label=None,
	from_=0,to=255,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_G_L,troughcolor='#4CAF50',command=G_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_G.place(x=x,y=y+30)							#Define a Scale and put it in position

	Scale_B = tk.Scale(root,label=None,
	from_=0,to=255,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_B_L,troughcolor='#448AFF',command=B_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_B.place(x=x,y=y+60)							#Define a Scale and put it in position

	canvas_cover=tk.Canvas(root,bg=color_bg,height=30,width=510,highlightthickness=0)
	canvas_cover.place(x=x,y=y+90)


def scale_PWM(x,y,w):
	def pwm0_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('pwm0 %s'%var_0.get()).encode())

	def pwm1_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('pwm1 %s'%var_1.get()).encode())

	def pwm2_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('pwm2 %s'%var_2.get()).encode())

	def call_Save(event):
		tcpClicSock.send(('Save').encode())


	Scale_0 = tk.Scale(root,label=None,
	from_=200,to=400,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_0,troughcolor='#212121',command=pwm0_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_0.place(x=x,y=y)							#Define a Scale and put it in position

	Scale_1 = tk.Scale(root,label=None,
	from_=200,to=400,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_1,troughcolor='#212121',command=pwm1_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_1.place(x=x,y=y+30)							#Define a Scale and put it in position

	Scale_2 = tk.Scale(root,label=None,
	from_=200,to=400,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_2,troughcolor='#212121',command=pwm2_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_2.place(x=x,y=y+60)							#Define a Scale and put it in position

	canvas_cover=tk.Canvas(root,bg=color_bg,height=30,width=510,highlightthickness=0)
	canvas_cover.place(x=x,y=y+90)

	Btn_Save = tk.Button(root, width=23, text='Save as Default',fg=color_text,bg='#212121',relief='ridge')
	Btn_Save.place(x=x+1,y=y+110)
	Btn_Save.bind('<ButtonPress-1>', call_Save)


def scale_FL(x,y,w):
	global Btn_CVFL
	def lip1_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('lip1 %s'%var_lip1.get()).encode())

	def lip2_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('lip2 %s'%var_lip2.get()).encode())

	def err_send(event):
		time.sleep(0.03)
		tcpClicSock.send(('err %s'%var_err.get()).encode())

	def call_Render(event):
		tcpClicSock.send(('Render').encode())

	def call_CVFL(event):
		tcpClicSock.send(('CVFL').encode())

	def call_WB(event):
		tcpClicSock.send(('WBswitch').encode())

	Scale_lip1 = tk.Scale(root,label=None,
	from_=0,to=480,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_lip1,troughcolor='#212121',command=lip1_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_lip1.place(x=x,y=y)							#Define a Scale and put it in position

	Scale_lip2 = tk.Scale(root,label=None,
	from_=0,to=480,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_lip2,troughcolor='#212121',command=lip2_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_lip2.place(x=x,y=y+30)							#Define a Scale and put it in position

	Scale_err = tk.Scale(root,label=None,
	from_=0,to=200,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_err,troughcolor='#212121',command=err_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_err.place(x=x,y=y+60)							#Define a Scale and put it in position

	canvas_cover=tk.Canvas(root,bg=color_bg,height=30,width=510,highlightthickness=0)
	canvas_cover.place(x=x,y=y+90)

	Btn_Render = tk.Button(root, width=10, text='Render',fg=color_text,bg='#212121',relief='ridge')
	Btn_Render.place(x=x+w+111,y=y+20)
	Btn_Render.bind('<ButtonPress-1>', call_Render)

	Btn_CVFL = tk.Button(root, width=10, text='CV FL',fg=color_text,bg='#212121',relief='ridge')
	Btn_CVFL.place(x=x+w+21,y=y+20)
	Btn_CVFL.bind('<ButtonPress-1>', call_CVFL)

	Btn_WB = tk.Button(root, width=23, text='LineColorSwitch',fg=color_text,bg='#212121',relief='ridge')
	Btn_WB.place(x=x+w+21,y=y+60)
	Btn_WB.bind('<ButtonPress-1>', call_WB)


def ultrasonic_radar(x,y):
	x_range = 2
	can_scan = tk.Canvas(root,bg=color_can,height=250,width=320,highlightthickness=0) #define a canvas
	can_scan.place(x=x,y=y) #Place the canvas
	line = can_scan.create_line(0,62,320,62,fill='darkgray')   #Draw a line on canvas
	line = can_scan.create_line(0,124,320,124,fill='darkgray') #Draw a line on canvas
	line = can_scan.create_line(0,186,320,186,fill='darkgray') #Draw a line on canvas
	line = can_scan.create_line(160,0,160,250,fill='darkgray') #Draw a line on canvas
	line = can_scan.create_line(80,0,80,250,fill='darkgray')   #Draw a line on canvas
	line = can_scan.create_line(240,0,240,250,fill='darkgray') #Draw a line on canvas

	can_tex_11=can_scan.create_text((27,178),text='%sm'%round((x_range/4),2),fill='#aeea00')	 #Create a text on canvas
	can_tex_12=can_scan.create_text((27,116),text='%sm'%round((x_range/2),2),fill='#aeea00')	 #Create a text on canvas
	can_tex_13=can_scan.create_text((27,54),text='%sm'%round((x_range*0.75),2),fill='#aeea00')  #Create a text on canvas


def new_number2view(x,y,info):
	print(info)
	x_range = 2
	dis_list=[]
	f_list=[]

	info = info.split()
	info = info[1:]

	total_number = len(info)
	print(total_number)

	can_scan_1 = tk.Canvas(root,bg=color_can,height=250,width=320,highlightthickness=0) #define a canvas
	can_scan_1.place(x=x,y=y) #Place the canvas
	line = can_scan_1.create_line(0,62,320,62,fill='darkgray')   #Draw a line on canvas
	line = can_scan_1.create_line(0,124,320,124,fill='darkgray') #Draw a line on canvas
	line = can_scan_1.create_line(0,186,320,186,fill='darkgray') #Draw a line on canvas
	line = can_scan_1.create_line(160,0,160,250,fill='darkgray') #Draw a line on canvas
	line = can_scan_1.create_line(80,0,80,250,fill='darkgray')   #Draw a line on canvas
	line = can_scan_1.create_line(240,0,240,250,fill='darkgray') #Draw a line on canvas

	for i in range (0,total_number):   #Scale the result to the size as canvas
		dis_info_get = info[i]
		dis_info_get = float(dis_info_get)
		if dis_info_get > 0:
			len_dis_1 = int((dis_info_get/x_range)*250)						  #600 is the height of canvas
			pos	 = int((i/total_number)*320)								#740 is the width of canvas
			pos_ra  = int(((i/total_number)*140)+20)						   #Scale the direction range to (20-160)
			len_dis = int(len_dis_1*(math.sin(math.radians(pos_ra))))		   #len_dis is the height of the line

			x0_l,y0_l,x1_l,y1_l=pos,(250-len_dis),pos,(250-len_dis)			 #The position of line
			x0,y0,x1,y1=(pos+3),(250-len_dis+3),(pos-3),(250-len_dis-3)		 #The position of arc

			if pos <= 160:													  #Scale the whole picture to a shape of sector
				pos = 160-abs(int(len_dis_1*(math.cos(math.radians(pos_ra)))))
				x1_l= (x1_l-math.cos(math.radians(pos_ra))*130)
			else:
				pos = abs(int(len_dis_1*(math.cos(math.radians(pos_ra)))))+160
				x1_l= x1_l+abs(math.cos(math.radians(pos_ra))*130)

			y1_l = y1_l-abs(math.sin(math.radians(pos_ra))*130)			  #Orientation of line

			line = can_scan_1.create_line(pos,y0_l,x1_l,y1_l,fill=color_line)   #Draw a line on canvas
			point_scan = can_scan_1.create_oval((pos+3),y0,(pos-3),y1,fill=color_oval,outline=color_oval) #Draw a arc on canvas

			can_tex_11=can_scan_1.create_text((27,178),text='%sm'%round((x_range/4),2),fill='#aeea00')	 #Create a text on canvas
			can_tex_12=can_scan_1.create_text((27,116),text='%sm'%round((x_range/2),2),fill='#aeea00')	 #Create a text on canvas
			can_tex_13=can_scan_1.create_text((27,54),text='%sm'%round((x_range*0.75),2),fill='#aeea00')  #Create a text on canvas

def scale_FC(x,y,w):
	global canvas_show
	def R_send(event):
		canvas_show.config(bg = RGB_to_Hex(int(var_R.get()), int(var_G.get()), int(var_B.get())))
		time.sleep(0.03)
		# tcpClicSock.send(('hsvH %s'%var_R.get()).encode())

	def G_send(event):
		canvas_show.config(bg = RGB_to_Hex(int(var_R.get()), int(var_G.get()), int(var_B.get())))
		time.sleep(0.03)
		# tcpClicSock.send(('hsvS %s'%var_G.get()).encode())

	def B_send(event):
		canvas_show.config(bg = RGB_to_Hex(int(var_R.get()), int(var_G.get()), int(var_B.get())))
		time.sleep(0.03)
		# tcpClicSock.send(('hsvV %s'%var_B.get()).encode())

	def call_SET(event):
		tcpClicSock.send(('FCSET %s'%rgb2hsv(int(var_R.get()), int(var_G.get()), int(var_B.get()))).encode())

	Scale_R = tk.Scale(root,label=None,
	from_=0,to=255,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_R,troughcolor='#FF1744',command=R_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_R.place(x=x,y=y)							#Define a Scale and put it in position

	Scale_G = tk.Scale(root,label=None,
	from_=0,to=255,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_G,troughcolor='#00E676',command=G_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_G.place(x=x,y=y+30)							#Define a Scale and put it in position

	Scale_B = tk.Scale(root,label=None,
	from_=0,to=255,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_B,troughcolor='#2979FF',command=B_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_B.place(x=x,y=y+60)							#Define a Scale and put it in position

	canvas_cover=tk.Canvas(root,bg=color_bg,height=30,width=510,highlightthickness=0)
	canvas_cover.place(x=x,y=y+90)

	canvas_show=tk.Canvas(root,bg=RGB_to_Hex(int(var_R.get()), int(var_G.get()), int(var_B.get())),height=35,width=170,highlightthickness=0)
	canvas_show.place(x=w+x+21,y=y+15)

	Btn_WB = tk.Button(root, width=23, text='Color Set',fg=color_text,bg='#212121',relief='ridge')
	Btn_WB.place(x=x+w+21,y=y+60)
	Btn_WB.bind('<ButtonPress-1>', call_SET)


def scale_ExpCom(x,y,w):#Z
	def EC_send(event):
		tcpClicSock.send(('setEC %s'%var_ec.get()).encode())
		time.sleep(0.03)

	def EC_default(event):
		var_ec.set(0)
		tcpClicSock.send(('defEC').encode())


	Scale_ExpCom = tk.Scale(root,label='Exposure Compensation Level',
	from_=-25,to=25,orient=tk.HORIZONTAL,length=w,
	showvalue=1,tickinterval=None,resolution=1,variable=var_ec,troughcolor='#212121',command=EC_send,fg=color_text,bg=color_bg,highlightthickness=0)
	Scale_ExpCom.place(x=x,y=y)							#Define a Scale and put it in position

	canvas_cover=tk.Canvas(root,bg=color_bg,height=30,width=510,highlightthickness=0)
	canvas_cover.place(x=x,y=y+50)

	Btn_dEC = tk.Button(root, width=23,height=2, text='Set Default Exposure\nCompensation Level',fg=color_text,bg='#212121',relief='ridge')
	Btn_dEC.place(x=x+w+21,y=y+3)
	Btn_dEC.bind('<ButtonPress-1>', EC_default)


def function_buttons(x,y):
	global function_stu, Btn_function_1, Btn_function_2, Btn_function_3, Btn_function_4, Btn_function_5, Btn_function_6, Btn_function_7
	def call_function_1(event):
		if function_stu == 0:
			tcpClicSock.send(('function_1_on').encode())
		else:
			tcpClicSock.send(('function_1_off').encode())

	def call_function_2(event):
		if function_stu == 0:
			tcpClicSock.send(('function_2_on').encode())
		else:
			tcpClicSock.send(('function_2_off').encode())

	def call_function_3(event):
		if function_stu == 0:
			tcpClicSock.send(('function_3_on').encode())
		else:
			tcpClicSock.send(('function_3_off').encode())

	def call_function_4(event):
		if function_stu == 0:
			tcpClicSock.send(('function_4_on').encode())
		else:
			tcpClicSock.send(('function_4_off').encode())

	def call_function_5(event):
		if function_stu == 0:
			tcpClicSock.send(('function_5_on').encode())
		else:
			tcpClicSock.send(('function_5_off').encode())

	def call_function_6(event):
		if function_stu == 0:
			tcpClicSock.send(('function_6_on').encode())
		else:
			tcpClicSock.send(('function_6_off').encode())

	def call_function_7(event):
		os.system('%s\\instruction.txt'%sys.path[0])
		# if function_stu == 0:
		# 	tcpClicSock.send(('function_7_on').encode())
		# else:
		# 	tcpClicSock.send(('function_7_off').encode())

	Btn_function_1 = tk.Button(root, width=8, text='RadarScan',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_2 = tk.Button(root, width=8, text='FindColor',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_3 = tk.Button(root, width=8, text='MotionGet',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_4 = tk.Button(root, width=8, text='LineTrack',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_5 = tk.Button(root, width=8, text='Automatic',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_6 = tk.Button(root, width=8, text='SteadyCam',fg=color_text,bg=color_btn,relief='ridge')
	Btn_function_7 = tk.Button(root, width=8, text='Instruction',fg=color_text,bg=color_btn,relief='ridge')

	Btn_function_1.place(x=x,y=y)
	Btn_function_2.place(x=x,y=y+35)
	Btn_function_3.place(x=x,y=y+70)
	Btn_function_4.place(x=x,y=y+105)
	Btn_function_5.place(x=x,y=y+140)
	# Btn_function_6.place(x=x,y=y+175)
	Btn_function_7.place(x=x,y=y+215)

	Btn_function_1.bind('<ButtonPress-1>', call_function_1)
	Btn_function_2.bind('<ButtonPress-1>', call_function_2)
	Btn_function_3.bind('<ButtonPress-1>', call_function_3)
	Btn_function_4.bind('<ButtonPress-1>', call_function_4)
	Btn_function_5.bind('<ButtonPress-1>', call_function_5)
	# Btn_function_6.bind('<ButtonPress-1>', call_function_6)
	Btn_function_7.bind('<ButtonPress-1>', call_function_7)


def loop():
	global root, var_Speed, var_R_L, var_G_L, var_B_L, var_0, var_1, var_2, var_lip1, var_lip2, var_err, var_R, var_G, var_B, var_ec
	root = tk.Tk()			
	root.title('PiCar-B v2.0 GUI')	  
	root.geometry('565x850')  
	root.config(bg=color_bg)  

	var_Speed = tk.StringVar()
	var_Speed.set(100)

	var_R_L = tk.StringVar()
	var_R_L.set(0)
	var_G_L = tk.StringVar()
	var_G_L.set(0)
	var_B_L = tk.StringVar()
	var_B_L.set(0)

	var_R = tk.StringVar()
	var_R.set(80)
	var_G = tk.StringVar()
	var_G.set(80)
	var_B = tk.StringVar()
	var_B.set(80)

	var_0 = tk.StringVar()
	var_0.set(300)
	var_1 = tk.StringVar()
	var_1.set(300)
	var_2 = tk.StringVar()
	var_2.set(300)

	var_lip1 = tk.StringVar()
	var_lip1.set(440)
	var_lip2 = tk.StringVar()
	var_lip2.set(380)
	var_err = tk.StringVar()
	var_err.set(20)

	var_ec = tk.StringVar() #Z
	var_ec.set(0)			#Z

	try:
		logo =tk.PhotoImage(file = 'logo.png')
		l_logo=tk.Label(root,image = logo,bg=color_bg)
		l_logo.place(x=30,y=13)
	except:
		pass

	motor_buttons(30,105)

	information_screen(330,15)

	connent_input(125,15)

	switch_button(30,195)

	servo_buttons(255,195)

	scale(30,230,203)

	scale_RGB(370,280,172)

	scale_PWM(370,400,172)

	ultrasonic_radar(30,290)

	function_buttons(480,15)

	scale_FL(30,550,320)

	scale_FC(30,650,320)

	scale_ExpCom(30,770,320) #Z

	root.mainloop()


if __name__ == '__main__':
	loop()
