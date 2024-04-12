import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

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

    # Find the best ARIMA model
    model = auto_arima(data, seasonal=False, trace=True, error_action='ignore', suppress_warnings=True,
                       d_range=[0, 2], p_range=[0, 2], q_range=[0, 2])
    print(model.summary())

    # Fit the best model
    best_order = model.order
    best_model = ARIMA(data, order=best_order)
    fitted = best_model.fit()

    # Forecast
    forecast = fitted.forecast(steps=10) 
    print("Forecast:", forecast)

    # Plot ACF and PACF of residuals
    residuals = pd.Series(fitted.resid)
    plot_acf(residuals)
    plot_pacf(residuals)
    plt.show()

# Test ADF on second differenced series
    adf_test2 = adfuller(data_diff, maxlag=1)
    print("\nADF Test on second differenced series:")
    print("1. ADF: ", adf_test2[0])
    print("2. p value: ", adf_test2[1])
    print("3. num of lags: ", adf_test2[2])
    print("4. num of observations used for ADF regression and critical values: ", adf_test2[3])
    print("5. critical values: ")
    for key, val in adf_test2[4].items():
        print("\t", key, ":", val)

#Test ARIMA MODEL 
# Figure out order for ARIMA
warnings.filterwarnings("ignore")
auto=auto_arima(data['Smooth'], stepwise=False, seasonal=False)
auto.summary()

# Fit model 
model=ARIMA(data['Smooth'], order=(0,2,1))
model_fit=model.fit()
print(model_fit.summary())

#White noise
residual=model_fit.resid[1:]
fig, ax = plt.subplots(1,2)
residual.plot(title='residual',ax=ax[0])
residual.plot(title='density', kind='kde', ax=ax[1])
c=plot_acf(residual, lags=20)
d=plot_pacf(residual, lags=20)

# Forecast to January 1, 2030
num_periods = 8  # Number of years to forecast
forecast = model_fit.get_forecast(steps=num_periods)

# Create DataFrame for forecast with the correct index
forecast_index = pd.date_range(start=data.index[-1] + pd.DateOffset(years=1), end='2030-01-01', freq=pd.offsets.YearBegin(1))
forecast_df = pd.DataFrame(index=forecast_index, columns=['forecast_auto'])
forecast_df['forecast_auto'] = forecast.predicted_mean.values

# Merge the original data with the forecast
data = pd.concat([data, forecast_df], axis=1)
print(data)
data.plot()
plt.show()

