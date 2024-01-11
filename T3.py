import gurobipy
import pandas as pd
import csv

n = 200#############################################
c = [416 for i in range(50)]#####################################################

f = []
w = []
m = len(c)
# print(m)
J = range(n)
I = range(m)

def readread():
    global f
    global w
    df = pd.read_excel(r'D:\Desktop\model5\one.xls',sheet_name='实例7')###################################################################
    data = df.values.tolist()
    f = [data[j][2] for j in J]
    w = [data[j][1] for j in J]
    print(f)
    print(w)

if __name__ == "__main__":
    #读数据
    readread()

    #模型建立
    MODEL = gurobipy.Model()

    #定义变量
    x = MODEL.addVars(m, n, lb=0.0, ub=1, vtype=gurobipy.GRB.CONTINUOUS, name="x")
    p = MODEL.addVars(m, n, vtype=gurobipy.GRB.BINARY, name="p")

    #更新模型
    MODEL.update()

    #目标函数
    MODEL.setObjective(sum([sum([f[j] * p[i,j] for j in J]) for i in I]), gurobipy.GRB.MINIMIZE)

    #约束条件
    MODEL.addConstrs((c[i] == gurobipy.quicksum([w[j] * x[i,j] for j in J]) for i in I),name="one")
    MODEL.addConstrs((1 == gurobipy.quicksum(x[i,j] for i in I) for j in J),name="two")
    MODEL.addConstrs((x[i,j] <= p[i,j] for i in I for j in J),name="three")



    # MODEL.Params.LogToConsole = True  # 显示求解过程
    # MODEL.Params.MIPGap = 0.0001  # 百分比界差
    # MODEL.Params.TimeLimit = 500  # 限制求解时间为 100s
    MODEL.optimize()

    list = []
    for v in MODEL.getVars():
        list.append([v.varName, v.x])
    print(list)
    with open("D:\Desktop\\three.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list)
