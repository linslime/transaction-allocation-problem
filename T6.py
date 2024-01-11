import gurobipy
import pandas as pd


n = 200#############################################
c = [208 for i in range(100)]#####################################################

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
    df = pd.read_excel(r'D:\Desktop\model5\one.xls',sheet_name='实例8')###################################################################
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
    x = MODEL.addVars(m,n,vtype=gurobipy.GRB.BINARY, name="x")
    k = MODEL.addVars(n,vtype=gurobipy.GRB.CONTINUOUS,name="k")
    u = MODEL.addVar(vtype=gurobipy.GRB.BINARY,name="u")

    full = MODEL.addVars(n,vtype=gurobipy.GRB.CONTINUOUS,name="full")
    v = MODEL.addVar(vtype=gurobipy.GRB.BINARY,name="v")
    #z = MODEL.addVars(1, vtype=gurobipy.GRB.INTEGER, name="CC")
    #z = MODEL.addVar(vtype=gurobipy.GRB.INTEGER, name='z')
    #更新模型
    MODEL.update()

    #目标函数
    MODEL.setObjective(gurobipy.quicksum([gurobipy.quicksum([f[j] * x[i,j] for j in J]) for i in I]), gurobipy.GRB.MINIMIZE)

    #约束条件
    MODEL.addConstrs((c[i] <= gurobipy.quicksum([w[j] * x[i,j] for j in J]) for i in I),name="one")
    MODEL.addConstrs((1 <= gurobipy.quicksum(x[i,j] for i in I) for j in J),name="two")

    #MODEL.addConstrs((k[j] == gurobipy.min_(1,(gurobipy.quicksum(x[i,j] for i in I) - 1)) for j in J),name="haha")
    MODEL.addConstrs((k[j] <= 1 for j in J),name="three")
    MODEL.addConstrs((k[j] <= (gurobipy.quicksum(x[i,j] for i in I) - 1) for j in J ),name="four")
    MODEL.addConstrs(((k[j] + M * u) >= 1 for j in J),name="five")
    MODEL.addConstrs(((k[j] + M * (1 - u)) >= (gurobipy.quicksum(x[i,j] for i in I) - 1) for j in J),name="six")

    MODEL.addConstrs((full[i] <= 1 for i in I),name="seven")
    MODEL.addConstrs((full[i] <= (gurobipy.quicksum(w[j] * x[i,j] for j in J) - c[i]) for i in I),name="eight")
    MODEL.addConstrs(((full[i] + M * v) >= 1 for i in I),name="nine")
    MODEL.addConstrs(((full[i] + M * (1 - v)) >= (gurobipy.quicksum(w[j] * x[i,j] for j in J) - c[i]) for i in I),name="ten")

    MODEL.addConstrs((full[i] == gurobipy.quicksum(x[i,j] * k[j] for j in J) for i in I),name="eleven")
    # MODEL.addConstrs((z <= gurobipy.quicksum(x[i,j] * f[j] for j in J) for i in I) , name="three")


    # MODEL.Params.LogToConsole = True  # 显示求解过程
    # MODEL.Params.MIPGap = 0.0001  # 百分比界差
    # MODEL.Params.TimeLimit = 10  # 限制求解时间为 100s
    MODEL.optimize()

    for v in MODEL.getVars():
        print(v.varName, v.x)
