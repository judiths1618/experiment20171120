# coding=utf-8
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import pre_handler as t
import gantt_data as g
import os


def pre_optimal_ass_fifo(pool_of_tasks, v, pos):
    """
    生成pre_scheduling assignment
    :param pool_of_tasks: 任务池
    :param v:虚拟机列表
    :return: pre_opt_ass
    """
    pre_opt_ass_fifo = []
    for l in range (10000):
        if not pool_of_tasks.empty() :
            tl1 = pool_of_tasks.get ()
            et1 = t.test_et (v, tl1, pos)
            ass1_fifo, f1, delays1 = t.ass1_fifo (v, tl1, et1, pos)
            pre_opt_ass_fifo += delays1
        else:
            break
        if not pool_of_tasks.empty ():
            tl2 = pool_of_tasks.get ()
            et2 = t.test_et (v, tl2, pos)
            wl = t.rand_wl (v, tl2, 3, 6)
            ass2_fifo, f2, delays2 = t.ass2 (v, tl2, wl, et2, pos)
            pre_opt_ass_fifo += delays2
        else:
            break
        if not pool_of_tasks.empty():
            tl3 = pool_of_tasks.get ()
            et3 = t.test_et (v, tl3, pos)
            unit_price = t.unit_price (v)
            pt3 = t.rand_pt (v, tl3, et3, unit_price, pos)
            ass3_fifo, f3, delays3 = t.ass3 (v, tl3, et3, pt3, pos)
            pre_opt_ass_fifo += delays3
        else:
            break
    taskNum = len(pre_opt_ass_fifo)
    gameSta = round(taskNum/8)
    print ('预分配结束', taskNum, gameSta)
    return pre_opt_ass_fifo, taskNum, gameSta


def test_sleep(it):
    """
    采集任务部署的时间戳等信息
    :param it: 任务部署方案
    :return: 任务的部署信息
    """
    icon = os.getpid ()
    timestamp1 = int (round (time.time () * 1000)) / 1000
    time.sleep (it[2])
    timestamp2 = int (round (time.time () * 1000)) / 1000
    setup = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (timestamp1))
    cutting = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (timestamp2))
    return [True, icon, it[0], it[1][0], it[1][1], setup, it[2], cutting, timestamp1, timestamp2]


def use_submit(pre_ass, v, pos):
    """
    采用多线程模拟多个云主机并行执行任务
    :param pre_ass:
    :param v:
    """
    print ('开始部署\n')
    fa = open ('.\\datafile\\' + pos + '\\res.csv', 'w')
    fa.write ('pid_num,vm,task_num,task,setup,duration,cutting\n')
    with ProcessPoolExecutor (max_workers=len (v)) as executor:
        futures = {executor.submit (test_sleep, it): it for it in pre_ass}
        try:
            for f in as_completed (futures):
                # print ('%s result is %s.' % (futures[f], f.result ()))
                fa.write (str (f.result ()[1]) + ',' + str (f.result ()[2]) + ',' +
                          str (f.result ()[3]) + ',' + str (f.result ()[4]) + ',' +
                          str (f.result ()[8]) + ',' + str (f.result ()[6]) + ',' +
                          str (f.result ()[9]) + '\n')
            fa.close ()
        except Exception as exc:
            print (exc)


if __name__ == '__main__':
    s = time.time ()
    x1 = [3, 7, 6, 4, 9]  # baseline+1
    x2 = [13, 17, 16, 14, 19]  # baseline+2
    x3 = [13, 27, 16, 24, 19]  # baseline+3
    x4 = [23, 27, 26, 24, 29]  # baseline+4
    x5 = [23, 37, 26, 34, 29]  # baseline+5
    x6 = [33, 37, 36, 34, 39]  # baseline+6
    x7 = [33, 47, 36, 44, 39]  # baseline+7
    x8 = [43, 47, 46, 44, 49]  # baseline+8
    x9 = [43, 57, 46, 54, 49]  # baseline+9
    x10 = [53, 57, 56, 54, 59]  # baseline+10
    x11 = [53, 67, 56, 64, 59]  # baseline+11
    x12 = [63, 67, 66, 64, 69]  # baseline+12
    x13 = [63, 77, 66, 74, 69]  # baseline+13
    x14 = [73, 77, 76, 74, 79]  # baseline+14
    x15 = [73, 87, 76, 84, 79]  # baseline+15
    x16 = [83, 87, 86, 84, 89]  # baseline+16
    x17 = [83, 97, 86, 94, 89]  # baseline+17
    x18 = [93, 97, 96, 94, 99]  # baseline+18
    x19 = [93, 107, 96, 104, 99]  # baseline+19
    x20 = [103, 107, 106, 104, 109]  # baseline+20
    X = [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16]
        # , x17, x18, x19, x20]
    for k, x in enumerate (X):
        for i in range(1,len(X)+1):
            pos = 'bigscale\\baseline+'+str(k+1)+'\\'+str(i)
            w1 = [str (1) + str (i + 1) for i in range (x[0])]
            w2 = [str (2) + str (i + 1) for i in range (x[1])]
            w3 = [str (3) + str (i + 1) for i in range (x[2])]
            w4 = [str (4) + str (i + 1) for i in range (x[3])]
            w5 = [str (5) + str (i + 1) for i in range (x[4])]

            p1 = [str (1) + str (i + 1) for i in range (3)]
            p2 = [str (2) + str (i + 1) for i in range (3)]
            p3 = [str (3) + str (i + 1) for i in range (2)]

            exec_pro1 = [7.1, 5.8, 4.8]
            exec_pro2 = [7.4, 6.2, 5.1]
            exec_pro3 = [6.7, 5.5, 4.3]

            exec_v = exec_pro1 + exec_pro2 + exec_pro3

            pri_pro1 = [0.023, 0.0464, 0.0928]
            pri_pro2 = [0.0246, 0.0493, 0.0739]
            pri_pro3 = [0.1053, 0.1244, 0.1373]

            price = pri_pro1 + pri_pro2 + pri_pro3
            Tn = w1 + w2 + w3 + w4 + w5
            Vn = p1 + p2 + p3

            V = t.rand_v ('v', Vn)
            vm_price = t.unit_price (V)
            task_pool = t.t_pool (Tn, 10000)  # 层级上限是10000

            print ('round ' + pos)
            pre_optimal_ass_fifoi, task_number, game_stage = pre_optimal_ass_fifo (task_pool, V, pos)
            use_submit (pre_optimal_ass_fifoi, V, pos)
            # 后续采集task number, game stage, makespan, workload, profit数据
            print ('采集数据')
            csv_file = '.\\datafile\\' + pos + '\\res.csv'
            ass1_file = '.\\datafile\\' + pos + '\\ass1.in'
            ass2_file = '.\\datafile\\' + pos + '\\ass2.in'
            ass3_file = '.\\datafile\\' + pos + '\\ass3.in'
            pid_nums = g.pid_num (csv_file)
            task_nums = g.task_num (csv_file)
            tasks = g.task (csv_file)
            vm_num = g.vm_num (pid_nums)
            color_num = g.color_num (tasks)
            setups = g.setup (csv_file)
            durations = g.duration (csv_file)
            cuttings = g.cutting (csv_file)
            tasks_xiabiao = g.task_xiabiao (tasks)

            setup_min = min (setups)
            max_num = max (vm_num) + 1
            setup = [round (setups[i] - setup_min, 3) for i in range (len (setups))]
            cutting = [round (cuttings[j] - setup_min, 3) for j in range (len (cuttings))]
            setup_max = max (cutting)

            # 统计每台vm（vm_num）上的workload
            wl = g.get_wl (vm_num)
            # 统计每台vm上的盈利，从而计算云厂商租出vm的收入
            pre_ass1 = g.get_ass1 (ass1_file)
            pre_ass2 = g.get_ass2 (ass2_file)
            pre_ass3 = g.get_ass3 (ass3_file)

            profit_list = g.profitList (pre_ass1 + pre_ass2 + pre_ass3, vm_price)
            profit_of_each_vm = g.profit (profit_list, V)

            # 统计整个workflow的最大完成时间makespan
            print ('round ' + pos)
            print ('makespan %.3f' % setup_max)
            print ('workload', wl)
            print ('profit of each vm', profit_of_each_vm)
            print (len (tasks), tasks)
            filename = '.\\datafile\\bigscale\\curve\\baseline_out.dat'
            fa = open (filename, 'a')
            fa.write (pos + '\t' + str (task_number) + '\t' + str (game_stage) + '\t' +
                      str (setup_max) + '\n')
            fa.close ()

    e = time.time ()
    print ('COST: %.3f.' % (e - s))