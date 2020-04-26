import pandas as pd
dt = '20200426'
dt = '20200424'
dt = '20200420'
path_in = "C:\\Users\\User\\PycharmProjects\\covad19-sim\\ETL\\DW\\raw_data\\gov_yishuv\\"
path_out = "C:\\Users\\User\\PycharmProjects\\covad19-sim\\Resources\\Datasets\\IsraelData\\"
file = "כלל הארץ לשליחה 26.04.20 שעה 09.00.xlsx"
file = "כלל הארץ 24.04.20 לשליחה.xlsx"
file = "20.04 כלל הארץ לשליחה.xlsx"

t = pd.read_excel(path_in + file,skiprows=7)
colnames = t.columns
new_names = \
[
"יישוב",
"pop2018",
"מספר נבדקים",
"מספר חולים מאומתים",
"מספר מחלימים",
"pct_growth_3",
"new_last_3",
"per_100k",
# "junk",
]
t.columns = new_names
t = t.melt(id_vars=new_names[0:2], value_vars=new_names[2:])
t = t[~t['variable'].isin(['pct_growth_3', 'junk', 'new_last_3', 'per_100k'])]
t = t.rename(columns={'variable': 'סוג מידע'})
t['date'] = pd.to_datetime(dt)
t.loc[:, 'StringencyIndex'] = 1.
t.to_csv(path_out + 'yishuv_' + dt + ".csv", index=False)

kl = ['20200426', '20200424', '20200420']
joined = pd.concat([pd.read_csv(path_out + 'yishuv_' + x + ".csv") for x in kl])
joined.to_csv(path_out + 'yishuv_file.csv', index=False)