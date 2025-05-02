import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# problem for a given VPP_j

def lower_level_j(J, t,lmda_ES, lmda_EP, Omega_j, P_j_VPP_p_max, P_j_VPP_s_max, delta, P_MT_max, P_MT_down, 
                  P_MT_up, P_BS_max, SoC_min, SoC_max, P_WT_max, E_max, load_1, a_i, b_i, c_i, e_i):

    ################################################################
    # Define the model and variables
    ################################################################
    for j in J:
        # indexes
        T = [i for i in range(t)]

        MT_set = [i for i in range(Omega_j[0])]
        BS_set = [i for i in range(Omega_j[1])]
        WT_set = [i for i in range(Omega_j[2])]
        print("MT_set", MT_set)
        print("BS_set", BS_set)
        print("WT_set", WT_set)

        # P_D = [load_1]  # demand for MT, BS, WT

        # P_D_MT = P_D[0]
        # P_D_BS = P_D[1]
        # P_D_WT = P_D[2]

        # the model
        m = gp.Model("lower_level_j") 

        P_j_VPP_p = {}
        P_j_VPP_s = {}
        P_j_VPP = {}

        for t in T:
            P_j_VPP_p[t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"P_j_VPP_p_{t}")
            P_j_VPP_s[t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"P_j_VPP_s_{t}")
            P_j_VPP[t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"P_j_VPP_{t}")

        P_j_MT = {}
        SOC_j = {}
        P_j_WT = {}
        C_MT = {}
        C_BS = {}
        P_j_BS = {}


        for t in T:
            for i in MT_set:
                P_j_MT[i,t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"P_j_MT_{i}_{t}")
                C_MT[i,t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"C_MT_{i}_{t}")
            
            for i in BS_set:
                P_j_BS[i,t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"P_j_BS_{i}_{t}")
                SOC_j[i,t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"SOC_j_{i}_{t}")
                C_BS[i,t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"C_BS_{i}_{t}")

            for i in WT_set:
                P_j_WT[i,t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"P_j_WT_{i}_{t}")

        # objective value
        m.setObjective(
            gp.quicksum(lmda_EP[t] * P_j_VPP_p[t] - lmda_ES[t] * P_j_VPP_s[t] for t in T)
            + gp.quicksum(C_MT[i,t] for i in MT_set for t in T)
            + gp.quicksum(C_BS[i,t] for i in BS_set for t in T),
            GRB.MINIMIZE)
        
        #constraint 14
        for t in T:
            for i in MT_set:
                m.addConstr(C_MT[i,t] == a_i[i] * (P_j_MT[i,t] * delta) * (P_j_MT[i,t] * delta)
                                        + b_i[i] * P_j_MT[i,t] * delta + c_i[i])

        #constraint 15
        for t in T:
            for i in BS_set:
                m.addConstr(C_BS[i,t] == e_i[i] * (P_j_BS[i,t] * delta) * (P_j_BS[i,t] * delta))

        # constraints (numeration from the paper)
        # (16)
        for t in T:
            m.addConstr(P_j_VPP[t] ==  P_j_VPP_p[t] - P_j_VPP_s[t])

        # (17)
        # part 1
        for t in T:
            m.addConstr(P_j_VPP_p[t] <=  P_j_VPP_p_max[j])
            m.addConstr(0 <= P_j_VPP_p[t])
        # part 2
        for t in T:
            m.addConstr(P_j_VPP_s[t] <=  P_j_VPP_s_max[j])
            m.addConstr(0 <= P_j_VPP_s[t])

        # (18)
        for t in T:
            m.addConstr(
                P_j_VPP[t] 
                + gp.quicksum(P_j_MT[i, t] * delta for i in MT_set)
                + gp.quicksum(P_j_BS[i, t] * delta for i in BS_set)
                + gp.quicksum(P_j_WT[i, t] * delta for i in WT_set)
                ==
                load_1[t]
    )

        # (19)
        # part 1
        for t in T:
            for i in MT_set:
                m.addConstr(0 <= P_j_MT[i,t])
                m.addConstr(P_j_MT[i,t] <= P_MT_max[i])

        # part 2
        for t in T[:len(T)-1]:
            for i in MT_set:
                m.addConstr(
                    P_MT_down[i]*delta <= P_j_MT[i,t+1] - P_j_MT[i,t]
                )
                m.addConstr(
                    P_j_MT[i,t+1] - P_j_MT[i,t] <= P_MT_up[i]*delta 
                )

        # (20)
        # part 1
        for t in T:
            for i in BS_set:
                m.addConstr(-P_BS_max[j] <= P_j_BS[i,t])
        for t in T:
            for i in BS_set:
                m.addConstr(P_j_BS[i,t] <= P_BS_max[j])

        # part 2
        for t in T[1:]:
            for i in BS_set:
                m.addConstr(SOC_j[i,t] == SOC_j[i,t-1] - delta/E_max[j] * P_j_BS[i,t])

        # part 3
        for t in T:
            for i in BS_set:
                m.addConstr(SoC_min[j] <= SOC_j[i,t])
                m.addConstr( SOC_j[i,t] <= SoC_max[j])

        # part 4
        for i in BS_set:
            m.addConstr(SOC_j[i,0] == SOC_j[i,len(T)-1])


        # (21)
        for t in T:
            for i in WT_set:
                m.addConstr(0 <= P_j_WT[i,t])
                m.addConstr(P_j_MT[i,t] <= P_WT_max[j][t])

            
        m.optimize()

        # check the optimization status
        if m.status == GRB.OPTIMAL:
            print("\n===== Optimal Decision Variables =====\n")

            # VPP trading
            print("P_j_VPP_p:")
            for t in T:
                print(f"t={t}: {P_j_VPP_p[t].X:.4f}")

            print("\nP_j_VPP_s:")
            for t in T:
                print(f"t={t}: {P_j_VPP_s[t].X:.4f}")

            print("\nP_j_VPP:")
            for t in T:
                print(f"t={t}: {P_j_VPP[t].X:.4f}")

            # MT
            print("\nP_j_MT:")
            for i in MT_set:
                for t in T:
                    print(f"MT {i}, t={t}: {P_j_MT[i,t].X:.4f}")

            # BS
            print("\nP_j_BS:")
            for i in BS_set:
                for t in T:
                    print(f"BS {i}, t={t}: {P_j_BS[i,t].X:.4f}")

            print("\nSOC_j:")
            for i in BS_set:
                for t in T:
                    print(f"BS {i}, t={t}: {SOC_j[i,t].X:.2f}%")

            # WT
            print("\nP_j_WT:")
            for i in WT_set:
                for t in T:
                    print(f"WT {i}, t={t}: {P_j_WT[i,t].X:.4f}")

            # Costs
            print("\nC_MT:")
            for i in MT_set:
                for t in T:
                    print(f"MT {i}, t={t}: {C_MT[i,t].X:.4f}")

            print("\nC_BS:")
            for i in BS_set:
                for t in T:
                    print(f"BS {i}, t={t}: {C_BS[i,t].X:.4f}")

        else:
            print("Optimization was not successful. Status:", m.status)


        # the decision variables
        return None



def read_prices_from_excel(filename):
    df = pd.read_excel(filename)

    lmda_EP = df["λ_VPPp (Buy Price)"].tolist()
    lmda_ES = df["λ_VPPs (Sell Price)"].tolist()
    
    return lmda_EP, lmda_ES

# Example usage
lmda_EP, lmda_ES = read_prices_from_excel("upper_level_decisions.xlsx")
## Main function
def main():
    t = 1  # time periods 

    ##############################
    ### PARAMETERS
    ##############################

    # parameters (global parameters)
    P_j_VPP_p_max = [10] 
    P_j_VPP_s_max = [10] 

    delta = 1

    # parameters (the upper level as parameters)
    lmda_EP , lmda_ES = read_prices_from_excel("upper_level_decisions.xlsx")

    # VPP_j has 1 MT, 2 BS, 1 WT
    Omega_j = [1, 2, 1]

    # Demand P_D for each DER type in VPP1
    load_1 = [20, 1.9, 2.0, 2.1, 2.2, 2.4, 2.6, 2.8, 2.9, 3.0, 3.2, 3.4,3.2, 3.1, 3.0, 2.8, 2.6, 2.5, 2.4, 2.3, 2.2, 2.2, 2.1, 2.1]
    # P_D = [
    #     [load_1],  # MT
    #     [load_1],  # BS
    #     [load_1]   # WT
    # ]
    load_1 = load_1[:t]

    # Microturbine parameters for VPP1
    P_MT_max = [6.0]  # MW
    P_MT_down = [-3.5]  # MW/h
    P_MT_up = [3.5]  # MW/h

    # Battery storage parameters for VPP1
    P_BS_max = [0.6]  # MW
    E_max = [1]       # MWh

    SoC_min = [30]  # %
    SoC_max = [90]  # %


    P_WT_max = [[2, 1.5, 1.6, 1.8, 1.3, 0.6, 2.8, 3.3, 3.9, 4, 3.3, 2.9,2.7, 2, 0.2, 3.2, 5.1, 3.1, 1.8, 2, 1.3, 1, 2, 3.8]] #MW
    P_WT_max = [P_WT_max[0][:t]]
    
    a_i = [0.08]
    b_i = [0.90]
    c_i = [1.20]

    e_i = [0.05, 0.045]
    j= [0]
    lower_level_j(j, t, lmda_ES, lmda_EP, Omega_j, P_j_VPP_p_max, P_j_VPP_s_max, delta,
                  P_MT_max, P_MT_down, P_MT_up, P_BS_max, SoC_min, SoC_max,
                  P_WT_max, E_max, load_1, a_i, b_i, c_i, e_i)
    
    


    ## Solve an instance
if __name__ == "__main__":
    main()