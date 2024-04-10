import pandas as pd
from statsmodels.tsa.stattools import adfuller

# Excel file bath
diachi = 'C:/Users/Admin/OneDrive - VietNam National University - HCM INTERNATIONAL UNIVERSITY/3rd Year/Time series/PRJ/smoothed.xlsx'

# Sheet name
sheets = ["00-04"]

# Looping for sheets
for sheet in sheets:
    print("Sheet:", sheet)
    
    # Sheet read
    datayear = pd.read_excel(diachi, sheet_name=sheet, header=0, usecols=[0])
    data = pd.read_excel(diachi, sheet_name=sheet, header=0, parse_dates=True, index_col=0, usecols=[0, 3])
    
    # 1st differencing
    data_diff = data.diff(periods=2).dropna()
    
    # Checking stationary of data after 1st differencing
    result = adfuller(data_diff['Smooth'], maxlag=2)  
    adf_statistic = result[0]
    p_value = result[1]
    
    # Calculate t
    t_value = adf_statistic / result[4]['5%']  #Choose significant level (1%, 5%, 10%)
    
    print('ADF Statistic: %f' % adf_statistic)
    print('p-value: %f' % p_value)
    print('Critical Values:')
    for key, value in result[4].items():
        print('\t%s: %.3f' % (key, value))
    
    print('t-value: %f' % t_value)
