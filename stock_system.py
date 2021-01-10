"""
Stock System

This module provides the basic functionality to simulate a stock System
"""

__version__ = "2.3"

from collections import defaultdict
from datetime import timedelta

from common import calc_total_days, set_selling_price

import numpy as np
import pandas as pd

PRNG = np.random.RandomState(42)

def set_random_state(seed:int) -> None:
    global PRNG
    PRNG = np.random.RandomState(seed)

#-------------------------------------------------------------------------#

# SIMULATION

def simulate(initial_investment=None, initial_stock_level=None, avg_daily_arrivals=None, control_frequency=None, growth=None, 
             decay_stock=None, decay_price=None, avg_sale_size=None, num_days=None, stock_floor=None, 
             stock_ceiling=None, min_order_delay=None, mode_order_delay=None, max_order_delay=None, max_arrivals=None, 
             min_arrivals=None, max_stock=None, initial_date=None, unit_cost=None, fixed_costs=None, profit=None, 
             price_ceiling=None,market_price=None, **kwargs):
    
    """Stock simulation"""
    
    events = {'order': np.inf,
              'arrival': PRNG.exponential(1 / avg_daily_arrivals),
              'simulation_end': num_days,
              'control': 0,
              'month_close':1}

    columns = ['clock', 'capital', 'stock', 'stock_floor', 'stock_ceiling', 'price', 'price_floor', 
               'price_ceiling', 'arrivals', 'sales', 'orders', 'losses', 'event']
    df = pd.DataFrame(columns = columns)
    
    stock_level = initial_stock_level
    stock_floor = stock_floor
    stock_ceiling = stock_ceiling
    
    capital_level = initial_investment
    
    price_ceiling = price_ceiling
    selling_price, price_floor = set_selling_price(profit, avg_daily_arrivals, unit_cost, fixed_costs, avg_sale_size, price_ceiling)

    initial_values = {'clock': 0,
                      'capital': capital_level,
                      'stock': stock_level,
                      'stock_floor': stock_floor,
                      'stock_ceiling': stock_ceiling,
                      'price': selling_price,
                      'price_floor': price_floor,
                      'price_ceiling': price_ceiling,
                      'arrivals': 0,
                      'sales': 0,
                      'orders': 0,
                      'losses': 0,
                      'event': 'init'
                       }
    
    
    df = df.append(initial_values, ignore_index=True)
    
    data = defaultdict(list)
    
    while True:

        current_event_type, current_event_time = min(events.items(), key=lambda x: x[1])
        
        # CONTROL EVENT
        if current_event_type == 'control':
            amount = stock_ceiling - stock_level
            
            if stock_level < stock_floor and amount > 0 and np.isinf(events['order']):
                ordering_cost = amount * unit_cost
                
                if capital_level < ordering_cost:
                    amount = capital_level // unit_cost
                    ordering_cost = amount * unit_cost
                    
                if amount >= 1:
                    events['order'] = current_event_time + PRNG.triangular(min_order_delay, mode_order_delay, max_order_delay)
                    capital_level -= ordering_cost
            
            events['control'] = current_event_time + control_frequency
    
    
        # ARRIVAL EVENT
        elif current_event_type == 'arrival':
            
            size_demand = 0
            accepted_price = market_price * (1 + PRNG.triangular(0,0.1,0.2))
            
            if accepted_price <= selling_price:
                size_demand = PRNG.poisson(avg_sale_size-1) + 1

                if size_demand <= stock_level:
                    stock_level -= size_demand
                    
                    # LOGISTIC GROWTH
                    avg_daily_arrivals += avg_daily_arrivals * growth * (max_arrivals - avg_daily_arrivals) / max_arrivals
                    avg_daily_arrivals = min(max_arrivals * 0.95, avg_daily_arrivals)

                    #INCREASE CAPITAL LEVEL
                    capital_level += selling_price * size_demand

                else:
                    # STOCK LOGISTIC DECAY
                    avg_daily_arrivals -= avg_daily_arrivals * decay_stock * (max_arrivals - avg_daily_arrivals) / max_arrivals
                    avg_daily_arrivals = max(min_arrivals, avg_daily_arrivals)
                    stock_floor = min(max_stock, stock_floor + size_demand)
                    stock_ceiling = min(max_stock, stock_ceiling + size_demand)
            
            else:
                # PRICE LOGISTIC DECAY 
                avg_daily_arrivals -= avg_daily_arrivals * decay_price * (max_arrivals - avg_daily_arrivals) / max_arrivals
                avg_daily_arrivals = max(min_arrivals, avg_daily_arrivals)            


            # UPDATE SELLING PRICE       
            selling_price,price_floor = set_selling_price(profit, avg_daily_arrivals, unit_cost, fixed_costs, avg_sale_size, price_ceiling)
            events['arrival'] = current_event_time + PRNG.exponential(1 / avg_daily_arrivals)
            
        # ORDER ARRIVAL EVENT
        elif current_event_type == 'order':
            stock_level += amount
            stock_level = min(max_stock, stock_level)
            events['order'] = np.inf 
    
        
        # SIMULATION END EVENT
        elif current_event_type == 'simulation_end':
            break
            
        elif current_event_type == 'month_close':
            # DECREASE CAPITAL LEVEL
            capital_level -= fixed_costs*12/365
            events['month_close'] = current_event_time + 1
            

        add_arrivals = current_event_type == 'arrival'
        add_orders = amount if current_event_type == 'order' else 0
        add_sales = size_demand if add_arrivals and size_demand <= stock_level else 0
        add_losses = size_demand if add_arrivals and size_demand > stock_level else 0

        data['clock'].append(current_event_time)
        data['capital'].append(capital_level)
        data['stock'].append(stock_level)
        data['stock_floor'].append(stock_floor)
        data['stock_ceiling'].append(stock_ceiling)
        data['price'].append(selling_price)
        data['price_floor'].append(price_floor)
        data['price_ceiling'].append(price_ceiling)
        data['arrivals'].append(add_arrivals)
        data['sales'].append(add_sales,)
        data['orders'].append(add_orders)
        data['losses'].append(add_losses)
        data['event'].append(current_event_type)

    df = df.append(pd.DataFrame(data), ignore_index=True)
    
    df['arrivals'] = df['arrivals'].cumsum()
    df['sales'] = df['sales'].cumsum()
    df['orders'] = df['orders'].cumsum()
    df['losses'] = df['losses'].cumsum()
    

    df['clock'] += np.abs(PRNG.normal(0, 0.001, size=len(df)))


    df.loc[len(df)] = df.loc[len(df)-1]
    df.loc[len(df)-1, 'clock'] = num_days
    df.loc[len(df)-1, 'event'] = 'END'
    
    df['timestamp'] = df['clock'].apply(lambda x: timedelta(days=x) + initial_date)
    
    return df