from datetime import datetime
import locale
import pandas as pd
import numpy as np

# print(locale.getlocale())
# print(datetime.strptime('25/May/2015', "%d/%b/%Y"))

days = [
    ['25/May/2015', '27/May/2015', '27/Apr/2015', '27/Jan/2015', '07/May/2015', '22/May/2015', '16/Jan/2015',
        '29/Jan/2015',
        '28/Feb/2015', '18/Feb/2015', '08/May/2015', '20/Jan/2015', '24/Jan/2015', '31/Mar/2015', '30/Apr/2015',
        '17/Feb/2015',
        '19/Mar/2015', '05/May/2015', '22/Jan/2015', '14/Aug/2015', '26/Feb/2015', '14/Mar/2015', '28/May/2015',
     '19/Mar/2015', '19/Mar/2015', '19/Mar/2015', '22/Mar/2016', '23/Mar/2016', '02/Feb/2016',
     '01/Feb/2016'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
     'x', 'y', 'z', 'a1', 'a2', 'a3', 'a4']
        ]

df = pd.DataFrame(days)
df = df.transpose()
df.columns = ['Dates', 'fil_names']

df['Dates'] = pd.to_datetime(df['Dates'])
df.sort_values(by=['Dates'], inplace=True, ignore_index=True)
print(df)


first_date = df.iloc[0]['Dates']
print(first_date)
print(type(first_date))
first_year = first_date.year
print(first_year)
print(type(first_year))

new_year = pd.Timestamp(f'{first_year}-01-01T00')
print(new_year)
if first_date == new_year:
    print('eq')
else:
    print('no')
    df.loc[-1] = [new_year, 'sample']
    df.index = df.index + 1
    df = df.sort_index()

print(df)
# first_date = df.head(1)['Dates']
# print(first_date)
# year = first_date.year
# print(year)


t = df.groupby(pd.Grouper(key="Dates", axis=0, freq="10D", sort=True))['fil_names'].apply(list).reset_index(name='new')
print(t)



