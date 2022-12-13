# run with
# sudo python3 scany.py
import time
from time import sleep
import RPi.GPIO as GPIO


# Print a message to indicate that the program is starting
print ("Programm startet")


class Motor:
    # Configure the Raspberry Pi's GPIO pins
    # Set warnings to False to suppress warning messages
    GPIO.setwarnings(False)
    # Set the numbering mode to use the BCM (Broadcom) pin numbers
    GPIO.setmode(GPIO.BCM)
    
    # Set the variables A, B, C, and D to the pin numbers
    # to which the stepper motor's wires are connected
    A=26
    B=19
    C=13
    D=6
    
    # Set the step time (the time each step should take)
    step_time=0.001

    # Set the specified GPIO pins to be outputs
    # and set their initial values to False (low)
    GPIO.setup(A,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    GPIO.setup(C,GPIO.OUT)
    GPIO.setup(D,GPIO.OUT)
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, False)

    
    
    # Define eight different step methods
    # Each step method sets the values of the GPIO pins
    # to turn the motor by a small amount
    def Step1():
        GPIO.output(Motor.D, True)
        sleep(Motor.step_time)
        GPIO.output(Motor.D, False)
        
    def Step2():
        GPIO.output(Motor.D, True)
        GPIO.output(Motor.C, True)
        sleep(Motor.step_time)
        GPIO.output(Motor.D, False)
        GPIO.output(Motor.C, False)
        
    def Step3():
        GPIO.output(Motor.C, True)
        sleep(Motor.step_time)
        GPIO.output(Motor.C, False)
        
    def Step4():
        GPIO.output(Motor.B, True)
        GPIO.output(Motor.C, True)
        sleep(Motor.step_time)
        GPIO.output(Motor.B, False)
        GPIO.output(Motor.C, False)
        
    def Step5():
        GPIO.output(Motor.B, True)
        sleep(Motor.step_time)
        GPIO.output(Motor.B, False)
        
    def Step6():
        GPIO.output(Motor.A, True)
        GPIO.output(Motor.B, True)
        sleep(Motor.step_time)
        GPIO.output(Motor.A, False)
        GPIO.output(Motor.B, False)
        
    def Step7():
        GPIO.output(Motor.A, True)
        sleep(Motor.step_time)
        GPIO.output(Motor.A, False)
    def Step8():
        GPIO.output(Motor.D, True)
        GPIO.output(Motor.A, True)
        sleep(Motor.step_time)
        GPIO.output(Motor.D, False)
        GPIO.output(Motor.A, False)
        
    # Define the turn function
    def turn (steps):
        # Loop for the number of steps
        while (steps > 0):
        # Call the Step1() through Step8() functions from the Motor module
            Motor.Step1()
            Motor.Step2()
            Motor.Step3()
            Motor.Step4()
            Motor.Step5()
            Motor.Step6()
            Motor.Step7()
            Motor.Step8()
            
            # Decrement the steps counter
            steps -= 1





# Main function
    
# Print a message
print("Los gehts")
# Sleep for 1 second
sleep(1)
# Call the turn function with 2450 steps
Motor.turn(2450)
# Clean up the GPIO pins
GPIO.cleanup()
# Print a message
print("Finished")

