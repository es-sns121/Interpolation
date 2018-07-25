# Install Oracle client by any of these, depending on python version:
#  easy_install cx_Oracle
#  pip install cx_Oracle
#  python -m pip install cx_Oracle
#
# Download the Oracle instant client binary from
#  http://www.oracle.com/technetwork/database/database-technologies/instant-client/downloads/index.html
# On Linux, unpack the instantclient-basiclite-linux.x64-12.2.0.1.0.zip
# and add the resulting directory to LD_LIBRARY_PATH

import cx_Oracle
from datetime import datetime, timedelta
import numpy as np
from scipy import interpolate

# ------------------ #
#   Subroutine(s)    #
# ------------------ #

def getChannelData(channel):
# Connect to RDB
    prod = "(DESCRIPTION=(LOAD_BALANCE=OFF)(FAILOVER=ON)(ADDRESS=(PROTOCOL=TCP)(HOST=snsappa.sns.ornl.gov)(PORT=1610))(ADDRESS=(PROTOCOL=TCP)(HOST=snsappb.sns.ornl.gov)(PORT=1610))(CONNECT_DATA=(SERVICE_NAME=prod_controls)))"
    conn = cx_Oracle.connect("sns_reports", "sns", prod)

    # Get the last hour.
    end = datetime.now()
    start = end - timedelta(hours=1)

    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.smpl_time AS Time, s.float_val AS Value
        FROM chan_arch.sample s
        JOIN chan_arch.channel c  ON c.channel_id = s.channel_id
        WHERE c.name = :1
        AND s.smpl_time BETWEEN :2 AND :3
        """,
        ( channel_flow_rate, start, end ))
    data = []
    for time, value in cursor:
        # Append time in seconds since epoch and sample value. 
        # Add four hours to correct for difference with UTC.
        data.append( ( (time - datetime(1970, 1, 1) + timedelta(hours=4)).total_seconds(), value) )

    conn.close()
    
    # Return as numpy array
    return np.asarray(data)

'''
returns the same number of time value arrays as passed.
All arrays will be aligned on the same time scale
All arrays will be interpolated using linear interpolation so that they are the same magnitude.
'''
def align(*time_value_arrays):
    
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
    
    #print datetime.fromtimestamp(new_time[0])
    #print datetime.fromtimestamp(new_time[-1])

    for time_value_array in time_value_arrays:
        value_array = time_value_array[:, 1]
    
    return time_value_arrays

# ---------------- #
#   Main routine   #
# ---------------- #

# Read configuration file
confs = {}
with open("connection.conf") as config_file:
    for line in config_file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, value = line.split('=')
        confs[key] = value

# Channel ID that the mass flow rate will be pulled from.
channel_flow_rate = confs['channel_flow_rate']

# Channel IDs that the in and out temperature will be pulled from.
channel_temp_in  = confs['channel_temp_in']
channel_temp_out = confs['channel_temp_out']

# Channel IDs that the in and out pressure will be pulled from.
channel_pressure_in  = confs['channel_pressure_in']
channel_pressure_out = confs['channel_pressure_out']

mass_flow = getChannelData(channel_flow_rate)
temp_in  = getChannelData(channel_temp_in)
temp_out = getChannelData(channel_temp_out)
pressure_in  = getChannelData(channel_pressure_in)
pressure_out = getChannelData(channel_pressure_out)

mass_flow, temp_in, temp_out, pressure_in, pressure_out = align(mass_flow, temp_in, temp_out, pressure_in, pressure_out)


