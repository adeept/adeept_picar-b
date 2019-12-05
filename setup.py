#!/usr/bin/python3
# File name   : setup.py
# Description : Software Setup
# Website     : www.adeept.com
# Author      : William
# Date        : 2019/11/21

import os
import time
import sys

def replace_num(file,initial,new_num):  
    newline=""
    str_num=str(new_num)
    with open(file,"r") as f:
        for line in f.readlines():
            if(line.find(initial) == 0):
                line = (str_num+'\n')
            newline += line
    with open(file,"w") as f:
        f.writelines(newline)

for x in range(1,4):
	if os.system("sudo apt-get update") == 0:
		break

# os.system("sudo apt-get purge -y wolfram-engine")
# os.system("sudo apt-get purge -y libreoffice*")
# os.system("sudo apt-get -y clean")
# os.system("sudo apt-get -y autoremove")

# for x in range(1,4):
# 	if os.system("sudo apt-get -y upgrade") == 0:
# 		break

for x in range(1,4):
	if os.system("sudo apt-get install -y i2c-tools") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install adafruit-pca9685") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install rpi_ws281x") == 0:
		break

##########SR###########
for x in range(1,4):
	if os.system("sudo apt-get install pulseaudio pulseaudio-utils libpulse-dev libpulse-java libpulse0") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y bison libasound2-dev swig") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y pulseaudio libpulse-dev") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y portaudio19-dev python3-all-dev python3-pyaudio") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -qq python3 python3-dev python3-pip build-essential swig libpulse-dev") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y gcc libffi-dev libssl-dev python3-dev") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install pyaudio") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y flac") == 0:
		break

for x in range(1,4):
	if os.system("sudo wget https://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz/download -O sphinxbase.tar.gz") == 0:
		break

for x in range(1,4):
	if os.system("sudo wget https://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz/download -O pocketsphinx.tar.gz") == 0:
		break

for x in range(1,4):
	if os.system("sudo tar -xzvf sphinxbase.tar.gz") == 0:
		break

for x in range(1,4):
	if os.system("sudo tar -xzvf pocketsphinx.tar.gz") == 0:
		break

try:
	os.system("cd sphinxbase-5prealpha/ && ./configure -enable-fixed && make && sudo make install")
except:
	pass

try:
	os.system("cd pocketsphinx-5prealpha/ && ./configure && make && sudo make install")
except:
	pass

try:
	os.system("sudo pip3 install pocketsphinx")
except:
	pass

try:
	os.system("sudo pip3 install SpeechRecognition")
except:
	pass
##########SR###########

for x in range(1,4):
	if os.system("sudo apt-get install -y python3-smbus") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install mpu6050-raspberrypi") == 0:
		break

try:
	replace_num("/boot/config.txt",'#dtparam=i2c_arm=on','dtparam=i2c_arm=on\nstart_x=1\n')
except:
	print('try again')

for x in range(1,4):
	if os.system("sudo pip3 install -U pip") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install numpy") == 0:
		break

for x in range(1,4):
	if os.system("sudo apt-get install -y libopencv-dev python3-opencv") == 0:
		break

for x in range(1,4):
	if os.system("sudo pip3 install imutils zmq pybase64 psutil") == 0:   ####
		break

for x in range(1,4):
	if os.system("sudo git clone https://github.com/oblique/create_ap") == 0:
		break

try:
	os.system("cd //home/pi/gwr/create_ap && sudo make install")
except:
	pass

try:
	os.system("cd //home/pi/create_ap && sudo make install")
except:
	pass

for x in range(1,4):
	if os.system("sudo apt-get install -y util-linux procps hostapd iproute2 iw haveged dnsmasq") == 0:
		break

try:
	os.system('sudo rm //home/pi/startup.sh')
except:
	pass

try:
	os.system('sudo touch //home/pi/startup.sh')
	with open("//home/pi/startup.sh",'w') as file_to_write:
		file_to_write.write("#!/bin/sh\nsudo python3 /%s/server/server.py"%sys.path[0])
except:
	pass

os.system('sudo chmod 777 //home/pi/startup.sh')

replace_num('/etc/rc.local','fi','fi\n//home/pi/startup.sh start')

print('restarting')

os.system("sudo reboot")
