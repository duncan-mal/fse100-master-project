import pyttsx3
import time
import sys
import RPi.GPIO as GPIO
from w1thermsensor import W1ThermSensor

thermprobe = W1ThermSensor()

GPIO.setmode(GPIO.BCM)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.IN)
GPIO.setup(6, GPIO.IN)
GPIO.setup(22, GPIO.OUT)

tts = pyttsx3.init()
tts.setProperty('rate', 150)

americanoMode = False   # Bool for temp mode
vibeNum = 0  # number of times vibration motor has ran
vibeTimer = 0 # timer for vibration motor

def shutdown():
    tts.say("Ok, Goodbye")
    tts.runAndWait()
    sys.exit(0)

def changetempmeasurment():
    global americanoMode
    tts.say("I, Changing Temperature Measurments")
    print("Changing Temperature Measurment")
    if americanoMode:
        americanoMode = False
    else:
        americanoMode = True
    tts.runAndWait()
    powerofftimer = 0
    while GPIO.input(6) == 1:
        if powerofftimer >= 50:
            shutdown()
        else:
            powerofftimer +=1
def distance():
	GPIO.output(17, 0)
	time.sleep(0.000002)

	GPIO.output(17, 1)
	time.sleep(0.00001)
	GPIO.output(17, 0)

	
	while GPIO.input(18) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(18) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def ultrasonicreading():
    #constant placeholder
    closeEnough = False
    distancenum = round(distance(), 2) 
    print(str(distancenum)+"cm")
    if(distancenum <25):
        closeEnough = True
        return closeEnough
    else:
        return closeEnough
    #go to read temp

def read_temp():
    global vibeTimer
    global vibeNum
    global americanoMode
    #Read Celsius temp from sensor (atm just using constant for testing)
    temp_reading = round(thermprobe.get_temperature())
    #reset vibration timer
    vibeTimer = 0
    vibeNum = 0

    #checking bounds for temp
    if temp_reading < -10 or temp_reading > 120:
        tts.say("Temp out of range")
        return

    #Determing if reading should be Fahrenheit or Celsius
    if americanoMode:
        temp_reading = (temp_reading * (9/5)) +32
        temp_reading = round(temp_reading)
        print(str(temp_reading)+"f")
        tts.say("Its " + str(temp_reading)+ " degrees fahrenheit")
    else:
        print(str(temp_reading)+"C")
        tts.say("Its " + str(temp_reading)+ " degrees celsius")

    #Run TTS engine and wait to prevent attempt at talking over its self
    tts.runAndWait()
    time.sleep(1)

def vibrate():
    global vibeNum
    global vibeTimer
    print("Vibrating Motor")
    print("Vibe Number: " + str(vibeNum + 1))
    for _ in range(3):
        GPIO.output(22, 1)
        time.sleep(0.5)
        GPIO.output(22, 0)
        time.sleep(0.5)
    vibeNum += 1
    vibeTimer = 0
    if vibeNum > 3:
        print("Killing Due To Inactivity")
        #exit code
        shutdown()


def main():
    global vibeTimer
    #Intial make aware that device is on
    time.sleep(1)
    tts.say("Hello")
    tts.runAndWait()

    while True:
        if GPIO.input(6) == 1:
            changetempmeasurment()
        #Reading from ultrasonic sensor (constant for testing)
        if ultrasonicreading():
            read_temp()
        else:
            time.sleep(1)
            vibeTimer += 1
            print("Vibe Timer: "+str(vibeTimer))
            if vibeTimer >= 20:
                vibrate()
main()
