import pandas as pd 
import numpy as np

df1 = pd.read_csv('stat_result.csv')
df1.columns = ['date_count', 'all_hours', 'c_min', 'c_max', 'c_med', 'c_med_med', 'u_min', 'u_max', 'u_med', 'u_med_med']

df2 = pd.read_csv('one_hour.csv')
df2.columns = ['date', 'startTime', 'endTime', 'day', 'c_total', 'u_total']

# log counts above and below the median value 
c_above_med = df2[df2.c_total >= df1.ix[0, 'c_med']]
c_below_med = df2[df2.c_total < df1.ix[0, 'c_med']]

c_above_med.to_csv('c_above_med.csv', index=False)
c_below_med.to_csv('c_below_med.csv', index=False)

#log counts above and below the median of median 
c_above_med_med = df2[df2.c_total >= df1.ix[0, 'c_med_med']]
c_below_med_med = df2[df2.c_total < df1.ix[0, 'c_med_med']]

c_above_med_med.to_csv('c_above_med_med.csv', index=False)
c_below_med_med.to_csv('c_below_med_med.csv', index=False)

# unique users above and below the median value 
u_above = df2[df2.u_total >= df1.ix[0, 'u_med']]
u_below = df2[df2.u_total < df1.ix[0, 'u_med']]

c_above_med.to_csv('u_above_med.csv', index=False)
c_below_med.to_csv('u_below_med.csv', index=False)

# unique users above and below the median of median value 
u_above = df2[df2.u_total >= df1.ix[0, 'u_med_med']]
u_below = df2[df2.u_total < df1.ix[0, 'u_med_med']]

c_above_med.to_csv('u_above_med_med.csv', index=False)
c_below_med.to_csv('u_below_med_med.csv', index=False)
