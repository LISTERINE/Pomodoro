from datetime import datetime, timedelta
from time import sleep
from functools import partial

class BaseTimer(object):
    """ Records current time and measures against time increments

    """

    def set_start_time(self):
        self.work_alarm = self.rest_alarm = datetime.now()
        self.alarms = [self.rest_alarm, self.work_alarm]
        self.alarm_times = [None, None]

    def set_time(self, is_work=False, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        if not self.alarm_times[is_work]:
            self.alarm_times[is_work] = {"hours":hours,
                                         "minutes":minutes,
                                         "seconds":seconds}

        delta = self.alarm_times[is_work]
        self.alarms[is_work] = datetime.now() + timedelta(**delta)

    def current_time(self):
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
    timer.set_rest_time(minutes=2)

    counter = 1
    while 1:
        sleep(5)
        if timer.current_time() > timer.alarms[counter%2]:
            alarm()
            counter += 1
