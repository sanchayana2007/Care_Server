#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    For All time conversion
'''

import time
from datetime import datetime as dtime


#return the date in numbers 
def timeStamp(Currendate):
    
    return time.mktime(dtime.strptime(Currendate, "%d/%m/%Y").timetuple())


def timeNowcurrentdate():
    
    return time.mktime(dtime.today().timetuple())


# return current timestamp in nanoeconds
def timeNow():
    
    return int(time.time() * 1000 * 1000)

class TimeUtil:

    @staticmethod
    def getSystemTimeInMilliseconds():
        dt = dtime.now()
        hh = int(dt.strftime('%H')) * 60 * 60
        mm = int(dt.strftime('%M')) * 60
        ss = int(dt.strftime('%S'))
        ms = int(dt.strftime('%f')[:-3])
        return int(hh + mm + ss) * 1000 + ms

    @staticmethod
    def getDayOfThisWeek():
        return int(dtime.now().strftime('%w'))

    @staticmethod
    def getDayOfThisWeekFromTimestamp(tmp):
        return int(datetime.datetime.fromtimestamp(tmp).strftime('%w'))


