"""
Interpolation

This module provides the Interpolation and Aggregation methods
"""

__version__ = "1.0"

from datetime import datetime, timedelta
import calendar

import stock_system
from stock_system import simulate, set_random_state

import common
from common import symmetric_simple_moving_average, calc_total_days

import numpy as np
import pandas as pd


def get_union_index(dfs):
    index_union = dfs[0].index
    for df in dfs[1:]:
        index_union = index_union.union(df.index)
    return pd.Series(index_union).drop_duplicates().reset_index(drop=True)


def interpolate(df, index, method='time'):
    aux = df.astype('float')
    aux = aux.reindex(index).fillna(method='ffill').fillna(method='bfill')
    return aux


def aggregate(parameters,replicates,columns=None):
    dfs = []
    seeds = list(range(40, 40 + replicates))
    for seed in seeds:
        set_random_state(seed)
        results = simulate(**parameters)
        results = results.set_index('timestamp')
        if columns is not None:
            dfs.append(results[columns])
        else:
            dfs.append(results)

    union_index = get_union_index(dfs)
    dfs_interpolates = [interpolate(df, union_index) for df in dfs]
    df_concat = pd.concat(dfs_interpolates)
    aggregated_df = df_concat.groupby(df_concat.index)

    return aggregated_df, dfs_interpolates


def aggregate_mean(parameters, replicates, columns):
    set_random_state(40)
    results = simulate(**parameters)
    results = results.set_index('timestamp')
    base_df = results.drop('event', axis=1)
    for index, seed in enumerate(range(41, 40 + replicates), start=1):
        set_random_state(seed)
        results = simulate(**parameters)
        results = results.set_index('timestamp')
        
        if columns is not None:
            results = results[columns]
        
        union_index = get_union_index([base_df, results])
        
        base_df = base_df.astype('float').reindex(union_index).fillna(method='ffill').fillna(method='bfill')
        results = results.astype('float').reindex(union_index).fillna(method='ffill').fillna(method='bfill')
        
        base_df = (results + index * base_df) / (index + 1)

    return base_df
