import pandas as pd
dt = '20200426'
dt = '20200424'
dt = '20200420'

dt = '20200430'
dt = '20200429'
dt = '20200501'
dt = '20200502'
dt = '20200504'
path_in = "C:\\Users\\User\\PycharmProjects\\covad19-sim\\ETL\\DW\\raw_data\\gov_yishuv\\"
path_out = "C:\\Users\\User\\PycharmProjects\\covad19-sim\\Resources\\Datasets\\IsraelData\\"
file = "כלל הארץ לשליחה 26.04.20 שעה 09.00.xlsx"
file = "כלל הארץ 24.04.20 לשליחה.xlsx"
file = "20.04 כלל הארץ לשליחה.xlsx"

file = "כלל הארץ לפרסום 30.04.20 שעה 08.00.xlsx"
# file = "כלל הארץ לשליחה 29.04.20 שעה 08.00.xlsx"

file = "כלל_הארץ_ומועצות_אזוריות_01_05_לפרסום.xlsx"
file = "כלל_הארץ_ומועצות_אזוריות_02_05_שעה_08_00_לפרסום.xlsx"
file = "דוח_חדש_כלל_הארץ_כולל_מועצות_אזוריות_04_05_20_שעה_20_30.xlsx"
t = pd.read_excel(path_in + file, skiprows=4)
# t = t.drop(columns=['Unnamed: 9','Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12'])
colnames = t.columns
new_names = \
[
"יישוב",
"pop2018",
"מספר נבדקים",
"מספר חולים מאומתים",
"מספר מחלימים",
"pct_growth_3",
"last3days",
"per_100k",
"junk",
]
t.columns = new_names
t = t.melt(id_vars=new_names[0:2], value_vars=new_names[2:])
t = t[~t['variable'].isin(['pct_growth_3', 'junk', 'per_100k'])]
t['value'] = pd.to_numeric(t['value'], errors='coerce').fillna(0).astype(int)
t = t.rename(columns={'variable': 'סוג מידע'})
t['date'] = pd.to_datetime(dt)
t.loc[:, 'StringencyIndex'] = None
t.to_csv(path_out + 'yishuv_' + dt + ".csv", index=False)

#-----------------------------Join files------------------------

p27 = pd.read_csv(path_out + 'yishuv_' + '20200426' + ".csv")
p27['date'] = pd.to_datetime('20200427')
p28 = p27.copy()
p28['date'] = pd.to_datetime('20200428')

p29 = pd.read_csv(path_out + 'yishuv_' + '20200429' + ".csv")
p30 = pd.read_csv(path_out + 'yishuv_' + '20200430' + ".csv")
joined = pd.concat([p27,p28,p29,p30])
joined = joined.dropna(subset=['יישוב', 'pop2018'])

p01 = pd.read_csv(path_out + 'yishuv_' + '20200501' + ".csv")
p02 = pd.read_csv(path_out + 'yishuv_' + '20200502' + ".csv")
joined = pd.concat([p01,p02])
joined = joined.dropna(subset=['יישוב', 'pop2018'])

p03 = pd.read_csv(path_out + 'yishuv_' + '20200502' + ".csv")
p03['date'] = pd.to_datetime('20200503')
p04 = t
joined = pd.concat([p03,p04])
joined = joined.dropna(subset=['יישוב', 'pop2018'])

yishuv_file = pd.read_csv(path_out + 'yishuv_file.csv')
yishuv_file = pd.concat([yishuv_file, joined])
yishuv_file['date'] = pd.to_datetime(yishuv_file['date'])

yishuv_file['last_updated'] = pd.to_datetime('20200504')

yishuv_file.to_csv(path_out + 'yishuv_file.csv', index=False)

# temp = pd.read_csv("C:\\Users\\User\\PycharmProjects\\covad19-sim\\Resources\\Datasets\\IsraelData\\gsheets.csv")