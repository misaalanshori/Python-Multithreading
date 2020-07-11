import threading
import requests
import json
import time
import sys
timedata = ""
info = ""
die = False
def getTime():
    global timedata, info
    while True:
        if die:
            break
        try:
            req = requests.get("http://worldtimeapi.org/api/timezone/Asia/Jakarta")
            info = "Last Update Succeeded"
        except:
            info = "Last Update Failed"
            return
        timeJson = json.loads(req.text)
        timeStr = timeJson["datetime"] + " " + timeJson["abbreviation"]
        timedata = timeStr
        time.sleep(1)

def printTime():
    while True:
        if die:
            break
        print("The current time is: " + timedata + "({})".format(info))
        time.sleep(0.25)

# timeSync = threading.Thread(target=getTime)
# timePrint = threading.Thread(target=printTime)
# timeSync.start()
# timePrint.start()
# timeSync.join()

try:
    timeSync = threading.Thread(target=getTime)
    timePrint = threading.Thread(target=printTime)
    timeSync.start()
    timePrint.start()
    while timePrint.isAlive(): 
        timePrint.join(1)  # not sure if there is an appreciable cost to this.
except (KeyboardInterrupt, SystemExit):
    die = True
    print('\n! Received keyboard interrupt, quitting threads.\n')
    sys.exit()