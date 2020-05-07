import urllib.request as request
import urllib.parse as parse
import json
import threading
#import logging_setup as log

import constants

class SimpleLightsToggle:
    def __init__(self, type, id, on, brightness=None):
        self.type = type
        self.id = id
        self.brightness = brightness
        self.on = on
        self.setupURL()
        self.setupBody()
        self.runReq()
        #event = threading.Event()
        #thread = threading.Thread(target=self.threaded_off, args=(event, type, id, brightness))
        #thread.start()

    def setupURL(self):
        if self.type == "group":
            self.url = "http://192.168.0.12/api/%s/groups/%s/action"%(constants.username, self.id)
        elif self.type == "motion_sensor":
            self.url = "http://192.168.0.12/api/%s/sensors/%s/config"%(constants.username, self.id)

    def setupBody(self):        
        if self.type == "group" and self.id == constants.hallway:
            self.body = json.dumps({"on": self.on, "bri": self.brightness}).encode('utf-8')
        if self.type == "motion_sensor":
            self.body = json.dumps({"on": self.on}).encode('utf-8')

    def runReq(self):
        req = request.Request(url=self.url, data=self.body,method='PUT')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        request.urlopen(req)
        #print(request.urlopen(req).read().decode('utf-8'))
        #print(resp.read().decode('utf-8'))