import matplotlib.pyplot as plt
from include.utils import *

TITLE_FONT_SIZE = 16
FONT_SIZE = 14


def execute_origin(path):
    target_error = calculate_target_error(path, TARGET_POINT, ORIGIN_SPEED_REDUCTION_SHIFT)
    res = pd.DataFrame(target_error, index=path.columns)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(res)
    ax.plot([0, len(res) - 1], [target_error[len(res) - 1], target_error[len(res) - 1]], color="brown")
    plt.title("Error changing with increasing iterations number: linear_velocity_proportional_factor "
              "= {linear_velocity_proportional_factor}, angular_velocity_proportional_factor = "
              "{angular_velocity_proportional_factor}, iteration_step_factor = {iteration_step_factor}"
              .format(linear_velocity_proportional_factor=ORIGIN_LINEAR_VELOCITY_PROPORTIONAL_FACTOR,
                      angular_velocity_proportional_factor=ORIGIN_ANGULAR_VELOCITY_PROPORTIONAL_FACTOR,
                      iteration_step_factor=ORIGIN_ITERATION_STEP_FACTOR),
              fontsize=TITLE_FONT_SIZE)
    plt.xlabel("Iteration number", fontsize=FONT_SIZE)
    plt.ylabel("Error", fontsize=FONT_SIZE)
    plt.show()


def find_quasioptimal_parameters():
    path = calculate_path(START_POSITION, LINEAR_VELOCITY_PROPORTIONAL_FACTOR,
                          ANGULAR_VELOCITY_PROPORTIONAL_FACTOR, ITERATION_STEP_FACTOR)
    target_error = calculate_target_error(path, TARGET_POINT, SPEED_REDUCTION_SHIFT)

    res = pd.DataFrame(target_error, index=path.columns)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(res)
    ax.plot([0, len(res) - 1], [target_error[len(res) - 1], target_error[len(res) - 1]], color="brown")
    plt.title("Error changing with increasing iterations number: "
              "linear_velocity_proportional_factor = {linear_velocity_proportional_factor}, "
              "angular_velocity_proportional_factor = {angular_velocity_proportional_factor}, "
              "iteration_step_factor = {iteration_step_factor}"
              .format(linear_velocity_proportional_factor=LINEAR_VELOCITY_PROPORTIONAL_FACTOR,
                      angular_velocity_proportional_factor=ANGULAR_VELOCITY_PROPORTIONAL_FACTOR,
                      iteration_step_factor=ITERATION_STEP_FACTOR),
              fontsize=TITLE_FONT_SIZE)
    plt.xlabel("Iteration number", fontsize=FONT_SIZE)
    plt.ylabel("Error", fontsize=FONT_SIZE)
    plt.show()


def show_path():
    path = calculate_path(START_POSITION, ORIGIN_LINEAR_VELOCITY_PROPORTIONAL_FACTOR,
                          ORIGIN_ANGULAR_VELOCITY_PROPORTIONAL_FACTOR, ITERATION_PATH_STEP_FACTOR)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(path.ix[0], path.ix[1], color="red")
    plt.title("Robot path", fontsize=TITLE_FONT_SIZE)
    plt.xlabel("X", fontsize=FONT_SIZE)
    plt.ylabel("Y", fontsize=FONT_SIZE)
    plt.show()


def estimate_convergence_rate(path):
    last_point = path[len(path.columns) - 1]
    c = 1, 1.05, 1.1
    ccframe = get_convergence_rate(path, last_point, c)
    b = int(len(ccframe) / len(c))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(ccframe.step[1:b], ccframe.cc[1:b], "k^", color="red")
    ax.plot(ccframe.step[b + 1:b + b], ccframe.cc[b + 1:b + b], "k+", color="green")
    ax.plot(ccframe.step[b + b + 1:], ccframe.cc[b + b + 1:], "k*", color="brown")
    plt.title("Estimation of the order and speed of convergence", fontsize=TITLE_FONT_SIZE)
    plt.xlabel("Step", fontsize=FONT_SIZE)
    plt.ylabel("Convergence rate", fontsize=FONT_SIZE)
    plt.show()

    order = [1.0]
    convergence_rate = get_convergence_rate(path, last_point, order)
    print("Velocity = ", 1 / convergence_rate.cc.mean())


def main():
    origin_path = calculate_path(START_POSITION, ORIGIN_LINEAR_VELOCITY_PROPORTIONAL_FACTOR,
                                 ORIGIN_ANGULAR_VELOCITY_PROPORTIONAL_FACTOR, ORIGIN_ITERATION_STEP_FACTOR)
    execute_origin(origin_path)
    find_quasioptimal_parameters()

    show_path()
    estimate_convergence_rate(origin_path)


if __name__ == "__main__":
    main()
