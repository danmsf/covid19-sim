import pandas as pd
dt = '20200426'
dt = '20200424'
dt = '20200420'

dt = '20200430'
dt = '20200429'
dt = '20200501'
dt = '20200502'
dt = '20200504'


dt = '20200506'
dt = '20200505'
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
file ="דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_06_05_20_שעה_11_00.xlsx"
file  = "כלל_הארץ_כולל_מועצות_אזוריות_לפרסום_05_05_שעה_11_00.xlsx"


dt = '20200508'
file = "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_08_05_20_שעה_11_00.xlsx"
# dt = '20200509'
# file = "1589011501844_דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_09_05_20_שעה.xlsx"
# dt = '20200510'
# file = "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_10_05_20_שעה_11_00.xlsx"
# dt = '20200511'
# file = "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_11_05_20_שעה_11_00.xlsx"
dt = '20200512'
file = "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_12_05_20_שעה_11_00.xlsx"
t = pd.read_excel(path_in + file, skiprows=4)
t = t.drop(columns=['Unnamed: 9','Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12','Unnamed: 13','Unnamed: 14'])
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

p05 = pd.read_csv(path_out + 'yishuv_' + '20200505' + ".csv")
p06 = pd.read_csv(path_out + 'yishuv_' + '20200506' + ".csv")
joined = pd.concat([p05, p06])
joined = joined.dropna(subset=['יישוב', 'pop2018'])

p07 = pd.read_csv(path_out + 'yishuv_' + '20200506' + ".csv")
p07['date'] = pd.to_datetime('20200507')
p08 = pd.read_csv(path_out + 'yishuv_' + '20200508' + ".csv")
p09 = pd.read_csv(path_out + 'yishuv_' + '20200509' + ".csv")
p10 = pd.read_csv(path_out + 'yishuv_' + '20200510' + ".csv")
p11 = pd.read_csv(path_out + 'yishuv_' + '20200511' + ".csv")
joined = pd.concat([p07, p08, p09, p10, p11])
joined = joined.dropna(subset=['יישוב', 'pop2018'])

joined = pd.read_csv(path_out + 'yishuv_' + '20200512' + ".csv")
joined = joined.dropna(subset=['יישוב', 'pop2018'])

yishuv_file = pd.read_csv(path_out + 'yishuv_file.csv')
yishuv_file = pd.concat([yishuv_file, joined])

yishuv_file['date'] = pd.to_datetime(yishuv_file['date'])

yishuv_file['last_updated'] = pd.to_datetime('20200512')

yishuv_file.to_csv(path_out + 'yishuv_file.csv', index=False)

# temp = pd.read_csv("C:\\Users\\User\\PycharmProjects\\covad19-sim\\Resources\\Datasets\\IsraelData\\gsheets.csv")