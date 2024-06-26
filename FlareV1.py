import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
# gpio 24 for buzzer
# gpio 23 - green
# gpio 4 - red

switchPINS = [37, 35, 33, 31, 29, 15, 13, 11]  # Pins for dip switch


for pin in switchPINS:
    GPIO.setup(pin, GPIO.OUT)


def check_dip_switch():
    for pin in switchPINS:
        if GPIO.input(pin) == GPIO.HIGH:  # Check if any switch is flipped
            print("Switch flipped.")
            GPIO.cleanup()
            exit()

try:
    # Set initial state for all switches (no action needed if we just want to monitor the switches)

    start_time = time.time()
    while time.time() - start_time < 60:  # Loop for 1 minute
        check_dip_switch()
        time.sleep(1)

    print("1 minute elapsed. Program terminating.")
finally:
    GPIO.cleanup()
