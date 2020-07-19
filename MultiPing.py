import threading
import os
import time
import sys
from sys import platform
import subprocess
import re

# if os.geteuid() != 0:
#     print("This script requires root privileges")
#     exit()

hosts = ["8.8.8.8", "1.1.1.1", "twitter.com", "instagram.com"]

timedata = ""
info = ""
die = False
results = {}
resAvg = {}
threadList = {}
avgCount = "2"


if platform == "linux" or platform == "darwin":
    command=["ping", "-c", avgCount] 
else:
    command=["ping", "-n", avgCount]

def ping(host, rto = 4):
    rto = rto
    cmd = command.copy()
    cmd.append(host)
    # print(cmd)
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        [out, err]=proc.communicate(timeout=rto)
        if proc.returncode == 0:
            if platform == "linux" or platform == "darwin":
                # rtt min/avg/max/mdev = 578.263/917.875/1013.707/132.095 ms
                avgRTT=re.search("rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)", str(out))
                return [avgRTT.group(2),avgRTT.group(1),avgRTT.group(3)]
            else:
                # Approximate round trip times in milli-seconds: Minimum = 63ms, Maximum = 64ms, Average = 63ms
                avgRTT=re.search("Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)", str(out))
                return [avgRTT.group(3),avgRTT.group(1),avgRTT.group(2)]
    except subprocess.TimeoutExpired:
        rtod = str(rto*1000)
        return [rtod, rtod, rtod]



def getResponseTime(host):
    global results, avg
    # if host not in results:
    results[host] = []
    resAvg[host] = []
    # print("ping {} started".format(host))
    while not die:
        try:
            pres = ping(host)
            results[host].append(pres)
            resAvg[host].append(pres[0])
            # print("ping {} success".format(host))
        except:
            # print("ping {} fail".format(host))
            continue

def printResult():
    global results
    print("Waiting for results...", end="\r")
    time.sleep(5)
    print(" "*30, end="\r")
    print("\n===================")
    maxLength = len(max(hosts, key=len)) + 1
    while not die:
        print(results)
        print(resAvg)
        # try:
        print("Address".rjust(maxLength) + "|" + "Min".rjust(8) + "|" +"Max".rjust(8) + "|" + "Avg".rjust(8) + "|" + "fullAvg".rjust(8))
        for i in results:
            print("|{}|{}ms|{}ms|{}ms|{}ms".format(i.rjust(maxLength), results[i][-1][1].rjust(8), results[i][-1][2].rjust(8), results[i][-1][0].rjust(8), str(round(sum(resAvg[i])/len(resAvg[i]), 2)).rjust(8)))
        print("\n===================")
        # except:
        #     print("Waiting for results...", end="\r")
        time.sleep(0.5)

try:
    for i in hosts:
        threadList[i] = threading.Thread(target=getResponseTime, args=(i,))
        threadList[i].start()
    resultPrinter = threading.Thread(target=printResult)
    resultPrinter.start()
    while resultPrinter.isAlive(): 
        resultPrinter.join(1)  # not sure if there is an appreciable cost to this.
except (KeyboardInterrupt, SystemExit):
    die = True
    print('\n! Received keyboard interrupt, quitting threads.\n')
    sys.exit()