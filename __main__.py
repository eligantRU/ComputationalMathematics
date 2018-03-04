import matplotlib.pyplot as plt
from include.utils import *


def main():
    res = cruise_control(proportional_factor=ORIGINAL_PROPORTIONAL_FACTOR, integral_factor=ORIGINAL_INTEGRAL_FACTOR)

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

    ###

    limit_time = get_no_error_time(res)

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
    plt.title("Velocity changing: proportional_factor={proportional_factor}, integral_factor={integral_factor}"
              .format(proportional_factor=ORIGINAL_PROPORTIONAL_FACTOR, integral_factor=ORIGINAL_INTEGRAL_FACTOR),
              fontsize=16)
    plt.xlabel("Time, s", fontsize=14)
    plt.ylabel("Velocity, m/s", fontsize=14)
    plt.show()

    ###

    res1 = cruise_control(proportional_factor=PROPORTIONAL_FACTOR, integral_factor=INTEGRAL_FACTOR)
    limit_time1 = get_no_error_time(res1)

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
    plt.title("Velocity changing: proportional_factor={proportional_factor}, integral_factor={integral_factor}"
              .format(proportional_factor=PROPORTIONAL_FACTOR, integral_factor=INTEGRAL_FACTOR), fontsize=16)
    plt.xlabel("Time, s", fontsize=14)
    plt.ylabel("Velocity, m/s", fontsize=14)
    plt.show()

    ###

    c = [1., 1.1, 1.2]
    convergence_rate_frame = get_convergence_rate(res1.v, c)
    b = int(len(convergence_rate_frame) / len(c))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(convergence_rate_frame.istep[1: b], convergence_rate_frame.cc[1:b], color="red")
    ax.plot(convergence_rate_frame.istep[b + 1: b + b], convergence_rate_frame.cc[b + 1: b + b], "k--", color="green")
    ax.plot(convergence_rate_frame.istep[b + b + 1:], convergence_rate_frame.cc[b + b + 1:], "k.", color="brown")
    plt.title("Estimation of the order and speed of convergence", fontsize=16)
    plt.xlabel("istep", fontsize=14)
    plt.ylabel("cc", fontsize=14)
    plt.show()

    order = [1.05]
    convergence_rate_frame = get_convergence_rate(res1.v, order)
    print("velocity = ", 1 / convergence_rate_frame.cc.mean())


if __name__ == "__main__":
    main()
