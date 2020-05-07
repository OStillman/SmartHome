import traffic
import datetime
import time
import constants
import time as sleep_count
import schedule
import json

from Requests import info_in

# Get Current day - Daily at 2am
# Read file for time to alarm, traffic etc.

def setTrafficTask():
        #TODO: When should the traffic task begin?
        SetTrafficTask()


def controlTrafficTask(traffic_length):
        now = datetime.datetime.now()
        print("Traffic Ran @ " + str(now))
        end_time = time.time() + 60 * traffic_length
        while time.time() < end_time:
            FetchTrafficTask()
            time.sleep(150)
        return schedule.CancelJob


class SetTrafficTask:

    def __init__(self):
        day_num = self.get_day()
        day_data = self.get_data(day_num)
        #TODO: Set run traffic start time, with x minutes "run for" variable
        # Pull out: Traffic Needed? Traffic_Time, Traffic_Length
        if self.traffic_required(day_data):
            print("Traffic Required")
            traffic_time = self.getTrafficTime(day_data)
            traffic_length = self.getTrafficLength(day_data)
            self.setTrafficTaskSchedule(traffic_time, traffic_length)

    def setTrafficTaskSchedule(self, traffic_start, traffic_length):
        schedule.every().day.at(traffic_start).do(controlTrafficTask, traffic_length=traffic_length)

    def get_day(self):
        today = datetime.date.today()
        return datetime.date.weekday(today)

    def get_data(self, day_num):
        data = self.get_file()
        data = data.days.day[day_num]
        print(data)
        return data

    def get_file(self):
        result = None
        with open('info.json') as f:
            result = info_in.info_from_dict(json.loads(f.read()))
        # print(result.days.day[0].alarm_time)
        return result

    def traffic_required(self, day_data):
        traffic_required = day_data.traffic_needed
        return traffic_required

    def getTrafficTime(self, day_data):
        time_required = day_data.traffic_time
        return time_required

    def getTrafficLength(self, day_data):
        traffic_length = day_data.traffic_length
        return traffic_length


class FetchTrafficTask():
    def __init__(self):
        traffic_time = self.getTraffic()
        #print(traffic_time)
        self.OutputTraffic(traffic_time)

    def getTraffic(self):
        return traffic.Traffic()

    def OutputTraffic(self, traffic_time):
        #TODO: Add light changes
        traffic_time = float(str(traffic_time))
        if traffic_time <= 4.3:
            #print(str(traffic_time))
            print("NO TRAFFIC") #0 - 4 minutes
        elif traffic_time <= 9.3:
            print("Traffic Building") #5 - 9 minutes
        elif traffic_time <= 14.3:
            print("Traffic Pretty Bad") #10 - 14 minutes
        elif traffic_time <= 19.3:
            print ("Traffic Awful") #15 - 19Minutes
        elif traffic_time > 19.3:
            print ("Traffic Really Very Awful") #20+ minutes

#setTrafficTask()
#FetchTrafficTask()

schedule.every().day.at("02:00").do(setTrafficTask)


while True:
    schedule.run_pending()
    sleep_count.sleep(1)
