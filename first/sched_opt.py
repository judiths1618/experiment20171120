#coding=utf-8
from threading import Thread, Condition, currentThread, enumerate
from time import ctime, sleep
import random
import threading,time
from queue import Queue
import datetime as dt
import data as t
import threads_kill as k
''' function: 实现基于生产者－消费者模式的实时调度方案
    @Parameters: Assq, Vq, cond
     Assq: 部署方案，全局的变量，共享队列
     Vq: 线程模拟的VM，全局变量，共享队列
     cond: 条件变量（区别于锁）机制
    @return: real-time scheduler
note:
    Producer:　部署方案入队Assq
    Consumer:　获取Assq中的iterm，匹配Vq的name，模拟部署，生成timestamp
'''

class Producer(Thread):
    def __init__(self, Ass, Assq):
        super(Producer, self).__init__()
        self.Ass = Ass
        self.Assq = Assq
    def run(self):
        if not self.Assq.full():
            print('入队...')
            self.Assq.put(self.Ass)
        else:
            print('队列Assq已满 %s' %self.Assq.qsize())

class Consumer(Thread):
    def __init__(self, index, Assq, flag):
        super(Consumer,self).__init__()
        self.index = index
        self.Assq = Assq
        self.flag = flag
    def run(self):
        if self.Assq.empty():
            print("当前Assq队列中的数量为%s" %Assq.qsize())
        else:
            while True:
                if self.flag == 0:
                    ass = self.Assq.get()
                    for item in ass.items():
                        f = open('res.txt','a')
                        self.setName(item[0])
                        t_setup = time.time()
                        sleep(item[1][list(item[1])[0]])
                        t_cutting = time.time()
                        print(currentThread().getName(),'虚拟机 %s 任务%s 完成' %(item[0],list(item[1])[0]))
                        f.write(str(item[0]+'\t'+str(item[1].keys())+'\t'+str(t_setup)+'\t'+str(t_cutting)+'\n'))
                        self.flag = 1
#                self.Assq.task_done()
                        f.close()

if __name__ == '__main__':
    Tn = [11,12,13,14,15,16,17,18,21,22,23,24,25,26,31,32,33,34,35,36,
            37,38,39,41,42,43,44,45,46,51,52,53,54,55,56,57,58]
    Vn = [11,12,13,14,15,16,21,22,23,24,25,26,31,32,33,34,35,36]
    loop_stage = 6 
    
    Assq = Queue(maxsize = 10)
    cond = Condition()
    flag = 0

    CurThreadsName = [] #获取线程名称
    while True:
        V,Vx = t.RandT('v', Vn, 1,6)
        curT,Tx = t.RandT('t', Tn, 0,6)
        if not (len(Tx) ==0 & len(V) ==0):
            print(V, curT)
            et = t.RandEt(V, curT)
            Ass1,f1 = t.Ass1(V, curT, et)
            print('部署方案１\n'+str(Ass1))
            if not Ass1 ==None:
                Producer(Ass1, Assq).start()
            sleep(1)
            for i in V:
                Consumer(V.index(i), Assq,flag).start()
            V2 = V
            curT2,Tn = t.RandT('t', Tn, 0, 3)
            et = t.RandEt(V2, curT2)
            UnitPrice = t.UnitPrice(V2)
            pt = t.RandPt(V2,curT2,et,UnitPrice)
            Ass3,f3 = t.Ass3(V2, curT2, et, pt)
            print('部署方案３\n'+str(Ass3))
            if not Ass3 ==None:
                Producer(Ass3, Assq).start() 
            for i in V2:
                Consumer(V2.index(i), Assq,cond).start()
        else:
            break
