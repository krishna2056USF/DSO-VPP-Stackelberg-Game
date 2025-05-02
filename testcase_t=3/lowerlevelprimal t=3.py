import gurobipy as gp
from gurobipy import GRB

model = gp.Model("Lower_Level_VPP")

# Time periods
T = [1, 2, 3]

# Time step
Δt = 1

λ_EP = [0.8,0.9,0.8] 
λ_ES = [0.34,0.34,0.34]   

# Demand for each time period
PD = [5.3, 2.2, 8] 

# Cost coefficients
a1, b1, c1 = 1, 1, 1
e1, e2 = 0.5, 0.3

# Capacity limits
PVPP_p_max = 3
PVPP_s_max = 3
PMT_max = 5
PMT_down, PMT_up = 1, 1
PBS1_max = 2
PBS2_max = 2
E1_max = 2
E2_max = 3
SOC1_min, SOC1_max = 0.2, 1.0
SOC2_min, SOC2_max = 0.2, 0.98
SOC1_0 = 0.5
SOC2_0 = 0.5
PWT_max = 1.5

# Decision variables
PVPP_p = model.addVars(T, name="PVPP_p", lb=0, ub=PVPP_p_max)
PVPP_s = model.addVars(T, name="PVPP_s", lb=0, ub=PVPP_s_max)
PVPP = model.addVars(T, name="PVPP")
PMT = model.addVars(T, name="PMT", lb=0, ub=PMT_max)
PBS1 = model.addVars(T, name="PBS1", lb=-PBS1_max, ub=PBS1_max)
PBS2 = model.addVars(T, name="PBS2", lb=-PBS2_max, ub=PBS2_max)
SOC1 = model.addVars(T, name="SOC1", lb=SOC1_min, ub=SOC1_max)
SOC2 = model.addVars(T, name="SOC2", lb=SOC2_min, ub=SOC2_max)
PWT = model.addVars(T, name="PWT", lb=0, ub=PWT_max)

# Objective function
model.setObjective(
    gp.quicksum(λ_EP[t-1] * PVPP_p[t] - λ_ES[t-1] * PVPP_s[t] for t in T) +
    gp.quicksum(a1 * (PMT[t] * Δt)**2 + b1 * PMT[t] * Δt + c1 for t in T) +
    gp.quicksum(e1 * (PBS1[t] * Δt)**2 + e2 * (PBS2[t] * Δt)**2 for t in T),
    GRB.MINIMIZE
)

# Constraints
for t in T:
    # PVPP flow definition
    model.addConstr(PVPP[t] == PVPP_p[t] - PVPP_s[t], name=f"PVPP_flow_{t}")
    # Power balance
    model.addConstr(PVPP[t] + (PMT[t] + PBS1[t] + PBS2[t] + PWT[t]) * Δt == PD[t-1] * Δt, name=f"power_balance_{t}")

# Ramp rate constraints for MT1
model.addConstr(PMT[2] - PMT[1] <= PMT_up * Δt)
model.addConstr(PMT[2] - PMT[1] >= -PMT_down * Δt)
model.addConstr(PMT[3] - PMT[2] <= PMT_up * Δt)
model.addConstr(PMT[3] - PMT[2] >= -PMT_down * Δt)

# SOC updates for BS1
model.addConstr(SOC1[1] == SOC1_0 - (Δt / E1_max) * PBS1[1])
model.addConstr(SOC1[2] == SOC1[1] - (Δt / E1_max) * PBS1[2])
model.addConstr(SOC1[3] == SOC1[2] - (Δt / E1_max) * PBS1[3])
model.addConstr(SOC1[3] == SOC1_0)

# SOC updates for BS2
model.addConstr(SOC2[1] == SOC2_0 - (Δt / E2_max) * PBS2[1])
model.addConstr(SOC2[2] == SOC2[1] - (Δt / E2_max) * PBS2[2])
model.addConstr(SOC2[3] == SOC2[2] - (Δt / E2_max) * PBS2[3])
model.addConstr(SOC2[3] == SOC2_0)

# Solve the model
model.optimize()

# Display results
if model.status == GRB.OPTIMAL:
    print("\nOptimal Solution:")
    for var in model.getVars():
        print(f"{var.VarName}: {var.X}")
    print(f"Objective Value: {model.ObjVal}")
else:
    print("No optimal solution found.")
