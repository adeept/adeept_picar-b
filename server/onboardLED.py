import RPi.GPIO as GPIO
import time

pin_led_1 = 5
pin_led_2 = 6
pin_led_3 = 13


GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_led_1, GPIO.OUT)
GPIO.setup(pin_led_2, GPIO.OUT)
GPIO.setup(pin_led_3, GPIO.OUT)


def control_led(pin, state):
    GPIO.output(pin, state)


try:
    while True:
        control_led(pin_led_1, True)
        time.sleep(0.1)
        control_led(pin_led_1, False)
        time.sleep(0.1)

        control_led(pin_led_2, True)
        time.sleep(0.1)
        control_led(pin_led_2, False)
        time.sleep(0.1)

        control_led(pin_led_3, True)
        time.sleep(0.1)
        control_led(pin_led_3, False)
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

# 清理GPIO设置
GPIO.cleanup()
