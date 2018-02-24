# coding = utf-8
import time
import re
import gantt
from datetime import datetime
import gantt_data as g
import pre_handler as t

s = time.time()
# csv_file = '.\\datafile\\res.csv'
# pid_numx = g.pid_num(csv_file)
# task_numx = g.task_num(csv_file)
# taskx = g.task(csv_file)
# setupx = g.setup(csv_file)
#
# min = min(setupx)

# setup = [setupx[i] - min for i in range(len(setupx))]
# vm_num = g.vm_num(pid_numx)
# color_num = g.color_num(taskx)
# durationx = g.duration(csv_file)

# print(color_num)
# print(task_numx)
# print(taskx)
# print(setup)
# print(durationx)

x = [6,7,6,3,6]

w1 = [str(1) + str(i + 1) for i in range(x[0])]
w2 = [str(2) + str(i + 1) for i in range(x[1])]
w3 = [str(3) + str(i + 1) for i in range(x[2])]
w4 = [str(4) + str(i + 1) for i in range(x[3])]
w5 = [str(5) + str(i + 1) for i in range(x[4])]

p1 = [str(1) + str(i + 1) for i in range(2)]
p2 = [str(2) + str(i + 1) for i in range(3)]
p3 = [str(3) + str(i + 1) for i in range(3)]

exec_pro1 = [7.7, 7.1, 5.8, 4.8]
exec_pro2 = [8.0, 7.4, 6.2, 5.1]
exec_pro3 = [7.4, 6.7, 5.5, 4.3]

exec_v = exec_pro1 + exec_pro2 + exec_pro3
Tn = w1 + w2 + w3 + w4 + w5
Vn = p1 + p2 + p3
V = t.rand_v('v', Vn)
vm_price = t.unit_price(V)
print(vm_price)
task_pool = t.t_pool(Tn)
task = task_pool.get()
print(task)
# t.test_et(V, task)

pos = '1'
ass3_file = '.\\datafile\\'+pos+'\\ass3.in'

fa = open(ass3_file,'r')
for line in fa.readlines():
    res = re.match('^ass3.*',line)
    if not res == None:
        print(res.group().replace('ass3',''))
e = time.time()
print('COST: %.3f' %(e-s))
