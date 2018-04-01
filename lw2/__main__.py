import matplotlib.pyplot as plt
from include.utils import *

epsX = PRECISION

## **1. АНАЛИЗ РАБОТЫ ПИ-РЕГУЛЯТОРА при ЗАДАННЫХ ЗНАЧЕНИЯХ**
# РАСЧЕТ ТРАЕКТОРИИ при ЗАДАННЫХ ЗНАЧЕНИЯХ ПАРАМЕТРОВ:*
xtr = calculate_path(START_POSITION, LINEAR_VELOCITY_PROPORTIONAL_FACTOR, ANGULAR_VELOCITY_PROPORTIONAL_FACTOR, ITERATION_STEP_FACTOR)

## *РАСЧЕТ И ВЫВОД ГРАФИКА ИЗМЕНЕНИЯ НЕВЯЗКИ:*
ind = xtr.columns
epsX = calculate_target_error(xtr, TARGET_POINT, SPEED_REDUCTION_SHIFT)
res = pd.DataFrame(epsX, index = ind)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(res)
ax.plot([0,len(res)-1], [epsX[len(res)-1], epsX[len(res)-1]], color="brown")
plt.title("Изменение погрешности с ростом итераций \
при linear_velocity_proportional_factor="+str(LINEAR_VELOCITY_PROPORTIONAL_FACTOR)+", angular_velocity_proportional_factor="+str(ANGULAR_VELOCITY_PROPORTIONAL_FACTOR)+", ITERATION_STEP_FACTOR="+str(ITERATION_STEP_FACTOR), fontsize=16)
plt.xlabel("номер итерации", fontsize=14)
plt.ylabel("погрешность", fontsize=14)
plt.show()

## 2. ПОИСК КВАЗИОПТИМАЛЬНЫХ ПАРАМЕТРОВ**
### РАСЧЕТ ТРАЕКТОРИИ СКОРОСТИ при ВЫБРАННЫХ ЗНАЧЕНИЯХ ПАРАМЕТРОВ ПИ-регулятора:*
linear_velocity_proportional_factor1 = 1
angular_velocity_proportional_factor1 = 2
iteration_step_factor1 = 0.5
# SPEED_REDUCTION_SHIFTopt = 0.5
xtr1 = calculate_path(START_POSITION, linear_velocity_proportional_factor1, angular_velocity_proportional_factor1, iteration_step_factor1)

# РАСЧЕТ И ВЫВОД ГРАФИКА ИЗМЕНЕНИЯ НЕВЯЗКИ:
ind1 = xtr1.columns
epsX = calculate_target_error(xtr1, TARGET_POINT, SPEED_REDUCTION_SHIFT)
res1 = pd.DataFrame(epsX, index = ind1)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(res1)
ax.plot([0,len(res1)-1], [epsX[len(res1)-1], epsX[len(res1)-1]], color="brown")
plt.title("Изменение погрешности с ростом итераций \
при linear_velocity_proportional_factor="+str(linear_velocity_proportional_factor1)+", angular_velocity_proportional_factor="+str(angular_velocity_proportional_factor1)+", ITERATION_STEP_FACTOR="+str(iteration_step_factor1), fontsize=16)
plt.xlabel("номер итерации", fontsize=14)
plt.ylabel("погрешность", fontsize=14)
plt.show()

# РАСЧЕТ ТРАЕКТОРИИ РОБОТА и ВЫВОД ГРАФИКА
# Для обеспечения плавности траектории выберем мелкий шаг ITERATION_STEP_FACTOR
ITERATION_STEP_FACTOR = 0.1
xtr2 = calculate_path(START_POSITION, LINEAR_VELOCITY_PROPORTIONAL_FACTOR, ANGULAR_VELOCITY_PROPORTIONAL_FACTOR, ITERATION_STEP_FACTOR)
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
last_point = xtr[len(xtr.columns)-1]
c = 1, 1.05, 1.1
ccframe = get_convergence_rate(xtr, last_point, c)
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
convergence_rate = get_convergence_rate(xtr, last_point, order)
print("velocity = ", 1 / convergence_rate.cc.mean())
