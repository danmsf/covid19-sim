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
files = ["כלל הארץ לשליחה 26.04.20 שעה 09.00.xlsx",
         "כלל הארץ 24.04.20 לשליחה.xlsx",
         "20.04 כלל הארץ לשליחה.xlsx",
         "כלל הארץ לפרסום 30.04.20 שעה 08.00.xlsx",
         "כלל הארץ לשליחה 29.04.20 שעה 08.00.xlsx",
         "כלל_הארץ_ומועצות_אזוריות_01_05_לפרסום.xlsx",
         "כלל_הארץ_ומועצות_אזוריות_02_05_שעה_08_00_לפרסום.xlsx",
         "דוח_חדש_כלל_הארץ_כולל_מועצות_אזוריות_04_05_20_שעה_20_30.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_06_05_20_שעה_11_00.xlsx",
         "כלל_הארץ_כולל_מועצות_אזוריות_לפרסום_05_05_שעה_11_00.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_08_05_20_שעה_11_00.xlsx",
         "1589011501844_דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_09_05_20_שעה.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_10_05_20_שעה_11_00.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_11_05_20_שעה_11_00.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_12_05_20_שעה_11_00.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_15_05_20_שעה_11_00.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_18_05_20_שעה_11_00.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_20_05_20_שעה_19_30.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_21_05_20_שעה_19_30.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_24_05_20_שעה_19_30.xlsx",
         "דוח_אקסל_כלל_הארץ_כולל_מועצות_אזוריות_25_05_20_שעה_19_30.xlsx"
         ]

dates = ['20200508',
         '20200509',
         '20200510',
         '20200511',
         '20200512',
         '20200515',
         '20200518',
         '20200519',
         '20200521',
         '20200524',
         '20200525'
         ]

file = files[-1]
dt = dates[-1]

t = pd.read_excel(path_in + file, skiprows=4)
t = t.drop(columns=['Unnamed: 9', 'Unnamed: 10', 'Unnamed: 11', 'Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14'])
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

# -----------------------------Join files------------------------

p22 = pd.read_csv(path_out + 'yishuv_' + '20200521' + ".csv")
p22['date'] = pd.to_datetime('20200522')
p23 = pd.read_csv(path_out + 'yishuv_' + '20200521' + ".csv")
p23['date'] = pd.to_datetime('20200523')
p24 = pd.read_csv(path_out + 'yishuv_' + '20200524' + ".csv")
p25 = pd.read_csv(path_out + 'yishuv_' + '20200525' + ".csv")
joined = pd.concat([p22, p23, p24, p25])
joined = joined.dropna(subset=['יישוב', 'pop2018'])

yishuv_file = pd.read_csv(path_out + 'yishuv_file.csv')
yishuv_file = pd.concat([yishuv_file, joined])
yishuv_file['last_updated'] = pd.to_datetime('20200525')
yishuv_file['date'] = pd.to_datetime(yishuv_file['date']).dt.date
yishuv_file.to_csv(path_out + 'yishuv_file.csv', index=False)

# temp = pd.read_csv("C:\\Users\\User\\PycharmProjects\\covad19-sim\\Resources\\Datasets\\IsraelData\\gsheets.csv")
