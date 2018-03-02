import pandas as pd
import matplotlib.pyplot as plt


def clamp(minimum, x, maximum):
    return max(minimum, min(x, maximum))


def cruise_control(proportional_factor, integral_factor=0.1, resist_factor=0.3, cruise_speed=30, max_force=100):
    v0 = 0
    m = 100
    dt = 1
    max_t = 400
    ind = list(range(max_t))
    min_force = -max_force
    t = ind * dt
    error_sum = 0
    v = [v0]
    for i in range(max_t):
        err = cruise_speed - v[i]
        error_sum += err
        force = proportional_factor * err + integral_factor * error_sum * dt
        force = clamp(min_force, force, max_force)
        v.append(v[i] + (force - resist_factor * v[i]) * dt / m)
    df_tv = pd.DataFrame(v[:max_t], index=t, columns=['v'])
    df_tv.index.name = 'T'
    return df_tv


res = cruise_control(proportional_factor=3, integral_factor=0.2, resist_factor=2, cruise_speed=35, max_force=100)

dv = 0.1
cruise_velocity = 35
plt.rcParams['font.fantasy'] = 'Arial', 'Times New Roman', 'Tahoma', 'Comic Sans MS', 'Courier'
plt.rcParams['font.family'] = 'fantasy'
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(res)
a1 = pd.Series(cruise_velocity, index=res.index)
ax.plot(a1, color='red')
a2 = pd.Series(cruise_velocity - 10 * dv, index=res.index)
ax.plot(a2, 'k--', color='green')
a3 = pd.Series(cruise_velocity + 10 * dv, index=res.index)
ax.plot(a3, 'k--', color='green')
plt.title('Изменение скорости: ПИ-регулятор', fontsize=16)
plt.xlabel(u'Время, с', fontsize=14)
plt.ylabel(u'Скорость, м/с', fontsize=14)
plt.show()


def get_no_error_time(data_frame, cruise_speed, precision):
    i = len(data_frame) - 1
    while (abs(cruise_speed - data_frame.v[i]) < precision) & (i > 1):
        i -= 1
    return data_frame.index[i]


limit_time = get_no_error_time(res, cruise_velocity, dv)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(res[50:])
a1 = pd.Series(cruise_velocity, index=res.index[50:])
ax.plot(a1, color='red')
a2 = pd.Series(cruise_velocity - 2 * dv, index=res.index[50:])
ax.plot(a2, 'k--', color='green')
a3 = pd.Series(cruise_velocity + 2 * dv, index=res.index[50:])
ax.plot(a3, 'k--', color='green')
ax.plot([limit_time, limit_time], [cruise_velocity - 10, cruise_velocity + 10], color='brown')
plt.title('Изменение скорости: ПИ-регулятор proportional_factor=3, integral_factor=0.2', fontsize=16)
plt.xlabel(u'Время, с', fontsize=14)
plt.ylabel(u'Скорость, м/с', fontsize=14)
plt.show()

res1 = cruise_control(proportional_factor=3, integral_factor=0.1, resist_factor=2, cruise_speed=35, max_force=100)
limit_time1 = get_no_error_time(res1, cruise_velocity, dv)

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(res1[50:])
a1 = pd.Series(cruise_velocity, index=res.index[50:])
ax.plot(a1, color='red')
a2 = pd.Series(cruise_velocity - 2 * dv, index=res.index[50:])
ax.plot(a2, 'k--', color='green')
a3 = pd.Series(cruise_velocity + 2 * dv, index=res.index[50:])
ax.plot(a3, 'k--', color='green')
ax.plot([limit_time1, limit_time1], [cruise_velocity - 4, cruise_velocity + 4], color='brown')
plt.title('Изменение скорости: ПИ-регулятор proportional_factor=3, integral_factor=0.1', fontsize=16)
plt.xlabel(u'Время, с', fontsize=14)
plt.ylabel(u'Скорость, м/с', fontsize=14)
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
        'istep': pd.Series(istep),
        'cc': pd.Series(cc),
        'pf': pd.Series(pf)
    })


c = [1., 1.1, 1.2]
convergence_rate_frame = get_convergence_rate(res1.v, cruise_velocity, c)
b = int(len(convergence_rate_frame) / len(c))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(convergence_rate_frame.istep[1:b], convergence_rate_frame.cc[1:b], color='red')
ax.plot(convergence_rate_frame.istep[b + 1: b + b], convergence_rate_frame.cc[b + 1: b + b], 'k--', color='green')
ax.plot(convergence_rate_frame.istep[b + b + 1:], convergence_rate_frame.cc[b + b + 1:], 'k.', color='brown')
plt.title('Оценка порядка и скорости сходимости', fontsize=16)
plt.xlabel(u'istep', fontsize=14)
plt.ylabel(u'cc', fontsize=14)
plt.show()

order = [1.05]
convergence_rate_frame = get_convergence_rate(res1.v, cruise_velocity, order)
print('velocity = ', 1 / convergence_rate_frame.cc.mean())
