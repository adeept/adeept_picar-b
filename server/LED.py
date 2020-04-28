#!/usr/bin/python3
# File name   : LED.py
# Description : WS_2812
# Website     : based on the code from https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/examples/strandtest.py
# Author      : original code by Tony DiCola (tony@tonydicola.com)
# Date        : 2019/02/23
import time
from rpi_ws281x import *
import argparse
import threading

# LED strip configuration:
LED_COUNT      = 12      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

ledfunc = ''

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

class LED:
    def __init__(self):
        self.LED_COUNT      = 16      # Number of LED pixels.
        self.LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
        self.LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
        args = parser.parse_args()

        # Create NeoPixel object with appropriate configuration.
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()

    # Define functions which animate LEDs in various ways.
    def colorWipe(self, R, G, B):
        """Wipe color across display a pixel at a time."""
        color = Color(R,G,B)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()

    def rainbow(self, wait_ms=20, iterations=1):
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256 * iterations):
            if ledfunc == 'rainbow':
                for i in range(self.strip.numPixels()):
                    if ledfunc == 'rainbow':
                        self.strip.setPixelColor(i, wheel((i + j) & 255))
                    else:
                        break
                self.strip.show()
                time.sleep(wait_ms / 1000.0)
            else:
                break
    
    def SideAWipe(self, R, G, B):
        """Wipe color across display a pixel at a time."""
        color = Color(R,G,B)
        for i in range(0, 6):
            self.strip.setPixelColor(i, color)
            self.strip.show()

    def SideBWipe(self, R, G, B):
        """Wipe color across display a pixel at a time."""
        color = Color(R,G,B)
        for i in range(6, 12):
            self.strip.setPixelColor(i, color)
            self.strip.show()


class LED_ctrl(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(LED_ctrl, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def run(self):
        global goal_pos, servo_command, init_get, functionMode
        while self.__running.isSet():
            self.__flag.wait()
            if ledfunc == 'police':
                time.sleep(0.1)
                led.SideAWipe(0, 0, 255)
                led.SideBWipe(255, 0, 0)
                time.sleep(0.03)
                led.colorWipe(0,0,0)
                time.sleep(0.03)

                led.SideAWipe(0, 0, 255)
                led.SideBWipe(255, 0, 0)
                time.sleep(0.03)
                led.colorWipe(0,0,0)
                time.sleep(0.03)

                led.SideAWipe(0, 0, 255)
                led.SideBWipe(255, 0, 0)
                time.sleep(0.03)
                led.colorWipe(0,0,0)
                time.sleep(0.03)

                time.sleep(0.1)
                led.SideAWipe(255, 0, 0)
                led.SideBWipe(0, 0, 255)
                time.sleep(0.03)
                led.colorWipe(0,0,0)
                time.sleep(0.03)

                led.SideAWipe(255, 0, 0)
                led.SideBWipe(0, 0, 255)
                time.sleep(0.03)
                led.colorWipe(0,0,0)
                time.sleep(0.03)

                led.SideAWipe(255, 0, 0)
                led.SideBWipe(0, 0, 255)
                time.sleep(0.03)
                led.colorWipe(0,0,0)
                time.sleep(0.03)
            elif ledfunc == 'rainbow':
                led.rainbow()
            elif ledfunc == '':
                self.pause()

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()

led = LED()
if __name__ == '__main__':
    led = LED()
    led.colorWipe(255,255,255)