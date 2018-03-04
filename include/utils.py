import pandas as pd

VELOCITY_PRECISION = 0.1
ROBOT_MASS = 100
START_VELOCITY = 0
MAX_TIME = 400
DELTA_TIME = 1

MAX_FORCE = 200
CRUISE_VELOCITY = 25
RESIST_FACTOR = 2

ORIGINAL_PROPORTIONAL_FACTOR = 3
ORIGINAL_INTEGRAL_FACTOR = 0.3

PROPORTIONAL_FACTOR = 3
INTEGRAL_FACTOR = 0.1


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def cruise_control(proportional_factor, integral_factor=0.1):
    ind = list(range(MAX_TIME))
    t = ind * DELTA_TIME
    error_sum = 0
    v = [START_VELOCITY]
    for i in range(MAX_TIME):
        err = CRUISE_VELOCITY - v[i]
        error_sum += err
        force = proportional_factor * err + integral_factor * error_sum * DELTA_TIME
        force = clamp(-MAX_FORCE, force, MAX_FORCE)
        v.append(v[i] + (force - RESIST_FACTOR * v[i]) * DELTA_TIME / ROBOT_MASS)
    df_tv = pd.DataFrame(v[: MAX_TIME], index=t, columns=["v"])
    df_tv.index.name = "T"
    return df_tv


def get_no_error_time(data_frame):
    i = len(data_frame) - 1
    while (abs(CRUISE_VELOCITY - data_frame.v[i]) < VELOCITY_PRECISION) & (i > 1):
        i -= 1
    return data_frame.index[i]


def get_convergence_rate(v, p):
    vf, pf = [], []
    cc = [1.]
    i = 0
    while v[i] < (CRUISE_VELOCITY - 0.1):
        i += 1
        vf.append(v[i])
    numv = len(vf)
    istep = list(range(numv)) * len(p)
    for n in range(len(p)):
        for m in range(numv):
            pf.append(p[n])
    vf = vf * len(p)
    for i in range(1, len(vf)):
        cc.append(abs(CRUISE_VELOCITY - vf[i]) / abs(CRUISE_VELOCITY - vf[i - 1])**pf[i])
    return pd.DataFrame({
        "istep": pd.Series(istep),
        "cc": pd.Series(cc),
        "pf": pd.Series(pf)
    })
