import threading
import Queue
import time
import datetime

class worker(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue
        self.thread_stop=False
 
    def run(self):
        while not self.thread_stop:
            print("vm number%d %s: waiting for task" %(self.ident,self.name))
            try:
                task=q.get(block=True, timeout=20)
            except Queue.Empty:
                print("Nothing to do! No task!")
                self.thread_stop=True
                break
    
        print("task recv: %s, task No: %d" % (task[0],task[1]))
        print("I am doing task!")
        print "my task time is %s. start at %s" %(task[0], datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S.%f'))
        time.sleep(task[0])
        print "my task time is %s. end at %s" %(task[0], datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S.%f'))

        q.task_done()
        res=q.qsize()
        if res>0:
            print("fuck!There are still %d tasks to do" % (res))

    def stop(self):
        self.thread_stop = True
 
if __name__ == "__main__":
 q=Queue.Queue(3)
 worker=worker(q)
 worker.start()
 q.put([23,1], block=True, timeout=None)
 q.put([16,2], block=True, timeout=None)
 q.put([39,3], block=True, timeout=None)
 q.put([88,4], block=True, timeout=None)
 q.put([21,5], block=True, timeout=None)
 print("***************leader:wait for finish!")
 q.join()
 print("***************leader:all task finished!")
