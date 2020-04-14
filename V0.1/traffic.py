#!/usr/bin/env python3
import urllib.request as request
import json
from Requests import traffic_data
import constants

# Fetch Traffic data, Pull out Base and Traffic Time, Work out Difference

class Traffic():
    
    def __init__(self):
        raw_data = self.pullData()
        traffic_times = self.sortData(raw_data)
        self.difference_time = self.difference(traffic_times)

    def __str__(self):
        return str(self.difference_time)

    def pullData(self):
        url = "https://route.ls.hereapi.com/routing/7.2/calculateroute.json?" \
            "apiKey={}" \
            "&waypoint0={}&waypoint1={}" \
            "&mode=fastest;car;traffic:disabled;&feature=tollroad:-3;".format(constants.API_KEY, constants.start, constants.stop) 
        return request.urlopen(url)

    def sortData(self, data):
        result = data.read().decode('utf-8')
        result = traffic_data.traffic_from_dict(json.loads(result))
        base_time = result.response.route[0].summary.base_time
        traffic_time = result.response.route[0].summary.base_time
        print("Base time: " + str(base_time / 60))
        print("Traffic Time: " + str(traffic_time / 60))
        return [base_time, traffic_time]

    def difference(self, times):
        base_time = int(times[0])
        traffic_time = int(times[1])
        difference_time = (traffic_time - base_time) / 60
        print("Traffic Adds: " + str(difference_time))
        return difference_time
        

