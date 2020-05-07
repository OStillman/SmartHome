import urllib.request as request
import json
import constants
from Requests import motionsensor

class Motion_Request():

    def __init__(self):
        motion_data = self.getData()
        self.motion_time = self.parseData(motion_data)

    def __str__(self):
        return str(self.motion_time)


    def getData(self):
        url = "http://192.168.0.12/api/%s/sensors/%s"%(constants.username, constants.motion_sensor_id)
        return request.urlopen(url)

    def parseData(self, data):
        result = data.read().decode('utf-8')
        result = motionsensor.motion_sensor_from_dict(json.loads(result))
        last_motion = result.state.lastupdated
        return last_motion