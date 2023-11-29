# This code is to take multiple on-chain data and test the unidirectional Garenger causality. For further information please refer to https://en.wikipedia.org/wiki/Granger_causality
import json
import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import grangercausalitytests


# insert your API key, Start Date & End Date
current_date = datetime.now()
delta_date = 365
start_date = int(datetime.timestamp(current_date-timedelta(days = delta_date)))
end_date = int(datetime.timestamp(current_date))
API_KEY = '2B1pxzrRCwECISMvVhDJ5c3jtPi'

#print(start_date,end_date)

# make API request for X = STH-SOPR & Y = Price
res_0 = requests.get('https://api.glassnode.com/v1/metrics/indicators/sopr_less_155',
    params={'a': 'BTC', 's': start_date, 'u': end_date, 'api_key': API_KEY})
res_1 = requests.get('https://api.glassnode.com/v1/metrics/market/price_usd_close',
    params={'a': 'BTC', 's': start_date, 'u': end_date, 'api_key': API_KEY})

# convert to pandas dataframe
dx = pd.read_json(res_0.text, convert_dates=['t'])
dy= pd.read_json(res_1.text, convert_dates=['t'])

# print the first 5 rows of X & Y
#print(dx.head(3), dy.head(3))

x = dx.index
y1 = dx['v']
y2 = dy['v']

# Plot Line1 (Left Y Axis)
fig, ax1 = plt.subplots(1,1,figsize=(16,9), dpi= 80)
ax1.plot(x, y1, color='tab:red')

# Plot Line2 (Right Y Axis)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot(x, y2, color='tab:blue')

# Decorations
# ax1 (left Y axis)
ax1.set_xlabel('Time', fontsize=20)
ax1.tick_params(axis='x', rotation=0, labelsize=12)
ax1.set_ylabel('STH-SOPR', color='tab:red', fontsize=20)
ax1.tick_params(axis='y', rotation=0, labelcolor='tab:red' )
ax1.grid(alpha=.4)

# ax2 (right Y axis)
ax2.set_ylabel("Price", color='tab:blue', fontsize=20)
ax2.tick_params(axis='y', labelcolor='tab:blue')
ax2.set_xticks(np.arange(0, len(x), 60))
ax2.set_xticklabels(x[::60], rotation=90, fontdict={'fontsize':10})
ax2.set_title("Visualizing Leading Indicator Phenomenon", fontsize=22)
fig.tight_layout()
plt.show()


#combine the data from two DataFrames
df = y2.join(y1)