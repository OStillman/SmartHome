#!/usr/bin/python3

import os, sys
import subprocess
import constants

from Hue import light_control as lights


class DoorWatcher:
    def __init__(self):
        self.procExe = subprocess.Popen("./receiver.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.runWatcher()

    def runWatcher(self):
        while self.procExe.poll() is None:
            line = self.procExe.stdout.readline()
            #print("Print:" + line)
            if constants.door_sensor in line:
                print("Door Open")
                lights.SimpleLightsToggle("group", constants.hallway_brightness, constants.hallway)
            elif line != "":
                print(line)


DoorWatcher()