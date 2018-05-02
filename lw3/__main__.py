import numpy as np
import matplotlib.pyplot as plt


def fill(n, val):
    a = np.empty(n)
    a.fill(val)
    return a


def calc_x(t):
    if 0. <= t < 0.4:
        return 0.2
    elif 0.4 <= t <= 0.6:
        return 0.6 - t
    else:
        return 0.


def calc_y(t):
    if 0. <= t < 0.4:
        return t
    elif 0.4 <= t <= 0.6:
        return 0.4
    else:
        return 1. - t


calc_y = np.vectorize(calc_y)
calc_x = np.vectorize(calc_x)


def main():
    t = np.linspace(0, 1, 11)
    x = calc_x(t)
    y = calc_y(t)
    plt.figure()
    plt.plot(x, y, '--o')
    plt.axis([-0.5, 1.5, -0.5, 1.5])
    plt.show()


if __name__ == "__main__":
    main()
