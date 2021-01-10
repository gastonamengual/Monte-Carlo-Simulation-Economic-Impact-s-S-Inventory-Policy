"""Common Functionality for the StockSystem"""

__version__ = "1.0"

from datetime import datetime, timedelta
import calendar

import numpy as np

# AUXILIARY FUNCTIONS
def symmetric_simple_moving_average(data, n=10):
    n = n//2
    smooth = [np.nan]*n
    for i in range(n,len(data)-n):
        smooth.append(np.mean(data[i-n:i+n]))
    smooth += [np.nan]*n
    return smooth

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime(year, month, day)

def calc_total_days(initial_date, months):
    return abs((initial_date - add_months(initial_date, months)).days)

def set_selling_price(profit, avg_daily_arrivals, unit_cost, fixed_costs, avg_sale_size, price_ceiling):
    
    units_sold_month = avg_daily_arrivals * avg_sale_size * 365/12
    total_month_cost = units_sold_month * unit_cost + fixed_costs
    
    price = total_month_cost * (1 + profit) / units_sold_month
    
    price_floor = total_month_cost // units_sold_month
    
    price = max(price_floor,price)
    price = min(price_ceiling,price)
    
    return price,price_floor