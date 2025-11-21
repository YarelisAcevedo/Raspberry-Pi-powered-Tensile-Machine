import RPi.GPIO as GPIO
from hx711 import HX711
from time import sleep
import sys
import time


hx = HX711(5, 6)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


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

print("Testing the LoadCell")
Loadcell()
time.sleep(2)
Loadcell()
time.sleep(2)


