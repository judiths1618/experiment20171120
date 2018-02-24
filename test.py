import numpy as np
from scipy import optimize

from scipy.optimize import linear_sum_assignment
def f(x):
    return -np.exp(-(x-0.7)**2)
res = optimize.minimize_scalar(f)
#res.success
x_min=res.x
print x_min

cost=np.array([[1,2,3,2,6,4.5,9,2],[4,5,6,0.23,9.2,1.7,5.2,7.3],[7,8,9,2.3,4.5,6.7,2.12,5]])
row_ind, col_ind = linear_sum_assignment(cost)
print row_ind, col_ind, cost[row_ind, col_ind].sum()

