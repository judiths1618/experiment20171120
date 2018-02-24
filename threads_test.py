from time import ctime, sleep
from threading import Thread, Condition
import threading,logging
import random
import datetime


task_stage1 = [23,16,39,88]
task_stage2 = [21,10,29,36]
#mapp = {'vm2': {'t3': 1.256}, 'vm3': {'t2': 2.1}, 'vm1': {'t1': 0.635}}

logging.basicConfig(
        level = logging.DEBUG,
        format = '[%(levelname)s] (%(threadName)-10s) %(message)s',
        )

class VM(Thread):
    def __init__(self, cond, index, mapp):
        super(VM, self).__init__()
        self.index = index
        self.cond = cond
        self.item = item

    def run(self):
        self.cond.acquire() #a
        print threading.currentThread().getName(), " VM %s is waiting! " %self.name
        self.cond.wait() #c
        
        print threading.currentThread().getName(), " %s executing. start at %s-" %(self.mapp, datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S.%f'))
        self.cond.notify()
        for i
        sleep(self.item)

        cond.release()
        print threading.currentThread().getName(), " %s finished. end at %s" %(self.mapp, datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S.%f'))
                
class Assignment(Thread):
    def __init__(self, index, cond, mapp):
        super(Assignment, self).__init__()
        self.index = index
        self.cond = cond
        self.mapp = mapp

    def run(self):
        sleep(1) #make sure that assignment is firstly executed

        self.cond.acquire()
        print "the assignment of task mapping is ready......"
        self.cond.notify()
        print "Mapping %s" %self.mapp
        for i in range(len(self.mapp)):
            item = mapp[mapp.keys()[i]][mapp[mapp.keys()[i]].keys()[0]]
            print item 
        self.cond.wait()

        print "Are your finished?"
        self.cond.notify()

        self.cond.release()

        print "Start to the next stage..."

def task2threads(task):
    threads = []
    for i in range(len(mapp)):
        threads.append(threading.Thread(target=VM,args=(i,)))
    return threads


mapp = {'vm2': {'t3': 1.256}, 'vm3': {'t2': 2.1}, 'vm1': {'t1': 0.635}}
cond = Condition()
# main func
if __name__== '__main__':
    Assignment(0, cond, mapp).start()
    for i in range(len(mapp)):
        item = mapp[mapp.keys()[i]][mapp[mapp.keys()[i]].keys()[0]]
        VM(i,cond,item).start()
    print "all over %s" %ctime()

