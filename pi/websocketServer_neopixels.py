#!/usr/bin/env python3
import sys
import time
import os
import traceback
import math


import RPi.GPIO as GPIO

from time import sleep

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


# set up the GPIO pin for the servo
servo_pin_lr = 12
servo_pin_ud = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_lr,GPIO.OUT)
GPIO.setup(servo_pin_ud,GPIO.OUT)

# set up PWM process
pwm_lr = GPIO.PWM(servo_pin_lr,50) # 50 Hz (20 ms PWM period)
pwm_ud = GPIO.PWM(servo_pin_ud,50) # 50 Hz (20 ms PWM period)


last_lr = 0
last_ud = 0

# pixelring
# based on https://raw.githubusercontent.com/themagpimag/monthofmaking2019/master/DisplayLights/rollcall.py

import threading
import board
import neopixel
import numpy as np

# LED strip configuration:
LED_COUNT   = 24      # Number of LED pixels.
LED_PIN     = board.D18      # GPIO pin
LED_BRIGHTNESS = 0.1  # LED brightness
LED_ORDER = neopixel.GRBW # order of LED colours. May also be RGB, GRBW, or RGBW

# lime and red
gokai_colours = [(207,240,10),(192,46,27)]

# Create NeoPixel object with appropriate configuration.
strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS, auto_write=False, pixel_order = LED_ORDER)

# turn it off
strip.fill((0,0,0))
strip.show()

# Create a way to fade/transition between colours using numpy arrays

def fade(colour1, colour2, percent):
    colour1 = np.array(colour1)
    colour2 = np.array(colour2)
    vector = colour2-colour1
    newcolour = (int((colour1 + vector * percent)[0]), int((colour1 + vector * percent)[1]), int((colour1 + vector * percent)[2]))
    #print("newcolour",newcolour,"percent",percent)
    return newcolour

# Create a function that will cycle through the colours selected above

def rollcall_cycle(wait):
    for j in range(len(gokai_colours)):
        for i in range(10):
            colour1 = gokai_colours[j]
            #print("colour1",j,gokai_colours[j])
            if j == 1:
                colour2 = gokai_colours[0]
            else:
                colour2 = gokai_colours[(j+1)]
            percent = i*0.1   # 0.1*100 so 10% increments between colours
            strip.fill((fade(colour1,colour2,percent)))
            strip.show()
            time.sleep(wait)

present = False
t1 = None

def foo():
       global present
       while True:
         rollcall_cycle(0.2)
         if(present == False):
            print("BREAK!")
            strip.fill((0,0,0))
            strip.show()
            break

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
        global present
        global t1
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

#          try:
 #           tilt(6.0)
  #          pan(6.0)
   #       except:
    #        traceback.print_exc()

          present = False
          try:
            t1.join()
          except:
            traceback.print_exc()

        if(command == "arrived"):

          try:
            tilt(2.0)
            time.sleep(0.5)
            pan(6.0)
          except:
            traceback.print_exc()
          present = True
          try:
             t1 = threading.Thread(target=foo, args=())
             t1.start()
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
