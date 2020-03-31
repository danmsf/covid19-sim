# https://docs.pymc.io/notebooks/ODE_API_introduction.html
# https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/
import pymc3 as pm
from pymc3.ode import DifferentialEquation
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import arviz as az
from models import SIR
import os
import theano
# os.environ["THEANO_FLAGS"] = "device=cuda"

times = np.arange(0, 5, 0.05)
times = np.arange(0, 160, 1)
# times = np.linspace(0, 160, 160)
# 1/gamma = time infectious ~ 14 ; or gamma = 1/D = 1/14
# beta*Nt = number of people in contact with infected person at time t; S/N of them are susceptible to contagion
# R0 = beta/gamma

# beta, gamma = 4, 1.0
# beta, gamma = 0.25, 1.0/14
beta, gamma = 0.25, 1./14
# Create true curves
# y0 = [S/N, I]
y = odeint(SIR, t=times, y0=[999.0/1000, 1.0/1000, 0.0], args=((beta, gamma),), rtol=1e-8)
# Observational model.  Lognormal likelihood isn't appropriate, but we'll do it anyway
yobs = np.random.lognormal(mean=np.log(y[1::]), sigma=[0.2, 0.3, 0.2])

plt.figure()
# plt.plot(times[1::], yobs, marker='o', linestyle='none')
plt.plot(times, y[:, 0], color='C0', alpha=0.5, label=f'$S(t)$')
plt.plot(times, y[:, 1], color='C1', alpha=0.5, label=f'$I(t)$')
plt.plot(times, y[:, 2], color='C2', alpha=0.5, label=f'$R(t)$')
plt.legend()
plt.title(f'R0={beta/gamma:.2f}; $\\beta$={beta}; $\\gamma$={gamma:.2f}; d={14}')
plt.show()



#------------------------------------------------------------ MCMC --------------------------------------------------

sir_model = DifferentialEquation(
    func=SIR,
    times=np.arange(1, 160, 1),
    n_states=3,
    n_theta=2,
    t0=0,
)

with pm.Model() as model4:
    sigma = pm.HalfCauchy('sigma', 1, shape=3)

    # R0 is bounded below by 1 because we see an epidemic has occurred
    R0 = pm.Bound(pm.Normal, lower=1)('R0', 2, 3)
    lam = pm.Lognormal('lambda', pm.math.log(2), 2)
    beta = pm.Deterministic('beta', lam*R0)

    sir_curves = sir_model(y0=[999.0/1000, 1.0/1000, 0.0], theta=[beta, lam])

    Y = pm.Lognormal('Y', mu=pm.math.log(sir_curves), sd=sigma, observed=yobs)

    prior = pm.sample_prior_predictive()
    step = pm.Metropolis()
    # trace = pm.sample(2000, tune=1000, target_accept=0.9, cores=1, step=step)
    # trace = pm.sample(500, tune=500, target_accept=0.9, cores=1, start={'lamda': 1.2, 'beta': 1./0.25})
    trace = pm.sample(500, tune=50, cores=1, start={'lamda': 0.016, 'beta': 0.25}, step=step)
    posterior_predictive = pm.sample_posterior_predictive(trace)

    data = az.from_pymc3(trace=trace, prior=prior, posterior_predictive=posterior_predictive)

# plots
pm.traceplot(trace);
pm.energyplot(trace);
az.plot_posterior(data, round_to=2, credible_interval=0.95);
pm.summary(trace, var_names=['R0']).round(0)
pm.forestplot(trace, var_names=['R0'])


# fig, ax = plt.subplots(figsize=(15, 8))
# returns.plot(ax=ax)
# ax.plot(returns.index, 1/np.exp(trace['s',::5].T), 'C3', alpha=.03);
# ax.set(title='volatility_process', xlabel='time', ylabel='volatility');
# ax.legend(['S&P500', 'stochastic volatility process']);


y_n = data.observed_data['Y']
plt.plot(times[1::], y_n[:, 0], color='C0', alpha=0.5, label=f'$S(t)$')
plt.plot(times[1::], y_n[:, 1], color='C1', alpha=0.5, label=f'$I(t)$')
plt.plot(times[1::], y_n[:, 2], color='C2', alpha=0.5, label=f'$R(t)$')
plt.legend()
plt.title(f'R0={beta/gamma:.2f}; $\\beta$={beta}; $\\gamma$={gamma:.2f}; d={14}')
plt.show()


y_n = data.post ['Y']
plt.plot(times[1::], y_n[:, 0], color='C0', alpha=0.5, label=f'$S(t)$')y
plt.plot(times[1::], y_n[:, 1], color='C1', alpha=0.5, label=f'$I(t)$')
plt.plot(times[1::], y_n[:, 2], color='C2', alpha=0.5, label=f'$R(t)$')
plt.legend()
plt.title(f'R0={beta/gamma:.2f}; $\\beta$={beta}; $\\gamma$={gamma:.2f}; d={14}')
plt.show()
