"""
Visualization Functions

This module provides all the functions to visualize data
"""

__version__ = "1.0"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from common import symmetric_simple_moving_average

plt.style.use("bmh")
plt.rcParams['figure.figsize'] = (16, 10 / 2)

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#-------------------------------------------------------------------------#


#--------------AGREGATE WITH PERIOD PLOT------------------#
def plot_aggregate_with_period(data_, period, title, min_=True, max_=True):
    
    resampled = data_.resample(period, closed="right")
    
    if min_ and max_:
        colors = ['darkred', 'darkcyan']
    else:
        colors = ['rebeccapurple'] * 2
    
    if min_:
        data = resampled.min()
        plt.step(data.index, data, color=colors[0], linestyle='--', label='Minimum')
    if max_:
        data = resampled.max()
        plt.step(data.index, data, color=colors[1], linestyle='--', label='Maximum')

    plt.xlabel('Days')
    plt.xlim(data_.index[0], data_.index[-1])
    
    plt.ylabel('Stock Level')
    
    plt.title(title)

    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()

#--------AGREGATE WITH PERIOD PLOT - MEAN/MEDIAN---------------#
def aggregate_with_period_low_high(data, low, high, period, title):
    
    resampled_data = data.resample(period, closed="right").mean()
    resampled_low = low.resample(period, closed="right").mean()
    resampled_high = high.resample(period, closed="right").mean()
    
    plt.step(resampled_data.index, resampled_data, color='rebeccapurple', linestyle='--', label='Middle')
    plt.step(resampled_data.index, resampled_low, color='darkred', linestyle='--', label='Low')
    plt.step(resampled_data.index, resampled_high, color='darkcyan', linestyle='--', label='High')
    
    plt.xlabel('Date')
    plt.xlim(resampled_data.index[0], resampled_data.index[-1])
    
    plt.ylabel('Stock Level')
    
    plt.title(title)

    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(f'visualization_pdfs/{title}.pdf')
    plt.show()

#--------------FLOW PLOT------------------#
def flow_plot(data, data_floor, data_ceiling, title, label_plot, label_floor, label_ceiling, label_y, with_floor, with_ceiling):
    
    plt.plot(data, label=label_plot, color='rebeccapurple',alpha=.7)

    #plt.plot(data.expanding().mean(), linestyle='--', color="olivedrab", label="Cum. Moving Avg")
    
    if with_floor:
        plt.step(data.index, data_floor, color="darkcyan", linestyle='--', label=label_floor)
        
    if with_ceiling:
        plt.step(data.index, data_ceiling, color="darkred", linestyle='--', label=label_ceiling)

    #plt.axhline(data.mean(), linestyle='--', color='darkgoldenrod', label=f'Mean: {data.mean():.2f}')

    plt.xlabel('Days')
    plt.xlim(data.index[0], data.index[-1])
    plt.xticks()

    plt.ylabel(label_y)

    plt.title(title)

    plt.legend(loc='upper left', ncol=3)
    plt.tight_layout()
    plt.savefig(f'visualization_pdfs/{title}.pdf')
    plt.show()

#--------------TIME SERIES PLOT------------------#
def plot_time_series(data_, period, column, min_=True, max_=False):
    if min_ and max_:
        raise Exception()
    
    if min_:
        data = data_.resample(period).min()
    else:
        data = data_.resample(period).max()

    daily_df = pd.DataFrame(data=np.diff(data, prepend=0), index=data.index, columns=[column])

    index = daily_df.index
    data = daily_df[column]

    plt.step(index, data, linewidth=1, color='rebeccapurple', label=column)
    plt.plot(index, symmetric_simple_moving_average(data, 30), label='Sym Simple Moving Avg',
             linestyle='--', linewidth=3, color='maroon')
    
    plt.plot(data.expanding().mean(), linestyle='--', linewidth=3, color="olivedrab", label="Cum. Moving Avg")
    
    plt.axhline(data.mean(), linestyle='--', linewidth=3, color='darkgoldenrod', label=f'Mean: {data.mean():.2f}')

    plt.xlabel('Days')
    plt.xlim(data_.index[0], data_.index[-1])
    
    plt.ylabel(column)
    
    plt.title(column)

    plt.legend()
    plt.tight_layout()
    plt.show()

#--------------TIME SERIES PLOT SHADOW------------------#
def plot_time_series_shadow(data, low, high, period, column, title):
    
    data = data.resample('D').mean()
    data_df = pd.DataFrame(np.diff(data, prepend=0), index=data.index, columns=[column])

    high = high.resample('D').mean()
    high_df = pd.DataFrame(np.diff(high, prepend=0), index=high.index, columns=[column])
    sym_high = symmetric_simple_moving_average(high_df[column],30)

    low = low.resample('D').mean()
    low_df = pd.DataFrame(np.diff(low, prepend=0), index=low.index, columns=[column])
    sym_low = symmetric_simple_moving_average(low_df[column],30)

    plt.plot(data_df[column], color='rebeccapurple')
    plt.fill_between(data_df.index, sym_low, sym_high, alpha=0.2, color='cyan')

    plt.xlabel('Days')
    plt.xlim(data_df.index[0], data_df.index[-1])
    
    plt.ylabel(column)
    
    plt.title(title)

    plt.tight_layout()
    plt.savefig(f'visualization_pdfs/{title}.pdf')
    plt.show()

#--------------SCATTER PLOT------------------#
def plot_scatter(data_, period, title, color, show=True):
    data = data_.resample(period).max()
    daily_losses_df = pd.DataFrame(data=np.diff(data, prepend=0), index=data.index, columns=['Daily Losses'])

    data = daily_losses_df['Daily Losses']
    data = data[data!=0].dropna()

    plt.scatter(data.index, data, marker='X', s=100, color=color)


    plt.xlabel('Days')
    
    plt.xlim(data_.index[0], data_.index[-1])
    
    plt.ylabel('Loss')
    
    plt.title(title)

    plt.tight_layout()
    if show:
        plt.show()

#--------------SHADOW PLOT------------------#
def shadow_plot(data,low,high,label_data,label_low_high,title,color):
    
    plt.plot(data, linestyle = "--", label=label_data, color=color)
    plt.fill_between(data.index, low, high, alpha=0.2, label=label_low_high, color=color)

    plt.title(title)
    plt.xlabel('Days')
    plt.ylabel('Capital ($)')
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.savefig(f'visualization_pdfs/{title}.pdf')