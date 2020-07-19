from sys import platform
import subprocess
import re
avgCount = "2"
if platform == "linux" or platform == "darwin":
    command=["ping", "-c", avgCount] 
else:
    command=["ping", "-n", avgCount]

def ping(host, rto = 10):
    rto = rto
    cmd = command.copy()
    cmd.append(host)
    print(cmd)
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

print(ping("google.com"))