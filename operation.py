#!/usr/bin/python3

import os, sys
import subprocess
import constants
import threading

from Hue import light_control as lights


class DoorWatcher:
    def __init__(self):
        self.procExe = subprocess.Popen("./receiver.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.runWatcher()

    def runWatcher(self):
        doorOpen = False
        while self.procExe.poll() is None:
            line = self.procExe.stdout.readline()
            #print("Print:" + line)
            if constants.door_sensor_open in line:
                if not doorOpen:
                    print("Door Open")
                    doorOpen = True
                    on_thread = threading.Thread(target=lights.SimpleLightsToggle, args=("group", constants.hallway, True, constants.hallway_brightness))
                    off_motion_thread = threading.Thread(target=lights.SimpleLightsToggle, args=("motion_sensor", constants.motion_sensor_id, False))
                    on_thread.start()
                    off_motion_thread.start()
                #lights.SimpleLightsToggle("group", constants.hallway_brightness, constants.hallway, True)
            elif constants.door_sensor_close in line:
                if doorOpen:
                    print("Door Closed")
                    doorOpen = False
                    off_thread = threading.Thread(target=lights.SimpleLightsToggle, args=("motion_sensor", constants.motion_sensor_id, True))
                    off_thread.start()
            elif line != "":
                print(line)


DoorWatcher()