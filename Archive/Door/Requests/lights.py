import urllib.request as request
import urllib.parse as parse
import constants
import json

from Requests import living_room

class HallwayToggle():

    def __init__(self, onoff):
        self.onoff = onoff
        self.sendRequest()

    def sendRequest(self):
        url = "http://192.168.0.12/api/%s/groups/%s/action"%(constants.username, constants.group)
        #print(url)
        body = json.dumps({"on": self.onoff}).encode('utf-8')
        req = request.Request(url=url, data=body,method='PUT')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        resp = request.urlopen(req)
        #print(resp.read().decode('utf-8'))

class LivingRoomAlert():

    def __init__(self, open):
        if open:
            constants.lroom_on_before = self.checkLight()
            self.startAlert()
        else:
            if constants.lroom_on_before:
                self.stopAlert(True)
            else:
                self.stopAlert(False)

    def startAlert(self):
        url = "http://192.168.0.12/api/%s/groups/%s/action"%(constants.username, constants.living_room)
        #print(url)
        body = json.dumps(
            {"on": True, "bri": 122, "hue": 4209,"sat": 117, "xy": [0.6424,0.2844],"ct": 410,"alert": "select"}
            ).encode('utf-8')
        req = request.Request(url=url, data=body,method='PUT')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        resp = request.urlopen(req)

    def checkLight(self):
        url = "http://192.168.0.12/api/%s/groups/%s"%(constants.username, constants.living_room)
        #print(url)
        body = json.dumps(
            {"on": True, "bri": 122, "hue": 4209,"sat": 117, "xy": [0.6424,0.2844],"ct": 410,"alert": "select"}
            ).encode('utf-8')
        req = request.Request(url=url, data=body,method='GET')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        resp = request.urlopen(req)
        result = living_room.living_room_from_dict(json.loads(resp.read().decode('utf-8')))
        return(result.state.all_on)
    
    def stopAlert(self, on):
        url = "http://192.168.0.12/api/%s/groups/%s/action"%(constants.username, constants.living_room)
        #print(url)
        body = json.dumps(
            {"on": on, "bri": 122,"hue": 4209,"sat": 117,"effect": "none","xy": [0.4842,0.3749],"ct": 410}
            ).encode('utf-8')
        req = request.Request(url=url, data=body,method='PUT')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        resp = request.urlopen(req)