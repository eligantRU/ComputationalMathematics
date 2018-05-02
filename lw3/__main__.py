from mpl_toolkits.mplot3d import Axes3D
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
    fig = plt.figure()
    ax = fig.gca(projection="3d")

    t = np.linspace(0, 1, 11)
    x = calc_x(t)
    y = calc_y(t)
    ax.plot(x, y, zs=0, zdir="x")

    ax.set_xlim(-0.4, 0.4)
    ax.set_ylim(-0.4, 0.6)
    ax.set_zlim(-0.3, 0.6)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    plt.show()


if __name__ == "__main__":
    main()
