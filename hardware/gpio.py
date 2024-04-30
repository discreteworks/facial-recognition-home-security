import RPi.GPIO as GPIO
from db.pin import Pin
import sys


class PinManager:
    def __init__(self):
        """
        Initialize board pins and signal handling.
        """
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        # setup available pins
        for item in Pin().get_pins():
            GPIO.setup(item[0], GPIO.OUT)
            GPIO.output(item[0], GPIO.HIGH)
   
    def pin_high(self, pin_no):
        """
        Set the pin high on GPIO.LOW to turn on the led for active low relay.
        """
        try:
            GPIO.output(pin_no, GPIO.LOW)
        except Exception as e:
             print("[Error] Pin not setup.")        

    def pin_reset(self):
        """
        Reset to turn off lights.
        """
        try:
            for item in Pin().get_pins():
                GPIO.output(item[0], GPIO.HIGH)
        except Exception as e:
             print("[Info] Pin not setup.")
        
    def cleanup(self):
        """
        Turn off the lights
        and gpio pin cleanup
        """
        self.pin_reset()
        GPIO.cleanup()
