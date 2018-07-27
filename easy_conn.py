# 
# Author(s): Evan Smith, smithej@ornl.gov
#

import sys
from RdbHelper import RdbHelper
import ChannelHelper as ch
import PlotHelper as ph
# ---------------- #
#   Main routine   #
# ---------------- #

# Provides a central location for all non externalized strings.
class Keys:
    config_file  = 'connection.conf'
    beam_power   = 'beam_power_channel_name'
    flow_rate    = 'flow_rate_channel_name'
    temp_in      = 'temp_in_channel_name'
    temp_out     = 'temp_out_channel_name'
    pressure_in  = 'pressure_in_channel_name'
    pressure_out = 'pressure_out_channel_name'
    
# Read configuration file
confs = {}
with open(Keys.config_file) as config_file:
    for line in config_file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, value = line.split('=')
        confs[key] = value

channels = []
beam_power_channel = None
if Keys.beam_power in confs and confs[Keys.beam_power].strip():
    beam_power_channel = confs[Keys.beam_power]
    channels.append(beam_power_channel)

# Channel ID that the mass flow rate values will be pulled from.
flow_rate_channel = confs[Keys.flow_rate]
channels.append(flow_rate_channel)
# Channel IDs that the in and out temperature values will be pulled from.
temp_in_channel  = confs[Keys.temp_in]
channels.append(temp_in_channel)
temp_out_channel = confs[Keys.temp_out]
channels.append(temp_out_channel)
# Channel IDs that the in and out pressure values will be pulled from.
pressure_in_channel  = confs[Keys.pressure_in]
channels.append(pressure_in_channel)
pressure_out_channel = confs[Keys.pressure_out]
channels.append(pressure_out_channel)

# Connect to RDB
rdbHelper = RdbHelper()
conn = rdbHelper.getConnection()
channelHelper = ch.ChannelHelper(conn)

data = []
for channel in channels:
    data.append(channelHelper.getChannelData(channel))

# interpolated_data is a tuple containing five or six arrays depending on if beam power was used.
times, interpolated_data = channelHelper.align(*data)

if '-p' not in sys.argv:
    for channel in channels:
        if channel is not None and channel.strip():
            print '{:>25}'.format(channel),
    print
    for i in range(len(times)):
        for array in interpolated_data:
            if array is not None:
                print '{:>25}'.format(array[i]),
            else:
                print '{:>25}'.format('-'),
        print
else:
    for i in range(len(data)):
        if interpolated_data[i] is not None:
            ph.plot(data[i][:, 0], data[i][:, 1], times, interpolated_data[i], channels[i])
        else:
            print 'Channel {} not plotted.'.format(channels[i])



