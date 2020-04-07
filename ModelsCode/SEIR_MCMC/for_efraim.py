import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

class Seiar:
    def __init__(self, p):

        self.N = p['N']
        self.S_0 = p['S_0']
        self.E_0 = p['E_0']
        self.I_0 = p['I_0']
        self.A_0 = p['A_0']
        self.R_0 = p['R_0']
        self.alpha = p['alpha']
        self.beta_ill = p['beta_ill']
        self.beta_asy = p['beta_asy']
        self.gamma_ill = p['gamma_ill']
        self.gamma_asy = p['gamma_asy']
        self.rho = p['rho']
        self.theta = p['theta']
        self.start_date_simulation = p['start_date_simulation']
        self.number_of_days = p['start_date_simulation'] + datetime.timedelta(p['number_of_days'])
        self.beta_asy_times = p['beta_asy_days']
        self.beta_asy_change = p['beta_asy_change']
        self.beta_ill_times = p['beta_ill_days']
        self.beta_ill_change = p['beta_ill_change']
        self.run_simulation()
        self.results=[]


    def model(self,t):
        S, E, I, A, R = [self.S_0/self.N], [self.E_0/self.N], [self.I_0/self.N], [self.A_0/self.N], [self.R_0/self.N]

        dt = t[1] - t[0]

        for tm in t[1:]:
            if tm in self.beta_asy_times:
                r = self.beta_asy_change[self.beta_asy_times.index(tm)]
                self.beta_asy = self.beta_asy * (1+r)
                print(tm, r, self.beta_asy)
                self.beta_asy_times.pop(0)
                self.beta_asy_change.pop(0)
            if tm in self.beta_ill_times:
                r = self.beta_ill_change[self.beta_ill_times.index(tm)]
                self.beta_ill = self.beta_ill * (1+r)
                print(tm, r, self.beta_ill)
                self.beta_ill_change.pop(0)
                self.beta_ill_times.pop(0)
            next_S = S[-1] - (self.rho * self.beta_ill * S[-1] * I[-1] + self.rho * self.beta_asy * S[-1] * A[-1]) * dt
            next_E = E[-1] + (self.rho * self.beta_ill * S[-1] * I[-1] + self.rho * self.beta_asy * S[-1] * A[-1] - self.alpha * E[-1]) * dt
            next_I = I[-1] + (self.theta * self.alpha * E[-1] - self.gamma_ill * I[-1]) * dt
            next_A = A[-1] + ((1 - self.theta) * self.alpha * E[-1] - self.gamma_asy * A[-1]) * dt
            next_R = R[-1] + (self.gamma_ill * I[-1] + self.gamma_asy * A[-1]) * dt

            S.append(next_S)
            E.append(next_E)
            I.append(next_I)
            A.append(next_A)
            R.append(next_R)

        return np.stack([S, E, I, A, R]).T

    def run_simulation(self):
        t_max = 600
        dt = .01
        t = np.linspace(0, t_max, int(t_max / dt) + 1)

        results = self.model(t)

        df = pd.DataFrame(results)
        df = df.rename(columns={df.columns[0]: 'S', df.columns[1]: 'E', df.columns[2]: 'I', df.columns[3]: 'A', df.columns[4]: 'R'})
        dates = pd.date_range(start=self.start_date_simulation, end='05/01/2030')
        df_I_E = df[::100].reset_index(drop=True)
        df_I_E.index = dates[:len(df_I_E)]

        df_I_E = df_I_E.rename(columns={'S': 'Susceptible', 'E': 'Exposed', 'I': 'Infected', 'A': 'Asymptomatic', 'R': 'Recovered'})
        infected_df = df_I_E[['Infected']] * self.N
        asymptomatic_df = df_I_E[['Asymptomatic']] * self.N
        recovered_df = df_I_E[['Recovered']] * self.N
        susceptible_df = df_I_E[['Susceptible']] * self.N
        exposed_df = df_I_E[['Exposed']] * self.N

        results = [
                    infected_df.loc[:self.number_of_days],
                    asymptomatic_df.loc[:self.number_of_days],
                    recovered_df.loc[:self.number_of_days],
                    susceptible_df.loc[:self.number_of_days],
                    exposed_df.loc[:self.number_of_days]
                   ]

        self.results = pd.concat(results, axis = 1).reset_index(drop=True)
        return 0

    def plot(self, colnames):
        plt.figure()
        for c in colnames:
            plt.plot(self.results[c], label=c)
        plt.legend(loc="upper left")
        plt.grid()

#-----------------------------------------------------------------------Run from here-----------------------------

seiar_params = {'N': 8740000.00,
                'S_0': 8739990.00,
                'E_0': 0.0,
                'A_0': 0.00,
                'I_0': 10.00,
                'R_0': 0.00,
                'alpha': 0.10,
                'beta_ill': 0.80,
                'beta_asy': 0.40,
                'gamma_ill': 0.05,
                'gamma_asy': 0.12,
                'rho': 0.50,
                'theta': 0.50,
                'start_date_simulation': datetime.date(2020, 3, 1),
                'number_of_days': 60,
                'beta_asy_days': [10, 15, 30],
                'beta_asy_change': [-0.9, -0.3, 0.4],
                'beta_ill_days': [10, 30, 50],
                'beta_ill_change': [0.2, 0.3, -0.4]
                }

model = Seiar(seiar_params)
model.run_simulation()
df = model.results
model.plot(["Exposed", "Infected", "Asymptomatic"])