import traffic
import microbit
import datetime
import constants
import time as sleep_count

# Call traffic, get API, compare base time with traffic time send to Microbit


class Operation():
    
    def __init__(self):
        self.delay_time = 300
        while True:
            weekday_day = self.getDay()
            time = self.getTime()
            if weekday_day <=5:
                print("It's a weekday")
                print(time)
                if (time > constants.time_start and time < constants.time_end):
                    self.startTraffic()
                else:
                    print("Outside the time")
                    self.outsideTime(weekday_day, time)
                # If weekday, get the time
                # If not between 7 & 7:55, work out seconds until and sleep for that amount
                # If is in golden time, fetch traffic every 5 minutes
            else:
                # Weekend doesn't need looping, work out seconds untill first loop needed and sleep till then
                print("Weekend") 
                self.outsideTime(weekday_day, time)
            sleep_count.sleep(self.delay_time)    

    def getDay(self):
        todays_date = datetime.date.today()
        weekday_day = datetime.date.weekday(todays_date) + 1
        return weekday_day

    def getTime(self):
        return datetime.datetime.now().time()

    def outsideTime(self, day, time):
        # If day = 1 - 4, check time and 12 hours - can it be done?
        # If yes - pause for 12
        # N0 = pause for 10 
        #microbit.MicrobitControl().blank()
        #self.delay_time = 300
        if day == 6:
            print ("It's Saturday")
            if time < constants.time_start:
                print("Delaying for 48 hours")
                self.delay_time = 172800
            else:
                print("Can't do 48, 24 instead")
                self.delay_time = 86400
        elif day == 7:
            print("It's Sunday")
            self.delay_time = 600
        else:
            print("Weekeday")
            self.delay_time = 600

    def startTraffic(self):
        print("Between the time")
        #microbit.MicrobitControl().download()
        self.getTraffic()
        self.delay_time = 300
        
    def getTraffic(self):
        traffic_time = str(traffic.Traffic())
        traffic_time = float(traffic_time)
        if traffic_time <= 4.3:
            #print(str(traffic_time))
            print("NO TRAFFIC") #0 - 4 minutes
            microbit.MicrobitControl().noTraffic()
        elif traffic_time <= 9.3:
            print("Traffic Building") #5 - 9 minutes
            microbit.MicrobitControl().trafficBuilding()
        elif traffic_time <= 14.3:
            print("Traffic Pretty Bad") #10 - 14 minutes
            microbit.MicrobitControl().trafficBad()
        elif traffic_time <= 19.3:
            print ("Traffic Awful") #15 - 19Minutes
            microbit.MicrobitControl().trafficAwful()
        elif traffic_time > 19.3:
            print ("Traffic Really Very Awful") #20+ minutes
            microbit.MicrobitControl().worstTraffic()

Operation()
