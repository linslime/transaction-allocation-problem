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

print("list",list)
print("f",f)
print("w",w)

tempx1 = list[:n * m]
print("tempx1",tempx1)

tempx2 = [i[1] for i in tempx1]
print("tempx2",tempx2)


x = [tempx2[i:i+n] for i in range(0,m * n,n)]
print("x",x)

p = copy.deepcopy(x)

for i in range(m):
    for j in range(n):
        p[i][j] = (p[i][j] * w[j])
print(p)

with open("D:\Desktop\\p.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(p)

with open("D:\Desktop\\x.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(x)
