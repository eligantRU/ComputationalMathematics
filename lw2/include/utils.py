import numpy as np
import pandas as pd
from math import *


def normalize_angle(fi):
    while abs(fi) > pi:
        fi -= 2 * pi * np.sign(fi)
    return fi


def calculate_angle_error(current_position, target_point):
    x, y, fi = current_position[0], current_position[1], current_position[2]
    target_x, target_y = target_point[0], target_point[1]
    return normalize_angle(atan2(-target_y - y, -target_x - x) - fi)


def calculate_position_error(current_position, target_point):
    x, y = current_position[0], current_position[1]
    target_x, target_y, target_angle = target_point[0], target_point[1], target_point[2]
    return sqrt(x**2 + y**2 + 2 * target_x * x + 2 * target_y * y + target_angle)


def calculate_speed_reduction(current_position, target_point, speed_reduction_shift):
    return speed_reduction_shift + abs(pi - calculate_angle_error(current_position, target_point)) / pi


def calculate_quadratic_norm(vec):
    result = 0
    for i in range(len(vec)):
        result += vec[i]**2
    return sqrt(result)


def calculate_residual(current_position, target_point, speed_reduction_shift):
    fi = current_position[2]
    position_error = calculate_position_error(current_position, target_point)
    speed_reduction = calculate_speed_reduction(current_position, target_point, speed_reduction_shift)
    return (
        position_error * speed_reduction * cos(fi),
        position_error * speed_reduction * sin(fi),
        calculate_angle_error(current_position, target_point)
    )


def calculate_target_error(current_position, target_point, speed_reduction_shift):
    error = []
    for ic in current_position.columns:
        error.append(calculate_quadratic_norm(
            calculate_residual(current_position[:][ic], target_point, speed_reduction_shift)[0:2]
        ))
    return error


def get_iteration_matrix(linear_velocity_proportional_factor, angular_velocity_proportional_factor):
    matrix = (
        linear_velocity_proportional_factor, 0, 0,
        0, linear_velocity_proportional_factor, 0,
        0, 0, angular_velocity_proportional_factor
    )
    return pd.DataFrame([matrix[0:3], matrix[3:6], matrix[6:9]])


def get_convergence_rate(path, xfin, p):
    steps_number = len(path.columns)
    pf, cc = [], []
    step = list(range(steps_number)) * len(p)
    i = 0
    for n in range(len(p)):
        for m in range(steps_number):
            pf.append(p[n])
    for ip in range(len(p)):
        cc.append(1.)
        for ix in range(1, steps_number):
            cc.append(
                calculate_quadratic_norm(xfin - path[:][ix]) / calculate_quadratic_norm(xfin - path[:][ix-1])**pf[i]
            )
            i += 1
    return pd.DataFrame({
        "step": pd.Series(step),
        "cc": pd.Series(cc),
        "pf": pd.Series(pf)
    })
