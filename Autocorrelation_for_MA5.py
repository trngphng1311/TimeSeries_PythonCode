
import pandas as pd
import numpy as np

# Excel file path
diachi = 'C:/Users/Admin/OneDrive - VietNam National University - HCM INTERNATIONAL UNIVERSITY/3rd Year/Time series/PRJ/smoothed.xlsx'

# Sheet name
sheets = ["50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 and above"]

# Sheet looping
for sheet in sheets:
    print("Sheet:", sheet)
    
    # Sheet reading
    datayear = pd.read_excel(diachi, sheet_name=sheet, header=0, usecols=[0])
    realdata = pd.read_excel(diachi, sheet_name=sheet, header=0, usecols=[1], skiprows=[0, 1], nrows=59)
    data = pd.read_excel(diachi, sheet_name=sheet, header=0, parse_dates=True, index_col=0, usecols=[0, 2], skiprows=[0, 1], nrows=59)
    
    # Change data to numpy
    data_array = np.array(data.iloc[:, 0])

    # Calculate autocorrelation for k = 1
    autocorr_k1 = np.corrcoef(data_array[:-1], data_array[1:])[0, 1]

    # Print autocorrelation for k = 1
    print("Autocorrelation (k = 1):", autocorr_k1)
