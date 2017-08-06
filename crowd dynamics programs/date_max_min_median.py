#find median of hours group by date
#step one median for a next step of median of median 

#find the min, max, sum, mean, median values per date and day 
#change the group by option from date/day or any suitable as needed. 

import pandas as pd 
from datetime import datetime
import csv

cols = ['date', 'startTime', 'endTime', 'day', 'count', 'unique']

df = pd.read_csv('o_1_hour.csv', header=None, names=cols)

c_max = df.groupby(['day'])[['count']].max()		#max of count day-wise
c_min = df.groupby(['day'])[['count']].min()		#min of count day-wise
u_max = df.groupby(['day'])[['unique']].max()		#max of unique day-wise
u_min = df.groupby(['day'])[['unique']].min()		#min of unique day-wise
c_sum = df.groupby(['day'])[['count']].sum()		#sum of count day-wise
u_sum = df.groupby(['day'])[['unique']].sum()		#sum of unique day-wise
c_mean = df.groupby(['day'])[['count']].mean().astype(int)		#avg of count day-wise
u_mean = df.groupby(['day'])[['unique']].mean().astype(int)	#avg of unique day-wise
c_med = df.groupby(['day'])[['count']].median().astype(int)	#median of count day-wise
u_med = df.groupby(['day'])[['unique']].median().astype(int)	#median of unique day-wise

#dictionary created with new data and respective column names
data_dictionary = {'day': df['day'].unique(), 'max_count': list(c_max['count']), 'min_count': list(c_min['count']), 'max_unique': list(u_max['unique']),
'min_unique': list(u_min['unique']), 'sum_count': list(c_sum['count']), 'sum_unique': list(u_sum['unique']), 'mean_count': list(c_mean['count']),
'mean_unique': list(u_mean['unique']), 'med_count': list(c_med['count']), 'med_unique': list(u_med['unique'])}

#construction of new dataframe with new dictionary formed
new_df = pd.DataFrame(data = data_dictionary)

#output
new_df.to_csv('o_day_min_max.csv', index = False)
'''
cols = ['date_count', 'all_hours','c_min', 'c_max', 'c_med', 'c_med_med', 'u_min', 'u_max', 'u_med', 'u_med_med']
stats = pd.DataFrame([[date_count, all_hours, c_min, c_max, c_med, c_med_med, u_min, u_max, u_med, u_med_med]], columns = cols)
#print (stats)
stats.to_csv('o_stats_by_date.csv', index=False)
'''
