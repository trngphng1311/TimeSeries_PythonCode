import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tools.eval_measures import aic

# Đường dẫn đến file Excel
diachi = 'C:/Users/Admin/OneDrive - VietNam National University - HCM INTERNATIONAL UNIVERSITY/3rd Year/Time series/PRJ/smoothed.xlsx'
sheet = "00-04"
data = pd.read_excel(diachi, sheet_name=sheet, header=0, parse_dates=True, index_col=0, usecols=[0, 3])

# Initialize variables for best model
best_aic = float('inf')  # Start with a high AIC
best_order = None

# Expand the range of values for p, d, q
for p in range(5):  # You can adjust the range based on your preferences
    for d in range(3):
        for q in range(5):
            try:
                order = (p, d, q)
                model = ARIMA(data['Smooth'], order=order)
                results = model.fit()
                current_aic = results.aic
                
                # Update best model if the current AIC is lower
                if current_aic < best_aic:
                    best_aic = current_aic
                    best_order = order

            except Exception as e:
                print(f'Error for ARIMA{order}: {e}')
                continue

print(f'Best Model: ARIMA{best_order} - AIC: {best_aic}')

