from gurobipy import Model, GRB

# Sets
T = [1, 2, 3]   # Time periods
J = [1]         # Single VPP for test case

# Parameters
                 
lambda_CEP = {1: 0.4, 2: 0.6, 3: 1.4}   # Selling price to wholesale market
lambda_CES = {1: 0.2, 2: 0, 3: 0}   # Buying price from wholesale market
M = 100  # Big-M value

# Fixed VPP responses (from lower-level test case)
P_VPP_p = {
    (1, 1): 2.999999999999093,
    (1, 2): 2.999999999997612,
    (1, 3): 2.9999999999989884
}

P_VPP_s = {
    (1, 1): 0.0,
    (1, 2): 0.0,
    (1, 3): 0.0
}


# Initialize model
model = Model('DSO_Upper_Level_Test')

# Decision Variables
lambda_ES = {t: model.addVar(lb=lambda_CES[t], ub=lambda_CEP[t], name=f"lambda_ES_{t}") for t in T}
lambda_EP = {t: model.addVar(lb=lambda_CES[t], ub=lambda_CEP[t], name=f"lambda_EP_{t}") for t in T}

P_DSO = {t: model.addVar(name=f"P_DSO_{t}") for t in T}
P_DSO_p = {t: model.addVar(lb=0, name=f"P_DSO_p_{t}") for t in T}
P_DSO_s = {t: model.addVar(lb=0, name=f"P_DSO_s_{t}") for t in T}

z = {t: model.addVar(vtype=GRB.BINARY, name=f"z_{t}") for t in T}

# Constraints
for t in T:
    # Power balance
    model.addConstr(P_DSO[t] == sum(P_VPP_p[j, t] - P_VPP_s[j, t] for j in J), name=f"Power_Balance_{t}")

    # Big-M constraints for Purchase Mode
    model.addConstr(-M * (1 - z[t]) <= P_DSO[t], name=f"BM_Purch_LB_{t}")
    model.addConstr(P_DSO[t] <= M * z[t], name=f"BM_Purch_UB_{t}")
    model.addConstr(-M * (1 - z[t]) <= P_DSO_p[t] - P_DSO[t], name=f"BM_Purch_Link_{t}")
    model.addConstr(P_DSO_p[t] <= M * z[t], name=f"BM_Purch_PBound_{t}")

    # Big-M constraints for Sale Mode
    model.addConstr(-M * (1 - z[t]) <= P_DSO_s[t], name=f"BM_Sale_LB_{t}")
    model.addConstr(P_DSO_s[t] <= M * (1 - z[t]), name=f"BM_Sale_UB_{t}")
    model.addConstr(-M * z[t] <= P_DSO_s[t] + P_DSO[t], name=f"BM_Sale_Link_{t}")

# Objective Function
profit = sum(
    lambda_CES[t] * P_DSO_s[t] - lambda_CEP[t] * P_DSO_p[t] +
    lambda_EP[t] * sum(P_VPP_p[j, t] for j in J) -
    lambda_ES[t] * sum(P_VPP_s[j, t] for j in J)
    for t in T
)

model.setObjective(profit, GRB.MAXIMIZE)

# Optimize
model.optimize()

# Display Results
for v in model.getVars():
    print(f"{v.VarName}: {v.X}")

print(f"Optimal Profit: {model.ObjVal}")
