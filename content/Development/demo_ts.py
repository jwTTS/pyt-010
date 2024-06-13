# %% Import Packages

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.tsa as tsa


# %% Time Series

sp500_vol = pd.read_csv('Output/SP500_vol.csv', header=0, index_col=0,
                        parse_dates=True)

ts500 = sp500_vol[['rtnClose', 'vol','vol_1', 'vol_ma_5', 'vol_ma_21']].copy()
ts500.dropna(inplace=True)

ts500['rtnClose'] *= 100
ts500[['vol', 'vol_1', 'vol_ma_5', 'vol_ma_21']] *= 10000
ts500['vol'].plot()


# %% ACF PACF
fig = plt.figure(figsize=(10,10))
ax1 = fig.add_subplot(2,1,1)
fig = sm.graphics.tsa.plot_acf(ts500['vol'].values, lags=40, ax=ax1)
ax2 = fig.add_subplot(2,1,2)
fig = sm.graphics.tsa.plot_pacf(ts500['vol'].values, lags=40, ax=ax2)
fig.show()



# %% ARMA Models (1,5) and (1,21)

arma = sm.tsa.ARMA(ts500['vol'], (1,5)).fit(disp=False)
arma.summary()

plt.plot(arma.resid)
plt.show()

arma = sm.tsa.ARMA(ts500['vol'], (1,21)).fit(disp=False)



# %% Forcasting Using ARMA model
arma = sm.tsa.ARMA(ts500['vol'], (1,5)).fit(disp=False)
y_hat = arma.fittedvalues
y_T, y_T_stderr, y_T_conf_int = arma.forecast(steps=5)

tsfore = pd.DataFrame(y_T, columns=['y_T']).join(pd.DataFrame(y_T_conf_int,
                      columns=['y_T_low', 'y_T_upper']))

last_day = max(ts500.index)
tsfore['date'] = [pd.to_datetime(last_day + pd.offsets.Day(i+1)) for i in range(5)]
tsfore.set_index('date', inplace=True, drop=True)

ts500.loc['2018':, 'vol'].plot()
y_hat.loc['2018':].plot()
tsfore['y_T'].plot()
plt.fill_between(tsfore.index, tsfore['y_T_low'], tsfore['y_T_upper'],
                 color = '#539caf', alpha=0.4)
plt.show()