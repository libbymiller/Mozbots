#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from time import sleep
import sys

# setup the GPIO pin for the servo
servo_pin_lr = 12
servo_pin_ud = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_lr,GPIO.OUT)
GPIO.setup(servo_pin_ud,GPIO.OUT)

# setup PWM process
pwm_lr = GPIO.PWM(servo_pin_lr,50) # 50 Hz (20 ms PWM period)
pwm_ud = GPIO.PWM(servo_pin_ud,50) # 50 Hz (20 ms PWM period)

last_lr = 0
last_ud = 0

def pan(to):
   print("panning",to)
   global last_lr
   pwm_lr.ChangeDutyCycle(to)
   time.sleep(0.5)
   pwm_lr.ChangeDutyCycle(0)
   last_lr = to

def tilt(to):
   global last_ud
   pwm_ud.ChangeDutyCycle(to)
   time.sleep(0.5)
   pwm_ud.ChangeDutyCycle(0)
   last_ud = to

pwm_lr.start(6.0)
pwm_ud.start(6.0)

pwm_lr.ChangeDutyCycle(0)
pwm_ud.ChangeDutyCycle(0)

tilt(float(sys.argv[1]))

GPIO.cleanup()

