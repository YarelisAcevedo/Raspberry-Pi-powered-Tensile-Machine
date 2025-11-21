import RPi.GPIO as GPIO
from time import sleep
import time

# GPIO Setup for motor
DIR = 17
STEP = 27
CW = 1
CCW = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

def run(direction, steps=18000, delay=0.0007):
    GPIO.output(DIR, direction)
    sleep(0.5)

    for _ in range(steps):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)

def forward():
    run(CW)

def backward():
    run(CCW)

try:
    print("Testing the motor")
    print("Moving clockwise...")
    forward()
    sleep(2)
    print("Moving counterclockwise...")
    backward()
    sleep(2)

finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
