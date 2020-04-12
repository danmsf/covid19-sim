import numpy as np
import pandas as pd
import altair as alt
from statsmodels.tsa.api import SimpleExpSmoothing, Holt

class Parameters2:
    def __init__(self, tau, init_infected, fi, theta, scenario, comparator_country, contagion_pi_country, countries):
        self.tau = tau
        self.init_infected = init_infected
        self.fi = fi  # proportion of infectives are never diagnosed
        self.theta = theta  # diagnosis daily rate

        self.scenario = scenario
        self.comparator_country = comparator_country
        self.contagion_pi_country = contagion_pi_country
        self.countries = countries


class OLG:
    """
    calc_asymptomatic start from first case
    exposed are the asymptomatic_infected with lag not only infected
    asymptomatic_infected eq 10 does not always grow but uses two diferent R0

    fi  # proportion of infectives are never diagnosed
    theta = theta  # diagnosis daily rate

    """

    def __init__(self, df, p: Parameters2):
        self.detected = []
        self.r_adj = np.array([])
        self.r_values = np.array([])
        self.R0D = int
        self.asymptomatic_infected = []
        self.df = pd.DataFrame()
        self.r_contagion = []

        self.tmp = None

        self.iter_countries(df, tau=p.tau, init_infected=p.init_infected, theta=p.theta, fi=p.fi, scenario=p.scenario,
                            comparator_country=p.comparator_country, contagion_pi_country=p.contagion_pi_country,
                            countries=p.countries)

    @staticmethod
    def next_gen(r0, tau, c0, ct):
        r0d = r0 / tau
        return ct * (1 + r0d) ** tau - c0 * r0d * (1 + r0d) ** (tau - 1)

    @staticmethod
    def true_a(fi, theta, d, d_prev):
        delta_detected = (d - d_prev)
        prev_asymptomatic_infected = 1 / (1 - fi) * (delta_detected / theta + d_prev)
        return prev_asymptomatic_infected

    @staticmethod
    def project_contagion(pi, r_prev, comparator_r_prev, comparator_r, s_prev, s, s_comparator_prev, s_comparator):
        r_comparator_delta_ln = np.log(comparator_r) / np.log(comparator_r_prev) - 1
        s_delta = s / s_prev - 1
        s_comparator_delta = s_comparator / s_comparator_prev - 1
        ln_r = np.log(r_prev) + r_comparator_delta_ln + pi * (s_delta - s_comparator_delta)
        return np.exp(ln_r)

    def iter_countries(self, df, tau, init_infected, theta, fi, scenario,
                       comparator_country, contagion_pi_country, countries='Israel'):
        for country in countries:
            df_tmp = df[df['Country'] == country].copy()
            self.process(detected=df_tmp['I'].values, init_infected=init_infected)
            self.calc_r(tau=tau, init_infected=init_infected, scenario=scenario)
            self.predict(tau=tau, scenario=scenario)
            self.calc_asymptomatic(fi=fi, theta=theta, init_infected=init_infected)
            self.write(df_tmp, tau=tau)


        if comparator_country is not None:
            df = df[df['Country'] == comparator_country].copy()
            self.calc_r(tau=tau, init_infected=init_infected, scenario=scenario)
            self.write_comparator(df)
        #     self.policy_on_contagion(countries, contagion_pi_country)

    def process(self, detected, init_infected):
        day_0 = np.argmax(detected > init_infected)
        detected = detected[day_0 - 1:]
        self.detected = []
        for t in range(1, len(detected)):
            self.detected.append(max(detected[t - 1] + 1, detected[t]))

    def calc_r(self, tau, init_infected, scenario):
        detected = self.detected
        forcast_cnt = sum(scenario['t'].values())
        r_values = np.array([(detected[0] / (init_infected + 1e-05) - 1) * tau])

        for t in range(1, len(detected)):
            if t <= tau:
                r_value = (detected[t] / (detected[t - 1] + 1e-05) - 1) * tau
            else:
                r_value = (detected[t] / (detected[t - 1] - detected[t - tau] + detected[t - tau - 1]) - 1) * tau
            r_values = np.append(r_values, max(r_value, 0))

        # holt_model = Holt(r_values, exponential=True).fit(smoothing_level=0.8, smoothing_slope=0.2)
        # holt = holt_model.forecast(forcast_cnt)

        r_adj_model = np.convolve(r_values, np.ones((tau,)) / tau, mode='full')[:-tau + 1]

        exp_smot_model = SimpleExpSmoothing(r_values[-tau:]).fit()
        exp_smot = exp_smot_model.forecast(forcast_cnt)

        # print(len(holt_model), len(r_adj_model), len(exp_smot))


        self.r_values, self.R0D, self.r_adj  = r_values, exp_smot[-1], r_values

    def predict(self, tau, scenario):
        t = len(self.detected) - tau
        cnt = 0

        for i in scenario['t'].keys():
            while cnt <= scenario['t'].get(i):
                c0 = self.detected[t - tau] if t - tau >= 0 else 0
                next_gen = self.next_gen(r0=self.R0D * (scenario['R0D'].get(i) + 1), tau=tau, c0=c0,
                                         ct=self.detected[t])
                self.detected.append(next_gen)
                t += 1
                cnt += 1

    def calc_asymptomatic(self, fi, theta, init_infected):
        asymptomatic_infected = [self.true_a(fi=fi, theta=theta, d=self.detected[0], d_prev=init_infected)]

        for t in range(1, len(self.detected)):
            prev_asymptomatic_infected = self.true_a(fi=fi, theta=theta, d=self.detected[t],
                                                     d_prev=self.detected[t - 1])
            asymptomatic_infected.append(
                max(prev_asymptomatic_infected, asymptomatic_infected[-1]))  # not in Michel's paper!!!!!!!

        self.asymptomatic_infected = asymptomatic_infected

    def write(self, df, tau):
        forcast_cnt = len(self.detected) - len(self.r_adj)
        df = df[-len(self.r_adj):][['Country', 'StringencyIndex']].copy()

        df['r_values'] = self.r_values
        df['R'] = self.r_adj
        df['I'] = self.detected[:len(self.r_adj)]

        predicted = pd.DataFrame(
            {'I': self.detected[-forcast_cnt:],
             'R': self.R0D})
        df = df.append(predicted, ignore_index=True)

        df['A'] = self.asymptomatic_infected
        df['A'] = df['A'].shift(periods=-1)
        df['E'] = df['A'].shift(periods=-tau - 1)
        df['A'] = df['A'] - df['I']
        df['Country'].fillna(method='ffill', inplace=True)
        df['corona_days'] = pd.Series(range(1, len(df) + 1))
        df['prediction_ind'] = np.where(df['corona_days'] < len(self.r_adj), 0, 1)
        self.df = pd.concat([self.df, df])

    def write_comparator(self, df):

        comparator_df = pd.DataFrame({'comparator_R':self.r_adj})
        comparator_df['comparator_Stringency'] = df[-len(self.r_adj):][['StringencyIndex']].copy()
        comparator_df['corona_days'] = list(range(1, comparator_df.shape[0] + 1))

        self.df = self.df.merge(comparator_df, on='corona_days', how='left')
        self.df['comparator_R'].fillna(self.R0D, inplace=True)

    def policy_on_contagion(self, countries, contagion_pi_country):
        for country in countries:
            print(country)
            tmp_country_df = self.df.query('Country == @country').copy()
            print(len(tmp_country_df))
            tmp_country_df[['R_prev', 'comparator_R_prev', 'StringencyIndex_prev', 'comparator_Stringency_prev']] \
                = tmp_country_df[['R', 'comparator_R', 'StringencyIndex', 'comparator_Stringency']].shift(periods=1)
            tmp_country_df['R_contagion_score'] = tmp_country_df.apply(
                lambda row: self.project_contagion(contagion_pi_country,
                                                   row['R_prev'],
                                                   row['comparator_R_prev'],
                                                   row['comparator_R'],
                                                   row['StringencyIndex_prev'],
                                                   row['StringencyIndex'],
                                                   row['comparator_Stringency_prev'],
                                                   row['comparator_Stringency']
                                                   ),
                axis=1)

            tmp_country_df.drop(['R_prev', 'comparator_R_prev', 'StringencyIndex_prev', 'comparator_Stringency_prev'],
                                axis=1, inplace=True)
            self.df = self.df.query('Country != @country').append(tmp_country_df)

    def plot_data(self, countries, var_in_multi_line='I'):
        country_count = self.df['Country'].nunique()

        if country_count == len(countries):
            plot_df = self.df.query('prediction_ind==0').melt(id_vars=['corona_days'], value_vars=['A', 'I', 'E'])
            plot_df_predict = self.df.query('prediction_ind==1').melt(id_vars=['corona_days'], value_vars=['A', 'I'])

        else:
            plot_df = self.df.query('prediction_ind==0').pivot(index='corona_days', columns='Country',
                                                               values=var_in_multi_line).reset_index().melt(
                id_vars=['corona_days'],
                value_vars=countries)
            plot_df_predict = self.df.query('prediction_ind==1').pivot(index='corona_days', columns='Country',
                                                                       values=var_in_multi_line).reset_index().melt(
                id_vars=['corona_days'],
                value_vars=countries)

        plot_df.dropna(inplace=True)
        plot_df_predict.dropna(inplace=True)
        plot_df['value'] = plot_df['value'].astype('int64')
        plot_df_predict['value'] = plot_df_predict['value'].astype('int64')

        color_group = 'variable' if country_count == 1 else 'Country'

        # The basic line
        line = alt.Chart(plot_df).mark_line(interpolate='basis').encode(
            x='corona_days:Q',
            y='value',
            color=color_group
        )

        line2 = alt.Chart(plot_df_predict).mark_line(interpolate='basis', strokeDash=[1, 1]).encode(
            x='corona_days:Q',
            y='value',
            color=color_group
        )

        return alt.layer(
            line, line2
        ).properties(
            width=600, height=300
        )

    def plot_data_contagion_score(self):

        plot_df = self.df.query('prediction_ind==0')[['corona_days', 'StringencyIndex', 'r_values']]
        plot_df = plot_df.melt(id_vars=['corona_days'], value_vars=['StringencyIndex', 'r_values']).dropna()

        plot_df_contagion = self.df.query('prediction_ind==0')[['corona_days', 'R_contagion_score']]
        # plot_df_contagion['R_contagion_score'].clip(upper=10, inplace=True)
        plot_df_contagion = plot_df_contagion.melt(id_vars=['corona_days'], value_vars=['R_contagion_score'])

        line = alt.Chart(plot_df).mark_line(interpolate='basis').encode(
            x='corona_days:Q',
            y='value',
            color='variable'
        )

        line2 = alt.Chart(plot_df_contagion).mark_line(interpolate='basis', strokeDash=[1, 1]).encode(
            x='corona_days:Q',
            y='value',
            color='variable'
        )

        return alt.vconcat(line, line2).configure_view(stroke='transparent')
