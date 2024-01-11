import gurobipy
import pandas as pd
import csv
import copy

n = 50
m = 50

J = range(n)
I = range(m)

df = pd.read_excel(r'D:\Desktop\three.xls',sheet_name='Sheet1')
list = df.values.tolist()

df = pd.read_excel(r'D:\Desktop\model5\one.xls',sheet_name='实例6')###################################################################
data = df.values.tolist()
f = [data[j][2] for j in J]
w = [data[j][1] for j in J]

tempx1 = list[:n * m]
print("tempx1",tempx1)

tempx2 = [i[1] for i in tempx1]
print("tempx2",tempx2)

x = [tempx2[i:i+n] for i in range(0,m * n,n)]
print(x)

for i in x:
    print(i)

p = [[w[j] * x[i][j] for j in range(n)] for i in range(m)]

sump = [sum(p[i]) for i in range(m)]
for i in sump:
    print(i)
print("p",p)

print("sump",sump)

# for i in x:
#     print(i)
k = [min(sum([x[i][j] for i in range(m)]) - 1 ,1) for j in range(n)]
print(len(x))

print(sum([x[i][0] for i in range(m)]))

print(list[n * m:])

print(k)

with open("D:\Desktop\\p.csv", "w" , newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(p)
pp = copy.deepcopy(p)
for i in range(n):
    for j in range(m):
        if x[i][j] == 1 and k[j] == 1:
            pp[i][j] = p[i][j] - (sump[i] - 100)

with open("D:\Desktop\\pp.csv", "w" , newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(pp)