#prints the current time sourced from a web api, time gets updated instantly and the time is printed every 0.25 seconds with different thread
import threading
import requests
import json
import time
import sys
timedata = ""
info = "Loading..."
die = False
seconds = 0.0

def getTime():
    global timedata, info, seconds
    while True:
        if die:
            break
        try:
            req = requests.get("http://worldtimeapi.org/api/timezone/Asia/Jakarta")
            info = "Last Update Succeeded"
            seconds = 0.0
        except:
            info = "Last Update Failed"
            return
        timeJson = json.loads(req.text)
        timeStr = timeJson["datetime"] + " " + timeJson["abbreviation"]
        timedata = timeStr

def printTime():
    global seconds
    while True:
        if die:
            break
        seconds += 0.25
        sys.stdout.write("\rThe current time is: " + timedata + "({}, {} Seconds ago)".format(info, seconds) + "   ")
        sys.stdout.flush()
        time.sleep(0.25)


try:
    timeSync = threading.Thread(target=getTime)
    timePrint = threading.Thread(target=printTime)
    timeSync.start()
    timePrint.start()
    while timePrint.is_alive(): 
        timePrint.join(1)  # not sure if there is an appreciable cost to this.
except (KeyboardInterrupt, SystemExit):
    die = True
    print('\n! Received keyboard interrupt, quitting threads.\n')
    sys.exit()