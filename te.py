import gurobipy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

nn = 50
c = [2000, 2000]
JJ = range(nn)
II = range(len(c))
ff = []
ww = []

list = []

def readread():
    global ff
    global ww
    df = pd.read_excel(r'D:\Desktop\model5\one.xls',sheet_name='实例1')
    data = df.values.tolist()
    ff = [data[j][2] for j in JJ]
    ww = [data[j][1] for j in JJ]

def model(n):

    f = ff[:n]
    w = ww[:n]
    m = len(c)

    J = range(n)
    I = range(m)


    # 模型建立
    MODEL = gurobipy.Model()

    # 定义变量
    x = MODEL.addVars(2, n, vtype=gurobipy.GRB.BINARY, name="x")
    # z = MODEL.addVars(1, vtype=gurobipy.GRB.INTEGER, name="CC")
    z = MODEL.addVar(vtype=gurobipy.GRB.INTEGER, name='z')
    # 更新模型
    MODEL.update()

    # 目标函数
    MODEL.setObjective(z, gurobipy.GRB.MAXIMIZE)

    # 约束条件
    MODEL.addConstrs((c[i] >= gurobipy.quicksum([w[j] * x[i, j] for j in J]) for i in I), name="one")
    MODEL.addConstrs((1 >= gurobipy.quicksum(x[i, j] for i in I) for j in J), name="two")
    MODEL.addConstrs((z <= gurobipy.quicksum(x[i, j] * f[j] for j in J) for i in I), name="three")

    MODEL.Params.LogToConsole = False  # 显示求解过程
    # MODEL.Params.MIPGap = 0.0001  # 百分比界差
    # MODEL.Params.TimeLimit = 30  # 限制求解时间为 100s
    MODEL.optimize()

    list.append(MODEL.getVars()[-1].x)

if __name__ == "__main__":
    #读数据
    readread()

    for k in range(51):
        model(k)
    for k in list:
        print(k)

    plt.plot([i for i in range(51)], list, '-p', color='grey',
             marker='o',
             markersize=8, linewidth=2,
             markerfacecolor='red',
             markeredgecolor='grey',
             markeredgewidth=2)
    plt.show()