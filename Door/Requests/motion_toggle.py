import urllib.request as request
import constants
import json

class Motion_Toggle():

    def __init__(self, onoff):
        self.onoff = onoff
        self.sendRequest()

    def sendRequest(self):
        url = "http://192.168.0.12/api/%s/sensors/%s/config"%(constants.username, constants.motion_sensor_id)
        #print(url)
        body = json.dumps({"on": self.onoff}).encode('utf-8')
        req = request.Request(url=url, data=body,method='PUT')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        resp = request.urlopen(req)