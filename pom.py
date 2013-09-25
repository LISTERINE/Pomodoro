from datetime import datetime, timedelta
from time import sleep
from functools import partial
from argparse import ArgumentParser
from sys import exit


class BaseTimer(object):
    """ Records current time and measures against time increments

    """

    def set_start_time(self):
        self.work_alarm_time = self.rest_alarm_time = datetime.now()
        self.alarm_ring_time = [self.rest_alarm_time, self.work_alarm_time]
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

    def work_alarm(self):
        print "Work over!"

    def rest_alarm(self):
        print "Break over!"

    def reset_alarm(self, next_alarm):
        self.alarm_setters[next_alarm](**self.alarm_deltas[next_alarm])

    def start_timer(self):
        self.alarm_callbacks = [self.rest_alarm, self.work_alarm]
        alarm_counter = 1
        while 1:
            sleep(5)
            if self.current_time() > self.alarm_ring_time[alarm_counter%2]:
               self.alarm_callbacks[alarm_counter%2]()
               alarm_counter += 1
               self.reset_alarm(alarm_counter%2)


def parse_input_time(input_time, output_time):
    try:
        input_time = [int(i) for i in input_time.split(":")]
        return {"hours":input_time[0],
                "minutes":input_time[1],
                "seconds":input_time[2]}
    except:
        print "Input error"
        print "Usage:"
        print "pom.py --worktime=HH:MM:SS --breaktime=HH:MM:SS"
        exit(1)



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--worktime", dest="work_time", type=str)
    parser.add_argument("--breaktime", dest="rest_time", type=str)
    args = parser.parse_args()

    work_time = rest_time = datetime.now()
    work_time = parse_input_time(args.work_time, work_time)
    rest_time = parse_input_time(args.rest_time, rest_time)

    timer = PomTimer()
    timer.set_work_time(**work_time)
    timer.set_rest_time(**rest_time)
    timer.start_timer()
