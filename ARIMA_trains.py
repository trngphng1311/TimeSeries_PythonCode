import pandas as pd
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
from statsmodels.tsa.arima.model import ARIMA
import warnings

# Read file and size
diachi = 'C:/Users/Admin/OneDrive - VietNam National University - HCM INTERNATIONAL UNIVERSITY/3rd Year/Time series/PRJ/smoothed.xlsx'
data = pd.read_excel(diachi, sheet_name='00-04', header=0, parse_dates=True, index_col=0, usecols=[0, 3])
data = data.dropna()
print('Shape of data', data.shape)
data.head()

# Check for stationary
def ad_test(data):
    datatest = adfuller(data, autolag='AIC')
    print("1. ADF: ", datatest[0])
    print("2. p value: ", datatest[1])
    print("3. num of lag: ", datatest[2])
    print("4. num of obser used for adf regression and critical values: ", datatest[3])
    print("5. critical value: ")
    for key, val in datatest[4].items():
        print("\t", key, ":", val)

# Call the ad_test function
ad_test(data['Smooth'])

# Figure out order for ARIMA
warnings.filterwarnings("ignore")
stepwise_fit = auto_arima(data['Smooth'], trace=True, suppress_warnings=True)
stepwise_fit.summary()
print(stepwise_fit.summary())

# Train model
print(data.shape)
train = data.iloc[:-30]
test = data.iloc[-30:]
print(train.shape, test.shape)

# Train model using the order selected by auto_arima
model = ARIMA(train['Smooth'], order=(2,0,1))
model = model.fit()
model.summary()
print(model.summary())