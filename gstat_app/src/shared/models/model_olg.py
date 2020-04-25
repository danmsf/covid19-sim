import numpy as np  # type: ignore
import pandas as pd  # type: ignore
# from src.shared.parameters import Parameters
import datetime
from statsmodels.tsa.api import SimpleExpSmoothing, Holt
import os
import streamlit as st

class OLGParameters:
    """Parameters."""

    def __init__(
            self,
            *,
            tau: int,
            init_infected: int,
            fi: float,
            theta: float,
            countries: list,
            scenario: dict,
            critical_condition_rate: float,
            recovery_rate: float,
            critical_condition_time: int,
            recovery_time: int,
            countries_list=None,

    ):
        # OLG
        self.tau = tau
        self.init_infected = init_infected
        self.fi = fi
        self.theta = theta
        self.countries = countries
        self.scenario = scenario
        self.critical_condition_rate = critical_condition_rate
        self.recovery_rate = recovery_rate
        self.critical_condition_time = critical_condition_time
        self.recovery_time = recovery_time
        self.countries_list = countries_list


def init_olg_params(olg_params) -> OLGParameters:
    return OLGParameters(
        tau=olg_params['tau'],
        init_infected=olg_params['init_infected'],
        fi=olg_params['fi'],
        theta=olg_params['theta'],
        countries=olg_params['countries'],
        scenario=olg_params['scenario'],
        critical_condition_rate=olg_params['critical_condition_rate'],
        recovery_rate=olg_params['recovery_rate'],
        critical_condition_time=olg_params['critical_condition_time'],
        recovery_time=olg_params['recovery_time'],
    )



@st.cache
class OLG:
    """
    calc_asymptomatic start from first case
    exposed are the asymptomatic_infected with lag not only infected
    asymptomatic_infected eq 10 does not always grow but uses two diferent R0

    fi  # proportion of infectives are never diagnosed
    theta = theta  # diagnosis daily rate

    """

    def __init__(self, df, p: OLGParameters, stringency=None, have_serious_data=False):
        self.detected = []
        self.jh_hubei = self.get_hubei()
        self.stringency = self.get_stringency(stringency)
        self.r_adj = np.array([])
        self.r_values = np.array([])
        self.r0d = np.array([])
        self.asymptomatic_infected = []
        self.df = pd.DataFrame()
        self.df_tmp = pd.DataFrame()
        self.tmp = None
        self.have_serious_data = have_serious_data
        self.iter_countries(df, p, self.jh_hubei, self.stringency)
        self.r_hubei = None
        self.r_predicted = []
        self.day_0 = None

    @staticmethod
    def next_gen(r0, tau, c0, ct):
        r0d = r0 / tau
        return r0d * (ct - c0) + ct

    @staticmethod
    def get_hubei():

        return np.array([41, 41, 41, 41, 41, 45, 62, 121, 198, 270, 375, 444, 444, 549, 761, 1058, 1423, 3554, 3554, 4903, 5806,
                7153, 11177, 13522, 16678, 19665, 22112, 24953, 27100, 29631, 31728, 33366, 33366, 48206, 54406, 56249,
                58182, 59989, 61682, 62031, 62442, 62662, 64084, 64084, 64287, 64786, 65187, 65596, 65914, 66337, 66907,
                67103, 67217, 67332, 67466, 67592, 67666, 67707, 67743, 67760, 67773, 67781, 67786, 67790, 67794, 67798,
                67799, 67800, 67800, 67800, 67800, 67800, 67800, 67801, 67801, 67801, 67801, 67801, 67801, 67801, 67801,
                67802, 67802, 67802, 67803, 67803, 67803, 67803, 67803, 67803, 67803, 67803, 67803, 67803, 67803, 67803,
                67803, 68128, 68128])

    @staticmethod
    def get_stringency(stringency):
        if stringency:
            return stringency
        else:
            return pd.DataFrame(data={'date': [datetime.datetime.today()], 'StringencyIndex': [100]})

    @staticmethod
    def true_a(fi, theta, d, d_prev, d_delta_ma):
        delta_detected = (d - d_prev)
        prev_asymptomatic_infected = (1 / (1 - fi)) * ((d_delta_ma) / theta + d_prev)
        return prev_asymptomatic_infected

    @staticmethod
    def crystal_ball_regression(r_prev, hubei_prev, hubei_prev_t2, s_prev_t7):
        crystal_ball_coef = {'intercept': 1.462, 'r_prev': 0.915, 'hubei_prev': 0.05, 'hubei_prev_t2': 0.058,
                             's_prev_t7': 0.0152}

        ln_r = crystal_ball_coef.get('intercept') + crystal_ball_coef.get('r_prev') * np.log(1 + r_prev) \
               + crystal_ball_coef.get('hubei_prev') * np.log(1 + hubei_prev) \
               + crystal_ball_coef.get('hubei_prev_t2') * np.log(1 + hubei_prev_t2) \
               - crystal_ball_coef.get('s_prev_t7') * s_prev_t7
        return np.exp(ln_r) - 1

    def iter_countries(self, df, p, jh_hubei, stringency):

        self.process(init_infected=250, detected=jh_hubei)
        self.calc_r(tau=p.tau, init_infected=250)
        self.r_hubei = self.r_adj
        r_hubei = self.r_adj
        for country in p.countries:
            self.df_tmp = df[df['country'] == country].copy()
            self.process(init_infected=p.init_infected)
            self.calc_r(tau=p.tau, init_infected=p.init_infected)
            if country == 'israel':
                self.predict(country, p.tau, r_hubei, stringency)
                self.predict_next_gen(tau=p.tau)
            self.calc_asymptomatic(fi=p.fi, theta=p.theta, init_infected=p.init_infected)
            self.write(stringency, tau=p.tau, critical_condition_rate=p.critical_condition_rate,
                       recovery_rate=p.recovery_rate, critical_condition_time=p.critical_condition_time,
                       recovery_time=p.recovery_time)

    def process(self, init_infected, detected=None):
        if detected is None:
            detected = self.df_tmp['total_cases'].values

        day_0 = np.argmax(detected >= init_infected)
        self.day_0 = day_0
        detected = detected[day_0:]
        self.detected = [detected[0]]
        for t in range(1, len(detected)):
            self.detected.append(max(detected[t - 1] + 1, detected[t]))

        if self.df_tmp is not None:
            self.df_tmp = self.df_tmp[day_0:]

    def calc_r(self, tau, init_infected):
        epsilon = 1e-06
        detected = self.detected
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
        self.r_values, self.r_adj, self.r0d = r_values, r_adj, r_adj

    def predict(self, country, tau, r_hubei, stringency):
        self.r_adj = np.clip(self.r_adj, 0, 100)
        forcast_cnt = len(stringency)
        if country == 'israel':
            # fill hubei
            if 0 < forcast_cnt + len(self.r_adj) - len(r_hubei):  ## TODO Shold use time series
                r_hubei = r_hubei.append(r_hubei[-1] * (forcast_cnt - len(r_hubei)))
            # StringencyIndex
            self.df_tmp['StringencyIndex'].fillna(method='ffill', inplace=True)
            tmp = self.df_tmp.copy()
            # normalize to day_0 and then shift forward 7 days so dont need to lag in regression
            tmp['StringencyIndex'].shift(periods=-(self.day_0 - 7)).fillna(method='ffill', inplace=True)
            cur_stringency = tmp['StringencyIndex'].values
            stringency = stringency['StringencyIndex'].values
            stringency = np.append(cur_stringency, stringency)
            self.r_predicted = [0]
            for t in range(1, len(self.r0d) + forcast_cnt + 7):
                if t <= 2:
                    projected_r = self.r0d[t]
                else:
                    projected_r = self.crystal_ball_regression(self.r0d[t - 1], r_hubei[t - 1], r_hubei[t - 2],
                                                               stringency[min(t, len(stringency) - 1)])
                if t >= len(self.r0d):
                    self.r0d = np.append(self.r0d, projected_r)
                self.r_predicted = np.append(self.r_predicted, projected_r)
        else:
            holt_model = Holt(self.r_adj[-tau:], exponential=True).fit(smoothing_level=0.1, smoothing_slope=0.9)
            self.r0d = np.append(self.r_adj, holt_model.forecast(forcast_cnt + 1))

        self.r0d = np.clip(self.r0d, 0, 100)

    def predict_next_gen(self, tau):
        t = len(self.detected)
        next_gen = self.detected[-1]
        c0 = self.detected[t - tau] if t - tau >= 0 else 0

        while t <= len(self.r0d) - 1:
            next_gen = self.next_gen(r0=self.r0d[t], tau=tau, c0=c0, ct=next_gen)
            self.detected.append(next_gen)
            t += 1

    def calc_asymptomatic(self, fi, theta, init_infected):
        detected_deltas = [self.detected[0]]

        for i in range(1, len(self.detected)):
            delta = self.detected[i] - self.detected[i - 1]
            detected_deltas.append(delta)

        detected_deltas_ma = np.convolve(detected_deltas, np.ones(int(4, )) / int(4), mode='full')[
                             :len(detected_deltas)]
        asymptomatic_infected = [
            self.true_a(fi=fi, theta=theta, d=self.detected[0], d_prev=init_infected, d_delta_ma=detected_deltas_ma[0])]

        for t in range(1, len(self.detected)):
            prev_asymptomatic_infected = self.true_a(fi=fi, theta=theta, d=self.detected[t],
                                                     d_prev=self.detected[t - 1], d_delta_ma=detected_deltas_ma[i])
            asymptomatic_infected.append(prev_asymptomatic_infected)
        self.asymptomatic_infected = asymptomatic_infected

    def calc_critical_condition(self, df, critical_condition_time, recovery_time, critical_condition_rate):
        # calc critical rate
        df['true_critical_rate'] = df['serious_critical'] / (
                df['total_cases'].shift(critical_condition_time) - df['total_cases'].shift(
            critical_condition_time + recovery_time))
        critical_rates = df['serious_critical'] / (
                df['total_cases'].shift(critical_condition_time) - df['total_cases'].shift(
            critical_condition_time + recovery_time))
        last_critical_rate = critical_rates.dropna().iloc[-7:].mean()

        # critical condition - currently using parameter
        df['Critical_condition'] = (df['total_cases'].shift(critical_condition_time)
                                    - df['total_cases'].shift(
                    critical_condition_time + recovery_time + 1)) * critical_condition_rate

        return df['Critical_condition']

    def write(self, stringency, tau, critical_condition_rate, recovery_rate, critical_condition_time, recovery_time):
        if self.have_serious_data == False:
            self.df_tmp['serious_critical'] = None
            self.df_tmp['new_cases'] = self.df_tmp['total_cases'] - self.df_tmp['total_cases'].shift(1)
            self.df_tmp['activecases'] = None
            self.df_tmp['total_deaths'] = None
            self.df_tmp['new_deaths'] = None

        df = self.df_tmp[
            ['date', 'country', 'StringencyIndex', 'serious_critical', 'new_cases', 'activecases', 'new_deaths',
             'total_deaths']].reset_index(drop=True).copy()
        df['r_values'] = self.r_values
        # pad df for predictions
        forcast_cnt = len(self.detected) - len(self.r_adj)
        if forcast_cnt > 0:
            predict_date = df['date'].max() + pd.to_timedelta(1, unit="D")
            prediction_dates = pd.date_range(start=predict_date.strftime('%Y-%m-%d'), periods=forcast_cnt)
            predicted = pd.DataFrame({'date': prediction_dates})
            predicted.loc[:forcast_cnt - 8, 'StringencyIndex'] = stringency['StringencyIndex'].values
            df = df.append(predicted, ignore_index=True)

        df['total_cases'] = self.detected
        df['R'] = self.r0d

        df['infected'] = self.asymptomatic_infected
        df['exposed'] = df['infected'].shift(periods=-tau)
        df['country'].fillna(method='ffill', inplace=True)
        df['corona_days'] = pd.Series(range(1, len(df) + 1))
        df['prediction_ind'] = np.where(df['corona_days'] <= len(self.r_adj), 0, 1)
        df['Currently Infected'] = np.where(df['corona_days'] <= (critical_condition_time + recovery_time),
                                            df['total_cases'],
                                            df['total_cases'] - df['total_cases'].shift(
                                                periods=(critical_condition_time + 6 + recovery_time)))

        df['Doubling Time'] = np.log(2) / np.log(1 + df['R'] / tau)

        df['dI'] = df['total_cases'] - df['total_cases'].shift(1)
        df['dA'] = df['infected'] - df['infected'].shift(1)
        df['dE'] = df['exposed'] - df['exposed'].shift(1)

        df['Critical_condition'] = self.calc_critical_condition(df, critical_condition_time, recovery_time,
                                                                critical_condition_rate)
        df['Recovery_Critical'] = df['dI'].shift(
            recovery_time + critical_condition_time) * critical_condition_rate * recovery_rate
        df['Mortality_Critical'] = df['dI'].shift(recovery_time + critical_condition_time) * critical_condition_rate * (
                    1 - recovery_rate)
        # df['Recovery_Critical'] = df['Recovery_Critical'] - df['Recovery_Critical'].shift(1)
        # df['Mortality_Critical'] = df['Mortality_Critical'] - df['Mortality_Critical'].shift(1)
        df['Recovery_Critical'] = df['Recovery_Critical'].apply(lambda x: max(x, 0)).fillna(0).astype(int)
        df['Mortality_Critical'] = df['Mortality_Critical'].apply(lambda x: max(x, 0)).fillna(0).astype(int)

        df['Total_Mortality'] = df['Mortality_Critical'].cumsum()
        df['Total_Critical_Recovery'] = df['Recovery_Critical'].cumsum()

        # fill with obsereved values
        if self.have_serious_data:
            print("hi")
            # df['Critical_condition'] = np.where(~df['serious_critical'].isna(), df['serious_critical'], df['Critical_condition'])
            # df['dI'] = np.where(~df['new_cases'].isna(), df['new_cases'], df['dI'])
            # df['Currently Infected'] = np.where(~df['activecases'].isna(), df['activecases'], df['Currently Infected'])
            # df['Total_Mortality'] = np.where(~df['total_deaths'].isna(), df['total_deaths'], df['Total_Mortality'])
            # df['Mortality_Critical'] = np.where(~df['new_deaths'].isna(), df['new_deaths'], df['Mortality_Critical'])

        df[['Critical_condition', 'Currently Infected', 'total_cases', 'exposed', 'Recovery_Critical',
            'Mortality_Critical']] = df[
            ['Critical_condition', 'Currently Infected', 'total_cases', 'exposed', 'Recovery_Critical',
             'Mortality_Critical']].round(0)
        if self.have_serious_data:
            df = df.rename(columns={'total_cases': 'Total Detected',
                                    'infected': 'Total Infected Predicted',
                                    'exposed': 'Total Exposed Predicted',
                                    'Total_Mortality': 'Total Deaths Predicted',
                                    'total_deaths': 'Total Deaths Actual',
                                    'dI': 'New Detected Predicted',
                                    'new_cases': 'New Detected Actual',
                                    'dA': 'New Infected Predicted',
                                    'dE': 'New Exposed Predicted',
                                    'Mortality_Critical': 'Daily Deaths Predicted',
                                    'new_deaths': 'Daily Deaths Actual',
                                    'Critical_condition': 'Daily Critical Predicted',
                                    'serious_critical': 'Daily Critical Actual',
                                    'Recovery_Critical': 'Daily Recovery Predicted',
                                    'Currently Infected': 'Currently Active Detected Predicted',
                                    'activecases': 'Currently Active Detected Actual',
                                    'true_critical_rate': 'Daily Critical Rate Actual',
                                    'r_hubei': 'R China-Hubei Actual',
                                    'r_predicted': 'R Predicted'
                                    })

        df['r_hubei'] = self.r_hubei[:df.shape[0]]
        if df.loc[0, 'country'] == 'israel':
            df['r_predicted'] = self.r_predicted[:df.shape[0]]
        self.df = pd.concat([self.df, df])


def get_sir_country_file(sir_country_file):
    sir_country_df = pd.read_csv(sir_country_file, parse_dates=['date'])
    # sir_country_df['I'] = sir_country_df['total_cases']
    return sir_country_df


class StringencyIndex:
    def __init__(self, countryname):
        OXDF = "OxCGRT_Download_180420_223736_Full.csv"
        self.filepath = os.path.join(os.getcwd(), "Resources", "Datasets", "CountryData", OXDF)
        self.oxford_df = pd.read_csv(os.path.join(os.getcwd(), "Resources", "Datasets", "CountryData", OXDF))
        self.countryname = countryname
        self.input_df = pd.DataFrame()
        self.output_df = pd.DataFrame()
        self.max_val = {'S1': 2., 'S2': 2., 'S3': 2., 'S4': 2., 'S5': 1., 'S6': 2., 'S7': 3.}
        self.project_til = None

    def get_latest(self):
        self.oxford_df = self.oxford_df.loc[self.oxford_df["CountryName"] == self.countryname, :]
        self.oxford_df["date"] = pd.to_datetime(self.oxford_df["Date"], format="%Y%m%d")
        s1_7 = tuple("S" + str(i) + "_" for i in range(1, 8, 1))
        keep_cols = [c for c in self.oxford_df.columns if c.startswith(s1_7)]
        keep_cols = [c for c in keep_cols if c.find('Notes') == -1]
        oxford_df = self.oxford_df.dropna(subset=['StringencyIndex'])
        oxford_df = oxford_df.fillna('ffill')
        oxford_df = oxford_df[keep_cols]
        oxford_dict = oxford_df[-1:].to_dict('records')[0]
        return oxford_dict

    def display_st(self, st, key=1):
        oxford_dict = self.get_latest()
        st.sidebar.subheader("Oxford Index")
        output = {}
        oxford_start = oxford_dict.copy()
        self.project_til = st.sidebar.date_input("Project until:", datetime.date.today() + datetime.timedelta(days=20), key=key)
        max_val = self.max_val
        for k, v in oxford_dict.items():
            if k.find('IsGeneral') > -1:
                output[k] = st.sidebar.checkbox(k, oxford_dict[k] * True, key=key) * 1.
            else:
                output[k] = st.sidebar.number_input(k.split("_")[1], value=oxford_dict[k], min_value=0.,
                                                    max_value=max_val[k[:2]], step=1., key=key)
                output[k + '_date'] = st.sidebar.date_input("Date " + k.split("_")[1],datetime.date.today() + datetime.timedelta(days=1), key=key)
                # add original date
                oxford_start[k + '_date'] = datetime.date.today()
        self.input_df = pd.DataFrame([oxford_start, output])

    def calculate_stringency(self):
        max_val = self.max_val
        temp = self.input_df.copy()
        cols = temp.columns
        date_cols = [c for c in cols if c.find('_date') > -1]
        temp[date_cols] = temp[date_cols].apply(lambda x: pd.to_datetime(x))
        # dts = temp[date_cols].apply(lambda x: max(x), axis=1).values
        # dts_range = pd.date_range(dts[0], dts[1])
        dts_range = pd.date_range(datetime.date.today(),  self.project_til)
        temp['times'] = None
        temp['times'] = [1, len(dts_range) - 1]

        temp = temp.loc[temp.index.repeat(temp.times)]
        temp.drop(columns='times', inplace=True)
        temp['date'] = dts_range
        cols = temp.columns
        cols = [c for c in cols if c.find('IsGeneral') == -1]
        cols = [c for c in cols if c.find('date') == -1]
        temp = temp.reset_index(drop=True)
        for k in cols:
            for i in temp.index:
                if temp.loc[i, k + "_date"] != temp.loc[i, 'date']:
                    temp.at[i, k] = temp.loc[i - 1, k]
                    try:
                        temp.at[i, k[:2] + "_IsGeneral"] = temp.loc[i - 1, k + "_IsGeneral"]
                    except:
                        pass

        for k in cols:
            if k[:2] != 'S7':
                temp[k[:2] + '_score'] = (temp[k] + temp[k[:2] + "_IsGeneral"]) / (max_val[k[:2]] + 1)
            else:
                temp[k[:2] + '_score'] = temp[k] / (max_val[k[:2]])

        cols = temp.columns
        score_cols = [c for c in cols if c.find("score") > -1]
        temp['StringencyIndex'] = temp[score_cols].apply(lambda x: np.average(x)*100, axis=1)
        cols = list(temp.columns)
        cols.insert(0, cols.pop(cols.index('StringencyIndex')))
        cols.insert(0, cols.pop(cols.index('date')))
        temp = temp.loc[:, cols]
        # temp = pd.merge(temp, self.oxford_df.loc[:, ["StringencyIndex", "date"]], "outer")
        self.output_df = temp
        return temp
