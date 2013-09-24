from datetime import datetime, timedelta
from time import sleep
from functools import partial

class BaseTimer(object):
    """ Records current time and measures against time increments

    """     
    def set_start_time(self):
        self.start_time = datetime.now()
        self.work_alarm = self.rest_alarm = self.start_time
        self.alarms = [self.rest_alarm, self.work_alarm]

    def set_time(self, is_work=False, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

        self.alarms[is_work] = self.start_time + timedelta(hours=hours,
                                                           minutes=minutes,
                                                           seconds=seconds)
    def time_now(self):
        return datetime.now()
        
    
class PomTimer(BaseTimer):
    def __init__(self):
        self.set_start_time()
        self.set_work_time = partial(self.set_time, is_work=True)
        self.set_rest_time = partial(self.set_time, is_work=False)
    
  
def alarm():
    print "time up!!!"


if __name__ == "__main__":
    
    timer = PomTimer()
    timer.set_work_time(minutes=1)
    timer.set_rest_time(minutes=5)

    counter = 1
    while 1:
        sleep(5)
        if timer.time_now() > timer.alarms[counter%2]:
            alarm()
            counter += 1
