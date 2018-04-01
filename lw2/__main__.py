import pandas as pd
import matplotlib.pyplot as plt
from include.utils import *

epsX = 0.1  # PRECISION
MAX_ITERATIONS_NUMBER = 100

# **ИСХОДНЫЕ ДАННЫЕ: параметры варианта**
START_POSITION = (0, 0, 0)  # x0 y0 fi0
TARGET_POINT = (4, 1, 17)  # A B C

# **ИСХОДНЫЕ ДАННЫЕ: подбираемые параметры**
alfa = 0.5     # - коэффициент альфа обеспечения сходимости (коэффициент итерационного шага)
betta = 0.5    # - коэффициент бетта для расчёта kB
LINEAR_VELOCITY_PROPORTIONAL_FACTOR = 0.5
ANGULAR_VELOCITY_PROPORTIONAL_FACTOR = 2


def do_iteration(linear_velocity_proportional_factor, angular_velocity_proportional_factor):
    vm = (linear_velocity_proportional_factor, 0, 0, 0, linear_velocity_proportional_factor, 0, 0, 0, angular_velocity_proportional_factor)
    return pd.DataFrame([vm[0:3], vm[3:6], vm[6:9]])


def iterMeth(x0, linear_velocity_proportional_factor, angular_velocity_proportional_factor, alfa=1, betta=0.5, epsX=0.1, maxIter=50):
    xtr = pd.Series(x0)
    xtr = pd.DataFrame(xtr, index=xtr.index)
    i = 1
    while (calculate_quadratic_norm(calculate_residual(x0, TARGET_POINT, betta)[0:2]) > epsX) \
                & (len(xtr.columns) < maxIter):
        F0 = calculate_residual(x0, TARGET_POINT, betta)
        F0 = pd.Series(F0)
        F0 = pd.DataFrame(F0, index=F0.index)
        x00 = pd.Series(x0)
        x00 = pd.DataFrame(x00, index=x00.index)
        x00 = x00.as_matrix() + np.dot(alfa*do_iteration(linear_velocity_proportional_factor,angular_velocity_proportional_factor).as_matrix(), F0.as_matrix())
        xtr[i] = x00
        x0 = xtr[i]
        i += 1
    ## возвращаем массив - в i-м столбце - i-е приближение
    return xtr


## **1. АНАЛИЗ РАБОТЫ ПИ-РЕГУЛЯТОРА при ЗАДАННЫХ ЗНАЧЕНИЯХ**
# РАСЧЕТ ТРАЕКТОРИИ при ЗАДАННЫХ ЗНАЧЕНИЯХ ПАРАМЕТРОВ:*
xtr = iterMeth(START_POSITION, LINEAR_VELOCITY_PROPORTIONAL_FACTOR, ANGULAR_VELOCITY_PROPORTIONAL_FACTOR, alfa, betta)

## *РАСЧЕТ И ВЫВОД ГРАФИКА ИЗМЕНЕНИЯ НЕВЯЗКИ:*
ind = xtr.columns
epsX = calculate_target_error(xtr, TARGET_POINT, betta)
res = pd.DataFrame(epsX, index = ind)
#
plt.rcParams["font.fantasy"] = "Arial", "Times New Roman", "Tahoma", "Comic Sans MS", "Courier"
plt.rcParams["font.family"] = "fantasy"
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(res)
ax.plot([0,len(res)-1], [epsX[len(res)-1], epsX[len(res)-1]], color="brown")
plt.title("Изменение погрешности с ростом итераций \
при linear_velocity_proportional_factor="+str(LINEAR_VELOCITY_PROPORTIONAL_FACTOR)+", angular_velocity_proportional_factor="+str(ANGULAR_VELOCITY_PROPORTIONAL_FACTOR)+", alfa="+str(alfa), fontsize=16)
plt.xlabel("номер итерации", fontsize=14)
plt.ylabel("погрешность", fontsize=14)
plt.show()

## 2. ПОИСК КВАЗИОПТИМАЛЬНЫХ ПАРАМЕТРОВ**
### РАСЧЕТ ТРАЕКТОРИИ СКОРОСТИ при ВЫБРАННЫХ ЗНАЧЕНИЯХ ПАРАМЕТРОВ ПИ-регулятора:*
linear_velocity_proportional_factor1 = 1
angular_velocity_proportional_factor1 = 2
alfa1 = 0.5
# bettaopt = 0.5
xtr1 = iterMeth(START_POSITION, linear_velocity_proportional_factor1, angular_velocity_proportional_factor1, alfa1)

# РАСЧЕТ И ВЫВОД ГРАФИКА ИЗМЕНЕНИЯ НЕВЯЗКИ:
ind1 = xtr1.columns
epsX = calculate_target_error(xtr1, TARGET_POINT, betta)
res1 = pd.DataFrame(epsX, index = ind1)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(res1)
ax.plot([0,len(res1)-1], [epsX[len(res1)-1], epsX[len(res1)-1]], color="brown")
plt.title("Изменение погрешности с ростом итераций \
при linear_velocity_proportional_factor="+str(linear_velocity_proportional_factor1)+", angular_velocity_proportional_factor="+str(angular_velocity_proportional_factor1)+", alfa="+str(alfa1), fontsize=16)
plt.xlabel("номер итерации", fontsize=14)
plt.ylabel("погрешность", fontsize=14)
plt.show()

# РАСЧЕТ ТРАЕКТОРИИ РОБОТА и ВЫВОД ГРАФИКА
# Для обеспечения плавности траектории выберем мелкий шаг alfa
alfa = 0.1
xtr2 = iterMeth(START_POSITION, LINEAR_VELOCITY_PROPORTIONAL_FACTOR, ANGULAR_VELOCITY_PROPORTIONAL_FACTOR, alfa, betta)
#
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(xtr2.ix[0], xtr2.ix[1], color="red")
plt.title("Траектория движения робота", fontsize=16)
plt.xlabel("X", fontsize=14)
plt.ylabel("Y", fontsize=14)
plt.show()


# 3.	ИССЛЕДУЕМ ПОРЯДОК И СКОРОСТЬ СХОДИМОСТИ
# ПРОГРАММА РАСЧЕТА ПОСЛЕДОВАТЕЛЬНОСТИ ОТНОШЕНИЯ:
def get_convergence_rate(x, xfin, p):
    numv = len(x.columns)
    pf, cc = [], []
    step = list(range(numv))*len(p)
    i = 0
    for n in range(len(p)):
        for m in range(numv):
            pf.append(p[n])
    for ip in range(len(p)):
        cc.append(1.)
        for ix in range(1, numv):
            cc.append(calculate_quadratic_norm(xfin - x[:][ix]) / calculate_quadratic_norm(xfin - x[:][ix-1])**pf[i])
            i += 1
    return pd.DataFrame({
        "step": pd.Series(step),
        "cc": pd.Series(cc),
        "pf": pd.Series(pf)
    })


xfin = xtr[len(xtr.columns)-1]
c = 1, 1.05, 1.1
ccframe = get_convergence_rate(xtr, xfin, c)
b = int(len(ccframe) / len(c))

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(ccframe.step[1:b], ccframe.cc[1:b], "k^", color="red")
ax.plot(ccframe.step[b+1:b+b], ccframe.cc[b+1:b+b], "k+", color="green")
ax.plot(ccframe.step[b+b+1:], ccframe.cc[b+b+1:], "k*", color="brown")
plt.title("Оценка порядка и скорости сходимости", fontsize=16)
plt.xlabel("step", fontsize=14)
plt.ylabel("cc", fontsize=14)
plt.show()

order = [1.0]
convergence_rate = get_convergence_rate(xtr, xfin, order)
print("velocity = ", 1 / convergence_rate.cc.mean())