import RPi.GPIO as GPIO
from time import sleep
import sys
import time

# GPIO Setup for motor
DIR = 10    # Direction pin
STEP = 8    # Step pin
CW = 1      # Clockwise
CCW = 0     # Counterclockwise

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

def forward():
    dir = 1
    run(dir)
    return

def backward():
    dir = 0
    run(dir)
    return

def run(dir):
    sleep(1.0)

    if dir == 1:
        GPIO.output(DIR,1)
        for x in range(18000):
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            sleep(.0005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            sleep(.0005) # Dictates how fast stepper motor will run
    
    if dir == 0:
        GPIO.output(DIR,0)
        for x in range(18000):
            # Set one coil winding to high
            GPIO.output(STEP,GPIO.HIGH)
            # Allow it to get there.
            sleep(.0005) # Dictates how fast stepper motor will run
            # Set coil winding to low
            GPIO.output(STEP,GPIO.LOW)
            sleep(.0005) # Dictates how fast stepper motor will run
    return

print("Testing the motor first")
print("Moving clockwise")
forward()
time.sleep(2)
print("Counterclockwise")
backward()
time.sleep(2)
