# coding = utf-8
import time

import curve_data as c

s = time.time()

pos1_keystr = '.\\datafile\\bigscale\\+'
pos2_keystr = '.\\datafile\\bigscale\\baseline+'

curv_keystr1 = '_curve_input.dat'
curv_keystr2 = '_baseline_curve_input.dat'
pos = '.\\datafile\\bigscale\\curve'
csv_in1 = pos + '\\'+curv_keystr1
csv_out1 = pos + '\\_curve_input.csv'

csv_in2 = pos + '\\'+curv_keystr2
csv_out2 = pos + '\\_baseline_curve_input.csv'
set_num = 20

# no_task = c.aver_per_set (c.cols (csv_out1, 'no_task'), set_num)
# stg = c.aver_per_set (c.cols (csv_out1, 'st_game'), set_num)

# ms_al1 = c.aver_per_set (c.cols (csv_out1, 'makespan'), set_num)
wl_al1 = c.aver_per_set (c.cols (csv_out1, 'workload'), set_num)
prf_al1 = c.aver_per_set (c.cols (csv_out1, 'profit'), set_num)

# ms_al2 = c.aver_per_set (c.cols (csv_out2, 'makespan'), set_num)
wl_al2 = c.aver_per_set (c.cols (csv_out2, 'workload'), set_num)
prf_al2 = c.aver_per_set (c.cols (csv_out2, 'profit'), set_num)

e = time.time()
print('COST: %.3f' %(e-s))
