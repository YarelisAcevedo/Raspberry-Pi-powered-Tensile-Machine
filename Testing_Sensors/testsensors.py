import RPi.GPIO as GPIO
from hx711 import HX711
from time import sleep
import sys
import time

# GPIO Setup for motor
DIR = 10    # Direction pin
STEP = 8    # Step pin
CW = 1      # Clockwise
CCW = 0     # Counterclockwise

# GPIO Setup for Ultrasonic Distance Sensor
T = 23   # Trigger pin
E = 7    # Echo pin

hx = HX711(5, 6)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(T, GPIO.OUT)
GPIO.setup(E, GPIO.IN)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

###################################################################

def Loadcell():
    hx.set_reading_format("MSB", "MSB")
    referenceUnit = 114
    hx.set_reference_unit(referenceUnit)

    hx.reset()

    hx.tare()

    print("Tare done! Add weight now...")

    val = hx.get_weight(5)
    print(val)

    hx.power_down()
    hx.power_up()
    time.sleep(0.1)

    return 

###################################################################

def distance():
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

    print(distance)

    return

###################################################################

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
print("Now testing distance sensor")
distance()
time.sleep(2)
print("Finally testing the LoadCell")
Loadcell()
time.sleep(2)
print("If something didn't work out, check the connections")
print("Bye!")


