"""Wyndor model from Hillier and Hillier *Introduction to Management Science*

One way to do it...
Original Author dlw
Modified ndg 

To run this you need pyomo and the glpk solver installed, and need to be
inside of the virtual environment.
When these dependencies are installed you can solve this way (glpk is default):
    
    pyomo wyndor.py

"""

#Explicit importing makes it more clear what a user needs to define
#versus what is included within the pyomo library
from coopr.pyomo import (ConcreteModel, Objective, Var, NonNegativeIntegers, maximize, Constraint)

Products = ['Doors', 'Windows', 'Tables']
ProfitRate = {'Doors':0.300, 'Windows':0.500, 'Tables':0.430}
Plants = ['Door Fab', 'Window Fab', 'Assembly']
HoursAvailable = {'Door Fab':4, 'Window Fab':4, 'Assembly':3}
HoursPerUnit = {('Doors','Door Fab'):0.21, ('Windows', 'Window Fab'):0.52,
                ('Doors','Assembly'):0.23, ('Windows', 'Assembly'):0.32,
                ('Windows', 'Door Fab'):0.30,('Doors', 'Window Fab'):0.20,
                ('Tables','Door Fab'):0.29, ('Tables','Window Fab'):0.34,
                ('Tables', 'Assembly'):0.41}

#Concrete Model
model = ConcreteModel()

#Decision Variables
model.WeeklyProd = Var(Products, within=NonNegativeIntegers)

#Objective
model.obj = Objective(expr=
            sum(ProfitRate[i] * model.WeeklyProd[i] for i in Products),
            sense = maximize)
for i in Products:
    print model.WeeklyProd[i]

def CapacityRule(model, p):
    """User Defined Capacity Rule
    
    Accepts a pyomo Concrete Model as the first positional argument,
    and and a plant index as a second positional argument
    """
    
    return sum(HoursPerUnit[i,p] * model.WeeklyProd[i] for i in Products) <= HoursAvailable[p]

#This statement is what Pyomo needs to generate one constraint for each plant
model.Capacity = Constraint(Plants, rule = CapacityRule)

#This is an optional code path that allows the script to be run outside of
#pyomo command-line.  For example:  python wyndor.py
if __name__ == '__main__':
   
    #This replicates what the pyomo command-line tools does
    from coopr.opt import SolverFactory
    opt = SolverFactory("glpk")
    instance = model.create()
    results = opt.solve(instance)
    #sends results to stdout
    results.write()
