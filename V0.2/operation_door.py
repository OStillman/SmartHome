from Requests import lights
from Requests import motion_request
from Requests import motion_toggle
import RPi.GPIO as GPIO
import time
import datetime as dt

import threading

# lights.HallwayToggle(False)


class Operation:

    def __init__(self):
        # self.doorOpen()
        time.sleep(60)
        self.trackDoor()

    def trackDoor(self):
        GPIO.setmode(GPIO.BCM)
	
	    # Was 18
        DOOR_SENSOR_PIN = 16

        isOpen = None
        oldIsOpen = None

        GPIO.setup(DOOR_SENSOR_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        while True: 
            oldIsOpen = isOpen 
            isOpen = GPIO.input(DOOR_SENSOR_PIN)
            if (isOpen and (isOpen != oldIsOpen)):  
                #Is now open
                self.doorOpen()
            elif (isOpen != oldIsOpen and oldIsOpen != None):  
                self.doorClose()
            time.sleep(0.1)

    def doorOpen(self):
        self.open_time = dt.datetime.now()
        print ("[Info]: " + str(self.open_time))
        print ("Door Open")
        motion_toggle.Motion_Toggle(False)
        lights.HallwayToggle(True)
        print("Lights on")
        lights.LivingRoomAlert(True)
        time.sleep(1)

    #def doorStillOpen(self):
    #    print("Door Still Open")
    #    self.open_time = dt.datetime.now()
    #    lights.HallwayToggle(True)
    #    time.sleep(5)
    
    def doorClose(self):
        print("Door Closed")
        motion_toggle.Motion_Toggle(True)
        lights.LivingRoomAlert(False)


# Operation()
job_thread = threading.Thread(target=Operation)
job_thread.start()


# _thread.start_new_thread(Operation, ())
