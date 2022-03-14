from datetime import datetime
import locale
import pandas as pd

# print(locale.getlocale())
# print(datetime.strptime('25/May/2015', "%d/%b/%Y"))

days = [
    ['25/May/2015', '27/May/2015', '27/Apr/2015', '27/Jan/2015', '07/May/2015', '22/May/2015', '16/Jan/2015',
        '29/Jan/2015',
        '28/Feb/2015', '18/Feb/2015', '08/May/2015', '20/Jan/2015', '24/Jan/2015', '31/Mar/2015', '30/Apr/2015',
        '17/Feb/2015',
        '19/Mar/2015', '05/May/2015', '22/Jan/2015', '14/Aug/2015', '26/Feb/2015', '14/Mar/2015', '28/May/2015',
     '19/Mar/2015', '19/Mar/2015', '19/Mar/2015', '01/Jan/2015'],
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
     'x', 'y', 'z', 'a1']
        ]

df = pd.DataFrame(days)
df = df.transpose()
df.columns = ['Dates', 'fil_names']

df['Dates'] = pd.to_datetime(df['Dates'])
df.sort_values(by=['Dates'], inplace=True)
print(df)

t = df.groupby(pd.Grouper(key="Dates", axis=0, freq="10D", sort=True))['fil_names'].apply(list).reset_index(name='new')
print(t)
