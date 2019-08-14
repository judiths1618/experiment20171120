import pre_handler as t
import gantt_data as g
import curve_data as c


# pos1 = 'bigscale\\+' + str (i) + '\\' + j
# pos2 = 'bigscale\\baseline+'+str(i)+'\\'+j
def res_data(pos_keystr,curv_keystr, V):
    a = [i for i in range (1, 16)]
    b = [str (i) for i in range (1, 16)]
    for i in a:
        aver_wl = []
        aver_prf = []
        for j in b:
            pos = pos_keystr + str (i) + '\\' + j

            csv_file = pos + '\\res.csv'
            ass1_file = pos + '\\ass1.in'
            ass2_file = pos + '\\ass2.in'
            ass3_file = pos + '\\ass3.in'

            print(csv_file)
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

            # 统计整个云环境的workload
            total_wl = round(sum(wl)/len(wl),3)

            pre_ass1 = g.get_ass1 (ass1_file)
            pre_ass2 = g.get_ass2 (ass2_file)
            pre_ass3 = g.get_ass3 (ass3_file)
            # 计算组内的workload的公平性
            csp1, csp2, csp3 = g.get_etc_vm(pre_ass1 + pre_ass2 + pre_ass3, V)
            fairness1 = g.fairness(csp1)
            fairness2 = g.fairness (csp2)
            fairness3 = g.fairness (csp3)

            ff = g.fairness(csp1+csp2+csp3)
            profit_list = g.profitList (pre_ass1 + pre_ass2 + pre_ass3, vm_price)
            # 统计每台vm上的盈利，从而计算云厂商租出vm的收入
            profit_of_each_vm = g.profit (profit_list, V)
            # 统计整个云环境的profit
            total_prf = round(sum(profit_of_each_vm)/len(profit_of_each_vm),3)

            # 统计整个workflow的最大完成时间makespan
            print('round ' +pos)
            print('makespan %.3f' %setup_max)
            # print ('total workload %.3f' %total_wl)
            # print('total profit %.3f' %total_prf)
            print (fairness1, fairness2, fairness3, ff)

            aver_wl.append (total_wl)
            aver_prf.append (total_prf)

            gantt_file_out = pos + '\\gantt_input.dat'
            fa = open (gantt_file_out, 'w')
            fa.write (str (max_num) + '\n')
            fa.write (str (len (setup)) + '\n')
            fa.write (str (setup_max) + '\n')
            fa.write (str (vm_num) + '\n')
            fa.write (str (color_num) + '\n')
            fa.write (str (setup) + '\n')
            fa.write (str (durations) + '\n')
            fa.write (str (tasks_xiabiao) + '\n')
            fa.write (str (wl) + '\n')
            fa.write (str (profit_of_each_vm) + '\n')
            fa.close ()

            # curv_file_out = '.\\datafile\\bigscale\\curve\\_baseline_curve_input.dat'
            crv_f = '.\\datafile\\bigscale\\curve\\'+ curv_keystr
            f = open (crv_f, 'a')
            f.write (pos + '\t' + str (len (tasks)) + '\t' + str (round (len (tasks) / 8)) + '\t' +
                     str (setup_max) + '\t' + str (total_wl) + '\t' + str (total_prf) +'\t'+
                     str(fairness1)+'\t'+str(fairness2)+'\t'+str(fairness3)+ '\t'+str(ff)+'\n')
            f.close ()
    print('数据重新填充完毕')


if __name__ == '__main__':
    p1 = [str (1) + str (i + 1) for i in range (3)]
    p2 = [str (2) + str (i + 1) for i in range (3)]
    p3 = [str (3) + str (i + 1) for i in range (2)]

    Vn = p1 + p2 + p3
    V = t.rand_v ('v', Vn)
    vm_price = t.unit_price (V)

    pos1_keystr = '.\\datafile\\bigscale\\+'
    pos2_keystr = '.\\datafile\\bigscale\\baseline+'

    curv_keystr1 = '_curve_input.dat'
    curv_keystr2 = '_baseline_curve_input.dat'
    # res_data (pos1_keystr, curv_keystr1,V)
    # res_data (pos2_keystr, curv_keystr2, V)

    pos = '.\\datafile\\bigscale\\curve'
    csv_in1 = pos + '\\'+curv_keystr1
    csv_out1 = pos + '\\_curve_input.csv'
    # c.txt2csv (csv_in1, csv_out1)  # 格式转换

    csv_in2 = pos + '\\'+curv_keystr2
    csv_out2 = pos + '\\_baseline_curve_input.csv'
    # c.txt2csv (csv_in2, csv_out2)

    curve_in = 'C:\\Users\\Judiths\\Documents\\MATLAB\\curve\\cmpr.dat'
    curve_csv_out = pos + '\\_curve_cmpr.csv'
    c.cmpr (csv_out1, csv_out2, curve_in, 15)
    c.txt2csv(curve_in, curve_csv_out)