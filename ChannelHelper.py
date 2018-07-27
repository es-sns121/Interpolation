# 
# Author(s): Evan Smith, smithej@ornl.gov
#

import cx_Oracle
import sys
from datetime import datetime, timedelta
import numpy as np
from scipy import interpolate


class ChannelHelper:
    def __init__(self, connection, sample='avg', verbose=False):
        self.connection = connection
        self.sample = sample
        self.verbose = verbose
        
    def __del__(self):
        self.connection.close()
        
    def getChannelData(self, channel, hours=1, start=None, end=None):
        """
        Retrieve the last hours worth of time, value pairs from the channel.
        
        Retrieves the last hours worth of time, value pairs from the passed channel.
        The time value pairs are returned as a two column NumPy array where the first
        column is the time values, and the second column is the sample values.
        The time in each row corresponds to the sample in the same row.
        
        Parameters
        ----------
        channel : String representing the channel name in the RDB
        
        Returns
        -------
        data : 2D NumPy array with time and sample values as the columns respectively.
        """
        
        # Get the last hour.
        if end is None:
            end = datetime.now()
        if start is None:
            start = end - timedelta(hours=hours)

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT s.smpl_time, s.float_val
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
            data.append( ( (time - datetime(1970, 1, 1)).total_seconds(), value) )
        
        return np.asarray(data)

    def align(self, *time_value_arrays):
        """
        Aligns passed (time, value) array tuples on the same time scale and interpolates the data so that each array has the same number of data points.
        
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
        
        # Initialize the sample_len.
        if self.sample in ('avg', 'up'):
            sample_len = 0
        else:
            sample_len = sys.maxint
        
        # If average, collect all lengths to calculate a mean.
        sample_lengths = []
        
        latest_start  = timedelta.min.total_seconds()
        earliest_stop = timedelta.max.total_seconds()
        
        for time_value_array in time_value_arrays:
            if len(time_value_array) == 0 or len(time_value_array[0]) == 0:
                continue
            
            length = len(time_value_array)
            
            if self.sample == 'up':
                # Find the max length of the passed arrays to find out the maximum number of samples.
                if (length > sample_len):
                    sample_len = length
            elif self.sample == 'down':
                if (length < sample_len):
                    sample_len = length
            elif self.sample == 'avg':
                sample_lengths.append(length)
            
            # We need to find the area where all of the arrays overlap in time.
            time_array  = time_value_array[:, 0]
            
            cur_start = time_array[0]  # Start time for the current array
            cur_stop  = time_array[-1] # Stop time for the current array
            
            if cur_start > latest_start:  # Find the latest start time in all of the passed arrays.
                latest_start = cur_start
            if cur_stop < earliest_stop:  # Find the earliest stop time in all of the passed arrays.
                earliest_stop = cur_stop
                
        if self.sample == 'avg':
            sample_len = int(np.mean(sample_lengths))
        
        if self.verbose:
            print 'Number of samples in interpolated data: ', sample_len
                      
        # Generate a new time array that the new interpolated value arrays can all align on.
        # NumPy array of times in the interval [start, stop] with max_len number of evenly spaced samples.
        new_times = np.linspace(latest_start, earliest_stop, sample_len) 
        
        new_value_arrays = []
        for time_value_array in time_value_arrays:
            
            if len(time_value_array) == 0 or len(time_value_array[0]) == 0:
                new_value_arrays.append(None)
                continue
            
            time_array  = time_value_array[:, 0]
            value_array = time_value_array[:, 1]
            
            
            new_value_arrays.append( 
                                    # Interpolate a new value array with the new x axis as the new times.
                                    np.interp( new_times, time_array, value_array ) 
                                   )       
        
        return (new_times, tuple(new_value_arrays))

    
