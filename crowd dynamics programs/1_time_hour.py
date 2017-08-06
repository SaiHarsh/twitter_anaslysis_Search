#split the data between hours as desired 

import pandas as pd
from datetime import datetime,time
import numpy as np

fn = r'00_Dart.csv'
#cols = ['UserID','StartTime','StopTime', 'gps1', 'gps2']

df = pd.read_csv(fn)
print df
# filter input data set ... 
start_hour = 18
end_hour = 23
df = df[(pd.to_datetime(df.Datetime, unit='s').dt.hour >= start_hour) & (pd.to_datetime(df.Datetime, unit='s').dt.hour <= end_hour)]

print df

df.to_csv('o_18_23_hour.csv', index=False, header=False)
