#!/usr/bin/python3

import os, sys
import subprocess


class DoorWatcher:
    def __init__(self):
        self.procExe = subprocess.Popen("./receiver.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        self.runWatcher()

    def runWatcher(self):
        while self.procExe.poll() is None:
            line = self.procExe.stdout.readline()
            #print("Print:" + line)
            if "12062824" in line:
                print("Door Open")
            elif line != "":
                print(line)


DoorWatcher()