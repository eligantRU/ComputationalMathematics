"""

Лабораторная работа МЕТОД НАИМЕНЬШИХ КВАДРАТОВ
Файл исходных данных: Dollar-5.xls

ВЫПОЛНИЛ: ст.гр.ПС-12, Усков В.Ю.
Вариант: 19
Дата начала неизвестности: 2017-08-01
Прогноз: на 21 дней вперед
Проверка точности прогноза: 21 дней

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.tseries.offsets import *
import matplotlib.pylab as pylab
from sklearn import grid_search, linear_model, metrics, model_selection
import time
import re
from datetime import datetime, timedelta
from math import *

                                                
LEARN_INTERVAL = datetime(2009, 1, 1), datetime(2015, 1, 1)
CHECK_INTERVAL = datetime(2015, 1, 2), datetime(2018, 4, 29)
RIDGE_COEFF = 18
L1_COEFF = 0.5 
                  
def calculate_months_average(data):
    month = 1
    dollors_month_sum = 0
    values_count = 0

    infos = []
    for row in data:
        if row["date"].month == month:
            dollors_month_sum = dollors_month_sum + row["dollar"]
            values_count = values_count + 1
        else:
            infos.append(dollors_month_sum / values_count)
            month = month % 12 + 1
            dollors_month_sum = 0
            values_count = 0
    return infos

def to_data_format(begin, days, dollars):
    if days.shape != dollars.shape:
        raise Exception('Length of days doesn`t mutch with length of dollars', days.shape, dollars.shape)
    data = []
    for index in range(0, len(days)):
        date = begin + timedelta(int(days[index]))
        data.append(dict([
            ("date", date),
            ("dollar", int(dollars[index])),
            ("day", days[index])
        ]))
    return data   
             
def beautify_data(raw_data):
    data = [];
    for index, row in raw_data.iterrows():
        date = [int(d) for d in re.split("\.", row["datetime"])]
        date.reverse()      
        date = datetime(*date)
        data.append(dict([
            ("date", date),
            ("dollar", float(row["dollar"])),
            ("day", index)
        ]))                   
    return data
           
def get_data(begin, end, data):
    dollars = []
    days = []
    for row in data:
        if begin < row["date"] <= end:
            dollars.append(row["dollar"])
            days.append(row["day"])
    return (np.array(days), np.array(dollars))

def create_functional(base_functions, days):
    functional = []
    for day in days:
        func_values = []
        for func in base_functions:
            func_values.append(func(day))
        functional.append(func_values);
    return np.matrix(functional);

def compute_base_functions_coefs_by_mnk(functional, days, dollars):
    transposed_functional = functional.transpose();
    return np.linalg.inv(transposed_functional * functional) * transposed_functional * np.matrix(dollars).transpose();


def compute_base_functions_coefs_by_l2(functional, days, dollars, redge_coeff):
    transposed_functional = functional.transpose();
    return np.linalg.inv(transposed_functional * functional - redge_coeff * np.identity(functional.shape[1])) * transposed_functional * np.matrix(dollars).transpose();    

def compute_base_functions_coefs_by_l1(base_functions, days, dollars, l1_coeff, l2_base_funcs_coeffs):
    equation_matrix = []
    free_members = []    
    for j in range(0, len(base_functions)):
        variables_coeffs = []       
        for k in range(0, len(base_functions)):
            coeff = 0.;
            for i in range(0, len(days)):
               coeff += 2 * base_functions[j](days[i]) * base_functions[k](days[i])
            variables_coeffs.append(coeff)
        equation_matrix.append(variables_coeffs)

        free_member = l1_coeff * np.sign(l2_base_funcs_coeffs[j])
        for i in range(0, len(days)):
            free_member += dollars[i] * base_functions[j](days[i])  
        free_members.append(free_member)
    return np.linalg.solve(equation_matrix, free_members)        

    
def compute_error(true_values, computed_values):
    if true_values.shape != computed_values.shape:
        raise Exception('Length of true values doesn`t mutch with length of computed values', true_values.shape, computed_values.shape)
    return ((true_values - computed_values)**2).sum()

def draw_plt(days, true_values, mnk_values, l2_values, l1_values):
    true_infos = calculate_months_average(
        to_data_format(LEARN_INTERVAL[0], days, true_values)
    )
    mnk_infos = calculate_months_average(
        to_data_format(LEARN_INTERVAL[0], days, mnk_values)
    )
    l2_infos = calculate_months_average(
        to_data_format(LEARN_INTERVAL[0], days, l2_values)
    )
    l1_infos = calculate_months_average(
        to_data_format(LEARN_INTERVAL[0], days, l1_values)
    )
    true_plt = plt.plot(range(0, len(true_infos)), true_infos, '-', label="true values")
    mnk_plt = plt.plot(range(0, len(mnk_infos)), mnk_infos, '-', label="mnk values")
    l2_plt = plt.plot(range(0, len(l2_infos)), l2_infos, '-', label="l2 values")
    l2_plt = plt.plot(range(0, len(l1_infos)), l1_infos, '-', label="l1 values")
    plt.legend()
    plt.show()    

  
def main():
    raw_data = pd.read_csv('./dollar-5.csv', encoding='cp1251', header=0,
                           sep=';', decimal=',', index_col=1, parse_dates=True)
    data = beautify_data(raw_data)                                              

    learn_days, learn_dollars = get_data(*LEARN_INTERVAL, data)
    check_days, check_dollars = get_data(*CHECK_INTERVAL, data)
    base_functions = [                 
        lambda x: sin(pi * x / 10000),
        lambda x: sin(pi * x / 1000), 
        lambda x: sin(pi * x / 100),
        lambda x: sin(pi * x / 10),  
        lambda x: sin(x),
        lambda x: cos(pi * x / 10000), 
        lambda x: cos(pi * x / 1000),   
        lambda x: cos(pi * x / 100),
        lambda x: cos(pi * x / 10),       
        lambda x: cos(x),      
        lambda x: tan(x),      
        lambda x: log(x),
        lambda x: log1p(x),
        lambda x: sqrt(x),    
        lambda x: x**2,        
        lambda x: x,        
        lambda x: 1,

    ]

    learn_functional = create_functional(base_functions, learn_days);
    check_functional = create_functional(base_functions, check_days);

    mnk_base_functions_coeffs = compute_base_functions_coefs_by_mnk(learn_functional, learn_days, learn_dollars)
    mnk_learn_dollars = np.array((learn_functional * mnk_base_functions_coeffs).transpose())[0]
    print("MNK learn error:", compute_error(learn_dollars, mnk_learn_dollars))
    mnk_check_dollars = np.array((check_functional * mnk_base_functions_coeffs).transpose())[0]
    print("MNK check error:", compute_error(check_dollars, mnk_check_dollars))

    l2_base_functions_coeffs = compute_base_functions_coefs_by_l2(learn_functional, learn_days, learn_dollars, RIDGE_COEFF)
    l2_learn_dollars = np.array((learn_functional * l2_base_functions_coeffs).transpose())[0]
    print("L2 learn error:", compute_error(learn_dollars, l2_learn_dollars))
    l2_check_dollars = np.array((check_functional * l2_base_functions_coeffs).transpose())[0]
    print("L2 check error:", compute_error(check_dollars, l2_check_dollars))
    
    l2_base_functions_coeffs = (np.array(l2_base_functions_coeffs).transpose())[0]
    l1_base_functions_coeffs = compute_base_functions_coefs_by_l1(base_functions, learn_days, learn_dollars, L1_COEFF, l2_base_functions_coeffs)
    l1_learn_dollars = np.array((learn_functional * np.matrix(l2_base_functions_coeffs).transpose()).transpose())[0]
    print("L1 learn error:", compute_error(learn_dollars, l1_learn_dollars))
    l1_check_dollars = np.array((check_functional * np.matrix(l1_base_functions_coeffs).transpose()).transpose())[0]
    print("L1 check error:", compute_error(check_dollars, l1_check_dollars))
    
    draw_plt(learn_days, learn_dollars, mnk_learn_dollars, l2_learn_dollars, l1_learn_dollars)
    draw_plt(check_days, check_dollars, mnk_check_dollars, l2_check_dollars, l1_check_dollars)

if __name__ == "__main__":
    main()