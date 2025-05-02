\ Model Lower_Level_VPP
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0xd56d923879a9b46
Minimize
  0.4 PVPP_p[1] + 0.8 PVPP_p[2] + 1.4 PVPP_p[3] + 0.6 PVPP_p[4]
   + 0.9 PVPP_p[5] - 0.5 PVPP_s[1] - 1.2 PVPP_s[2] - 0.34 PVPP_s[3]
   - 0.7 PVPP_s[4] - 0.8 PVPP_s[5] + PMT[1] + PMT[2] + PMT[3] + PMT[4]
   + PMT[5] + 0 SOC1[4] + 0 SOC1[5] + 0 SOC2[4] + 0 SOC2[5] + 5 Constant
   + [ 2 PMT[1] ^2 + 2 PMT[2] ^2 + 2 PMT[3] ^2 + 2 PMT[4] ^2 + 2 PMT[5] ^2
   + PBS1[1] ^2 + PBS1[2] ^2 + PBS1[3] ^2 + PBS1[4] ^2 + PBS1[5] ^2
   + 0.6 PBS2[1] ^2 + 0.6 PBS2[2] ^2 + 0.6 PBS2[3] ^2 + 0.6 PBS2[4] ^2
   + 0.6 PBS2[5] ^2 ] / 2 
Subject To
 PVPP_flow_1: - PVPP_p[1] + PVPP_s[1] + PVPP[1] = 0
 power_balance_1: PVPP[1] + PMT[1] + PBS1[1] + PBS2[1] + PWT[1] = 1
 PVPP_flow_2: - PVPP_p[2] + PVPP_s[2] + PVPP[2] = 0
 power_balance_2: PVPP[2] + PMT[2] + PBS1[2] + PBS2[2] + PWT[2] = 1.5
 PVPP_flow_3: - PVPP_p[3] + PVPP_s[3] + PVPP[3] = 0
 power_balance_3: PVPP[3] + PMT[3] + PBS1[3] + PBS2[3] + PWT[3] = 2
 PVPP_flow_4: - PVPP_p[4] + PVPP_s[4] + PVPP[4] = 0
 power_balance_4: PVPP[4] + PMT[4] + PBS1[4] + PBS2[4] + PWT[4] = 2.5
 PVPP_flow_5: - PVPP_p[5] + PVPP_s[5] + PVPP[5] = 0
 power_balance_5: PVPP[5] + PMT[5] + PBS1[5] + PBS2[5] + PWT[5] = 1
 R10: - PMT[1] + PMT[2] <= 1
 R11: - PMT[1] + PMT[2] >= -1
 R12: - PMT[2] + PMT[3] <= 1
 R13: - PMT[2] + PMT[3] >= -1
 R14: PBS1[1] + SOC1[1] = 0.5
 R15: PBS1[2] - SOC1[1] + SOC1[2] = 0
 R16: PBS1[3] - SOC1[2] + SOC1[3] = 0
 R17: SOC1[3] = 0.5
 R18: 0.3333333333333333 PBS2[1] + SOC2[1] = 0.5
 R19: 0.3333333333333333 PBS2[2] - SOC2[1] + SOC2[2] = 0
 R20: 0.3333333333333333 PBS2[3] - SOC2[2] + SOC2[3] = 0
 R21: SOC2[3] = 0.5
Bounds
 PVPP_p[1] <= 3
 PVPP_p[2] <= 3
 PVPP_p[3] <= 3
 PVPP_p[4] <= 3
 PVPP_p[5] <= 3
 PVPP_s[1] <= 3
 PVPP_s[2] <= 3
 PVPP_s[3] <= 3
 PVPP_s[4] <= 3
 PVPP_s[5] <= 3
 PMT[1] <= 5
 PMT[2] <= 5
 PMT[3] <= 5
 PMT[4] <= 5
 PMT[5] <= 5
 -2 <= PBS1[1] <= 2
 -2 <= PBS1[2] <= 2
 -2 <= PBS1[3] <= 2
 -2 <= PBS1[4] <= 2
 -2 <= PBS1[5] <= 2
 -2 <= PBS2[1] <= 2
 -2 <= PBS2[2] <= 2
 -2 <= PBS2[3] <= 2
 -2 <= PBS2[4] <= 2
 -2 <= PBS2[5] <= 2
 0.2 <= SOC1[1] <= 1
 0.2 <= SOC1[2] <= 1
 0.2 <= SOC1[3] <= 1
 0.2 <= SOC1[4] <= 1
 0.2 <= SOC1[5] <= 1
 0.2 <= SOC2[1] <= 0.98
 0.2 <= SOC2[2] <= 0.98
 0.2 <= SOC2[3] <= 0.98
 0.2 <= SOC2[4] <= 0.98
 0.2 <= SOC2[5] <= 0.98
 PWT[1] <= 1
 PWT[2] <= 1
 PWT[3] <= 1
 PWT[4] <= 1
 PWT[5] <= 1
 Constant = 1
End
