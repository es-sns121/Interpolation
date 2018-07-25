# 
# Author(s): Evan Smith, smithej@ornl.gov
#

import cx_Oracle

from datetime import datetime, timedelta
import numpy as np
from scipy import interpolate

import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import matplotlib.patches as mpatches
from matplotlib.dates import DateFormatter

class ChannelHelper:
    def __init__(self, connection):
        self.connection = connection
    
    def __del__(self):
        self.connection.close()
        
    def getChannelData(self, channel):
        """
        Retrieve the last hours worth of time, value pairs from the channel.
        
        Retrieve's the last hours worth of time, value pairs from the passed channel.
        The time value pairs are returned as a two column NumPy array where the first
        column is the time values, and the second column is the sample values.
        The time in each row correspons to the sample in the same row.
        
        Parameters
        ----------
        channel : String representing the channel name in the RDB
        
        Returns
        -------
        data : 2D NumPy array with time and sample values as the columns respectively.
        """
        
        # Get the last hour.
        end = datetime.now()
        start = end - timedelta(hours=1)

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT s.smpl_time AS Time, s.float_val AS Value
            FROM chan_arch.sample s
            JOIN chan_arch.channel c  ON c.channel_id = s.channel_id
            WHERE c.name = :1
            AND s.smpl_time BETWEEN :2 AND :3
            ORDER BY s.smpl_time
            """,
            ( channel, start, end ))
        data = []
        for time, value in cursor:
            # Append time in seconds since epoch and sample value. 
            # Add four hours to correct for difference with UTC.
            data.append( ( (time - datetime(1970, 1, 1) + timedelta(hours=4)).total_seconds(), value) )
        
        # Return as numpy array
        return np.asarray(data)

    def align(self, *time_value_arrays):
        """
        Aligns passed (time, value) array tuples on the same time scale and iterpolates the data so that each array has the same number of datapoints.
        
        All arrays will be aligned on the same time scale.
        All arrays will be interpolated using linear interpolation so that they are the same magnitude.
        Returns the same number of time value arrays as passed.
        
        Parameters
        ----------
        *time_value_arrays : a variadic input of time array and value array tuples.
            example: align((times1, data1), (times2, data2) ....)
        
        Returns
        -------
        (time, data) :  times array, data tuple
            - time is the times array that all of the new data arrays are aligned on.
            - data is a tuple containing all of the interpolated data arrays.
        """
        
        max_len = 0
        latest_start  = timedelta.min.total_seconds()
        earliest_stop = timedelta.max.total_seconds()
        
        for time_value_array in time_value_arrays:
            length = len(time_value_array)
            
            # Find the max length of the passed arrays to find out the maximum number of samples.
            if (length > max_len):
                max_len = length
              
            # We need to find the area where all of the arrays overlap in time.
            time_array  = time_value_array[:, 0]
            
            cur_start = time_array[0]  # Start time for the current array
            cur_stop  = time_array[-1] # Stop time for the current array
            
            if cur_start > latest_start:  # Find the latest start time in all of the passed arrays.
                latest_start = cur_start
            if cur_stop < earliest_stop:  # Find the earliest stop time in all of the passed arrays.
                earliest_stop = cur_stop

        
        # Generate a new time array that the new interpolated value arrays can all align on.
        # NumPy array of times in the interval [start, stop] with max_len number of evenly spaced samples.
        new_time = np.linspace(latest_start, 
                               earliest_stop, 
                               max_len) 
        
        new_value_arrays = []
        for time_value_array in time_value_arrays:
            
            time_array  = time_value_array[:, 0]
            value_array = time_value_array[:, 1]
            
            new_value_arrays.append( 
                                    # Interpolate a new value array with the new x axis as the new times. 
                                    np.interp( new_time, np.asarray(time_array), np.asarray(value_array)) 
                                   )       
        
        return (new_time, tuple(new_value_arrays))

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
