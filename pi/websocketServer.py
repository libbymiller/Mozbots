#!/usr/bin/env python3
import sys
import time
import os
import traceback
import math


import RPi.GPIO as GPIO


from time import sleep

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

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

class SimpleEcho(WebSocket):

    def handleMessage(self):
        global last_lr
        global last_ud
        command = self.data
        print("command",command)

        if(command == "left_a_bit"):
          p = last_lr
          print("p",p)
          try:
            if(p+2.0 < 12):
              pan(p+2.0)
            else:
              print("too far left!")
          except:
            traceback.print_exc()

        if(command == "right_a_bit"):
          p = last_lr
          print("p",p)
          try:
            if(p-2.0 > 0.0):
              pan(p-2.0)
            else:
              print("too far right!")
          except:
            traceback.print_exc()

        if(command == "down_a_bit"):
          t = last_ud
          print("t",t)
          try:
            print("t - down a bit",t)
            if(t+2.0 < 12):
              tilt(t+2.0)
            else:
              print("too far forward!")

          except:
            traceback.print_exc()

        if(command == "up_a_bit"):
          t = last_ud
          print("t",t)
          try:
            if(t-2.0 > 0):
              tilt(t-2.0)
            else:
              print("too far back!")
          except:
            traceback.print_exc()


# used by the software mostly
        if(command == "gone"):

          t = servo_ud.angle
          p = servo_lr.angle

          try:
            tilt(6.0)
            pan(6.0)
          except:
            traceback.print_exc()

        if(command == "arrived"):

          t = 6.0
          p = 6.0

          try:
            tilt(6.0)
            time.sleep(0.5)
            pan(6.0)
          except:
            traceback.print_exc()

        if(command == "leaving"):
          tilt(6.0)

        if(command == "left"):
          pan(2.0)

        if(command == "right"):
          pan(10.0)

        if(command == "halt"):

          try:
            tilt(6.0)
            pan(6.0)
            sys.stdout.flush()
          except:
            traceback.print_exc()

          time.sleep(5)
          result = os.system("/home/pi/stop_all.sh")

        if(command == "reboot"):
          tilt(6.0)
          pan(6.0)
          time.sleep(5)
          result = os.system("/home/pi/restart.sh")


    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')



pwm_lr.start(6.0)
pwm_ud.start(6.0)
pwm_lr.ChangeDutyCycle(0)
pwm_ud.ChangeDutyCycle(0)

server = SimpleWebSocketServer('', 80, SimpleEcho)
server.serveforever()

