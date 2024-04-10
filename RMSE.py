#For Holt smoothing method
# import the required modules
import pandas as pd
from sklearn.metrics import mean_squared_error

# read the csv data
diachi ='C:/Users/Admin/OneDrive - VietNam National University - HCM INTERNATIONAL UNIVERSITY/3rd Year/Time series/PRJ/smoothed.xlsx'
i=input()
datayear = pd.read_excel(diachi, sheet_name=i, header=0, usecols=[0])
realdata = pd.read_excel(diachi,sheet_name=i,header=0,usecols=[1])
data = pd.read_excel(diachi, sheet_name=i, header=0, parse_dates=True, index_col=0, usecols=[0, 3])

rmse = mean_squared_error(data, realdata, squared=False)
print("RMSE=",rmse)