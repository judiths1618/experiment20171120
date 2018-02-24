#xiaorui.cc
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import time

task = []

class Producer(threading.Thread):
   def run(self):
       while True:
           if con.acquire():
               print "producer role ---------------------"
               if len(task) > 1000:
                   con.wait()
               else:
                   for i in range(100):
                       task.append(i)
                   msg = self.name+' produce 100, count=' + str(len(task))
                   print msg
                   con.notify()
                   time.sleep(1)
                   con.release()

class Consumer(threading.Thread):
   def run(self):
       while True:
           if con.acquire():
               print "consumer role"
               if len(task) < 100:
                   con.wait()
               else:
                   for i in range(10):
                       task.pop()
                   msg = self.name+' consume 3, count='+str(len(task))
                   print msg
                   con.notify()
                   time.sleep(2)
                   con.release()

con = threading.Condition()

def test():
    for i in range(2):
        p = Producer()
        p.start()
    for i in range(5):
        c = Consumer()
        c.start()
if __name__ == '__main__':
    test()
