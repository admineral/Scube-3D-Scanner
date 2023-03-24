import time
from time import sleep
import RPi.GPIO as GPIO

# Set GPIO mode and disable warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Function to write data to a log file
def write(parameter, value):
    with open("/home/pi/shared/log/" + parameter + ".log", "w") as file:
        file.write(str(value))

# Function to load data from a log file
def load(parameter):
    with open("/home/pi/shared/log/" + parameter + ".log", "r") as file:
        parameter = file.read()
    return parameter

# Motor control pins
control_pins = [5, 11, 9, 10]

# Load home position counter and increment by 5
homecounter = str(load("home"))
stepshome = int(homecounter) + int(5)

# Initialize control pins and set output to 0
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)

    # Define halfstep sequence for motor control
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

# Execute motor movement based on halfstep sequence
for i in range(stepshome):
    for halfstep in range(8):
        for pin in range(4):
            GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
        time.sleep(0.001)

# Clean up GPIO pins
GPIO.cleanup()

# Reset home position counter and update the log file
write("home", 0)

# Set message payload to 0
msg['payload'] = "0"

# Return message
return msg
