import csv
import re
# csv_file = '.\\datafile\\res.csv'

def pid_num(csv_file):
    """
    返回进程号列表
    :param csv_file: 输出文件
    :return: 进程号（相当于虚拟机标识）
    """
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        pid_num = [row['pid_num'] for row in reader]
    return pid_num


def vm_num(pid_num):
    """
    返回虚拟机标识列表
    :param pid_num: 进程号列表
    :return: 虚拟机标识列表
    """
    vm_num = []
    d = {'x': -1}
    counter = 0
    for i in range(len(pid_num)):
        if not pid_num[i] in d.keys():
            d.update({pid_num[i]: counter})
            tmp = counter
            counter += 1
        else:
            tmp = d[pid_num[i]]
        vm_num.append(tmp)
    return vm_num


def task_num(csv_file):
    """
    返回任务编号列表
    :param csv_file:
    :return: 任务编号列表
    """
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        task_num = [int(row['task_num']) for row in reader]
    return task_num


def task(csv_file):
    """
    返回任务列表
    :param csv_file:
    :return: 任务列表
    """
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        task = [row['task'] for row in reader]
    return task


def vm(csv_file):
    """
    返回虚拟机列表
    :param csv_file:
    :return: 虚拟机列表
    """
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        vm = [row['vm'] for row in reader]
    return vm


def task_xiabiao(task):
    """
    返回任务下标列表
    :param task: 任务列表
    :return: 任务下标列表
    """
    task_num = []
    for i in task:
        i = ''.join(i.split('t'))
        task_num.append(int(i))
    return task_num


def vm_xiabiao(vm):
    """
    返回虚拟机下标列表
    :param vm: 虚拟机列表
    :return: 虚拟机下标列表
    """
    vm_id = []
    for i in vm:
        i = ''.join(i.split('v'))
        vm_id.append(int(i))
    return vm_id


def color_num(task):
    """
    创建颜色列表（同一工作流中的任务用一种颜色）
    :param task: 任务列表
    :return: 颜色列表
    """
    color_num = []
    for i in task:
        color_num.append(int(i[1]) - 1)
    return color_num


def setup(csv_file):
    """
    创建任务起始时间戳列表
    :param csv_file:
    :return: 任务起始时间戳列表
    """
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        setup = [round(float(row['setup']),3) for row in reader]
    return setup


def duration(csv_file):
    """
    创建运行停留时间列表
    :param csv_file:
    :return: 运行停留时间列表
    """
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        duration = [float(row['duration']) for row in reader]
    return duration


def cutting(csv_file):
    """
    创建任务截止时间戳列表
    :param csv_file:
    :return: 任务截止时间列表
    """
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        cutting = [round(float(row['cutting']),3) for row in reader]
    return cutting


def get_wl(vm_num):
    wl = []
    for i in set (vm_num):
        wl.append (vm_num.count (i))
    return wl


def get_ass1(ass1_file):
    res1 = []
    fa = open (ass1_file, 'r')
    for line in fa.readlines ():
        res = re.match ('^ass1.*', line)
        if not res == None:
            res1.append(res.group ().replace ('ass1', ''))
    return res1


def get_ass2(ass2_file):
    res2 = []
    fa = open (ass2_file, 'r')
    for line in fa.readlines ():
        res = re.match ('^ass2.*', line)
        if not res == None:
            res2.append(res.group ().replace ('ass2', ''))
    return res2

def get_ass3(ass3_file):
    res3 = []
    fa = open (ass3_file, 'r')
    for line in fa.readlines ():
        res = re.match ('^ass3.*', line)
        if not res == None:
            res3.append(res.group ().replace ('ass3', ''))
    return res3


def get_etc_vm(pre_ass, V):
    csp1 = []
    csp2 = []
    csp3 = []
    for z in V[0:3]:
        for x in pre_ass:
            y = eval (x)
            for i, j in y.items ():
                for k, l in j.items ():
                    if i == z:
                        vm_etc = (i, l)
                        # print(vm_etc)
                        csp1.append (vm_etc)
    for z in V[3:6]:
        for x in pre_ass:
            y = eval (x)
            for i, j in y.items ():
                for k, l in j.items ():
                    if i == z:
                        vm_etc = (i, l)
                        # print (vm_etc)
                        csp2.append (vm_etc)
    for z in V[6:len(V)]:
        for x in pre_ass:
            y = eval (x)
            for i, j in y.items ():
                for k, l in j.items ():
                    if i == z:
                        vm_etc = (i, l)
                        # print (vm_etc)
                        csp3.append (vm_etc)
    return csp1, csp2, csp3


def fairness(csp):
    etc = []
    pfetc = []
    for x in csp:
        etc.append(x[1])
        pfetc.append(x[1]*x[1])
    fairness = round(sum(etc)*sum(etc)/(len(etc)*sum(pfetc)),6)
    return fairness


def profitList(pre_ass, vm_price):
    profitlist = []
    for x in pre_ass:
        y = eval(x)
        for i,j in y.items():
            for k,l in j.items():
                vm_profit = (i, vm_price[i] * l)
                # print(vm_profit)
                profitlist.append(vm_profit)
    return profitlist


def profit(profitList, vm):
    vm_pro = []
    for v in vm:
        vm_set = []
        for i,j in profitList:
            if  i==v:
                vm_set.append(j)
        vm_pro.append(round(sum(vm_set),3))
    return vm_pro