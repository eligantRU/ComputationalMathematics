import matplotlib.pyplot as plt
from lw1.include.utils import *


TITLE_FONT_SIZE = 16
FONT_SIZE = 14


def execute_origin(res):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(res)
    a1 = pd.Series(CRUISE_VELOCITY, index=res.index)
    ax.plot(a1, color="red")
    a2 = pd.Series(CRUISE_VELOCITY - 10 * VELOCITY_PRECISION, index=res.index)
    ax.plot(a2, "k--", color="green")
    a3 = pd.Series(CRUISE_VELOCITY + 10 * VELOCITY_PRECISION, index=res.index)
    ax.plot(a3, "k--", color="green")
    plt.title("Velocity changing", fontsize=TITLE_FONT_SIZE)
    plt.xlabel("Time, s", fontsize=FONT_SIZE)
    plt.ylabel("Velocity, m/s", fontsize=FONT_SIZE)
    plt.show()


def execute_origin_with_limit_time(res):
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
    plt.title("Velocity changing(proportional_factor={proportional_factor}, integral_factor={integral_factor})"
              .format(proportional_factor=ORIGINAL_PROPORTIONAL_FACTOR, integral_factor=ORIGINAL_INTEGRAL_FACTOR),
              fontsize=TITLE_FONT_SIZE)
    plt.xlabel("Time, s", fontsize=FONT_SIZE)
    plt.ylabel("Velocity, m/s", fontsize=FONT_SIZE)
    plt.show()


def execute_with_limit_time(origin_res, res):
    limit_time1 = get_no_error_time(res)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(res[50:])
    a1 = pd.Series(CRUISE_VELOCITY, index=origin_res.index[50:])
    ax.plot(a1, color="red")
    a2 = pd.Series(CRUISE_VELOCITY - 2 * VELOCITY_PRECISION, index=origin_res.index[50:])
    ax.plot(a2, "k--", color="green")
    a3 = pd.Series(CRUISE_VELOCITY + 2 * VELOCITY_PRECISION, index=origin_res.index[50:])
    ax.plot(a3, "k--", color="green")
    ax.plot([limit_time1, limit_time1], [CRUISE_VELOCITY - 4, CRUISE_VELOCITY + 4], color="brown")
    plt.title("Velocity changing(proportional_factor={proportional_factor}, integral_factor={integral_factor})"
              .format(proportional_factor=PROPORTIONAL_FACTOR, integral_factor=INTEGRAL_FACTOR), fontsize=TITLE_FONT_SIZE)
    plt.xlabel("Time, s", fontsize=FONT_SIZE)
    plt.ylabel("Velocity, m/s", fontsize=FONT_SIZE)
    plt.show()


def estimate_convergence_rate(res):
    c = [1., 1.1, 1.2]
    convergence_rate_frame = get_convergence_rate(res.v, c)
    b = int(len(convergence_rate_frame) / len(c))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(convergence_rate_frame.step[1: b], convergence_rate_frame.cc[1:b], color="red")
    ax.plot(convergence_rate_frame.step[b + 1: b + b], convergence_rate_frame.cc[b + 1: b + b], "k--", color="green")
    ax.plot(convergence_rate_frame.step[b + b + 1:], convergence_rate_frame.cc[b + b + 1:], "k.", color="brown")
    plt.title("Estimation of the order and speed of convergence", fontsize=TITLE_FONT_SIZE)
    plt.xlabel("step", fontsize=FONT_SIZE)
    plt.ylabel("convergence rate", fontsize=FONT_SIZE)
    plt.show()

    order = [1.05]
    convergence_rate_frame = get_convergence_rate(res.v, order)
    print("velocity = ", 1 / convergence_rate_frame.cc.mean())


def main():
    origin_res = cruise_control(proportional_factor=ORIGINAL_PROPORTIONAL_FACTOR,
                                integral_factor=ORIGINAL_INTEGRAL_FACTOR)
    res = cruise_control(proportional_factor=PROPORTIONAL_FACTOR, integral_factor=INTEGRAL_FACTOR)

    execute_origin(origin_res)
    execute_origin_with_limit_time(origin_res)
    execute_with_limit_time(origin_res, res)
    estimate_convergence_rate(res)


if __name__ == "__main__":
    main()
