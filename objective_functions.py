"""
Objective Functions

This module returns the different objective functions for the Optimization process

"""

__version__ = "1.0"

import numpy as np
from stock_system import simulate

########### Objective Function - Profit without losses ###########
def objective_function_pnl(trial, parameters):

    parameters["control_frequency"] = trial.suggest_int('control_frequency', 1, 30)
    parameters["initial_stock_level"] = trial.suggest_int('initial_stock_level', 0, 3000)
    parameters["stock_floor"] =  trial.suggest_int('stock_floor', 0, 3000)
    parameters["stock_ceiling"] =  trial.suggest_int('stock_ceiling', 0, 3000)
    
    replicates = 5
    end_capitals = []
    always_positive = True
    
    try:
        for _ in range(replicates):
            results = simulate(**parameters)
            end_capitals.append(results['capital'].iloc[-1])
            always_positive &= np.all(results['capital'] >= 0)
            if not always_positive:
                return 0
    except KeyboardInterrupt:
        raise
    except:
        return np.nan
      
    end_capital = np.mean(end_capitals)
    
    return end_capital - parameters["initial_investment"] #



########### Objective Function - Profit with losses ###########
def objective_function_pl(trial, parameters):

    parameters["control_frequency"] = trial.suggest_int('control_frequency', 1, 30)
    parameters["initial_stock_level"] = trial.suggest_int('initial_stock_level', 0, 3000)
    parameters["stock_floor"] =  trial.suggest_int('stock_floor', 0, 3000)
    parameters["stock_ceiling"] =  trial.suggest_int('stock_ceiling', 0, 3000)
    
    replicates = 5
    end_capitals = []
    
    try:
        for _ in range(replicates):
            results = simulate(**parameters)
            end_capitals.append(results['capital'].iloc[-1])
    except KeyboardInterrupt:
        raise
    except:
        return np.nan

    end_capital = np.mean(end_capitals)
    
    return end_capital - parameters["initial_investment"]



########### Objective Function - Even ###########
def objective_function_e(trial, parameters):

    parameters["control_frequency"] = trial.suggest_int('control_frequency', 1, 30)
    parameters["initial_stock_level"] = trial.suggest_int('initial_stock_level', 0, 3000)
    parameters["stock_floor"] =  trial.suggest_int('stock_floor', 0, 3000)
    parameters["stock_ceiling"] =  trial.suggest_int('stock_ceiling', 0, 3000)
    
    replicates = 5
    mean_capital = []
    
    try:
        for _ in range(replicates):
            results = simulate(**parameters)
            mean_capital.append(results['capital'].mean())
    except KeyboardInterrupt:
        raise
    except:
        return np.nan

    
    return np.abs(np.mean(mean_capital) - parameters["initial_investment"])



########### Objective Function - Loss ###########
def objective_function_l(trial, parameters):

    parameters["control_frequency"] = trial.suggest_int('control_frequency', 1, 30)
    parameters["initial_stock_level"] = trial.suggest_int('initial_stock_level', 0, 3000)
    parameters["stock_floor"] =  trial.suggest_int('stock_floor', 0, 3000)
    parameters["stock_ceiling"] =  trial.suggest_int('stock_ceiling', 0, 3000)
    
    replicates = 5
    end_capitals = []
    
    try:
        for _ in range(replicates):
            results = simulate(**parameters)
            end_capitals.append(results['capital'].iloc[-1])
    except KeyboardInterrupt:
        raise
    except:
        return np.nan 
        
    end_capital = np.mean(end_capitals)
    
    return end_capital - parameters["initial_investment"]