# coding=utf-8
import random, csv, sys
from datetime import datetime
from queue import PriorityQueue, Queue
from numpy import array, zeros
from scipy.optimize import linear_sum_assignment
import numpy as np
import km


def t_pool(tn):
    """
将工作流中的任务分层级
    :param tn: 工作流
    :return: 任务池队列，队列中的每一个元素都是一个优先级队列的元素列表
    """
    ta_pool = Queue()
    for l in range(100):
        if not len(tn) == 0:
            tll = []
            tl, tx = t_queue('t', tn, 0, random.randint(8, 10), l)
            while not tl.empty():
                tll.append(tl.get())
            ta_pool.put(tll)
    return ta_pool


def t_queue(char, tn, start, end, level):
    """
    切割序列生成阶段性的任务列表且分层级
    :param char: ‘t’
    :param tn: 任务的编号列表
    :param start: 起始索引
    :param end: 结束索引
    :param level: 层级
    :return: t_queue优先级队列, tn剩余的编号序列
    """
    ta_queue = PriorityQueue(1000)
    t = tn[start:end]
    for i in t:
        ta_queue.put((level, char + str(i)))
        tn.remove(i)
    return ta_queue, tn


def rand_v(char, vn):
    """
    生成虚拟机列表
    :param char: ‘v’
    :param vn:
    :return: v
    """
    v = []
    for i in vn:
        v.append(char + str(i))
    return v


def rand_et(v, t, rs, re):
    """
    生成基于随机数的执行时间表 
    :param v: 当前可用的VM的集合
    :param t: 当前任务队列的集合
    :param rs: 随机数下限
    :param re: 随机数上限
    :return: et
    """
    c = []
    f = open('.\\datafile\\et.in', 'a')
    f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
    for i in range(len(v)):
        c.append(
            [round(random.uniform(rs, re), 3) for j, t in enumerate(t)])
    et = array(c)
    f.write(str(et) + '\n')
    f.close()
    return et


# 三家生产商、4种虚拟机规格的任务执行时间中心值
# exec_pro1 = [7.7, 7.1, 5.8, 4.8]
# exec_pro2 = [8.0, 7.4, 6.2, 5.1]
# exec_pro3 = [7.4, 6.7, 5.5, 4.3]
exec_pro1 = [7.1, 5.8, 4.8]
exec_pro2 = [7.4, 6.2, 5.1]
exec_pro3 = [6.7, 5.5, 4.3]
exec_v = exec_pro1 + exec_pro2 + exec_pro3


def test_et(v, t, pos):
    """
    创建基于中心值的执行时间矩阵
    :param v: 虚拟机列表
    :param t: 任务列表
    :return: 实验测试执行时间列表
    """
    c = []
    f = open('.\\datafile\\'+pos+'\\et.in', 'a')
    f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
    for i in range(len(v)):
        c.append(
            [round(random.uniform(exec_v[i] * (1 - 0.02), exec_v[i] * (1 + 0.02)), 3) for j, t in enumerate(t)])
    t_et = array(c)
    f.write(str(t_et) + '\n')
    f.close()
    return t_et


# 三家生产商、4种不同规格的虚拟机租用单价
# pri_pro1 = [0.0058, 0.023, 0.0464, 0.0928]
# pri_pro2 = [0.0185, 0.0246, 0.0493, 0.0739]
# pri_pro3 = [0.1053, 0.1244, 0.1373, 0.2502]
pri_pro1 = [0.023, 0.0464, 0.0928]
pri_pro2 = [0.0246, 0.0493, 0.0739]
pri_pro3 = [0.1373, 0.2502]
price = pri_pro1 + pri_pro2 + pri_pro3


def unit_price(v):
    """
    生成vm的单价字典
    :param v: 虚拟机列表
    :return: 虚拟机租用的单位时间价格
    """
    # unit_price = {i: round(random.uniform(0, 1), 3) for i in v}
    vm_price = {i: price[v.index(i)] for i in v}
    return vm_price


def rand_pt(v, t, et, vm_price, pos):
    """
    生成基于执行时间矩阵的价格矩阵
    :param v: 虚拟机
    :param t: 任务
    :param et: 任务执行时间矩阵
    :param vm_price: 虚拟机的租用单价
    :return: pt
    """
    pt = zeros(et.shape)
    f = open('.\\datafile\\'+pos+'\\pt.in', 'a')
    f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
    for i, v in enumerate(v):
        for j in range(len(t)):
            pt[i][j] = et[i][j] * vm_price[v]
    f.write(str(pt) + '\n')
    f.close()
    return pt


def ass1(v, t, et, pos):
    """
    生成部署方案１－最小化最大完成时间
    :param v: 虚拟机
    :param t: 任务
    :param et: 执行时间矩阵
    :return: ass1
    """
    pre_ass1 = {}
    f1 = zeros(et.shape)
    delays = []
    f = open('.\\datafile\\'+pos+'\\ass1.in', 'a')
    f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
    c_row_ind, c_col_ind = linear_sum_assignment(et)
    c_min_sum = et[c_row_ind, c_col_ind].sum()
    f.write('f1' + '\t' + str(c_min_sum) + '\n')
    for i in range(min(et.shape)):
        f1[c_row_ind[i]][c_col_ind[i]] = et[c_row_ind[i]][c_col_ind[i]]
        pre_ass1[v[c_row_ind[i]]] = {t[c_col_ind[i]]: round(et[c_row_ind[i]][c_col_ind[i]], 4)}
        delays.append((v[c_row_ind[i]], t[c_col_ind[i]], et[c_row_ind[i]][c_col_ind[i]]))
    f.write(str(f1) + '\n')
    f.write('ass1' + str(pre_ass1) + '\n')
    f.close()
    return pre_ass1, f1, delays


def ass3(v, t, et, pt, pos):
    """
    生成部署方案3-按价格最大权匹配
    :param v: 虚拟机
    :param t: 任务
    :param et: 执行时间矩阵
    :param pt: 价格矩阵
    :return: ass3
    """
    pre_ass3 = {}
    f3 = zeros(et.shape)
    backup = zeros(et.shape)
    delays = []
    f = open('.\\datafile\\'+pos+'\\ass3.in', 'a')
    f.write(datetime.now().strftime('%Y-%m-%d:%H:%M:%S') + '\n')
    r_row_ind, r_col_ind = km.km_max(pt)
    r_max_sum = pt[r_row_ind, r_col_ind].sum()
    f.write('f3' + '\t' + str(r_max_sum) + '\n')
    for i in range(min(et.shape)):
        f3[r_row_ind[i]][r_col_ind[i]] = pt[r_row_ind[i]][r_col_ind[i]]
        pre_ass3[v[r_row_ind[i]]] = {t[r_col_ind[i]]: round(et[r_row_ind[i]][r_col_ind[i]], 4)}
        backup[r_row_ind[i]][r_col_ind[i]] = et[r_row_ind[i]][r_col_ind[i]]
        delays.append((v[r_row_ind[i]], t[r_col_ind[i]], et[r_row_ind[i]][r_col_ind[i]]))
    f.write(str(f3) + '\n')
    f.write(str(backup) + '\n')
    f.write('ass3' + str(pre_ass3) + '\n')
    f.close()
    return pre_ass3, f3, delays
