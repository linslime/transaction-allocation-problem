import gurobipy
import pandas as pd

n = 200  #############################################
c = [416 for i in range(50)]  #####################################################

f = []
w = []
m = len(c)
# print(m)
J = range(n)
I = range(m)
M = 10000000000

def readread():
    global f
    global w
    df = pd.read_excel(r'D:\Desktop\model5\one.xls',sheet_name='实例7')  ###################################################################
    data = df.values.tolist()
    f = [data[j][2] for j in J]
    w = [data[j][1] for j in J]
    # print(f)
    # print(w)


if __name__ == "__main__":
    # 读数据
    readread()

    # 模型建立
    MODEL = gurobipy.Model()

    # 定义变量
    x = MODEL.addVars(m, n, lb=0.0, ub=1, vtype=gurobipy.GRB.CONTINUOUS, name="x")
    p = MODEL.addVars(m, n, vtype=gurobipy.GRB.BINARY, name="p")

    # k = MODEL.addVars(n, vtype=gurobipy.GRB.CONTINUOUS, name="k")
    # u = MODEL.addVars(n, vtype=gurobipy.GRB.BINARY, name="u")

    # full = MODEL.addVars(m, vtype=gurobipy.GRB.CONTINUOUS, name="full")
    # v = MODEL.addVars(m,vtype=gurobipy.GRB.BINARY, name="v")
    # 更新模型
    MODEL.update()

    # 目标函数
    MODEL.setObjective(sum([sum([f[j] * p[i, j] for j in J]) for i in I]), gurobipy.GRB.MINIMIZE)

    # 约束条件
    MODEL.addConstrs((c[i] == gurobipy.quicksum([w[j] * x[i, j] for j in J]) for i in I), name="one")
    MODEL.addConstrs((1 == gurobipy.quicksum(x[i, j] for i in I) for j in J), name="two")
    MODEL.addConstrs((x[i, j] <= p[i, j] for i in I for j in J), name="three")

    # MODEL.addConstrs((k[j] <= 1 for j in J), name="three")
    # MODEL.addConstrs((k[j] <= (gurobipy.quicksum(p[i, j] for i in I) - 1) for j in J), name="four")
    # MODEL.addConstrs(((k[j] + M * u[j]) >= 1 for j in J), name="five")
    # MODEL.addConstrs(((k[j] + M * (1 - u[j])) >= (gurobipy.quicksum(p[i, j] for i in I) - 1) for j in J), name="six")

    # MODEL.addConstrs((full[i] <= 1 for i in I), name="seven")
    # MODEL.addConstrs((full[i] <= (gurobipy.quicksum(w[j] * p[i, j] for j in J) - c[i]) for i in I), name="eight")
    # MODEL.addConstrs(((full[i] + M * v[i]) >= 1 for i in I), name="nine")
    # MODEL.addConstrs(((full[i] + M * (1 - v[i])) >= (gurobipy.quicksum(w[j] * p[i, j] for j in J) - c[i]) for i in I),name="ten")

    # MODEL.addConstrs((3 >= gurobipy.quicksum(p[i, j] * k[j] for j in J) for i in I), name="eleven")
    # MODEL.addConstrs((400 >= gurobipy.quicksum(p[i, j] * k[j] for j in J) for i in I), name="eleven")
    # MODEL.Params.LogToConsole = True  # 显示求解过程
    # MODEL.Params.MIPGap = 0.0001  # 百分比界差
    # MODEL.Params.TimeLimit = 3  # 限制求解时间为 100s
    MODEL.optimize()

    for v in MODEL.getVars():
        print(v)
