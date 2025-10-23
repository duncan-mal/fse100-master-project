import pyttsx3
import time
import sys
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

thermprobe = W1ThermSensor()

GPIO.setmode(GPIO.BCM)

tts = pyttsx3.init()
tts.setProperty('rate', 150)

americanoMode = False   # Bool for temp mode
global vibeNum  # number of times vibration motor has ran
global vibeTimer # timer for vibration motor


def ultrasonicreading():
    #constant placeholder
    distance = 15
    closeEnough = False

    while(not closeEnough):
        #keep reading until close enough
        if(distance <25):
            closeEnough = True

    return closeEnough
    #go to read temp

def read_temp():
    #Read Celsius temp from sensor (atm just using constant for testing)
    temp_reading = thermprobe.get_temperature()

    #reset vibration timer
    vibeTimer = 0

    #checking bounds for temp
    if temp_reading < -10 or temp_reading > 120:
        tts.say(" Temp out of range")
        return

    #Determing if reading should be Fahrenheit or Celsius
    if americanoMode:
        temp_reading = (temp_reading * (9/5)) +32
        print(temp_reading)
        tts.say(str(temp_reading)+ " degrees fahrenheit")
    else:
        print(temp_reading)
        tts.say( str(temp_reading)+ " degrees celsius")

    #Run TTS engine and wait to prevent attempt at talking over its self
    tts.runAndWait()
    time.sleep(4)

def vibrate():
    print("Vibrating Motor")
    vibeNum += 1
    vibeTimer = 0
    if vibeNum >= 3:
        #exit code
        sys.exit(0)


def main():
    vibeNum = 0
    vibeTimer = 0
    #Intial make aware that device is on
    time.sleep(1)
    tts.say("Hello")
    tts.runAndWait()

    while True:
        #Reading from ultrasonic sensor (constant for testing)
        if ultrasonicreading():
            read_temp()
        else:
            time.sleep(1)
            vibeTimer += 1
            if vibeTimer >= 60:
                vibrate()
main()
