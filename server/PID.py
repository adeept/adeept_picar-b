#! /usr/bin/python3
# File name   : PID.py
# Website     : www.adeept.com
# Author      : William
# Date        : 2019/11/21
import time

class PID:
    def __init__(self):
        self.Kp = 0
        self.Kd = 0
        self.Ki = 0
        self.Initialize()

    def SetKp(self,invar):
        self.Kp = invar

    def SetKi(self,invar):
        self.Ki = invar

    def SetKd(self,invar):
        self.Kd = invar

    def SetPrevError(self,preverror):
        self.prev_error = preverror

    def Initialize(self):
        self.currtime = time.time()
        self.prevtime = self.currtime

        self.prev_error = 0

        self.Cp = 0
        self.Ci = 0
        self.Cd = 0

    def GenOut(self,error):
        self.currtime = time.time()
        dt = self.currtime - self.prevtime
        de = error - self.prev_error

        self.Cp = self.Kp*error
        self.Ci += error*dt

        self.Cd = 0
        if dt > 0:
            self.Cd = de/dt

        self.prevtime = self.currtime
        self.prev_error = error

        return self.Cp + (self.Ki*self.Ci) + (self.Kd*self.Cd)
'''
pid = PID()
pid.SetKp(Kp)
pid.SetKd(Kd)
pid.SetKi(Ki)

fb = 0
outv = 0

PID_loop = True

while PID_loop:
    error = Sp - fb

    outv = pid.GenOut(error)
    AnalogOut(outv)

    time.sleep(0.05)

    fb = AnalogIn(fb_input)
    pass
'''