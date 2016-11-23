from threading import Lock, Event
import thread
import time

class MyClass(object):

    def __init__(self):
        print "[Main] Init"
        self.number_list = []
        self.lock = Lock()
        self.threads_finished = Event()
        self.number_threads = 0
        self.number_threads_finished = 0
        self.counting_finished = False


    def first_call(self):
        print "[Main] First_call"
        for i in range(1, 10):
            thread.start_new_thread(self.thread_function, (i,))
            self.lock.acquire()
            self.number_threads += 1
            self.lock.release()

        self.wait_for_threads()
        print "[Main] Finished"
        print "[Main] {}".format(self.number_list)


    def wait_for_threads(self):
        self.lock.acquire()
        self.counting_finished = True
        if self.number_threads > self.number_threads_finished:
            self.lock.release()
            print "[Main] Waiting"
            self.threads_finished.wait()
            print "[Main] Free"
        else:
            print "[Main] No need for waiting"
            self.lock.release()


    def thread_function(self, n):
        self.lock.acquire()
        print "[Thread {}] Hello!".format(n)
        self.number_list.append(n)
        self.lock.release()

        self.lock.acquire()
        self.number_threads_finished += 1
        if self.counting_finished and self.number_threads == self.number_threads_finished:
            print "[Thread {}] Last one - Set event!".format(n)
            print "[Thread {}] Bye!".format(n)
            self.lock.release()
            self.threads_finished.set()
        else:
            print "[Thread {}] Bye!".format(n)
            self.lock.release()


mc = MyClass()
try:
    mc.first_call()
except:
    print "Error"

