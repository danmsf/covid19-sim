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
p21 = pd.read_csv(path_out + 'yishuv_' + '20200420' + ".csv")
p21['date'] = pd.to_datetime('20200421')
p22 = p21.copy()
p22['date'] = pd.to_datetime('20200422')
p23 = p22.copy()
p23['date'] = pd.to_datetime('20200423')

p24 = pd.read_csv(path_out + 'yishuv_' + '20200424' + ".csv")
p24['date'] = pd.to_datetime('20200424')
p25 = p24.copy()
p25['date'] = pd.to_datetime('20200425')
p26 = pd.read_csv(path_out + 'yishuv_' + '20200426' + ".csv")

joined = pd.concat([p21,p22,p23,p24,p25,p26])
joined.to_csv(path_out + 'yishuv_file.csv', index=False)
temp = pd.read_csv("C:\\Users\\User\\PycharmProjects\\covad19-sim\\Resources\\Datasets\\IsraelData\\gsheets.csv")