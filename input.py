#-*-  coding:utf-8 -*-
#coding=utf-8
import datetime
import numpy as np
from scipy.optimize import linear_sum_assignment
import km


# we need handle 32 datasets, and the matrix 3 x 3 for each dataset. 
h1=[6.994,7.221,7.342,7.451,7.440,7.452,7.501,7.684,7.773,7.771,7.969,8.342,8.558,8.737,8.760,8.689,8.829,8.791,8.905,8.884,8.907,8.782,8.801,8.872,8.851,8.964,9.014,9.151,9.120,9.213,9.201,9.187,9.175]
h2=[14.234,14.715,14.928,14.349,14.031,13.821,13.622,13.701,13.783,13.723,13.543,13.261,13.102,13.171,12.938,12.724,12.893,12.715,12.517,12.310,12.124,12.272,12.127,12.105,12.113,12.108,12.078,12.057,12.063,12.054,12.046,12.048,12.037]
h3=[31.875,32.225,32.938,33.164,33.505,33.422,33.414,33.515,33.388,33.052,32.941,32.981,33.132,33.019,33.171,33.206,33.328,33.423,33.545,34.027,34.101,34.312,34.564,34.652,34.689,34.671,34.795,34.806,34.821,34.987,34.934,35.136,35.119]

t1=[6.524,6.481,6.442,6.468,6.397,6.384,6.373,6.382,6.293,6.172,6.153,6.144,6.004,6.217,6.060,6.124,5.949,5.781,5.723,5.824,5.843,5.792,5.791,5.785,5.793,5.784,5.772,5.770,5.683,5.690,5.671,5.652,5.653]
t2=[13.873,13.955,13.924,13.868,13.801,13.795,13.862,13.884,13.943,14.025,14.213,14.235,14.262,14.201,14.211,14.224,14.253,14.261,14.237,14.279,14.284,14.332,14.361,14.368,14.355,14.360,14.371,14.379,14.384,14.381,14.390,14.385,14.397]
t3=[32.135,32.005,31.978,31.994,31.785,31.692,31.604,31.524,31.608,31.482,31.441,31.354,31.422,31.279,31.261,31.286,31.338,31.343,31.315,31.277,31.231,31.342,31.307,31.315,31.304,31.289,31.294,31.281,31.289,31.271,31.265,31.260,31.259]

a1=[7.234,7.196,7.240,7.237,7.265,7.288,7.280,7.301,7.294,7.317,7.330,7.327,7.329,7.319,7.328,7.337,7.344,7.349,7.348,7.341,7.437,7.426,7.445,7.431,7.432,7.451,7.446,7.455,7.451,7.459,7.462,7.463,7.461]
a2=[14.334,14.528,14.449,14.631,14.761,14.692,14.774,14.883,14.903,15.013,15.062,15.157,15.211,15.210,15.341,15.393,15.475,15.417,15.500,15.474,15.482,15.442,15.512,15.509,15.520,15.518,15.523,15.536,15.529,15.531,15.538,15.541,15.545]
a3=[27.381,27.521,27.938,28.071,28.205,28.432,28.504,28.525,28.648,28.752,28.841,28.784,28.796,28.839,28.817,28.826,28.871,29.024,29.445,29.320,29.531,29.442,29.550,29.549,29.557,29.608,29.602,29.628,29.629,29.675,29.641,29.712,29.661]

# create tuples
def typeI(h1,t1,a1):
    type1 = []
    for i in range(len(h1)):
        type1.append((h1[i],t1[i],a1[i]))
    return type1
#type1 = typeI(h1,t1,a1)

def typeII(h2,t2,a2):
    type2 = []
    for j in range(len(h2)):
         type2.append((h2[j],t2[j],a2[j]))
    return type2
#type2 = typeII(h2,t2,a2)

def typeIII(h3,t3,a3):
    type3 = []
    for k in range(len(h3)):
        type3.append((h3[k],t3[k],a3[k]))
    return type3
#type3 = typeIII(h3,t3,a3)

# create a special matrix from 3 types, and the result as 
#a input execution time matrix for the schedule strategies
def ExeTimeMatri(index, type1, type2, type3):
    for i in type1:
        type1[type1.index(i)] = list(i)
    for j in type2:
        type2[type2.index(j)] = list(j)
    for k in type3:
        type3[type3.index(k)] = list(k)
    a = [type1[index], type2[index], type3[index]]
    v = np.array(a)
    return v
#v0 = ExeTimeMatri(0, type1, type2, type3)

Providers = ['Huawei', 'Tengxun', 'Amazon']
# Huawei Cloud: s2(1,2) 0.15 yuan/h ;
# Tengxun Cloud: t2(1,2) 0.16 yuan/h   ;
# Amazon Cloud: t2.small(1,2) 0.152 yuan/h ($0.023/h)
ProfitRate = {'Huawei':0.15, 'Tengxun':0.16, 'Amazon':0.152}
TaskTypes = ['typeI', 'tyepII', 'typeIII']

def SecondPerUnit(Providers, TaskTypes, v0):
    x0 = {}
    for i in Providers:
        for j in TaskTypes:
            x0.update(dict([((j,i),v0[TaskTypes.index(j)][Providers.index(i)])]))
    return x0

def ProfitPerUnit(TaskTypes, Providers,v0):
    x0 = {}
    for j in TaskTypes:
        for i in Providers:
            x0.update(dict([((j,i),ProfitRate[i]*v0[TaskTypes.index(j)][Providers.index(i)])]))
    return x0	

def ProfitMatri(TaskTypes, Providers, v0):
    for j in TaskTypes:
        for i in Providers:
            v0[TaskTypes.index(j)][Providers.index(i)]=v0[TaskTypes.index(j)][Providers.index(i)]*ProfitRate[i]
    return v0

type1 = typeI(h1,t1,a1)
type2 = typeII(h2,t2,a2)
type3 = typeIII(h3,t3,a3)
v0 = ExeTimeMatri(0, type1, type2, type3)
SecondPerUnit = SecondPerUnit(Providers, TaskTypes, v0)
ProfitPerUnit = ProfitPerUnit(TaskTypes, Providers, v0)
p0 = ProfitMatri(TaskTypes, Providers, v0)


for i in range(33):
    a = np.zeros((3,3))
    b = np.zeros((3,3))

    v = ExeTimeMatri(i, type1,type2,type3)# execution time matrix
    p = ProfitMatri(TaskTypes, Providers, v)# profit matrix
    v_row_ind, v_col_ind = linear_sum_assignment(v)
    v_min_sum = v[v_row_ind, v_col_ind].sum()
    p_row_ind, p_col_ind = km.km_max(p)
    p_max_sum = p[p_row_ind, p_col_ind].sum()
    for j in range(3):
#	    a[v_row_ind[j]][v_col_ind[j]] = 1
#	    b[p_row_ind[j]][p_col_ind[j]] = 1
        a[v_row_ind[j]][v_col_ind[j]] = v[v_row_ind[j]][v_col_ind[j]]
        b[p_row_ind[j]][p_col_ind[j]] = p[p_row_ind[j]][p_col_ind[j]]

        print(a)
        print(b)
        for x in range(3):
            for y in range(3):
                print(a[x][y])
    print(datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S.%f'))
    fa = open('res.txt', 'a')
    time = datetime.datetime.now().strftime('%Y-%m-%d:%H:%M:%S')
    fa.write(time+'\n')
    fa.write('\ta'+str(i)+ '\t'+str(v_min_sum) +
            '\t\t\tb'+str(i)+'\t'+str(p_max_sum)+'\n')
    for k in  range(3):
        fa.write('\t'+str(a[k,:])+'\t\t\t'+str(b[k,:])+'\n')
    fa.close()