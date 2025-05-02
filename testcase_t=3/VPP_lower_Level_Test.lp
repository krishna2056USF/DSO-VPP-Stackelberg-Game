\ Model Lower_Level_VPP
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x450ebb0f82aa516d
Minimize
  10 PVPP_p[1] + 12 PVPP_p[2] + 11 PVPP_p[3] - 7 PVPP_s[1] - 9 PVPP_s[2]
   - 8 PVPP_s[3] + PMT[1] + PMT[2] + PMT[3] + 3 Constant + [ 2 PMT[1] ^2
   + 2 PMT[2] ^2 + 2 PMT[3] ^2 + PBS1[1] ^2 + PBS1[2] ^2 + PBS1[3] ^2
   + 0.6 PBS2[1] ^2 + 0.6 PBS2[2] ^2 + 0.6 PBS2[3] ^2 ] / 2 
Subject To
 PVPP_flow_1: - PVPP_p[1] + PVPP_s[1] + PVPP[1] = 0
 power_balance_1: PVPP[1] + PMT[1] + PBS1[1] + PBS2[1] + PWT[1] = 4
 PVPP_flow_2: - PVPP_p[2] + PVPP_s[2] + PVPP[2] = 0
 power_balance_2: PVPP[2] + PMT[2] + PBS1[2] + PBS2[2] + PWT[2] = 5
 PVPP_flow_3: - PVPP_p[3] + PVPP_s[3] + PVPP[3] = 0
 power_balance_3: PVPP[3] + PMT[3] + PBS1[3] + PBS2[3] + PWT[3] = 6
 R6: - PMT[1] + PMT[2] <= 1
 R7: - PMT[1] + PMT[2] >= -1
 R8: - PMT[2] + PMT[3] <= 1
 R9: - PMT[2] + PMT[3] >= -1
 R10: 0.1 PBS1[1] + SOC1[1] = 0.5
 R11: 0.1 PBS1[2] - SOC1[1] + SOC1[2] = 0
 R12: 0.1 PBS1[3] - SOC1[2] + SOC1[3] = 0
 R13: SOC1[3] = 0.5
 R14: 0.1 PBS2[1] + SOC2[1] = 0.5
 R15: 0.1 PBS2[2] - SOC2[1] + SOC2[2] = 0
 R16: 0.1 PBS2[3] - SOC2[2] + SOC2[3] = 0
 R17: SOC2[3] = 0.5
Bounds
 PVPP_p[1] <= 3
 PVPP_p[2] <= 3
 PVPP_p[3] <= 3
 PVPP_s[1] <= 3
 PVPP_s[2] <= 3
 PVPP_s[3] <= 3
 PMT[1] <= 5
 PMT[2] <= 5
 PMT[3] <= 5
 -2 <= PBS1[1] <= 2
 -2 <= PBS1[2] <= 2
 -2 <= PBS1[3] <= 2
 -2 <= PBS2[1] <= 2
 -2 <= PBS2[2] <= 2
 -2 <= PBS2[3] <= 2
 0.2 <= SOC1[1] <= 1
 0.2 <= SOC1[2] <= 1
 0.2 <= SOC1[3] <= 1
 0.2 <= SOC2[1] <= 1
 0.2 <= SOC2[2] <= 1
 0.2 <= SOC2[3] <= 1
 PWT[1] <= 3
 PWT[2] <= 3
 PWT[3] <= 3
 Constant = 1
End
