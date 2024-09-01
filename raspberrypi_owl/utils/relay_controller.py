import time
import RPi.GPIO as GPIO

class RelayController:
    def __init__(self, relay_pins):
        self.relay_pins = relay_pins
        GPIO.setmode(GPIO.BOARD)
        for pin in relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def activate_relay(self, relay_id, duration):
        GPIO.output(self.relay_pins[relay_id], GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(self.relay_pins[relay_id], GPIO.LOW)

    def boom_flush(self, duration=5):
        """Activate all relays at once for a specified duration."""
        for relay in self.relay_pins:
            GPIO.output(relay, GPIO.HIGH)
        time.sleep(duration)
        for relay in self.relay_pins:
            GPIO.output(relay, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()
