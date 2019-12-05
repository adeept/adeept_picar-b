#!/usr/bin/env/python
# File name   : server.py
# Production  : PiCar-C
# Website     : www.adeept.com
# Author      : William
# Date        : 2019/11/21

import socket
import threading
import time
import os
import LED
import move
import servo
import switch
servo.servo_init()
switch.switchSetup()
switch.set_all_switch_off()
Led  = LED.LED()
Led.colorWipe(80,255,0)

step_set = 1
speed_set = 100
rad = 0.6

direction_command = 'no'
turn_command = 'no'
servo_command = 'no'
pos_input = 1
catch_input = 1
cir_input = 6

servo_speed  = 5

ledthread = LED.LED_ctrl()
ledthread.start()

class Servo_ctrl(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Servo_ctrl, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            if servo_command == 'lookleft':
                servo.lookleft(servo_speed)
            elif servo_command == 'lookright':
                servo.lookright(servo_speed)
            elif servo_command == 'up':
                servo.up(servo_speed)
            elif servo_command == 'down':
                servo.down(servo_speed)
            time.sleep(0.03)

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()


def app_ctrl():
    global servo_move
    app_HOST = ''
    app_PORT = 10123
    app_BUFSIZ = 1024
    app_ADDR = (app_HOST, app_PORT)

    servo_move = Servo_ctrl()
    servo_move.start()
    servo_move.pause()

    def  ap_thread():
        os.system("sudo create_ap wlan0 eth0 Groovy 12345678")

    def setup():
        move.setup()

    def appCommand(data_input):
        global direction_command, turn_command, servo_command
        if data_input == 'forwardStart\n':
            direction_command = 'forward'
            move.move(speed_set, direction_command)

        elif data_input == 'backwardStart\n':
            direction_command = 'backward'
            move.move(speed_set, direction_command)

        elif data_input == 'leftStart\n':
            turn_command = 'left'
            servo.turnLeft()
            move.move(speed_set, direction_command)

        elif data_input == 'rightStart\n':
            turn_command = 'right'
            servo.turnRight()
            move.move(speed_set, direction_command)

        elif 'forwardStop' in data_input:
            if turn_command == 'no':
                move.motorStop()

        elif 'backwardStop' in data_input:
            if turn_command == 'no':
                move.motorStop()

        elif 'leftStop' in data_input:
            turn_command = 'no'
            servo.turnMiddle()
            move.motorStop()

        elif 'rightStop' in data_input:
            turn_command = 'no'
            servo.turnMiddle()
            move.motorStop()

        if data_input == 'lookLeftStart\n':
            servo_command = 'lookleft'
            servo_move.resume()

        elif data_input == 'lookRightStart\n': 
            servo_command = 'lookright'
            servo_move.resume()

        elif data_input == 'downStart\n':
            servo_command = 'down'
            servo_move.resume()

        elif data_input == 'upStart\n':
            servo_command = 'up'
            servo_move.resume()

        elif 'lookLeftStop' in data_input:
            servo_move.pause()
            servo_command = 'no'
        elif 'lookRightStop' in data_input:
            servo_move.pause()
            servo_command = 'no'
        elif 'downStop' in data_input:
            servo_move.pause()
            servo_command = 'no'
        elif 'upStop' in data_input:
            servo_move.pause()
            servo_command = 'no'


        if data_input == 'aStart\n':
            if LED.ledfunc != 'police':
                LED.ledfunc = 'police'
                ledthread.resume()
            elif LED.ledfunc == 'police':
                LED.ledfunc = ''
                ledthread.pause()

        elif data_input == 'bStart\n':
            if LED.ledfunc != 'rainbow':
                LED.ledfunc = 'rainbow'
                ledthread.resume()
            elif LED.ledfunc == 'rainbow':
                LED.ledfunc = ''
                ledthread.pause()

        elif data_input == 'cStart\n':
            switch.switch(1,1)
            switch.switch(2,1)
            switch.switch(3,1)

        elif data_input == 'dStart\n':
            switch.switch(1,0)
            switch.switch(2,0)
            switch.switch(3,0)

        elif 'aStop' in data_input:
            pass
        elif 'bStop' in data_input:
            pass
        elif 'cStop' in data_input:
            pass
        elif 'dStop' in data_input:
            pass

        print(data_input)

    def appconnect():
        global AppCliSock, AppAddr
        try:
            s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("1.1.1.1",80))
            ipaddr_check=s.getsockname()[0]
            s.close()
            print(ipaddr_check)

            AppSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            AppSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            AppSerSock.bind(app_ADDR)
            AppSerSock.listen(5)
            print('waiting for App connection...')
            AppCliSock, AppAddr = AppSerSock.accept()
            print('...App connected from :', AppAddr)
        except:
            ap_threading=threading.Thread(target=ap_thread)       #Define a thread for AP Mode
            ap_threading.setDaemon(True)                          #'True' means it is a front thread,it would close when the mainloop() closes
            ap_threading.start()                                  #Thread starts

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

            AppSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            AppSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            AppSerSock.bind(app_ADDR)
            AppSerSock.listen(5)
            print('waiting for App connection...')
            AppCliSock, AppAddr = AppSerSock.accept()
            print('...App connected from :', AppAddr)

    appconnect()
    setup()
    app_threading=threading.Thread(target=appconnect)         #Define a thread for app connection
    app_threading.setDaemon(True)                             #'True' means it is a front thread,it would close when the mainloop() closes
    app_threading.start()                                     #Thread starts

    while 1:
        data = ''
        data = str(AppCliSock.recv(app_BUFSIZ).decode())
        if not data:
            continue
        appCommand(data)
        pass

if __name__ == '__main__':
    app_ctrl()