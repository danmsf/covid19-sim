import streamlit as st

import pandas as pd
import numpy as np
import numpy as np
import statsmodels.api as sm

from datetime import timedelta

# from src.shared.models.model_olg import *
# from src.shared.models.data import CountryData
# from src.shared.charts.charts_olg import *
# from src.shared.utils import get_table_download_link
# import altair as alt
# from src.shared.settings import DEFAULTS, load_data, user_session_id
class NaiveParameters:
    """Parameters."""

    def __init__(self, *, tau: int, init_infected: int):
        self.tau = tau
        self.init_infected = init_infected


class naiveModel:
    def __init__(self, df, p):
        self.stringency_df = df
        self.tau = p.tau
        self.init_infected = p.init_infected
        self.df, self.israel_day = self.calc_df()

    #     # st.cache
    #     def get_file(self):
    #         return pd.read_csv(pathfile, parse_dates=['Date'])

    def calc_r(self, detected):
        epsilon = 1e-06
        init_infected = self.init_infected
        tau = self.tau
        r_values = np.array([(detected[0] / (init_infected + epsilon) - 1) * tau])
        for t in range(1, len(detected)):
            if t <= tau:
                r_value = (detected[t] / (detected[t - 1] + epsilon) - 1) * tau
            elif t > tau:
                r_value = (detected[t] / (
                            detected[t - 1] - detected[t - tau] + detected[t - tau - 1] + epsilon) - 1) * tau
            r_values = np.append(r_values, max(r_value, 0))
            r_adj = np.convolve(r_values, np.ones(int(tau, )) / int(tau), mode='full')[:len(detected)]
            r_adj = np.clip(r_adj, 0, 100)
        # self.r_values, self.r_adj, self.r0d = r_values, r_adj, r_adj
        print(len(detected), len(r_adj))
        return r_adj

    def norm_r(self, df):
        # calculate corona days and cutoff
        df = df[df['ConfirmedCases'] >= self.init_infected]
        df['day0'] = df.groupby('CountryName')['Date'].transform(min)
        df['corona_days'] = (df['Date'] - df['day0']).dt.days

        # get todays Israel day - and current R and S
        israel_day = df[df['CountryName'] == 'Israel']['corona_days'].max()
        israel_stringency = df[(df['CountryName'] == 'Israel') & (df['corona_days'] == israel_day)][
            'StringencyIndexForDisplay'].max()
        israel_r = df[(df['CountryName'] == 'Israel') & (df['corona_days'] == israel_day)]['r_adj'].max()

        # Normalize countries Rs to today's Israels R
        countryd_r = df[(df['corona_days'] == israel_day)][['CountryName', 'r_adj']]
        countryd_r['norm_r'] = israel_r - countryd_r['r_adj']
        df = pd.merge(df, countryd_r[['CountryName', 'norm_r']])
        df['r_adjn'] = df['r_adj'] + df['norm_r']
        return df, israel_day

    def calc_df(self):
        df = self.stringency_df
        df = df[df['ConfirmedCases'] > self.init_infected]
        df.sort_values(['CountryName', 'Date'], inplace=True)
        df['r_adj'] = df.groupby('CountryName')['ConfirmedCases'].transform(lambda x: self.calc_r(x.values))
        return self.norm_r(df)

    # logic for choosing countries is external
    # expecting input of type: df[df.CountryName.isin(countryList)]
    # @staticmethod
    def avgCountries(self, df):
        countries_avg = df[df['r_adjn'] > 0].groupby('corona_days', as_index=False)['r_adjn'].mean()
        lowess = sm.nonparametric.lowess
        countries_avg['r_adjn'] = lowess(countries_avg['r_adjn'], countries_avg['corona_days'], frac=1. / 10, it=0)[:, 1]
        countries_avg['prediction_ind'] = 1
        return countries_avg[countries_avg['corona_days'] > self.israel_day]

    def predict(self, countryList):
        pred = self.avgCountries(self.df[self.df.CountryName.isin(countryList)])
        df_israel = self.df.loc[self.df.CountryName == 'Israel', ['Date', 'corona_days', 'r_adjn', 'day0']]
        df_israel['prediction_ind'] = 0
        df_israel = pd.concat([df_israel, pred])
        df_israel['day0'] = df_israel['day0'].ffill()
        df_israel.loc[df_israel.prediction_ind == 1, 'Date'] = df_israel['day0'] + pd.to_timedelta(df_israel['corona_days'], unit='D')
        return df_israel

    # TODO: Add Predictions for Counts:

    #     self.predict_next_gen(tau=p.tau)
    #
    # self.calc_asymptomatic(fi=p.fi, theta=p.theta, init_infected=p.init_infected)
    # self.write(stringency, tau=p.tau, critical_condition_rate=p.critical_condition_rate,
    #            recovery_rate=p.recovery_rate, critical_condition_time=p.critical_condition_time,
    #            recovery_time=p.recovery_time)

# TODO: Control Model Parameters
def display_sidebar(naive_params):
    st.sidebar.subheader("GSTAT Naive Model parameters")
    naive_params['tau'] = st.sidebar.number_input(
        "Tau rate (number of days infectious)",
        min_value=2,
        value=naive_params['tau'],
        step=1,
        format="%i",
    )

    naive_params['init_infected'] = st.sidebar.number_input(
        "Minimum cases for calculation",
        min_value=0,
        value=naive_params['init_infected'],
        step=10,
        format="%i",
    )
    return naive_params


def display_filtes(filters_dict):
    filters_dict['days_range'] = st.sidebar.slider("Choose Corona Days Forward Range for Policy Value", 1, 20, (5, 10))
    filters_dict['stringency_range'] = st.sidebar.slider("Choose Stringency Range", 20., 100., (45., 90.))
    return filters_dict


def write():
    pathfile = "C:\\Users\\User\\Downloads\\OxCGRT_Download_280420_162625_Full.csv"
    data = pd.read_csv(pathfile, parse_dates=['Date'])
    naive_params = {'tau': 14, 'init_infected': 100, }
    naive_params = display_sidebar(naive_params)
    p = NaiveParameters(**naive_params)
    model = naiveModel(data, p)
    filters_dict = {'days_range': (1, 10), 'stringency_range': (45., 90.)}
    filters_dict = display_filtes(filters_dict)
    df_r = model.df.copy()
    cond = ((df_r['corona_days'] - model.israel_day).between(*filters_dict['days_range'])) & \
           (df_r['StringencyIndexForDisplay'].between(*filters_dict['stringency_range']))

    allCountries = list(df_r.loc[df_r['corona_days'] > model.israel_day]['CountryName'].unique())
    countryList = list(df_r.loc[cond]['CountryName'].unique())
    countryList = st.multiselect("Select Countries for prediction", allCountries, countryList)
    pred = model.predict(countryList)
    # st.write(pred)
    st.line_chart(pred.set_index('corona_days')['r_adjn'])
    print(naive_params)


if __name__ == "__main__":
    write()
