#!/usr/bin/env python
import time
def changedate(data="2018-1-11 08:08:08"):
    a = data
    timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

if __name__ == '__main__':
    print changedate()
