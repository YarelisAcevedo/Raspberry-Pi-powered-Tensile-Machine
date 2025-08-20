import RPi.GPIO as GPIO
from time import sleep
import threading

# GPIO Setup
DIR = 10    # Direction pin
STEP = 8    # Step pin
CW = 1      # Clockwise
CCW = 0     # Counterclockwise

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

class MotorControl:
    def __init__(self):
        self.running = False
        self.lock = threading.Lock()
        self.thread = None

    def move_motor(self, direction, steps=18000, delay=0.0005):
        """ Moves the motor in the specified direction """
        with self.lock:
            GPIO.output(DIR, direction)
        for _ in range(steps):
            if not self.running:
                break
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        self.running = False  # mark motor finished

    def start_motor(self, direction, steps=18000):
        """ Start motor in a separate thread """
        if self.running:
            return  # already running
        self.running = True
        self.thread = threading.Thread(
            target=self.move_motor,
            args=(direction, steps),
            daemon=True
        )
        self.thread.start()

    def stop_motor(self):
        """ Stop motor by setting flag """
        self.running = False

    def cleanup(self):
        """ Cleanup GPIO pins """
        self.stop_motor()
        if self.thread and self.thread.is_alive():
            self.thread.join()
        GPIO.cleanup()
