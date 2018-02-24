#coding=utf-8
import asyncio
import time
import data as t
from decimal import Decimal
from threading import Timer

'''function: 基于贪心策略的实时调度
    @Parameters: V,T,Ass,flag
     falg: 0表示vm可用，任务可被接受；1表示vm正在被占用，任务被拒绝
    @return: 实时调度
note:阶段性的实时调度
'''

def printInfo():
    now = time.time()
    print(now)

async def MyTask(v,t,Ass):
    flag = 0
    if flag == 0:
        setup = time.time()
        x = float(Ass[v][t])
        await asyncio.sleep(x)
        #print(v,t,Ass[v][t])
        cutting = time.time()
        print("Setup %s cutting %s. VM %s: task %s = %s" %(str(setup), str(cutting),v, t, str(Ass[v][t])))
        flag = 1
    else:
        print('%s 正在被占用，任务被拒绝')

start = time.time()
Ass1 = {'v12': {'t16': Decimal('1.0517')}, 'v13': {'t15': Decimal('6.1417')}, 'v14': {'t17': Decimal('2.2848')}, 'v15': {'t21': Decimal('4.3280')}, 'v16': {'t14': Decimal('1.7016')}}
Ass2 = {'v12': {'t18': Decimal('16.6392')}, 'v13': {'t21': Decimal('12.5071')}, 'v14': {'t15': Decimal('16.9291')}, 'v15': {'t17': Decimal('15.9631')}, 'v16': {'t12': Decimal('16.9097')}}

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    MyTask('v12','t16',Ass1),
    MyTask('v13','t15',Ass1),
    MyTask('v14','t17',Ass1),
    MyTask('v15','t21',Ass1),
    MyTask('v16','t14',Ass1),
#    ))
#loop.run_until_complete(asyncio.gather(
    MyTask('v12','t18',Ass2),
    MyTask('v13','t21',Ass2),
    MyTask('v14','t15',Ass2),
    MyTask('v15','t17',Ass2),
    MyTask('v16','t12',Ass2)
    ))
end = time.time()
print("Time %.3f seconds" %(end-start))
