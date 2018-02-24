# coding=utf-8
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import pre_handler as t
import os


def pre_optimal_ass(pool_of_tasks, v, pos):
    """
    生成pre_scheduling assignment
    :param pool_of_tasks: 任务池
    :param v:虚拟机列表
    :return: pre_opt_ass
    """
    print('正在pre-scheduling...')
    pre_opt_ass = []
    while not pool_of_tasks.empty():
        tl1 = pool_of_tasks.get()
#        et1 = t.rand_et(v, tl1, 3, 5)
        et1 = t.test_et(v, tl1, pos)
        ass1, f1, delays1 = t.ass1(v, tl1, et1, pos)
        # print(ass1)
        tl3 = pool_of_tasks.get()
#        et3 = t.rand_et(v, tl3, 6, 9)
        et3 = t.test_et(v, tl3, pos)
        unit_price = t.unit_price(v)
        pt3 = t.rand_pt(v, tl3, et3, unit_price, pos)
        ass3, f3, delays3 = t.ass3(v, tl3, et3, pt3, pos)
        # print(ass3)
        pre_opt_ass += delays1+delays3
    return pre_opt_ass


def test_sleep(it):
    """
    采集任务部署的时间戳等信息
    :param it: 任务部署方案
    :return: 任务的部署信息
    """
    icon = os.getpid()
    timestamp1 = int(round(time.time() * 1000))/1000
    time.sleep(it[2])
    timestamp2 = int(round(time.time() * 1000))/1000
    setup = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp1))
    cutting = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp2))
    return [True, icon, it[0], it[1][0], it[1][1], setup, it[2], cutting, timestamp1, timestamp2]


def use_submit(pre_ass, v, pos):
    """
    采用多线程模拟多个云主机并行执行任务
    :param pre_ass:
    :param v:
    """
    fa = open('.\\datafile\\'+pos+'\\res.csv', 'w')
    fa.write('pid_num,vm,task_num,task,setup,duration,cutting\n')
    with ProcessPoolExecutor(max_workers=len(v)) as executor:
        futures = {executor.submit(test_sleep, it): it for it in pre_ass}
        try:
            for f in as_completed(futures):
                # print('%s result is %s.' % (futures[f], f.result()))
                fa.write(str(f.result()[1]) + ',' + str(f.result()[2]) + ',' +
                        str(f.result()[3]) + ',' + str(f.result ()[4])+ ',' +
                        str(f.result()[8]) + ',' + str(f.result()[6]) + ','+
                        str(f.result()[9])+'\n')
            fa.close()
        except Exception as exc:
            print(exc)


def use_map(pre_ass, v):
    with ProcessPoolExecutor(max_workers=len(v)) as executor:
        print(executor._work_ids)
        try:
            results = executor.map(test_sleep, pre_ass)
            for it, [result, setup, duration, cutting] in zip(pre_ass, results):
                print('%s result is %s. start at %s, cutting at %s. COST: %s'
                      % (it[0], result, setup, cutting,duration))
        except Exception as exc:
            print(exc)


if __name__ == '__main__':
    s = time.time()
    x = [6,7,6,3,6]
    w1 = [str(1) + str(i + 1) for i in range(x[0])]
    w2 = [str(2) + str(i + 1) for i in range(x[1])]
    w3 = [str(3) + str(i + 1) for i in range(x[2])]
    w4 = [str(4) + str(i + 1) for i in range(x[3])]
    w5 = [str(5) + str(i + 1) for i in range(x[4])]

    p1 = [str(1) + str(i + 1) for i in range(3)]
    p2 = [str(2) + str(i + 1) for i in range(3)]
    p3 = [str(3) + str(i + 1) for i in range(2)]

    exec_pro1 = [7.1, 5.8, 4.8]
    exec_pro2 = [7.4, 6.2, 5.1]
    exec_pro3 = [5.5, 4.3]

    exec_v = exec_pro1 + exec_pro2 + exec_pro3

    pri_pro1 = [0.023, 0.0464, 0.0928]
    pri_pro2 = [0.0246, 0.0493, 0.0739]
    pri_pro3 = [0.1373, 0.2502]

    price = pri_pro1 + pri_pro2 + pri_pro3
    Tn = w1 + w2 + w3 + w4 + w5
    Vn = p1 + p2 + p3

    pos = '16'
    V = t.rand_v('v', Vn)
    vm_price = t.unit_price(V)
    task_pool = t.t_pool(Tn)

    pre_optimal_ass = pre_optimal_ass(task_pool, V, pos)
    print('round '+pos)
    print(pre_optimal_ass)
    use_submit(pre_optimal_ass, V, pos)
#    use_map(pre_optimal_ass, V)  # 按照 pre_optimal_ass 顺序执行
    # 采集makespan, workload, profit数据

    e = time.time()
    print('COST: %.3f.' % (e - s))
