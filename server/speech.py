#!/usr/bin/python3
# File name   : speech.py
# Description : Speech Recognition 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William & Authors from https://github.com/Uberi/speech_recognition#readme
# Date        : 2018/10/12
import speech_recognition as sr
import move
import RPIservo
import robotLight
import time

scGear = RPIservo.ServoCtrl()
scGear.moveInit()

move.setup()

RL=robotLight.RobotLight()

v_command=''
speed_set = 80

def setup():
    move.setup()


def run():
    global v_command
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(device_index =2,sample_rate=48000) as source:
        r.record(source,duration=2)
        #r.adjust_for_ambient_noise(source)
        RL.both_off()
        RL.yellow()
        print("Command?")
        audio = r.listen(source)
        RL.both_off()
        RL.blue()

    try:
        v_command = r.recognize_sphinx(audio,
        keyword_entries=[('forward',1.0),('backward',1.0),
        ('left',1.0),('right',1.0),('stop',1.0)])        #You can add your own command here
        print(v_command)
        RL.both_off()
        RL.cyan()
    except sr.UnknownValueError:
        print("say again")
        RL.both_off()
        RL.red()
    except sr.RequestError as e:
        RL.both_off()
        RL.red()
        pass

    #print('pre')

    if 'forward' in v_command:
        scGear.moveAngle(2, 0)
        move.motor_left(1, 0, speed_set)
        move.motor_right(1, 0, speed_set)
        time.sleep(2)
        move.motorStop()

    elif 'backward' in v_command:
        scGear.moveAngle(2, 0)
        move.motor_left(1, 1, speed_set)
        move.motor_right(1, 1, speed_set)
        time.sleep(2)
        move.motorStop()

    elif 'left' in v_command:
        scGear.moveAngle(2, 45)
        move.motor_left(1, 0, speed_set)
        move.motor_right(1, 0, speed_set)
        time.sleep(2)
        move.motorStop()
        scGear.moveAngle(2, 0)

    elif "right" in v_command:
        scGear.moveAngle(2,-45)
        move.motor_left(1, 0, speed_set)
        move.motor_right(1, 0, speed_set)
        time.sleep(2)
        move.motorStop()
        scGear.moveAngle(2, 0)

    elif 'stop' in v_command:
        move.motorStop()

    else:
        pass
