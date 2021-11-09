import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
start_year = 2009
end_year = 2021
profit, Reserve_fund = 0, 0
Reserve_monthly = 100000
# 1329.T:topix 1343.T:j-reit
stock_list = [['ACWI', 0.30, 0.33], ['SPY', 0.25, 0.0945], ['1329.T', 0.10, 0.11], ['EEM', 0.05, 0,70],  ['AGG', 0.05, 0.04], ['TLT', 0.05, 0.15], ['RWR', 0.03, 0.25], ['1343.T', 0.02, 0.16], ['GLD', 0.15, 0.4]]
asset_list = [[0, 0, 0] for i in range(len(stock_list))]
sum_log_1 = [[0] for i in range(((end_year-start_year)*12))]
sum_log_2 = [[0] for i in range(((end_year-start_year)*12))]
sum_log_3 = [[0] for i in range(((end_year-start_year)*12))]


# Read issue and Make compute 'change ratio'
def read_issue(issue_name):
    start = start_year
    issue = '../data/' + issue_name + '.csv'
    df_issue = pd.read_csv(issue,
                           index_col='Date', parse_dates=True)
    list_cry = [[0, 0] for i in range((end_year-start))]
    list_crm = [[0, 0] for i in range((end_year-start)*12)]
    for i in range((end_year-start_year)):
        df_specific_year_old = df_issue[dt.datetime(start, 1, 1):
                                        dt.datetime(start, 12, 31)]
        open_price_old = round(float(df_specific_year_old.iat[0, 0]), 2)
        if open_price_old < 1:
            open_price_old = round(float(df_specific_year_old.iat[1, 0]), 2)
        df_specific_year_new = df_issue[dt.datetime(start+1, 1, 1):
                                        dt.datetime(start+1, 12, 31)]
        open_price_new = round(float(df_specific_year_new.iat[0, 0]), 2)
        if open_price_new < 1:
            open_price_new = round(float(df_specific_year_old.iat[1, 0]), 2)
        change_ratio_year = round((open_price_new-open_price_old)/open_price_old, 3)
        list_cry[i][0] = str(start) + ':' + str(start+1)
        list_cry[i][1] = change_ratio_year
        for j in range(12):
            month = j + 1
            df_specific_m_o = df_issue[dt.datetime(start, month, 1):
                                       dt.datetime(start, month, 27)]
            open_price_o = round(float(df_specific_m_o.iat[0, 0]), 6)
            if open_price_o < 1:
                open_price_o = round(float(df_specific_m_o.iat[1, 0]), 6)
            if month < 12:
                df_specific_m_n = df_issue[dt.datetime(start, month+1, 1):
                                           dt.datetime(start, month+1, 27)]
            else:
                df_specific_m_n = df_issue[dt.datetime(start+1, 1, 1):
                                           dt.datetime(start+1, 1, 27)]
            open_price_n = round(float(df_specific_m_n.iat[0, 0]), 6)
            if open_price_n < 1:
                open_price_n = round(float(df_specific_m_o.iat[1, 0]), 6)
            change_ratio_month = round((open_price_n-open_price_o)/open_price_o, 6)
            list_crm[i*12+j][0] = str(start) + '-' +str(month) + ':' + str(start) + '-' +str(month+1)
            list_crm[i*12+j][1] = change_ratio_month
        start += 1
    list_cry.insert(0, 0)
    list_crm.insert(0, 0)
    return list_cry, list_crm


def rebalance(sum_now1, sum_now2, sum_now3):
    for o in range(len(stock_list)):
        asset_list[o][2] = stock_list[o][1]*sum_now3


# asset maker
result_list_y = [[0] for i in range(len(stock_list))]
result_list_m = [[0] for i in range(len(stock_list))]
print(stock_list[8])
# compute change ratio of each issue
for i in range(len(stock_list)):
    result_list_y[i], result_list_m[i] = read_issue(stock_list[i][0])
# compute asset of each time
for j in range((end_year-start_year)):
    for k in range(12):
        sum_now1, sum_now2, sum_now3 = 0, 0, 0
        print('----------')
        print(str(start_year+j) + '-' + str(k))
        list = [[0, 0, 0] for i in range(len(stock_list))]
        for m in range(len(stock_list)):
            reserve_money_plus, reserve_money = 0, 0
            # reserve_money for each issue
            reserve_money_plus = stock_list[m][1] * Reserve_monthly
            reserve_money = asset_list[m][0]
            if j*12+k >= 1:
                asset1 = round(asset_list[m][1] * float(1+result_list_m[m][j*12+k][1]), 6)
                asset2 = round(asset_list[m][2] * float(1+result_list_m[m][j*12+k][1]), 6)
            else:
                asset1, asset2 = 0, 0
            asset_list[m][0] = round(reserve_money_plus + reserve_money, 6)
            asset_list[m][1] = round(reserve_money_plus + asset1, 6)
            asset_list[m][2] = round(reserve_money_plus + asset2, 6)
            if k == 11:
                asset_list[m][1] = round(asset_list[m][1] * (1-stock_list[m][2]*0.01), 6)
                asset_list[m][2] = round(asset_list[m][2] * (1-stock_list[m][2]*0.01), 6)
            sum_now1 += asset_list[m][0]
            sum_now2 += asset_list[m][1]
            sum_now3 += asset_list[m][2]
        print(asset_list[8])
        for p in range(len(stock_list)):
            list[p][0] = round(asset_list[p][0] / sum_now1, 3)
            list[p][1] = round(asset_list[p][1] / sum_now2, 3)
            list[p][2] = round(asset_list[p][2] / sum_now3, 3)
        # print(list)
        Reserve_fund += Reserve_monthly
        sum_log_1[j*12+k] = sum_now1
        sum_log_2[j*12+k] = sum_now2
        sum_log_3[j*12+k] = sum_now3
    rebalance(sum_now1, sum_now2, sum_now3)
time_array = np.arange((end_year-start_year)*12)
sum_log_1_array = np.array(sum_log_1)
sum_log_2_array = np.array(sum_log_2)
sum_log_3_array = np.array(sum_log_3)
plt.plot(time_array, sum_log_1_array, label='Reserve Money')
plt.plot(time_array, sum_log_2_array, label='Constant Buy')
plt.plot(time_array, sum_log_3_array, label='Rebalance')
plt.legend()
plt.grid()
plt.show()
