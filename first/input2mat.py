import pre_handler as t
import gantt_data as g


if __name__ == '__main__':
    p1 = [str (1) + str (i + 1) for i in range (3)]
    p2 = [str (2) + str (i + 1) for i in range (3)]
    p3 = [str (3) + str (i + 1) for i in range (2)]

    Vn = p1 + p2 + p3
    V = t.rand_v ('v', Vn)
    vm_price = t.unit_price (V)
    # print (vm_price)

    pos = '16'
    csv_file = '.\\datafile\\'+pos+'\\res.csv'
    ass1_file = '.\\datafile\\'+pos+'\\ass1.in'
    ass3_file = '.\\datafile\\'+pos+'\\ass3.in'
    pid_nums = g.pid_num(csv_file)
    task_nums = g.task_num(csv_file)
    tasks = g.task(csv_file)
#    vms = g.vm(csv_file)
    vm_num = g.vm_num(pid_nums)
    color_num = g.color_num(tasks)
    setups = g.setup(csv_file)
    durations = g.duration(csv_file)
    cuttings = g.cutting(csv_file)
    tasks_xiabiao = g.task_xiabiao(tasks)

    setup_min = min(setups)
    max_num = max(vm_num) + 1
    setup = [round(setups[i] - setup_min, 3) for i in range(len(setups))]
    cutting = [round(cuttings[j] - setup_min, 3) for j in range(len(cuttings))]
    setup_max = max(cutting)

    # 统计每台vm（vm_num）上的workload
    wl = g.get_wl(vm_num)
    # 统计每台vm上的盈利，从而计算云厂商租出vm的收入
    pre_ass1 = g.get_ass1(ass1_file)
    pre_ass3 = g.get_ass3(ass3_file)
    profit_list = g.profitList(pre_ass1+pre_ass3, vm_price)
    profit_of_each_vm = g.profit(profit_list, V)

    # 统计整个workflow的最大完成时间makespan
    print('round ' +pos)
    print('makespan %.3f' %setup_max)
    print('workload',wl)
    print('profit of each vm', profit_of_each_vm)
    # print(tasks)
    # print(vm_num)
    # print(max_num)
    # print(setup)
    # print(durations)
    # print(cutting)

    filename = 'C:\\Users\\Judiths\\Documents\\MATLAB\\gantt\\'+pos+'\\input.dat'
    fa = open(filename, 'w')
    fa.write(str(max_num)+'\n')
    fa.write(str(len(setup))+'\n')
    fa.write(str(setup_max)+'\n')
    fa.write(str(vm_num)+'\n')
    fa.write(str(color_num)+'\n')
    fa.write(str(setup)+'\n')
    fa.write(str(durations)+'\n')
    fa.write(str(tasks_xiabiao)+'\n')
    fa.write(str(wl)+'\n')
    fa.write(str(profit_of_each_vm)+'\n')

    fa.close()
