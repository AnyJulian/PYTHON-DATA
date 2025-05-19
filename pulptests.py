import pulp

x1 = pulp.LpVariable('x1', lowBound=0)
x2 = pulp.LpVariable('x2', lowBound=0)

z = pulp.LpProblem("Cout_minimum", pulp.LpMinimize)

z += 3*x1 + x2, 'Function objective'
z += x1 + x2 >= 2, 'Constraint 1'
z += x1 + 2*x2 >= 5, 'Constraint 2'

z.solve()

for variable in z.variables():
    print(variable.name, '=', variable.varValue)

print(pulp.value(z.objective))

#matplotlib.pyplot
# plt.plot(x,y)

#Seaborn