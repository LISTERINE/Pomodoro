from datetime import datetime, timedelta
from time import sleep
from functools import partial

class BaseTimer(object):
    """ Records current time and measures against time increments

    """

    def set_start_time(self):
        self.work_alarm = self.rest_alarm = datetime.now()
        self.alarm_ring_time = [self.rest_alarm, self.work_alarm]
        self.alarm_deltas = [None, None]

    def set_time(self, is_work=False, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        if not self.alarm_deltas[is_work]:
            self.alarm_deltas[is_work] = {"hours":hours,
                                         "minutes":minutes,
                                         "seconds":seconds}

        delta = self.alarm_deltas[is_work]
        self.alarm_ring_time[is_work] = datetime.now() + timedelta(**delta)

    def current_time(self):
        return datetime.now()


class PomTimer(BaseTimer):
    def __init__(self):
        self.set_start_time()
        self.set_work_time = partial(self.set_time, is_work=True)
        self.set_rest_time = partial(self.set_time, is_work=False)
        self.alarm_setters = [self.set_rest_time, self.set_work_time]


    def reset_alarm(self, next_alarm):
        self.alarm_setters[next_alarm](**self.alarm_deltas[next_alarm])



def alarm():
    print "time up!!!"


if __name__ == "__main__":

    timer = PomTimer()
    timer.set_work_time(minutes=30)
    timer.set_rest_time(minutes=5)

    counter = 1
    while 1:
        sleep(5)
        if timer.current_time() > timer.alarm_ring_time[counter%2]:
            alarm()
            counter += 1
            timer.reset_alarm(counter%2)
