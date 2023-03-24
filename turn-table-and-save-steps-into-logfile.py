# Import required modules
import time
from time import sleep
import RPi.GPIO as GPIO

# Store payload value in the variable 'value'
value = int(msg['payload'])

# Define control pins for the rotary table motor
control_pins = [26, 19, 13, 6]

# Set up GPIO outputs on the Raspberry Pi
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Define a function to write data to a log file
def write(parameter, value):
    with open("/home/pi/shared/log/" + parameter + ".log", "w") as file:
        file.write(str(value))

# Define a function to read data from a log file
def load(parameter):
    with open("/home/pi/shared/log/" + parameter + ".log", "r") as file:
        parameter = file.read()
    return parameter

# Load home position value from log file and store in 'homecounterTT'
homecounterTT = int(load("homeTT"))

# Set up motor control pins and initialize output to 0
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

    # Define half-step sequence for motor control
    halfstep_seq = [
        [1, 0, 0, 1],
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
    ]

# Move the motor by the number of steps specified in 'value'
for i in range(value):
    for halfstep in range(8):

        # Iterate through each motor position in the sequence
        for pin in range(4):
            GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])

        # Delay to allow for motor movement
        time.sleep(0.001)

# Calculate new home position and update log file
newHome = homecounterTT - value
write("homeTT", newHome)

# Clean up GPIO pins
GPIO.cleanup()

# Return message
return msg

