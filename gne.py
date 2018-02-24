"""GNE model from essay Yuandou Wang*

One way to do it...
Original Author Yuandou Wang
Modified ***

To run this you need pyomo and the glpk solver installed, and need to be
inside of the virtual environment.
When these dependencies are installed you can solve this way (glpk is default):
    
    pyomo gne.py

"""

#Explicit importing makes it more clear what a user needs to define
#versus what is included within the pyomo library
#from _future_ import devision
from pyomo.environ import *

#Concrete Model
model = ConcreteModel()

#Parameters
model.providers=Set()
model.tasks=Set()

#ProfitRate={'Hw':3,'TengX':4.5,'Amaz':5}

model.v=Param(model.tasks, model.providers)
model.types=Param(model.tasks)
model.nums=Param(model.providers)
print model.v, model.types

#Decision Variables
model.x=Var(model.providers,domain=NonNegativeIntegers)

#Objective
def obj_expression(model):
    return summation(model.v, model.x)

model.obj = Objective(rule=obj_expression, sense = maximize)

#Constraints
def ax_constraint_rule(model,i):
    return sum(model.v[i][j] * model.x[j] for j in model.providers) > model.types[i]
model.AxbConstraint = Constraint(model.tasks, rule=ax_constraint_rule)    


#This is an optional code path that allows the script to be run outside of
#pyomo command-line.  For example:  python wyndor.py
if __name__ == '__main__':
   
    #This replicates what the pyomo command-line tools does
    from coopr.opt import SolverFactory
    opt = SolverFactory("glpk")
    instance = model.create()
    res_gne = opt.solve(instance)
    #sends results to stdout
    res_gne.write()
