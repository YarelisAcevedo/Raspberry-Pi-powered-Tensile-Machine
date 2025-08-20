import RPi.GPIO as GPIO
import time
from hx711 import HX711
from time import sleep
import threading

# GPIO Setup for Ultrasonic Distance Sensor
T = 23   # Trigger pin
E = 7    # Echo pin

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(T, GPIO.OUT)
GPIO.setup(E, GPIO.IN)

class SensorReading:
    def __init__(self):
        self.load = 0
        self.distance = 0
        self.running = False
        self.lock = threading.Lock()
        self.thread = None

        # Initialize HX711 load cell
        self.hx = HX711(6, 5)   # (DT, SCK)
        self.hx.set_reference_unit(1)
        self.hx.reset()
        self.hx.tare()

    def read_loadcell(self):
        """ Reads the load cell value """
        with self.lock:
            val = self.hx.get_weight(5)
            self.hx.power_down()
            self.hx.power_up()
            return val

    def read_distance(self):
        """ Measures distance using ultrasonic sensor """
        with self.lock:
            GPIO.output(T, True)
            sleep(0.00001)
            GPIO.output(T, False)

            start_time = time.time()
            stop_time = time.time()

            while GPIO.input(E) == 0:
                start_time = time.time()

            while GPIO.input(E) == 1:
                stop_time = time.time()

            time_elapsed = stop_time - start_time
            distance = (time_elapsed * 34300) / 2
            return distance

    def _update_readings(self):
        """ Continuously updates readings in the background """
        while self.running:
            try:
                self.load = self.read_loadcell() * 35  # Scale factor
                self.distance = self.read_distance()
            except Exception as e:
                print(f"Sensor error: {e}")
            sleep(0.5)  # adjust reading frequency

    def start_reading(self):
        """ Start sensor readings in a background thread """
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._update_readings, daemon=True)
        self.thread.start()

    def stop_reading(self):
        """ Stop reading sensors """
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
