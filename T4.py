import gurobipy
import pandas as pd
import csv

n = 50#############################################
#c = [100,200,300,400,500,500,600,700,800,900]#####################################################
c = [100 for i in range(50)]

f = []
w = []
m = len(c)
# print(m)
J = range(n)
I = range(m)
M = 100000000

def readread():
    global f
    global w
    df = pd.read_excel(r'D:\Desktop\model5\one.xls',sheet_name='实例6')###################################################################
    data = df.values.tolist()
    f = [data[j][2] for j in J]
    w = [data[j][1] for j in J]
    # print(f)
    # print(w)

if __name__ == "__main__":
    #读数据
    readread()

    #模型建立
    MODEL = gurobipy.Model()

    #定义变量
    x = MODEL.addVars(m,n,vtype=gurobipy.GRB.BINARY, name="x")
    k = MODEL.addVars(n,vtype=gurobipy.GRB.BINARY,name="k")
    # u = MODEL.addVars(n,vtype=gurobipy.GRB.BINARY,name="u")
    #
    # full = MODEL.addVars(m,vtype=gurobipy.GRB.BINARY,name="full")
    # v = MODEL.addVars(m,vtype=gurobipy.GRB.BINARY,name="v")

    uu = MODEL.addVars(m,n,vtype=gurobipy.GRB.BINARY,name="uu")
    # ha = MODEL.addVars(n,vtype=gurobipy.GRB.CONTINUOUS,name="ha")
    #z = MODEL.addVars(1, vtype=gurobipy.GRB.INTEGER, name="CC")
    #z = MODEL.addVar(vtype=gurobipy.GRB.INTEGER, name='z')
    #更新模型
    MODEL.update()

    #目标函数
    MODEL.setObjective(gurobipy.quicksum([gurobipy.quicksum([f[j] * x[i,j] for j in J]) for i in I]), gurobipy.GRB.MINIMIZE)

    #约束条件
    MODEL.addConstrs((c[i] <= gurobipy.quicksum([w[j] * x[i,j] for j in J]) for i in I),name="one")
    MODEL.addConstrs((1 <= gurobipy.quicksum(x[i,j] for i in I) for j in J),name="two")
    MODEL.addConstrs(((gurobipy.quicksum(k[j] * x[i,j] * w[j] for j in J) >= gurobipy.quicksum(x[i,j] * w[j] for j in J) - c[i]) for i in I),name="haha")
    # MODEL.addConstrs(((gurobipy.quicksum(x[i,j] for i in I) * w[j] - gurobipy.quicksum(k[j] * x[i,j] * (gurobipy.quicksum(x[i,j] * w[j] for j in J) - c[i]) for i in I) == w[j]) for j in J),name="h")

    # MODEL.addConstrs(((gurobipy.quicksum(x[i, j] for i in I) * w[j] + gurobipy.quicksum(uu[i,j] * c[i] for i in I) - gurobipy.quicksum(uu[i,j] * x[i, jj] * w[jj] for i in I for jj in J ) == w[j]) for j in J),name="h")
    # MODEL.addConstrs((uu[i,j] <= k[i] for i in I for j in J),name="uu1")
    # MODEL.addConstrs((uu[i,j] <= x[i,j] for i in I for j in J),name="uu2")
    # MODEL.addConstrs((uu[i,j] >= k[i] + x[i,j] - 1 for i in I for j in J) ,name="uu3")

    MODEL.addConstrs((k[j] <= 1 for j in J),name="three")
    MODEL.addConstrs((k[j] <= (gurobipy.quicksum(x[i,j] for i in I) - 1) for j in J ),name="four")
    MODEL.addConstrs(((k[j] + M * u[j]) >= 1 for j in J),name="five")
    MODEL.addConstrs(((k[j] + M * (1 - u[j])) >= (gurobipy.quicksum(x[i,j] for i in I) - 1) for j in J),name="six")
    #
    # MODEL.addConstrs((full[i] <= 1 for i in I),name="seven")
    # MODEL.addConstrs((full[i] <= (gurobipy.quicksum(w[j] * x[i,j] for j in J) - c[i]) for i in I),name="eight")
    # MODEL.addConstrs(((full[i] + M * v[i]) >= 1 for i in I),name="nine")
    # MODEL.addConstrs(((full[i] + M * (1 - v[i])) >= (gurobipy.quicksum(w[j] * x[i,j] for j in J) - c[i]) for i in I),name="ten")
    #
    # MODEL.addConstrs((full[i] == gurobipy.quicksum(x[i,j] * k[j] for j in J) for i in I),name="eleven")
    # MODEL.addConstrs((z <= gurobipy.quicksum(x[i,j] * f[j] for j in J) for i in I) , name="three")


    # MODEL.Params.LogToConsole = False  # 显示求解过程
    # MODEL.Params.MIPGap = 0.0001  # 百分比界差
    # MODEL.Params.TimeLimit = 10  # 限制求解时间为 100s
    MODEL.optimize()
    # list = []
    # for v in MODEL.getVars():
    #     list.append([v.varName,int(v.x)])
    # print(list)
    # with open("D:\Desktop\\three.csv", "w" , newline="") as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(list)

