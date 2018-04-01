import pandas as pd
import matplotlib.pyplot as plt
from include.utils import *
#
###**ИСХОДНЫЕ ДАННЫЕ: фиксированные параметры**
epsX = 0.1   # - допустимая погрешность по невязке (отклонение от пункта назначения)
nticks = 100    # Допустимый максимум итераций
###**ИСХОДНЫЕ ДАННЫЕ: параметры варианта**
x0 = 0   # - координата по x начального расположения робота
y0 = 0     # - координата по y начального расположения робота
fi0 = 0    # - начальный азимутальный угол направления движения робота
Apar = 4  # - параметр А
Bpar = 1 # - параметр В
Cpar = 17 # - параметр С
###**ИСХОДНЫЕ ДАННЫЕ: подбираемые параметры**
alfa = 0.5     # - коэффициент альфа обеспечения сходимости (коэффициент итерационного шага)
betta = 0.5    # - коэффициент бетта для рачета kB
kV = 0.5  # - коэффициент пропорционального регулятора линейной скорости
kw = 2   # - коэффициент пропорционального регулятора угловой скорости

### **ПРОГРАММА РАСЧЕТА ТРАЕКТОРИИ ДВИЖЕНИЯ РОБОТА (итерационная функция):**
def Qfun(kV, kw):
    vm = (kV, 0, 0, 0, kV, 0, 0, 0, kw)
    Qmat = pd.DataFrame([vm[0:3], vm[3:6], vm[6:9]])
    return Qmat
#
def iterMeth(x0, kV, kw, alfa=1, betta=0.5, epsX=0.1, maxIter= 50):
    Apar = 4  # - параметр А
    Bpar = 1 # - параметр В
    Cpar = 17 # - параметр С
    xtr = pd.Series(x0)
    xtr = pd.DataFrame(xtr, index=xtr.index)
    i = 1
    while (calculate_quadratic_norm(calculate_residual(x0, (Apar, Bpar, Cpar), betta)[0:2]) > epsX) \
                & (len(xtr.columns) < maxIter):
        F0 = calculate_residual(x0, (Apar, Bpar, Cpar), betta)
        F0 = pd.Series(F0)
        F0 = pd.DataFrame(F0, index=F0.index)
        x00 = pd.Series(x0)
        x00 = pd.DataFrame(x00, index=x00.index)
        x00 = x00.as_matrix() + np.dot(alfa*Qfun(kV,kw).as_matrix(), F0.as_matrix())
        xtr[i] = x00
        x0 = xtr[i]
        i += 1
    ## возвращаем массив - в i-м столбце - i-е приближение
    return xtr

## **1. АНАЛИЗ РАБОТЫ ПИ-РЕГУЛЯТОРА при ЗАДАННЫХ ЗНАЧЕНИЯХ**
# РАСЧЕТ ТРАЕКТОРИИ при ЗАДАННЫХ ЗНАЧЕНИЯХ ПАРАМЕТРОВ:*
s0 = (x0, y0, fi0)
xtr = iterMeth(s0, kV, kw, alfa, betta)

## *РАСЧЕТ И ВЫВОД ГРАФИКА ИЗМЕНЕНИЯ НЕВЯЗКИ:*
ind = xtr.columns
epsX = calculate_target_error(xtr, (Apar, Bpar, Cpar), betta)
res = pd.DataFrame(epsX, index = ind)
#
plt.rcParams["font.fantasy"] = "Arial", "Times New Roman", "Tahoma", "Comic Sans MS", "Courier"
plt.rcParams["font.family"] = "fantasy"
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(res)
ax.plot([0,len(res)-1], [epsX[len(res)-1], epsX[len(res)-1]], color="brown")
plt.title("Изменение погрешности с ростом итераций \
при kV="+str(kV)+", kw="+str(kw)+", alfa="+str(alfa), fontsize=16)
plt.xlabel("номер итерации", fontsize=14)
plt.ylabel("погрешность", fontsize=14)
plt.show()

## 2. ПОИСК КВАЗИОПТИМАЛЬНЫХ ПАРАМЕТРОВ**
### РАСЧЕТ ТРАЕКТОРИИ СКОРОСТИ при ВЫБРАННЫХ ЗНАЧЕНИЯХ ПАРАМЕТРОВ ПИ-регулятора:*
kV1 = 1
kw1 = 2
alfa1 = 0.5
# bettaopt = 0.5
xtr1 = iterMeth(s0, kV1, kw1, alfa1)
xtr1
# РАСЧЕТ И ВЫВОД ГРАФИКА ИЗМЕНЕНИЯ НЕВЯЗКИ:
ind1 = xtr1.columns
epsX = calculate_target_error(xtr1, (Apar, Bpar, Cpar), betta)
res1 = pd.DataFrame(epsX, index = ind1)
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(res1)
ax.plot([0,len(res1)-1], [epsX[len(res1)-1], epsX[len(res1)-1]], color="brown")
plt.title("Изменение погрешности с ростом итераций \
при kV="+str(kV1)+", kw="+str(kw1)+", alfa="+str(alfa1), fontsize=16)
plt.xlabel("номер итерации", fontsize=14)
plt.ylabel("погрешность", fontsize=14)
plt.show()

# РАСЧЕТ ТРАЕКТОРИИ РОБОТА и ВЫВОД ГРАФИКА
# Для обеспечения плавности траектории выберем мелкий шаг alfa
alfa = 0.1
xtr2 = iterMeth(s0, kV, kw, alfa, betta)
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