from datetime import datetime
import locale

print(locale.getlocale())

print(datetime.strptime('25/May/2015', "%d/%b/%Y"))

days = ['25/May/2015', '27/May/2015', '27/Apr/2015', '27/Jan/2015', '07/May/2015', '22/May/2015', '16/Jan/2015',
        '29/Jan/2015',
        '28/Feb/2015', '18/Feb/2015', '08/May/2015', '20/Jan/2015', '24/Jan/2015', '31/Mar/2015', '30/Apr/2015',
        '17/Feb/2015',
        '19/Mar/2015', '05/May/2015', '22/Jan/2015', '14/Aug/2015', '26/Feb/2015', '14/Mar/2015', '28/May/2015']

days_sorted = sorted(days, key=lambda day: datetime.strptime(day, "%d/%b/%Y"))
print(days_sorted)
