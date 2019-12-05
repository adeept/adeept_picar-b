#!/usr/bin/python3
# File name   : speech.py
# Description : Speech Recognition 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William & Authors from https://github.com/Uberi/speech_recognition#readme
# Date        : 2019/11/21

import speech_recognition as sr
# import pyaudio

# p = pyaudio.PyAudio()
# info = p.get_host_api_info_by_index(0)
# numdevices = info.get('deviceCount')
# for i in range(0, numdevices):
#         if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
#             print ("Input Device id "+str(i)+" - "+p.get_device_info_by_host_api_device_index(0, i).get('name'))
import time

v_command=''

def run():
    global v_command
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(device_index =2,sample_rate=48000) as source:
        r.record(source,duration=2)
        # #r.adjust_for_ambient_noise(source)

        print("Voice Command?")
        # audio = r.listen(source)

        try:
            v_command = r.recognize_sphinx(r.listen(source),
            keyword_entries=[('forward',1.0),('backward',1.0),
            ('left',1.0),('right',1.0),('stop',1.0)])        #You can add your own command here

            print(v_command)
        except sr.UnknownValueError:
            print("say again")
        except sr.RequestError as e:
            print("RE")
            pass

        return v_command


if __name__ == '__main__':

    time.sleep(1)
    commandGenOut = run()
    print(commandGenOut)
    time.sleep(1)