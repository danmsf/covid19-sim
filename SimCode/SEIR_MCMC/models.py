# def SIR(y, t, p):
#     # dSdt = -beta * S * I / N
#     # dIdt = beta * S * I / N - gamma * I
#     # dRdt = gamma * I
#
#     # gamma = 1 / D ~ 1 / Days infectious
#     # beta = probability of transmission
#     # R0 = beta/gamma
#     # F = beta * I
#
#
#     # beta, gamma = p[0], p[1]
#     # S, I = y[0], y[1]
#     ds = -p[0] * y[0] * y[1]
#     di = p[0] * y[0] * y[1] - p[1] * y[1]
#     dr = p[1] * y[1]
#     return [ds, di]


def SIR(y, t, p):
    # dSdt = -beta * S * I / N
    # dIdt = beta * S * I / N - gamma * I
    # dRdt = gamma * I

    # gamma = 1 / D ~ 1 / Days infectious
    # beta = probability of transmission
    # R0 = beta/gamma
    # F = beta * I

    beta, gamma = p[0], p[1]
    S, I, R = y[0], y[1], y[2]
    N = S + I + R

    ds = - beta * S * I / N
    di = beta * S * I / N - gamma * I
    dr = gamma * I
    return [ds, di, dr]


def SEIR(y, t, p):
    # No reinfection
    # Lamda - birth rate
    # mu - death rate
    # dSdt = -beta * S * I / N
    # dIdt = beta * S * I / N - gamma * I
    # dRdt = gamma * I

    # gamma = 1 / D ~ 1 / Days infectious
    # beta = probability of transmission per contact
    # epsilon = rate of progression from E to I
    # r = Num contacts at t
    # R0 = r * beta * 1/(gamma + mu) * epsilon/(epsilon + mu)
    # R0 = (Num contacts at t) * (prob of transmission per contact) * (duration of infection) * (prob of surviving Exposed stage)
    # F = beta * I

    beta, gamma, eps = p[0], p[1], p[2]
    S, E, I, R = y[0], y[1], y[2], y[3]
    N = S + E + I + R

    # simple model
    Lamda = 0.0
    mu = 0.0
    r = 1.0

    ds = - r * beta * S * I / N + (Lamda - mu) * S
    de = r * beta * S * I / N - (eps + mu) * E
    di = eps * E - (gamma + mu) * I
    dr = gamma * I - mu * R
    return [ds, de, di, dr]


def SEIR_B(y, t, p):
    beta, gamma,  eps = p[0], p[1], p[2]
    # alpha - government reaction strength [0,1]
    # k - individual reaction strength [0,1]
    # beta[t] = beta[0] * (1 - alpha) * (1 - D/N)**k
    # [(1 - alpha) * (1 - D/N)**k] = r from simple SEIR = Num contacts at t
    # alpha = effect of government shutdown
    # D = public perception of risk of severe cases and deaths
    # [(1 - D/N)**k] = social distancing because of perceived fear
    # C = number of cumulative cases (reported and not)

    S, E, I, R, D = y[0], y[1], y[2], y[3], y[4]
    N = S + E + I + R

    # simple model
    Lamda = 0.0
    mu = 0.0

    ds = - beta[t] * S * I / N + (Lamda - mu) * S
    de = beta[t] * S * I / N - (eps + mu) * E
    di = eps * E - (gamma + mu) * I
    dr = gamma * I - mu * R
    dN = - mu * N
    dD = d * gamma * I - lamda * D
    dc = eps * E
    return [ds, de, di, dr]


def SEIR_B_zoo(y, t, p):
    beta, gamma, mu, eps = p[0], p[1], p[2], p[3]
    # alpha - government reaction strength [0,1]
    # k - individual reaction strength [0,1]
    # beta[t] = beta[0] * (1 - alpha) * (1 - D/N)**k
    S, E, I, R, F = y[0], y[1], y[2], y[3], y[4]
    N = S + E + I + R

    # simple model
    Lamda = 0.0
    r = 1.0
    ds = - r * beta[0] * S * F / N - r * beta[t] * S * I / N + (Lamda - mu) * S
    de = r * beta[0] * S * F / N + r * beta[t] * S * I / N - (eps + mu) * E
    di = eps * E - (gamma + mu) * I
    dr = gamma * I - mu * R
    dN = - mu * N
    dD = d * gamma * I - lamda * D
    dc = eps * E
    return [ds, de, di, dr]