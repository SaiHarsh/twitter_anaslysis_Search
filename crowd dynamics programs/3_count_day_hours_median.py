#Find the median per day 

import pandas as pd 
from datetime import datetime
import csv

df = pd.read_csv('o_1_hour.csv')
df.columns = ['date', 'startTime', 'endTime', 'day', 'count', 'unique']


date_count = df['date'].nunique()
all_median = round(df['count'].median())
all_hours = df['startTime'].count()
#med_med = df.groupby(['date','count']).median()

print date_count
print all_median
print all_hours

cols = ['date_count', 'all_median', 'all_hours']
stats = pd.DataFrame([[date_count, all_median, all_hours]], columns = cols)
#print (stats)
stats.to_csv('o_day_median.csv', index=False)
#med_med.to_csv('med_day.csv', index=False, header=False)
