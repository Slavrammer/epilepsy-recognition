import os
from statsmodels.tsa.stattools import adfuller, kpss
import matplotlib.pyplot as plt
import pandas as pd

# Path
os.chdir(input('Enter your path'))

data = pd.read_csv('16.csv', skiprows = 4)


x = data.iloc[:500, 1]
x = x.dropna()
#x = x.iloc[:44962]
#x = x.iloc[:89924]

# data peaks
plt.plot(x)
plt.show()

df = x.iloc[:4875]

plt.plot(df)
plt.show()

# ADF Test
result = adfuller(x, autolag='AIC')
print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')
for key, value in result[4].items():
    print('Critial Values:')
    print(f'   {key}, {value}')

# KPSS Test
result = kpss(x, regression='c')
print('\nKPSS Statistic: %f' % result[0])
print('p-value: %f' % result[1])
for key, value in result[3].items():
    print('Critial Values:')
    print(f'   {key}, {value}')
