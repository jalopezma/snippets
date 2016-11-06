from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from random import randint
from time import sleep
import threading

def threadFunc(worker, numWorkers):
    global finishedThreads
    global jobs
    sleepTime = randint(1, 10)
    print "[Worker {0}]\tSTARTS ({1})".format(worker, sleepTime)
    sleep(sleepTime)
    mutex.acquire()
    job = jobs.pop(0)
    mutex.release()

    sleepTime = randint(1, 2)
    sleep(sleepTime)
    print "[Worker {0}]\tDOING job {1}".format(worker, job)

    finishedMutex.acquire()
    finishedThreads = finishedThreads + 1
    print "[Worker {0}]\tFinished items(count me): {1}".format(worker, finishedThreads)
    if finishedThreads==numWorkers:
        print "[Worker {0}]\tAll finished. Send event".format(worker)
        event.set()
    finishedMutex.release()
    print "[Worker {0}]\tEXIT".format(worker)

finishedThreads = 0
jobs = range(1, 51)
worker = 0

mutex = threading.Lock()
finishedMutex = threading.Lock()
event = threading.Event()

scheduler = BackgroundScheduler()
scheduler.add_executor(ThreadPoolExecutor(max_workers=20))
scheduler.start()


for job in jobs:
    worker += 1
    scheduler.add_job(threadFunc, args=[worker, len(jobs)], max_instances=1000, misfire_grace_time=86400)

print "[Main]\t\tWait for event"
event.wait()
print "[Main]\t\tExit"
