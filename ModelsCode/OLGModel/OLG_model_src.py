import numpy as np
import pandas as pd
import altair as alt
from statsmodels.tsa.api import SimpleExpSmoothing, Holt
from SimCode.src.penn_chime.models import CountryData
from penn_chime.settings import DEFAULTS


class Parameters:
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

    def __init__(self, df, p: Parameters):
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
        return (ct - c0)* (r0d) + ct

    @staticmethod
    def true_a(fi, theta, d, d_prev):
        delta_detected = (d - d_prev)
        prev_asymptomatic_infected = (1 / (1 - fi)) * (delta_detected / theta + d_prev)
        return prev_asymptomatic_infected

    @staticmethod
    def project_contagion(pi, r_prev, comparator_r_prev, comparator_r, s_prev, s, s_comparator_prev, s_comparator):
        r_comparator_delta_ln = np.log(comparator_r) / np.log(comparator_r_prev) - 1
        s_delta = s / s_prev - 1
        s_comparator_delta = s_comparator / s_comparator_prev - 1
        ln_r = np.log(r_prev) + r_comparator_delta_ln + pi * (s_delta - s_comparator_delta)
        return np.exp(ln_r)

    def iter_countries(self, df, p):
        for Country in p.countries:
            df_tmp = df[df['Country'] == Country].copy()
            self.process(detected=df_tmp['I'].values, init_infected=p.init_infected)
            self.calc_r(tau=p.tau, init_infected=p.init_infected)
            self.predict(tau=p.tau, scenario=p.scenario)
            self.calc_asymptomatic(fi=p.fi, theta=p.theta, init_infected=p.init_infected)
            self.write(df_tmp, tau=p.tau, critical_condition_rate=p.critical_condition_rate,
                       recovery_rate=p.recovery_rate, critical_condition_time=p.critical_condition_time,
                       recovery_time=p.recovery_time)

    def process(self, detected, init_infected):
        day_0 = np.argmax(detected > init_infected)
        detected = detected[day_0 - 1:]
        self.detected = []
        for t in range(1, len(detected)):
            self.detected.append(max(detected[t - 1] + 1, detected[t]))

    def calc_r(self, tau, init_infected):
        epsilon = 1e-06
        detected = self.detected
        r_values = np.array([(detected[0] / (init_infected + epsilon) - 1) * tau])

        for t in range(1, len(detected)):
            if t <= tau:
                r_value = (detected[t] / (detected[t - 1] + epsilon) - 1) * tau
            elif t > tau:
                r_value = (detected[t] / (detected[t - 1] - detected[t - tau] + detected[t - tau - 1]) - 1) * tau
            r_values = np.append(r_values, max(r_value, 0))
        # print(len(holt_model), len(r_adj_model), len(exp_smot))
        r_values = np.convolve(r_values, np.ones(int(tau/2,)) / int(tau/2), mode='full')[:len(detected)]

        self.r_values = r_values

    def predict(self, tau, scenario):
        forcast_cnt = sum(scenario['t'].values())
        t = len(self.detected) - 1
        cnt, predicted_cnt = 0, 0

        holt_model = Holt(self.r_values[-tau:], exponential=True).fit(smoothing_level=0.1, smoothing_slope=0.9)
        self.r0d = holt_model.forecast(forcast_cnt)

        # r_adj_model = np.convolve(self.r_values, np.ones((tau,)) / tau, mode='valid')[:-tau + 1]

        # exp_smot_model = SimpleExpSmoothing(self.r_values[-tau:]).fit()
        # exp_smot = exp_smot_model.forecast(forcast_cnt)

        self.r_adj = self.r_values
        temp = 0
        for i in scenario['t'].keys():
            predicted_cnt += cnt
            cnt = 0
            while cnt < scenario['t'].get(i):
                c0 = self.detected[t - tau] if t - tau >= 0 else 0
                if cnt == 0:
                    temp += self.r0d[predicted_cnt + cnt] * (scenario['R0D'].get(i))
                self.r0d[predicted_cnt + cnt] = (self.r0d[predicted_cnt + cnt] + temp)
                next_gen = self.next_gen(r0=self.r0d[predicted_cnt+cnt], tau=tau,
                                         c0=c0, ct=self.detected[t])
                # print(scenario['t'].get(i), cnt, c0, self.detected[t])
                self.detected.append(next_gen)
                t += 1
                cnt += 1

        # final decsecnt
        # self.r0d.clip(min=0.0001, inplace=True)
        end_forecast = holt_model.forecast(tau)
        end_forecast_normed = end_forecast / end_forecast.max(axis=0)
        end_r0d = end_forecast_normed * temp
        self.r0d = np.append(self.r0d, end_r0d)

        cnt = 0
        while cnt < tau:
            c0 = self.detected[t - tau] if t - tau >= 0 else 0
            next_gen = self.next_gen(r0=self.r0d[predicted_cnt + cnt], tau=tau,
                                     c0=c0, ct=self.detected[t])
            # print(predicted_cnt + cnt, self.r0d[predicted_cnt + cnt], t)
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

    def write(self, df_o, tau, critical_condition_rate, recovery_rate, critical_condition_time, recovery_time):
        forcast_cnt = len(self.detected) - len(self.r_adj)
        df = df_o[-len(self.r_adj):][['date', 'Country', 'StringencyIndex', ]].copy()

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
        # df['A'] = df['A'].shift(periods=-1)
        df['E'] = df['A'].shift(periods=-tau)
        # df['A'] = df['A'] - df['I']
        df['Country'].fillna(method='ffill', inplace=True)
        df['corona_days'] = pd.Series(range(1, len(df) + 1))
        df['prediction_ind'] = np.where(df['corona_days'] <  len(self.r_adj), 0, 1)

        df['Currently Infected'] = np.where(df['corona_days'] < (critical_condition_time+recovery_time),
                               df['I'],
                               df['I'] - df['I'].shift(periods=+critical_condition_time+recovery_time))

        df['Critical_condition'] = df['Currently Infected'] * critical_condition_rate
        df['Recovery_Critical'] = df['Critical_condition'] * recovery_rate
        df['Mortality_Critical'] = df['Critical_condition'] - df['Recovery_Critical']

        df['Critical_condition'] = df['Critical_condition'].shift(periods=critical_condition_time).round(0)
        df[['Mortality_Critical', 'Recovery_Critical']] = df[['Mortality_Critical', 'Recovery_Critical']].shift(periods=critical_condition_time+recovery_time).round(0)

        df['Doubling Time'] = np.log(2)/np.log(1+df['R']/tau)
        # print(df_o.columns)
        # df.loc[:len(self.r_adj), 'Critical_condition'] = df_o.loc[-len(self.r_adj):, 'serious_critical']
        df['temp_cr'] =None
        df_o = df_o.reset_index()
        # df = df.reset_index()
        print(len(self.r_adj))
        df['dI'] = df['I'] - df["I"].shift(1)
        df['dA'] = df['A'] - df["A"].shift(1)
        df['dE'] = df['E'] - df["E"].shift(1)
        df = df.merge(df_o[['date', 'serious_critical', 'new_cases', 'activecases']], "left")
        df['Critical_condition'] = np.where(~df['serious_critical'].isna(), df['serious_critical'], df['Critical_condition'])
        df['dI'] = np.where(~df['new_cases'].isna(), df['new_cases'], df['dI'])
        df['Currently Infected'] = np.where(~df['activecases'].isna(), df['activecases'], df['Currently Infected'])
        df = df.rename(columns={'I': 'Total Detected', 'A': 'Total Infected', 'E': 'Total Exposed',
                                'dI': 'New Detected', 'dA': 'New Infected', 'dE': 'New Exposed'})
        self.df = pd.concat([self.df, df])



scenario = {'t': {0: 20, 1: 90},
            'R0D': {0: 0, 1: 0}} ## TODO t: == 20+

p = Parameters(tau=14,
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





countrydata = CountryData(DEFAULTS.country_files)
# countrydata.stringency_df['CountryName'] = countrydata.stringency_df['CountryName'].str.lower()
countrydata = CountryData(DEFAULTS.country_files)
countrydata.country_df.drop('I', axis=1, inplace=True)
countrydata.country_df.rename(columns={'total_cases':'I'}, inplace=True)

country_dict = {'countries_list': set(countrydata.country_df['Country'].values)}
DEFAULTS.olg_params.update(country_dict)


DEFAULTS.olg_params['countries_list']

olg_model = OLG(countrydata.country_df, p)

# olg_model.df.to_csv('original_copy.csv', index=False)



# class OLG:
#     """
#     calc_asymptomatic start from first case
#     exposed are the asymptomatic_infected with lag not only infected
#     asymptomatic_infected eq 10 does not always grow but uses two diferent R0
#
#     fi  # proportion of infectives are never diagnosed
#     theta = theta  # diagnosis daily rate
#
#     """
#
#     def __init__(self, df, p: Parameters):
#         self.detected = []
#         self.r_adj = np.array([])
#         self.r_values = np.array([])
#         self.r0d = int
#         self.asymptomatic_infected = []
#         self.df = pd.DataFrame()
#         self.tmp = None
#
#         self.iter_countries(df, p)
#
#     @staticmethod
#     def next_gen(r0, tau, c0, ct):
#         r0d = r0 / tau
#         # return ct * (1 + r0d) ** tau - c0 * r0d * (1 + r0d) ** (tau - 1) # Eq 2
#         return c0 * (r0d) + ct
#
#     @staticmethod
#     def true_a(fi, theta, d, d_prev):
#         delta_detected = (d - d_prev)
#         prev_asymptomatic_infected = (1 / (1 - fi)) * (delta_detected / theta + d_prev)
#         return prev_asymptomatic_infected
#
#     @staticmethod
#     def project_contagion(pi, r_prev, comparator_r_prev, comparator_r, s_prev, s, s_comparator_prev, s_comparator):
#         r_comparator_delta_ln = np.log(comparator_r) / np.log(comparator_r_prev) - 1
#         s_delta = s / s_prev - 1
#         s_comparator_delta = s_comparator / s_comparator_prev - 1
#         ln_r = np.log(r_prev) + r_comparator_delta_ln + pi * (s_delta - s_comparator_delta)
#         return np.exp(ln_r)
#
#     def iter_countries(self, df, p):
#         for country in p.countries:
#             df_tmp = df[df['country'] == country].copy()
#             self.process(detected=df_tmp['I'].values, init_infected=p.init_infected)
#             self.calc_r(tau=p.tau, init_infected=p.init_infected, scenario=p.scenario)
#             self.predict(tau=p.tau, scenario=p.scenario)
#             self.calc_asymptomatic(fi=p.fi, theta=p.theta, init_infected=p.init_infected)
#             self.write(df_tmp, tau=p.tau, critical_condition_rate=p.critical_condition_rate,
#                        recovery_rate=p.recovery_rate, critical_condition_time=p.critical_condition_time,
#                        recovery_time=p.recovery_time)
#
#     def process(self, detected, init_infected):
#         day_0 = np.argmax(detected > init_infected)
#         detected = detected[day_0 - 1:]
#         self.detected = []
#         print(detected[:3])
#         for t in range(1, len(detected)):
#             print(t, detected[t - 1], detected[t])
#             self.detected.append(max(detected[t - 1] + 1, detected[t]))
#
#     def calc_r(self, tau, init_infected, scenario):
#         epsilon = 1e-06
#         detected = self.detected
#         r_values = np.array([(detected[0] / (init_infected + epsilon) - 1) * tau])
#
#         for t in range(1, len(detected)):
#             if t <= tau:
#                 r_value = (detected[t] / (detected[t - 1] + epsilon) - 1) * tau
#             elif t > tau:
#                 r_value = (detected[t] / (detected[t - 1] - detected[t - tau] + detected[t - tau - 1]) - 1) * tau
#             r_values = np.append(r_values, max(r_value, 0))
#         # print(len(holt_model), len(r_adj_model), len(exp_smot))
#         r_values = np.convolve(r_values, np.ones((int(tau/2),)) / int(tau/2), mode='full')[:len(detected)]
#
#         self.r_values = r_values
#
#     def predict(self, tau, scenario):
#         forcast_cnt = sum(scenario['t'].values())
#         t = len(self.detected) - 1
#         cnt, predicted_cnt = 0, 0
#
#         holt_model = Holt(self.r_values[-tau:], exponential=True).fit(smoothing_level=0.1, smoothing_slope=0.9)
#         self.r0d = holt_model.forecast(forcast_cnt)
#
#         r_adj_model = np.convolve(self.r_values, np.ones((tau,)) / tau, mode='full')[:-tau + 1]
#
#         exp_smot_model = SimpleExpSmoothing(self.r_values[-tau:]).fit()
#         exp_smot = exp_smot_model.forecast(forcast_cnt)
#         # self.r0d = np.linspace(self.r_values[-1], 0.05, forcast_cnt)[:forcast_cnt] #exp_smot_model.forecast(forcast_cnt)
#
#         self.r_adj = self.r_values
#
#         for i in scenario['t'].keys():
#             predicted_cnt += cnt
#             cnt = 0
#             while cnt < scenario['t'].get(i):
#                 c0 = self.detected[t - tau] if t - tau >= 0 else 0
#                 self.r0d[predicted_cnt+cnt] = self.r0d[predicted_cnt+cnt] * (scenario['R0D'].get(i) + 1)
#                 next_gen = self.next_gen(r0=self.r0d[predicted_cnt+cnt], tau=tau,
#                                          c0=c0, ct=self.detected[t])
#
#                 self.detected.append(next_gen)
#                 t += 1
#                 cnt += 1
#
#     def calc_asymptomatic(self, fi, theta, init_infected):
#         asymptomatic_infected = [self.true_a(fi=fi, theta=theta, d=self.detected[0], d_prev=init_infected)]
#
#         for t in range(1, len(self.detected)):
#             prev_asymptomatic_infected = self.true_a(fi=fi, theta=theta, d=self.detected[t],
#                                                      d_prev=self.detected[t - 1])
#             # asymptomatic_infected.append(
#             #     max(prev_asymptomatic_infected, asymptomatic_infected[-1]))  # not in Michel's paper!!!!!!!
#
#             asymptomatic_infected.append(prev_asymptomatic_infected)
#         self.asymptomatic_infected = asymptomatic_infected
#
#     def write(self, df_o, tau, critical_condition_rate, recovery_rate, critical_condition_time, recovery_time):
#         forcast_cnt = len(self.detected) - len(self.r_adj)
#         df = df_o[-len(self.r_adj):][['date', 'country', 'StringencyIndex']].copy()
#         print(df_o.columns)
#
#         df['r_values'] = self.r_values
#         df['R'] = self.r_adj
#         df['I'] = self.detected[:len(self.r_adj)]
#
#         predict_date = df['date'].max() + pd.to_timedelta(1, unit="D")
#         prediction_dates = pd.date_range(start=predict_date.strftime('%Y-%m-%d'), periods=forcast_cnt)
#
#         predicted = pd.DataFrame(
#             {'date': prediction_dates,
#              'I': self.detected[-forcast_cnt:],
#              'R': self.r0d,
#              })
#         df = df.append(predicted, ignore_index=True)
#
#         df['A'] = self.asymptomatic_infected
#         df['A'] = df['A'].shift(periods=-1)
#         df['E'] = df['A'].shift(periods=-tau -1)
#         # df['A'] = df['A'] - df['I']
#         df['corona_days'] = pd.Series(range(1, len(df) + 1))
#         df['prediction_ind'] = np.where(df['corona_days'] < len(self.r_adj), 0, 1)
#         df['dI'] = df['I'] - df["I"].shift(1)
#         df['dA'] = df['A'] - df["A"].shift(1)
#         df['dE'] = df['E'] - df["E"].shift(1)
#         df['Currently Infected'] = np.where(df['corona_days'] < (critical_condition_time+recovery_time),
#                                df['I'],
#                                df['I'] - df['I'].shift(periods=+critical_condition_time+recovery_time))
#
#         df['country'].fillna(method='ffill', inplace=True)
#         df['Currently Infected'].fillna(method='ffill', inplace=True)
#         df['Critical_condition'] = df['Currently Infected'] * critical_condition_rate
#         df['Recovery_Critical'] = df['Critical_condition'] * recovery_rate
#         df['Mortality_Critical'] = df['Critical_condition'] - df['Recovery_Critical']
#
#
#         df['Critical_condition'] = df['Critical_condition'].shift(periods=critical_condition_time).round(0)
#         df[['Mortality_Critical', 'Recovery_Critical']] = df[['Mortality_Critical', 'Recovery_Critical']].shift(periods=critical_condition_time+recovery_time).round(0)
#
#         df['Critical_condition_roll_sum'] = df['Critical_condition'].rolling(recovery_time).sum()
#         df['Critical_condition_roll_sum'] = df['Critical_condition_roll_sum'].shift(periods=critical_condition_time).round(0)
#
#
#         df['Doubling Time'] = np.log(2)/np.log(1+df['R']/tau)
#         df.rename(columns={'I': 'Total Detected', 'A': 'Total Infected', 'E': 'Total Exposed',
#                                 'dI': 'New Detected', 'dA': 'New Infected', 'dE': 'New Exposed'}, inplace=True)
#         self.df = pd.concat([self.df, df])

