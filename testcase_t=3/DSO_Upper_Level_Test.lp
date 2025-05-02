\ Model DSO_Upper_Level_Test
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0xd3fb6fab364511c4
Maximize
  0 lambda_ES_1 + 0 lambda_ES_2 + 0 lambda_ES_3 + 3 lambda_EP_1
   + 3 lambda_EP_2 + 3 lambda_EP_3 - 0.4 P_DSO_p_1 - 0.6 P_DSO_p_2
   - 1.4 P_DSO_p_3 + 0.2 P_DSO_s_1
Subject To
 Power_Balance_1: P_DSO_1 = 3
 BM_Purch_LB_1: - P_DSO_1 + 100 z_1 <= 100
 BM_Purch_UB_1: P_DSO_1 - 100 z_1 <= 0
 BM_Purch_Link_1: P_DSO_1 - P_DSO_p_1 + 100 z_1 <= 100
 BM_Purch_PBound_1: P_DSO_p_1 - 100 z_1 <= 0
 BM_Sale_LB_1: - P_DSO_s_1 + 100 z_1 <= 100
 BM_Sale_UB_1: P_DSO_s_1 + 100 z_1 <= 100
 BM_Sale_Link_1: - P_DSO_1 - P_DSO_s_1 - 100 z_1 <= 0
 Power_Balance_2: P_DSO_2 = 3
 BM_Purch_LB_2: - P_DSO_2 + 100 z_2 <= 100
 BM_Purch_UB_2: P_DSO_2 - 100 z_2 <= 0
 BM_Purch_Link_2: P_DSO_2 - P_DSO_p_2 + 100 z_2 <= 100
 BM_Purch_PBound_2: P_DSO_p_2 - 100 z_2 <= 0
 BM_Sale_LB_2: - P_DSO_s_2 + 100 z_2 <= 100
 BM_Sale_UB_2: P_DSO_s_2 + 100 z_2 <= 100
 BM_Sale_Link_2: - P_DSO_2 - P_DSO_s_2 - 100 z_2 <= 0
 Power_Balance_3: P_DSO_3 = 3
 BM_Purch_LB_3: - P_DSO_3 + 100 z_3 <= 100
 BM_Purch_UB_3: P_DSO_3 - 100 z_3 <= 0
 BM_Purch_Link_3: P_DSO_3 - P_DSO_p_3 + 100 z_3 <= 100
 BM_Purch_PBound_3: P_DSO_p_3 - 100 z_3 <= 0
 BM_Sale_LB_3: - P_DSO_s_3 + 100 z_3 <= 100
 BM_Sale_UB_3: P_DSO_s_3 + 100 z_3 <= 100
 BM_Sale_Link_3: - P_DSO_3 - P_DSO_s_3 - 100 z_3 <= 0
Bounds
 0.2 <= lambda_ES_1 <= 0.4
 lambda_ES_2 <= 0.6
 lambda_ES_3 <= 1.4
 0.2 <= lambda_EP_1 <= 0.4
 lambda_EP_2 <= 0.6
 lambda_EP_3 <= 1.4
Binaries
 z_1 z_2 z_3
End
