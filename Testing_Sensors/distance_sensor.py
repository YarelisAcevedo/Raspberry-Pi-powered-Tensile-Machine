import RPi.GPIO as GPIO
from time import sleep
import sys
import time

# GPIO Setup for Ultrasonic Distance Sensor
T = 23   # Trigger pin
E = 7    # Echo pin

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(T, GPIO.OUT)
GPIO.setup(E, GPIO.IN)

#set Trigger to HIGH
GPIO.output(T, True)

#set Trigger after 0.01ms to LOW
time.sleep(0.00001)
GPIO.output(T, False)

StartTime = time.time()
StopTime = time.time()

#save StartTime
while GPIO.input(E) == 0:
    StartTime = time.time()

#save time of arrival
while GPIO.input(E) == 1:
    StopTime = time.time()

#time difference between start and arrival
TimeElapsed = StopTime - StartTime
#multiply with the sonic speed (34300 cm/s
#and divide by 2
distance = (TimeElapsed * 34300)/2

print("Testing the distance sensor:")
print(distance)
