import pandas as pd
import matplotlib.pyplot as plt


# TODO: use template strings or string.format to show constants

VELOCITY_PRECISION = 0.1
ROBOT_MASS = 100
V0 = 0
MAX_TIME = 400
DELTA_TIME = 1

MAX_FORCE = 200
CRUISE_VELOCITY = 25
RESIST_FACTOR = 2

ORIGINAL_PROPORTIONAL_FACTOR = 3
ORIGINAL_INTEGRAL_FACTOR = 0.3

PROPORTIONAL_FACTOR = 3
INTEGRAL_FACTOR = 0.3


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def cruise_control(proportional_factor, integral_factor=0.1, resist_factor=RESIST_FACTOR, cruise_speed=CRUISE_VELOCITY,
                   max_force=MAX_FORCE):
    m = ROBOT_MASS
    ind = list(range(MAX_TIME))
    min_force = -max_force
    t = ind * DELTA_TIME
    error_sum = 0
    v = [V0]
    for i in range(MAX_TIME):
        err = cruise_speed - v[i]
        error_sum += err
        force = proportional_factor * err + integral_factor * error_sum * DELTA_TIME
        force = clamp(min_force, force, max_force)
        v.append(v[i] + (force - resist_factor * v[i]) * DELTA_TIME / m)
    df_tv = pd.DataFrame(v[:MAX_TIME], index=t, columns=["v"])
    df_tv.index.name = "T"
    return df_tv


res = cruise_control(proportional_factor=3, integral_factor=0.2, resist_factor=RESIST_FACTOR,
                     cruise_speed=CRUISE_VELOCITY, max_force=MAX_FORCE)

plt.rcParams["font.fantasy"] = "Arial", "Times New Roman", "Tahoma", "Comic Sans MS", "Courier"
plt.rcParams["font.family"] = "fantasy"
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(res)
a1 = pd.Series(CRUISE_VELOCITY, index=res.index)
ax.plot(a1, color="red")
a2 = pd.Series(CRUISE_VELOCITY - 10 * VELOCITY_PRECISION, index=res.index)
ax.plot(a2, "k--", color="green")
a3 = pd.Series(CRUISE_VELOCITY + 10 * VELOCITY_PRECISION, index=res.index)
ax.plot(a3, "k--", color="green")
plt.title("Velocity changing", fontsize=16)
plt.xlabel("Time, s", fontsize=14)
plt.ylabel("Velocity, m/s", fontsize=14)
plt.show()


def get_no_error_time(data_frame, cruise_speed, velocity_precision):
    i = len(data_frame) - 1
    while (abs(cruise_speed - data_frame.v[i]) < velocity_precision) & (i > 1):
        i -= 1
    return data_frame.index[i]


limit_time = get_no_error_time(res, CRUISE_VELOCITY, VELOCITY_PRECISION)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(res[50:])
a1 = pd.Series(CRUISE_VELOCITY, index=res.index[50:])
ax.plot(a1, color="red")
a2 = pd.Series(CRUISE_VELOCITY - 2 * VELOCITY_PRECISION, index=res.index[50:])
ax.plot(a2, "k--", color="green")
a3 = pd.Series(CRUISE_VELOCITY + 2 * VELOCITY_PRECISION, index=res.index[50:])
ax.plot(a3, "k--", color="green")
ax.plot([limit_time, limit_time], [CRUISE_VELOCITY - 10, CRUISE_VELOCITY + 10], color="brown")
plt.title("Velocity changing: proportional_factor=3, integral_factor=0.2", fontsize=16)
plt.xlabel("Time, s", fontsize=14)
plt.ylabel("Velocity, m/s", fontsize=14)
plt.show()

res1 = cruise_control(proportional_factor=3, integral_factor=0.1, resist_factor=RESIST_FACTOR,
                      cruise_speed=CRUISE_VELOCITY, max_force=MAX_FORCE)
limit_time1 = get_no_error_time(res1, CRUISE_VELOCITY, VELOCITY_PRECISION)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(res1[50:])
a1 = pd.Series(CRUISE_VELOCITY, index=res.index[50:])
ax.plot(a1, color="red")
a2 = pd.Series(CRUISE_VELOCITY - 2 * VELOCITY_PRECISION, index=res.index[50:])
ax.plot(a2, "k--", color="green")
a3 = pd.Series(CRUISE_VELOCITY + 2 * VELOCITY_PRECISION, index=res.index[50:])
ax.plot(a3, "k--", color="green")
ax.plot([limit_time1, limit_time1], [CRUISE_VELOCITY - 4, CRUISE_VELOCITY + 4], color="brown")
plt.title("Velocity changing: proportional_factor=3, integral_factor=0.1", fontsize=16)
plt.xlabel("Time, s", fontsize=14)
plt.ylabel("Velocity, m/s", fontsize=14)
plt.show()


def get_convergence_rate(v, cruise_speed, p):
    vf, pf = [], []
    cc = [1.]
    i = 0
    while v[i] < (cruise_speed - 0.1):
        i += 1
    vf.append(v[i])
    numv = len(vf)
    istep = list(range(numv)) * len(p)
    for n in range(len(p)):
        for m in range(numv):
            pf.append(p[n])
    vf = vf * len(p)
    for i in range(1, len(vf)):
        cc.append(abs(cruise_speed - vf[i]) / abs(cruise_speed - vf[i-1])**pf[i])
    return pd.DataFrame({
        "istep": pd.Series(istep),
        "cc": pd.Series(cc),
        "pf": pd.Series(pf)
    })


c = [1., 1.1, 1.2]
convergence_rate_frame = get_convergence_rate(res1.v, CRUISE_VELOCITY, c)
b = int(len(convergence_rate_frame) / len(c))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(convergence_rate_frame.istep[1:b], convergence_rate_frame.cc[1:b], color="red")
ax.plot(convergence_rate_frame.istep[b + 1: b + b], convergence_rate_frame.cc[b + 1: b + b], "k--", color="green")
ax.plot(convergence_rate_frame.istep[b + b + 1:], convergence_rate_frame.cc[b + b + 1:], "k.", color="brown")
plt.title("Estimation of the order and speed of convergence", fontsize=16)
plt.xlabel("istep", fontsize=14)
plt.ylabel("cc", fontsize=14)
plt.show()

order = [1.05]
convergence_rate_frame = get_convergence_rate(res1.v, CRUISE_VELOCITY, order)
print("velocity = ", 1 / convergence_rate_frame.cc.mean())
