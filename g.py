import numpy as np
from gurobipy import *

MAXORDER = 50
MAXPLATFORM = 2

I = list(range(MAXORDER))
J = list(range(MAXPLATFORM))

fi = [17, 17, 17, 12, 40, 10, 29, 21, 46, 1, 11, 47, 16, 46, 18, 21, 28, 44, 8, 25, 42, 18, 37, 41, 43, 37, 48, 30, 29,
      29, 43, 22, 24, 32, 8, 1, 21, 22, 2, 33, 38, 45, 32, 37, 14, 48, 40, 42, 38, 38]
wi = [183, 3, 149, 87, 52, 72, 100, 186, 49, 5, 197, 136, 98, 85, 188, 153, 154, 43, 160, 123, 111, 93, 53, 9, 31, 114,
      12, 133, 9, 142, 77, 127, 97, 166, 53, 130, 147, 146, 92, 12, 6, 15, 107, 95, 195, 180, 190, 18, 88, 129]

ci = [2000, 2000]

fi = np.array(fi)
wi = np.array(wi)
ci = np.array(ci)

# try:
# Create a new model
m = Model("ass_mov")

# Create variables

x = m.addVars(I, J, vtype=GRB.BINARY,name="x")
z = m.addVar()

m.update()

m.setObjective(z, GRB.MAXIMIZE)


# Set objective
m.addConstrs((sum(x[i, j] for j in J) <= 1 for i in I), "c0")
m.addConstrs((sum(wi[i] * x[i, j]for i in I) <= ci[j] for j in J), "c1")
m.addConstrs((z <= sum(fi[i] * x[i, j] for i in I) for j in J), "c3")

m.optimize()

for v in m.getVars():
    print(v.varName, v.x)

#print('Obj:', m.objVal)

# except GurobiError:
#     print('Error reported')