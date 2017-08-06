import pandas as pd
from datetime import datetime,time
import numpy as np

df = pd.read_csv('o_1_hour.csv', header=None) 
df.columns=['Date', 'StartTime', 'EndTime', 'Day', 'SumCount', 'UniqueCount']

time_merge = df.groupby(['StartTime', 'EndTime']).agg({'SumCount': ['sum'], 'UniqueCount': {'median': lambda x: np.median(x).round(0)}})

day_merge = df.groupby(['StartTime', 'EndTime', 'Day']).agg({'SumCount': ['sum'],'UniqueCount': {'median': lambda x: np.median(x).round(0)}})

time_merge.to_csv('o_one_hour_time_result.csv', header=False)
day_merge.to_csv('o_one_hour_day_result.csv', header=False)
