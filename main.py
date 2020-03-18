#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


import time 
import math
import random
import urequests
import utime
import ujson
import ubinascii


# Write your program here
ev3 = EV3Brick()
ev3.speaker.beep()


Key = 'BSpkqTmmiCwPhBimQjk8VItZb7lCPIoMzEM8nFuZVx'

def SL_setup():
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
          print(reply)
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = urequests.get(urlValue,headers=headers).text
          data = ujson.loads(value)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result
     
def Create_SL(Tag, Type):
     urlBase, headers = SL_setup()
     urlTag = urlBase + Tag
     propName={"type":Type,"path":Tag}
     try:
          urequests.put(urlTag,headers=headers,json=propName).text
     except Exception as e:
          print(e)

#Initialize Motors and variables
arm = Motor(Port.C)
hand = Motor(Port.D)
button = TouchSensor(Port.S1)
destangle = 0 #This is the angle being written to the arm

def DropInCup(ang):
    arm.reset_angle(0)
    hand.reset_angle(0)
    #arm rotates to angle at a somewhat slow speed
    arm.run_angle(50,ang)
    #hand drops the lego piece in the correct cup
    hand.run_angle(100,90)
    #hand returns to normal position
    hand.run_angle(100,-90)
    arm.run_angle(50,-ang)
    return
brick = ''

while(True):
    if button.pressed()==True:
        brick = Get_SL('Brick')
        print(brick)
        print(len(brick))
        print(brick == ("White angled"))
        wait(500)
        if brick == "Red L":
            print('Herrrrreeeeef')
            destangle = 0
        if brick == "Black T":
            destangle = 20
        if brick == "Axel to holes":
            destangle = 40
        if brick == "Gray L":
            destangle = 60
        if brick == "White angled":
            print('Here')
            destangle = 80
        print(destangle)
        DropInCup(destangle)
        
        
    
    