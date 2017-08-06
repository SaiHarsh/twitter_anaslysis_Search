import pandas as pd 
import numpy as np

'''
df1 = pd.read_csv('stat_result.csv')
df1.columns = ['date_count', 'all_hours', 'c_min', 'c_max', 'c_med', 'c_med_med', 'u_min', 'u_max', 'u_med', 'u_med_med']
'''

df2 = pd.read_csv('u_above_med.csv')
df2.columns = ['date', 'startTime', 'endTime', 'day', 'c_total', 'u_total']


df2['class'] = pd.qcut(df2.u_total, q=[0, .4, .8, 1.], labels=['normaly', 'fairly', 'highly'])

#print df2

df2.to_csv('class_result.csv', index=None)
