import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
import matplotlib.pyplot as plt

# Read file and size
diachi = 'C:/Users/Admin/OneDrive - VietNam National University - HCM INTERNATIONAL UNIVERSITY/3rd Year/Time series/PRJ/smoothed.xlsx'
xls = pd.ExcelFile(diachi)

# Loop through each sheet in the Excel file
for sheet_name in xls.sheet_names:
    print("Sheet:", sheet_name)
    data = pd.read_excel(diachi, sheet_name=sheet_name, header=0, parse_dates=True, index_col=0, usecols=[0,3])
    data = data.dropna()
    print('Shape of data', data.shape)
    data.head()
    print(data['Smooth'])

    #Differencing
    adf_test1 = adfuller(data, maxlag=10)
    if adf_test1[1] > 0.05:
        data_diff1 = data.diff().dropna()
        adf_test_diff1 = adfuller(data_diff1, maxlag=10)
        if adf_test_diff1[1] > 0.05:
            data_diff = data_diff1.diff().dropna()
            adf_test_diff = adfuller(data_diff, maxlag=10)
            if adf_test_diff[1] > 0.05:
                print("After second differencing, data is still non-stationary.")
            else:
                print("After second differencing, data becomes stationary.")
                data = data_diff
        else:
            print("After first differencing, data becomes stationary.")
            data = data_diff1
    else:
        print("Data is stationary without differencing.")

    # Fit a Simple Exponential Smoothing model
    ses_model = SimpleExpSmoothing(data)
    ses_fit = ses_model.fit()

    # Forecast using SES
    forecast_ses = ses_fit.forecast(5)  # Forecasting 5 years into the future using SES
    print("SES Forecast:", forecast_ses)

    # Plot the data and forecast
    plt.plot(data.index, data, label='Actual')
    plt.plot(pd.date_range(start=data.index[-1], periods=6, freq='A'), np.append(data.iloc[-1], forecast_ses), label='Forecast')
    plt.legend()
    plt.title('Simple Exponential Smoothing Forecast')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.show()
