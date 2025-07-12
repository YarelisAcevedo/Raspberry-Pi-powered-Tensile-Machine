import RPi.GPIO as GPIO
from hx711 import HX711
from time import sleep
import threading

# GPIO Setup for Load Cell and Distance Sensor
T = 23   # Trigger pin
E = 7    # Echo pin

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(T, GPIO.OUT)
GPIO.setup(E, GPIO.IN)

# Initialize Load Cell
class SensorReading:
    def __init__(self):
        self.load = 0
        self.distance = 0
        self.running = False
        self.lock = threading.Lock()

        # Now initialize HX711 properly
        self.hx = HX711(6, 5)
        self.hx.set_reference_unit(1)
        self.hx.reset()
        self.hx.tare()

class SensorReading:
    def __init__(self):
        self.load = 0
        self.distance = 0
        self.running = False
        self.lock = threading.Lock()

    def read_loadcell(self):
        """ Reads the load cell value """
        with self.lock:
            val = self.hx.get_weight(5)
            self.hx.power_down()
            self.hx.power_up()
            return val

    def read_distance(self):
        """ Measures distance using the proximity sensor """
        with self.lock:
            GPIO.output(T, True)
            sleep(0.00001)
            GPIO.output(T, False)

            start_time = sleep(0.00001)
            stop_time = sleep(0.00001)

            while GPIO.input(E) == 0:
                start_time = sleep(0.00001)

            while GPIO.input(E) == 1:
                stop_time = sleep(0.00001)

            time_elapsed = stop_time - start_time
            distance = (time_elapsed * 34300) / 2
            return distance

    def start_reading(self):
        """ Start reading sensors in a separate thread """
        self.running = True
        threading.Thread(target=self._update_readings).start()

    def stop_reading(self):
        """ Stop reading sensors """
        self.running = False

    def _update_readings(self):
        """ Continuously updates readings in the background """
        while self.running:
            self.load = self.read_loadcell() * 35  # Scale the load value
            self.distance = self.read_distance()
            sleep(1)
