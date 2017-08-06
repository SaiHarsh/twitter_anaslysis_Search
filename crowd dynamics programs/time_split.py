import pandas as pd
from datetime import datetime,time
import numpy as np


fn = r'USC_1.csv'
cols = ['UserID','StartTime','StopTime']
df = pd.read_csv(fn, header=None, names=cols)

df['m'] = df.StopTime + df.StartTime
df['d'] = df.StopTime - df.StartTime

# 'start' and 'end' for the reporting DF: `r`
# which will contain equal intervals (1 hour in this case)
start = pd.to_datetime(df.StartTime.min(), unit='s').date()
end = pd.to_datetime(df.StopTime.max(), unit='s').date() + pd.Timedelta(days=1)

# building reporting DF: `r`
freq = '1H'  # 1 Hour frequency
idx = pd.date_range(start, end, freq=freq)
r = pd.DataFrame(index=idx)
r['start'] = (r.index - pd.datetime(1970,1,1)).total_seconds().astype(np.int64)

# 1 hour in seconds, minus one second (so that we will not count it twice)
interval = 60*60 - 1

r['LogCount'] = 0
r['UniqueIDCount'] = 0


for i, row in r.iterrows():
        # intervals overlap test
        # https://en.wikipedia.org/wiki/Interval_tree#Overlap_test
        # i've slightly simplified the calculations of m and d
        # by getting rid of division by 2,
        # because it can be done eliminating common terms
    u = df[np.abs(df.m - 2*row.start - interval) < df.d + interval].UserID
    r.ix[i, ['LogCount', 'UniqueIDCount']] = [len(u), u.nunique()]

r['Day'] = pd.to_datetime(r.start, unit='s').dt.weekday_name.str[:3]
r['StartTime'] = pd.to_datetime(r.start, unit='s').dt.time
r['EndTime'] = pd.to_datetime(r.start + interval + 1, unit='s').dt.time

#df.to_csv((r[r.LogCount > 0])'example.csv')
print(r[r.LogCount > 0])
