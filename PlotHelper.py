# 
# Author(s): Evan Smith, smithej@ornl.gov
#

import platform
import sys

# Tkl/Tk isn't supported on windows so don't try to import matplotlib.
if platform.system() == 'Windows':
    print 'import PlotHelper ...'
    print 'Matplotlib relies on Tkl/Tk graphical library which is not supported on windows.'
    print 'It is suggested you remove this import and please consider other alternatives.'
    sys.exit(0)

import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.patches as mpatches
from matplotlib.dates import DateFormatter

def plot(self, oldtimes, oldvalues, newtimes, newvalues, title):
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
