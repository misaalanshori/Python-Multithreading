# creates multiple threads to say hello world using the _thread module
import _thread as thread
runThreads = 8
def threadPrint(thread, string):
    global runThreads
    print("Thread-{}: {}".format(thread, string))
    runThreads -= 1

for i in range(1,runThreads+1):
    thread.start_new_thread(threadPrint, (str(i), "Hello World"))

while True:
    if runThreads == 0:
        exit()
    pass