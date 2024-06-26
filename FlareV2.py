import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# pins
REDindicator = 8 # pin
GREENindicator = 12 # pin
buzzerPIN = 16 # pin for input of buzzer  
switchPINS = [37, 35, 33, 31, 29, 27, 23, 21] # pins for dip switch
NNANDpins = [22, 5, 7, 3, 13, 19, 11, 15]  # inputs from tcobbler to gates
ANDpins = [26, 40, 18, 24, 36, 38, 28, 32]  # inputs from tcobbler to gates

def clear_leds():
    GPIO.output(REDindicator, GPIO.LOW)
    GPIO.output(GREENindicator, GPIO.LOW)

# set up pins
for pin in [REDindicator, GREENindicator, buzzerPIN]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in NNANDpins + ANDpins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in switchPINS:
    GPIO.setup(pin, GPIO.IN)

# clear leds at the start
clear_leds ()

def buzz(success):
    if success:
        GPIO.output(buzzerPIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(buzzerPIN, GPIO.LOW)
    else:
        for _ in range(3):
            GPIO.output(buzzerPIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(buzzerPIN, GPIO.LOW)
            time.sleep(0.2)

def sequence_lights(sequence): # this function validates the input sequence against the switches- the output of this function is boolean. 
    # if there is a switch flipped, initial_switch_states is false and tells the code to turn LED red, if not it goes to the next 
    # number in the sequence and repeats this process, all lights must be 'success' for GREENindicator light to be on (all switches must be closed)
    
    success = True
    initial_switch_states = [GPIO.input(pin) for pin in switchPINS]  # Store initial switch states

    for i in range(8):
        index = sequence[i] - 1
        switchInput = GPIO.input(switchPINS[index])

        # signals for NAND gates
        GPIO.output(NNANDpins[index], GPIO.HIGH)

        # Simulating NAND gate output (True if any input is False)
        nand_output = not (switchInput and GPIO.input(NNANDpins[index]))

        # signals for AND gates
        GPIO.output(ANDpins[index], GPIO.HIGH)

        # AND gate output
        and_output = nand_output and GPIO.input(ANDpins[index])

        if initial_switch_states[index] == GPIO.HIGH:  # check if switch is flipped
            # red LED should turn on bc of fail
            success = False
            GPIO.output(REDindicator, GPIO.HIGH)
            GPIO.output(GREENindicator, GPIO.LOW)
        else:
            if and_output:
                # AND gate output produces a GREEN LED
                GPIO.output(REDindicator, GPIO.LOW)
                GPIO.output(GREENindicator, GPIO.HIGH)
            else:
                # red led is on bc of failure
                GPIO.output(REDindicator, GPIO.HIGH)
                GPIO.output(GREENindicator, GPIO.LOW)

        time.sleep(3)  # 3 second delay

    if success:
        # green led for 'success'
        GPIO.output(REDindicator, GPIO.LOW)
        GPIO.output(GREENindicator, GPIO.HIGH)
        buzz(True)
    else:
        # red led for 'failure'
        GPIO.output(REDindicator, GPIO.HIGH)
        GPIO.output(GREENindicator, GPIO.LOW)
        buzz(False)

    return success

try:
    while True:
        input_sequence = input("Enter the sequence (8 space-separated numbers): ")
        sequence = list(map(int, input_sequence.split()))
        if len(sequence) == 8 and all(1 <= num <= 8 for num in sequence):
            GPIO.output(REDindicator, GPIO.LOW)
            GPIO.output(GREENindicator, GPIO.LOW)
            clear_leds()
            sequence_lights(sequence)
        else:
            print("Enter 8 numbers between 1 and 8.")
finally:
    GPIO.cleanup()
