import gurobipy as gp
from gurobipy import GRB

def upper_level(t, j, P_DSO_s, P_DSO_p, P_VPP_p, P_VPP_s, lmda_CES, lmda_CEP, bigM):

    ################################################################
    # Define the model and variables
    ################################################################

    # indexes
    T = [i for i in range(t)]
    J = [i for i in range(j)]


    # the model
    m = gp.Model("upper_level") 

    # the decision variables

    # continuous variables
    lmda_ES = {}
    lmda_EP = {}
    P_DSO = {}
    for t in T:
        lmda_ES[t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"lmda_ES_{t}")
        lmda_EP[t] = m.addVar(vtype=GRB.CONTINUOUS, name=f"lmda_EP_{t}")

        P_DSO[t] =  m.addVar(vtype=GRB.CONTINUOUS, name=f"P_DSO_{t}")

    # integer 0-1 variables
    z_1 = {}
    z_2 = {}
    for t in T:
        z_1[t] = m.addVar(vtype=GRB.BINARY, name=f"z_1_{t}")
        z_2[t] = m.addVar(vtype=GRB.BINARY, name=f"z_2_{t}")

    # objective value
    m.setObjective(
        gp.quicksum(lmda_CES[t]*P_DSO_s[t] - lmda_CEP[t]*P_DSO_p[t] for t in T) 
        + gp.quicksum(lmda_EP[t] * P_VPP_p[j][t] - lmda_ES[t] * P_VPP_s[j][t] for t in T for j in J),
                   GRB.MAXIMIZE)

    # constraints (numeration from the paper)

    # (3)
    for t in T:
        # first part:
        m.addConstr(lmda_ES[t] <= lmda_CEP[t])
        m.addConstr(lmda_CES[t] <= lmda_ES[t])

        # second part: 
        m.addConstr(lmda_EP[t] <= lmda_CEP[t])
        m.addConstr(lmda_CES[t] <= lmda_EP[t])  

    # (4)
    for t in T:
        m.addConstr(
            P_DSO[t] == gp.quicksum(
                P_VPP_p[j][t] - P_VPP_s[j][t] for j in J
            )
        )

    # (9)
    for t in T:
        # part 1
        m.addConstr(
            - bigM * (1 - z_1[t]) <= P_DSO[t]
            )
        m.addConstr(
            P_DSO[t] <= bigM * z_1[t]
            )
        
        # part 2
        m.addConstr(
            - bigM * (1 - z_1[t]) <= P_DSO_p[t] - P_DSO[t]
            )
        m.addConstr(
            P_DSO_p[t] - P_DSO[t] <= bigM * (1 - z_1[t])
            )
        
        # part 3
        m.addConstr(
            - bigM * z_1[t] <= P_DSO_p[t]
            )
        m.addConstr(
            P_DSO_p[t] <= bigM * z_1[t]
            )
        
    # (10)
    for t in T:
        # part 1
        m.addConstr(
            - bigM * (1 - z_2[t]) <= P_DSO[t]
            )
        m.addConstr(
            P_DSO[t] <= bigM * z_2[t]
            )
        
        # part 2
        m.addConstr(
            - bigM * (1 - z_2[t]) <= P_DSO_s[t] 
            )
        m.addConstr(
            P_DSO_s[t] <= bigM * (1 - z_2[t])
            )
        
        # part 3
        m.addConstr(
            - bigM * z_2[t] <= P_DSO_s[t] + P_DSO[t]
            )
        m.addConstr(
            P_DSO_s[t] + P_DSO[t] <= bigM * z_2[t]
            )
        

    # (11)
    for t in T:
        m.addConstr(
            z_1[t] == z_2[t]
            )

    return None



## Main function
def main():
    t = 2 # time periods
    j = 3 # number of VPPs

    bigM = 10000
    ##############################
    ### PARAMETERS
    ##############################

    # parameters (global paramenters)
    lmda_CES = [1, 2]
    lmda_CEP = [1, 2]

    # parameters (the lower level as parameters)
    P_DSO_s = [1,2]
    P_DSO_p = [1,2]

    P_VPP_p = [[1,2],[1,2],[1,2]]   # j x t
    P_VPP_s = [[1,2],[1,2],[1,2]]   # j x t


    # input data
    upper_level(t, j, P_DSO_s, P_DSO_p, P_VPP_p, P_VPP_s, lmda_CES, lmda_CEP, bigM)


    ## Solve an instance
if __name__ == "__main__":
    main()