import pandas as pd

bus_data = {
    "Bus Number": list(range(1, 34)),
    "Type": ["Reference"] + ["PQ"] * 16 + ["PQ/PV"] + ["PQ"] * 3 + ["PQ/PV"] + ["PQ"] * 2 + ["PQ/PV"] + ["PQ"] * 7 + ["PQ/PV"],
    "Active Demand (MW)": [0, 0.1, 0.09, 0.12, 0.06, 0.06, 0.2, 0.2, 0.06, 0.06, 0.045, 0.06, 0.06, 0.12, 0.06, 0.06, 0.06,
                           0.09, 0.09, 0.09, 0.09, 0.09, 0.09, 0.42, 0.42, 0.06, 0.06, 0.06, 0.12, 0.2, 0.15, 0.21, 0.06],
    "Reactive Demand (MVAr)": [0, 0.06, 0.04, 0.08, 0.03, 0.02, 0.1, 0.1, 0.02, 0.02, 0.03, 0.035, 0.035, 0.08, 0.01, 0.02, 0.02,
                               0.04, 0.04, 0.04, 0.04, 0.05, 0.2, 0.2, 0.025, 0.025, 0.02, 0.07, 0.6, 0.07, 0.1, 0.04, 0.04],
    "Minimum Voltage (p.u.)": [1.05] * 33,
    "Maximum Voltage (p.u.)": [0.95] * 33,
    "Number of Phases": ["3 (ABC)", "2 (AB)", "1 (A)", "2 (BC)", "1 (B)", "1 (C)", "3 (ABC)", "3 (ABC)", "1 (A)", "1 (B)", "1 (C)",
                         "1 (A)", "1 (B)", "2 (AC)", "1 (C)", "1 (A)", "1 (B)", "1 (C)", "1 (A)", "1 (B)", "1 (C)", "1 (A)", "1 (B)",
                         "3 (ABC)", "3 (ABC)", "1 (C)", "1 (A)", "1 (B)", "2 (AB)", "1 (C)", "2 (BC)", "3 (ABC)", "1 (A)"],
    "Connection Type": ["Y"] * 6 + ["D"] + ["Y"] * 17 + ["D"] + ["Y"] * 8,
    "Number of Wires": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]
}

df = pd.DataFrame(bus_data)

csv_filename_fixed = "data/33bus_demand_data.csv"
df.to_csv(csv_filename_fixed, index=False)

data = {
    "Bus Number": [1, 18, 22, 25, 33],
    "Active Capacity (MW)": [4, 0.2, 0.2, 0.2, 0.2],
    "Reactive Capacity (MVAr)": [2.5, 0, 0, 0, 0],
    "Type": ["Feeder (Conventional Generation)", "DG", "DG", "DG", "DG"],
    "Cost Function ($/h)": [
        "0.003P^2 + 12P + 240",
        "0.0026P^2 + 10.26P + 210",
        "0.0026P^2 + 10.26P + 210",
        "0.0026P^2 + 10.26P + 210",
        "0.0026P^2 + 10.26P + 210"
    ]
}

df = pd.DataFrame(data)

csv_filename_fixed = "data/33bus_generation_data.csv"
df.to_csv(csv_filename_fixed, index=False)


data = {
    "Branch Number": list(range(1, 36)),
    "From Bus": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 2, 19, 20, 21, 3, 23, 24, 6, 26, 27, 28, 29, 30, 31, 32, 21, 12, 25],
    "To Bus": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 8, 22, 29],
    "Type": ["Fixed"] * 32 + ["Switchable"] * 3,
    "R (Ω)": [0.0922, 0.493, 0.366, 0.3811, 0.819, 0.1872, 0.7114, 1.03, 1.044, 0.1966, 
              0.3744, 1.468, 0.5416, 0.591, 0.7463, 1.289, 0.732, 0.164, 1.5042, 0.4095, 
              0.7089, 0.4512, 0.898, 0.896, 0.203, 0.2842, 1.059, 0.8042, 0.5075, 0.9744, 
              0.3105, 0.341, 2, 2, 0.5],
    "X (Ω)": [0.047, 0.2511, 0.1864, 0.1941, 0.707, 0.6188, 0.2351, 0.74, 0.74, 0.065, 
              0.1238, 1.155, 0.7129, 0.526, 0.545, 1.721, 0.574, 0.1565, 1.3354, 0.4784, 
              0.9373, 0.3083, 0.7091, 0.7011, 0.1034, 0.1447, 0.9337, 0.7006, 0.2585, 0.963, 
              0.3619, 0.5302, 2, 2, 0.5]
}

df = pd.DataFrame(data)
csv_filename_fixed = "data/33bus_line_data.csv"
df.to_csv(csv_filename_fixed, index=False)


data = {
    "Bus Number": [18, 33],
    "Type": ["Capacitive", "Capacitive"],
    "Reactive Capacity (MVAr)": [0.4, 0.6]
}

df = pd.DataFrame(data)

csv_filename_fixed = "data/33bus_compensators_data.csv"
df.to_csv(csv_filename_fixed, index=False)

csv_filename_fixed
