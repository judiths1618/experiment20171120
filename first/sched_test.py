#coding=utf-8
from threading import Timer, Thread, Condition, currentThread, enumerate
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
def printInfo():
    setup_t = time.time()
    return setup_t

def myTimer(delay):
    t = Timer(delay, printInfo)
