import RPi.GPIO as GPIO
from time import sleep
import sys
import time

# GPIO Setup for Ultrasonic Distance Sensor
T = 24   # Trigger pin
E = 23    # Echo pin

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(T, GPIO.OUT)
GPIO.setup(E, GPIO.IN)

print("Measuring distance.....")

try:
	while True:
		GPIO.output(T, False)
		time.sleep(0.5)

		GPIO.output(T, True)
		time.sleep(0.00001)
		GPIO.output(T, False)

		while GPIO.input(E) == 0:
			pulse_start = time.time()

		while GPIO.input(E) == 1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		print("Distance: ", distance, " cm")

except KeyboardInterrupt:
	GPIO.cleanup()

