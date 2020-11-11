import sheets
import quickstart
import pandas as pd
from pandas.tseries.offsets import BDay
import datetime
import numpy as np
import calendar_bairesdev

f_list=[]
SAMPLE_RANGE_NAME_1 = 'Checklist!I1'

#apply drive_search function
quickstart.drive_search(f_list)

df = pd.DataFrame(f_list)

#switch to date time format for pandas
df['createdTime'] = pd.to_datetime(df['createdTime']).dt.date

#get the score using sheets() function with the file id and the range as parameters,
df['score'] = df.apply(lambda row: sheets.sheets(row['id'], SAMPLE_RANGE_NAME_1), axis = 1)
#extract the number
df['score'] = df.score.str.extract('(\d+)')
#turn to float
df['score'] = pd.to_numeric(df['score'], downcast='float')

#df['name'] = df.name.str.slice(10:df.name.str.find('High'))

#create nextDate field which tells us when should the next meeting be carried out
df['nextDate'] = df.apply(lambda row: row['createdTime'] + datetime.timedelta(7) if row['score'] > 80.00 else\
    row['createdTime'] + BDay(3), axis=1)

#create filter for dates
filt = (df['nextDate'] >= np.datetime64('today') - np.timedelta64(3,'D'))
df = df[filt]

df['devName'] = df['name'].str.extract(pat = '([A-Z]\w{0,}\w{0,})',expand= True)

print(df.head())

df.to_csv('D:\BairesDev\HP_checklist.csv')

#print(df.dtypes)

#print(df.head())

