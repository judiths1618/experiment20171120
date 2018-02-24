#coding=utf-8
from time import ctime, sleep
from threading import Thread, currentThread, Condition
import threading,logging
import random,time
import datetime as dt

from queue import Queue
import data as t
logging.basicConfig(
        level = logging.DEBUG,
        format = '[%(levelname)s] (%(threadName)-10s) %(message)s',
        )

def VM():
    current = yield
    while True:
        t_setup = time.time()
        item = yield current   #传入部署方案
        time.sleep(item[1][list(item[1])[0]])
        t_cutting = time.time()
        print('---虚拟机 %s 执行任务 %s at %f, %s' %(item[0],list(item[1])[0],t_setup,t_cutting))
#def

def threads_pool(Ass1):
    threads = []
    for i in range(len(Ass1)):
        threads.append(threading.Thread(target=VM))
    return threads

# main func
if __name__== '__main__':
    #T = ['t1','t2','t3','t4','t5','t6']
    #V = ['v11','v12','v13','v21','v31','v33','v34']
    Tn = [11,12,13,14,15,16,17,18,21,22,23,24,25,26,31,32,33,34,35,36,
            37,38,39,41,42,43,44,45,46,51,52,53,54,55,56,57,58]
    Vn = [11,12,13,14,15,16,21,22,23,24,25,26,31,32,33,34,35,36]
#    Assq = Queue()
    flag = 0

    V,Vx = t.RandT('v', Vn, 1,4)
    T,Tx = t.RandT('t', Tn, 2,7)
    
    et = t.RandEt(V,T) 
    Ass1,f1 = t.Ass1(V, T, et) 
    UnitPrice = t.UnitPrice(V)
    pt = t.RandPt(V,T,et,UnitPrice)
    Ass3,f3 = t.Ass3(V, T, et, pt)

    print('部署开始时间　%s' %dt.datetime.now().strftime('%Y-%m-%d: %H:%M:%S.%f'))
    s = time.time()
    it = VM()
    next(it)

    for i in Ass1.items():
        print(i)
        it.send(i)
    vms_pool = threads_pool(Ass1)
    for vm in vms_pool:
        vm.setDaemon(True)
        vm.start()
    sleep(3)
    '''
    for i in Ass3.items():
        Assq.put(i)
    vms_pool = threads_pool(Ass3, Assq)
    for vm in vms_pool:
        vm.setDaemon(True)
        vm.start()
'''
    vm.join()
    e = time.time()
    print('所有线程完成时间 %s' %dt.datetime.now().strftime('%Y-%m-%d: %H:%M:%S.%f'))
    print('所有用时: %f' %(round(e-s, 4)))

