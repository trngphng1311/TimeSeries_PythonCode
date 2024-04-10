import pandas as pd
import matplotlib.pyplot as plt

diachi = 'C:/Users/Admin/OneDrive - VietNam National University - HCM INTERNATIONAL UNIVERSITY/3rd Year/Time series/PRJ/smoothed.xlsx'
data = pd.read_excel(diachi, sheet_name=None)

# Create a single figure and axis outside the loop
fig, ax = plt.subplots()

for sheet_name, df in data.items():
    df['moving_average'] = df['value'].rolling(window=3).mean()

    # Plot each sheet on the same axis
    ax.plot(df['Year, t'], df['value'], label=f'{sheet_name} - Original Data')
    ax.plot(df['Year, t'], df['moving_average'], label=f'{sheet_name} - Moving Average')

# Set title and labels
ax.set_title('Original Data and Moving Average')
ax.set_xlabel('Year, t')
ax.set_ylabel('Value')
ax.legend()

# Show the combined plot
plt.show()