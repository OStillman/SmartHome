#!/usr/bin/python3

import os, sys
import subprocess
import constants
import threading
import time
import requests
import json

from Hue import light_control as lights


class DoorWatcher:
    def __init__(self):
        self.doorOpen = False
        if constants.__DevMode__:
            self.DevMode()
        else:
            self.procExe = subprocess.Popen("./receiver.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            self.runWatcher()

    def runWatcher(self):
        while self.procExe.poll() is None:
            line = self.procExe.stdout.readline()
            #print("Print:" + line)
            if constants.door_sensor_open in line:
                if not self.doorOpen:
                    self.DoorOpened()
                #lights.SimpleLightsToggle("group", constants.hallway_brightness, constants.hallway, True)
            elif constants.door_sensor_close in line:
                if self.doorOpen:
                    self.DoorClosed()                    
            elif line != "":
                print(line)

    def DevMode(self):
        print("Devmode on")
        time.sleep(2)
        self.DoorOpened()
        time.sleep(2)
        self.DoorClosed()


    def DoorOpened(self):
        print("Door Open")
        self.doorOpen = True
        payload = {"Sensor": "Front_Door", "Status": "Open"}
        open_thread = threading.Thread(target=self.sendRequest, args=(payload,))
        open_thread.start()
        '''
        self.doorOpen = True
        on_thread = threading.Thread(target=lights.SimpleLightsToggle, args=("group", constants.hallway, True, constants.hallway_brightness))
        off_motion_thread = threading.Thread(target=lights.SimpleLightsToggle, args=("motion_sensor", constants.motion_sensor_id, False))
        on_thread.start()
        off_motion_thread.start()
        '''

    def DoorClosed(self):
        print("Door Closed")
        self.doorOpen = False
        payload = {"Sensor": "Front_Door", "Status": "Closed"}
        close_thread = threading.Thread(target=self.sendRequest, args=(payload,))
        close_thread.start()
        '''
        self.doorOpen = False
        off_thread = threading.Thread(target=lights.SimpleLightsToggle, args=("motion_sensor", constants.motion_sensor_id, True))
        off_thread.start()
        '''

    def sendRequest(self, payload):
        if constants.__DevMode__:
            requests.post("http://raspberrypi.local:5000/door", data=json.dumps(payload))
        else:
            requests.post("http://raspberrypi.local/door", data=json.dumps(payload))

DoorWatcher()