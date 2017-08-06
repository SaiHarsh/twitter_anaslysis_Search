import pandas as pd 
from datetime import datetime
import csv

df = pd.read_csv('mini_out.csv')
df.columns = ['date', 'startTime', 'endTime', 'day', 'count', 'unique']

df_1 = pd.read_csv('out.csv')
df_1.columns = ['date', 'count_med', 'unique_med']

date_count = df['date'].nunique()
all_hours = df['startTime'].count()

c_max = df['count'].max()
c_min = df['count'].min()
c_med = int(round(df['count'].median()))
c_med_med = int(round(df_1['count_med'].median()))

u_max = df['unique'].max()
u_min = df['unique'].min()
u_med = int(round(df['unique'].median()))
u_med_med = int(round(df_1['unique_med'].median()))

print date_count
print all_hours
print c_min
print c_max
print c_med
print c_med_med
print u_min
print u_max
print u_med
print u_med_med

cols = ['date_count', 'all_hours','c_min', 'c_max', 'c_med', 'c_med_med', 'u_min', 'u_max', 'u_med', 'u_med_med']
stats = pd.DataFrame([[date_count, all_hours, c_min, c_max, c_med, c_med_med, u_min, u_max, u_med, u_med_med]], columns = cols)
#print (stats)
stats.to_csv('result_mini.csv', index=False)

