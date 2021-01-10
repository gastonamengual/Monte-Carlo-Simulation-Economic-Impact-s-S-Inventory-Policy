"""
Parameters

This module returns the parameters of the Stock Simulation

Parameters with '#' are those optimized. 
"""

__version__ = "1.0"	

from datetime import datetime, timedelta
import calendar

from common import symmetric_simple_moving_average, calc_total_days

initial_date = datetime(2020, 1, 1)
months = 6

def get_parameters_pnl():

    parameters = {
        "avg_daily_arrivals" : 3,
        "avg_sale_size" : 2,
        "max_arrivals" : 500,
        "min_arrivals" : 1,
        "growth" : 0.005,
        "decay_stock" : 0.1,
        "decay_price": 0.001,
        "initial_investment": 5000,
        "profit": 2,
        "unit_cost": 3,
        "fixed_costs": 5000,
        "num_days": calc_total_days(initial_date, months),
        "initial_date": initial_date,
        "min_order_delay" : 0.5,
        "mode_order_delay" : 1,
        "max_order_delay" : 6,
        "market_price": 7,
        "price_ceiling": 14,
        "max_stock" : 3000,

        "control_frequency" : 1,
        "initial_stock_level" : 2754,
        "stock_floor" : 2807,
        "stock_ceiling" : 2799,
    }

    return parameters, months

def get_parameters_pl():

    parameters = {
        "avg_daily_arrivals" : 3,
        "avg_sale_size" : 2,
        "max_arrivals" : 500,
        "min_arrivals" : 1,
        "growth" : 0.005,
        "decay_stock" : 0.1,
        "decay_price": 0.001,
        "initial_investment": 5000,
        "profit": 2,
        "unit_cost": 3,
        "fixed_costs": 5000,
        "num_days": calc_total_days(initial_date, months),
        "initial_date": initial_date,
        "min_order_delay" : 0.5,
        "mode_order_delay" : 1,
        "max_order_delay" : 6,
        "market_price": 7,
        "price_ceiling": 14,
        "max_stock" : 3000,

        "control_frequency" : 1,
        "initial_stock_level" : 441,
        "stock_floor" : 2827,
        "stock_ceiling" : 2889,
    }

    return parameters, months

def get_parameters_e():

    parameters = {
        "avg_daily_arrivals" : 3,
        "avg_sale_size" : 2,
        "max_arrivals" : 500,
        "min_arrivals" : 1,
        "growth" : 0.005,
        "decay_stock" : 0.1,
        "decay_price": 0.001,
        "initial_investment": 5000,
        "profit": 2,
        "unit_cost": 3,
        "fixed_costs": 5000,
        "num_days": calc_total_days(initial_date, months),
        "initial_date": initial_date,
        "min_order_delay" : 0.5,
        "mode_order_delay" : 1,
        "max_order_delay" : 6,
        "market_price": 7,
        "price_ceiling": 14,
        "max_stock" : 3000,

        "control_frequency" : 22,
        "initial_stock_level" : 2349,
        "stock_floor" : 3,
        "stock_ceiling" : 65,
    }

    return parameters, months

def get_parameters_l():

    parameters = {
        "avg_daily_arrivals" : 3,
        "avg_sale_size" : 2,
        "max_arrivals" : 500,
        "min_arrivals" : 1,
        "growth" : 0.005,
        "decay_stock" : 0.1,
        "decay_price": 0.001,
        "initial_investment": 5000,
        "profit": 2,
        "unit_cost": 3,
        "fixed_costs": 5000,
        "num_days": calc_total_days(initial_date, months),
        "initial_date": initial_date,
        "min_order_delay" : 0.5,
        "mode_order_delay" : 1,
        "max_order_delay" : 6,
        "market_price": 7,
        "price_ceiling": 14,
        "max_stock" : 3000,

        "control_frequency" : 27,
        "initial_stock_level" : 0,
        "stock_floor" : 0,
        "stock_ceiling" : 137,
    }

    return parameters, months