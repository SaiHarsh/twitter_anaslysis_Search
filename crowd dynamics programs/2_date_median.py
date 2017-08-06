#find median of hours group by date
#step one median for a next step of median of median 

import pandas as pd 
from datetime import datetime
import csv

cols = ['date', 'startTime', 'endTime', 'day', 'count', 'unique']

df = pd.read_csv('o_1_hour.csv', header=None, names=cols)

df.groupby(['date'])[['count','unique']].agg({'count':'median','unique':'median'}).round().astype(int).to_csv('o_one_hour_date_median.csv', header=None)

