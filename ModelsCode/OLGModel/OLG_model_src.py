import numpy as np
import pandas as pd
import altair as alt
from statsmodels.tsa.api import SimpleExpSmoothing, Holt


class Parameters2:
    def __init__(self, tau, init_infected, fi, theta, scenario, countries, critical_condition_rate, recovery_rate, critical_condition_time,recovery_time):
        self.tau = tau
        self.init_infected = init_infected
        self.fi = fi  # proportion of infectives are never diagnosed
        self.theta = theta  # diagnosis daily rate

        self.scenario = scenario
        self.countries = countries
        self.critical_condition_rate = critical_condition_rate
        self.recovery_rate = recovery_rate
        self.critical_condition_time = critical_condition_time
        self.recovery_time = recovery_time


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
        self.r0d = int
        self.asymptomatic_infected = []
        self.df = pd.DataFrame()
        self.tmp = None


        self.iter_countries(df, p)

    @staticmethod
    def next_gen(r0, tau, c0, ct):
        r0d = r0 / tau
        # return ct * (1 + r0d) ** tau - c0 * r0d * (1 + r0d) ** (tau - 1) # Eq 2
        return c0 * (r0d) + ct

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

    # def iter_countries(self, df, p, init_infected=p.init_infected, theta=p.theta, fi=p.fi, scenario=p.scenario,
    #                         countries=p.countries, critical_condition_rate=p.critical_condition_rate,
    #                         recovery_rate= p.recovery_rate, critical_condition_time=p.critical_condition_time, recovery_time=p.recovery_time countries='israel')

    def iter_countries(self, df, p):

        for country in p.countries:
            df_tmp = df[df['country'] == country].copy()
            self.process(detected=df_tmp['I'].values, init_infected=p.init_infected)
            self.calc_r(tau=p.tau, init_infected=p.init_infected, scenario=p.scenario)
            self.predict(tau=p.tau, scenario=p.scenario)
            self.calc_asymptomatic(fi=p.fi, theta=p.theta, init_infected=p.init_infected)
            self.write(df_tmp, tau=p.tau, critical_condition_rate=p.critical_condition_rate,
                       recovery_rate=p.recovery_rate, critical_condition_time=p.critical_condition_time,
                       recovery_time=p.recovery_time)

    def process(self, detected, init_infected):

        day_0 = np.argmax(detected > init_infected)
        detected = detected[day_0 - 1:]
        print('detected', detected)
        self.detected = []
        for t in range(1, len(detected)):
            self.detected.append(max(detected[t - 1] + 1, detected[t]))

    def calc_r(self, tau, init_infected, scenario):
        detected = self.detected
        r_values = np.array([(detected[0] / (init_infected + 1e-05) - 1) * tau])

        for t in range(1, len(detected)):
            if t <= tau:
                r_value = (detected[t] / (detected[t - 1] + 1e-05) - 1) * tau
            elif t > tau:
                r_value = (detected[t] / (detected[t - 1] - detected[t - tau] + detected[t - tau - 1]) - 1) * tau
            r_values = np.append(r_values, max(r_value, 0))
        # print(len(holt_model), len(r_adj_model), len(exp_smot))
        self.r_values = r_values

    def predict(self, tau, scenario):
        forcast_cnt = sum(scenario['t'].values())
        t = len(self.detected) - 1
        cnt, predicted_cnt = 0, 0

        # holt_model = Holt(self.r_values[-tau:], exponential=True).fit(smoothing_level=0.6, smoothing_slope=0.3)
        #
        # self.r0d = holt_model.forecast(forcast_cnt)

        r_adj_model = np.convolve(self.r_values, np.ones((tau,)) / tau, mode='full')[:-tau + 1]

        exp_smot_model = SimpleExpSmoothing(self.r_values[-tau:]).fit()
        self.r0d = np.linspace(0.5, 0.05, forcast_cnt+15)[:forcast_cnt] #exp_smot_model.forecast(forcast_cnt)

        self.r_adj = self.r_values

        for i in scenario['t'].keys():
            predicted_cnt += cnt
            cnt = 0
            while cnt < scenario['t'].get(i):
                c0 = self.detected[t - tau] if t - tau >= 0 else 0
                next_gen = self.next_gen(r0=self.r0d[cnt + predicted_cnt] * (scenario['r0d'].get(i) + 1), tau=tau,
                                         c0=c0, ct=self.detected[t])
                print(self.r0d[cnt + predicted_cnt] * (scenario['r0d'].get(i) + 1), c0, self.detected[t], next_gen, )
                self.detected.append(next_gen)
                t += 1
                cnt += 1


    def calc_asymptomatic(self, fi, theta, init_infected):
        asymptomatic_infected = [self.true_a(fi=fi, theta=theta, d=self.detected[0], d_prev=init_infected)]

        for t in range(1, len(self.detected)):
            prev_asymptomatic_infected = self.true_a(fi=fi, theta=theta, d=self.detected[t],
                                                     d_prev=self.detected[t - 1])
            # asymptomatic_infected.append(
            #     max(prev_asymptomatic_infected, asymptomatic_infected[-1]))  # not in Michel's paper!!!!!!!

            asymptomatic_infected.append(prev_asymptomatic_infected)
        self.asymptomatic_infected = asymptomatic_infected

    def write(self, df, tau, critical_condition_rate, recovery_rate, critical_condition_time, recovery_time):
        forcast_cnt = len(self.detected) - len(self.r_adj)
        df = df[-len(self.r_adj):][['date', 'country', 'StringencyIndex', ]].copy()

        df['r_values'] = self.r_values
        df['R'] = self.r_adj
        df['I'] = self.detected[:len(self.r_adj)]

        predict_date = df['date'].max() + pd.to_timedelta(1, unit="D")
        prediction_dates = pd.date_range(start=predict_date.strftime('%Y-%m-%d'), periods=forcast_cnt)

        predicted = pd.DataFrame(
            {'date': prediction_dates,
             'I': self.detected[-forcast_cnt:],
             'R': self.r0d,
             })
        df = df.append(predicted, ignore_index=True)

        df['A'] = self.asymptomatic_infected
        df['A'] = df['A'].shift(periods=-1)

        # df['I_prev'] = df['I'].shift(periods=-1)
        df['dI'] = df['I'] - df["I"].shift(1)
        df['E'] = df['A'].shift(periods=-tau - 1)
        df['A'] = df['A'] - df['I']
        df['country'].fillna(method='ffill', inplace=True)
        df['corona_days'] = pd.Series(range(1, len(df) + 1))
        df['prediction_ind'] = np.where(df['corona_days'] < len(self.r_adj), 0, 1)

        df['cur_I'] = np.where(df['corona_days'] < (critical_condition_time+recovery_time),
                               df['I'],
                               df['I'] - df['I'].shift(periods=+critical_condition_time+recovery_time))

        df['Critical_condition'] = df['cur_I'] * critical_condition_rate
        df['Recovery_Critical'] = df['Critical_condition'] * recovery_rate
        df['Mortality_Critical'] = df['Critical_condition'] - df['Recovery_Critical']

        df['Critical_condition'] = df['Critical_condition'].shift(periods=critical_condition_time).round(0)
        df[['Mortality_Critical', 'Recovery_Critical']] = df[['Mortality_Critical', 'Recovery_Critical']].shift(periods=critical_condition_time+recovery_time).round(0)
        self.df = pd.concat([self.df, df])

    def plot_data(self, countries, var_in_multi_line='I'):
        country_count = self.df['country'].nunique()

        if country_count == len(countries):
            plot_df = self.df.query('prediction_ind==0').melt(id_vars=['corona_days'], value_vars=['A', 'I', 'E'])
            plot_df_predict = self.df.query('prediction_ind==1').melt(id_vars=['corona_days'],
                                                                      value_vars=['A', 'I', 'E'])

        else:
            plot_df = self.df.query('prediction_ind==0').pivot(index='corona_days', columns='country',
                                                               values=var_in_multi_line).reset_index().melt(
                id_vars=['corona_days'],
                value_vars=countries)
            plot_df_predict = self.df.query('prediction_ind==1').pivot(index='corona_days', columns='country',
                                                                       values=var_in_multi_line).reset_index().melt(
                id_vars=['corona_days'],
                value_vars=countries)

        plot_df.dropna(inplace=True)
        plot_df_predict.dropna(inplace=True)
        plot_df['value'] = plot_df['value'].astype('int64')
        plot_df_predict['value'] = plot_df_predict['value'].astype('int64')

        color_group = 'variable' if country_count == 1 else 'country'

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


print("hello")
scenario = {'t': {0: 20, 1: 90},
            'r0d': {0: 0, 1: 0}} ## TODO t: == 20+

p = Parameters2(tau=14,
                init_infected=100,
                fi=0.25,
                theta=0.0771,
                countries=['israel'],
                scenario=scenario,
                critical_condition_rate=0.05,
                       recovery_rate=0.4,
                critical_condition_time=10,
                       recovery_time=6
               )

df = pd.read_csv('C:\\Users\\User\\PycharmProjects\\covad19-sim\\Resources\\all_dates.csv')
olg_model = OLG(df, p)
