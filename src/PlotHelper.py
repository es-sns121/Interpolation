# 
# Author(s): Evan Smith, smithej@ornl.gov
#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.patches as mpatches
from matplotlib.dates import DateFormatter

def plotRawVersusInterpolated(oldtimes, oldvalues, newtimes, newvalues, title):
        """
        Plot a comparison of raw values and times versus interpolated values and times.
        
        Plots raw values and times with a red line.
        Plots interpolated values and times with blue crosses.
        
        Parameters
        ----------
            oldtimes  : NumPy array of times (seconds since epoch)
            oldvalues : NumPy array of values
            newtimes  : NumPy array of times (seconds since epoch)
            newvalues : NumPy array of interpolated values
            tite : String, the plot title.
        """
        # Date format is "year:month:day hour:minute:second"
        formatter = DateFormatter("%y:%m:%d %H:%M:%S")
        fig, ax = plt.subplots()
        ax.plot(mdate.epoch2num(np.asarray(oldtimes)), np.asarray(oldvalues), 'r-', mdate.epoch2num(newtimes), newvalues, 'b*')
        ax.xaxis.set_major_formatter(formatter)
        plt.title(title)
        fig.canvas.set_window_title(title)

        # Create the plot legend
        red_patch  = mpatches.Patch(color='red' , label='Raw Data')
        blue_patch = mpatches.Patch(color='blue', label='Interpolated Data')
        plt.legend(handles=[red_patch, blue_patch])
        
        plt.show()

def plotTraceWithTimeAsX(x_values, y_values, title, ylabel, trace='r-'):
        # Date format is "year:month:day hour:minute:second"
        formatter = DateFormatter("%m/%d/%Y")
        fig, ax = plt.subplots()
        plt.plot(mdate.epoch2num(np.asarray(x_values)), np.asarray(y_values), trace)
        ax.xaxis.set_major_formatter(formatter)
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Time")
        
        plt.title(title)
        fig.canvas.set_window_title(title)
        plt.show()
