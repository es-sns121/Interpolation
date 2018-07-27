# 
# Author(s): Evan Smith, smithej@ornl.gov
#

from RdbHelper import RdbHelper
import ChannelHelper as ch

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
    pressure_in  = 'pressure_out_channel_name'
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

beam_power_channel = None
if Keys.beam_power in confs and confs[Keys.beam_power].strip():
    beam_power_channel = confs[Keys.beam_power]
    
# Channel ID that the mass flow rate values will be pulled from.
flow_rate_channel = confs[Keys.flow_rate]

# Channel IDs that the in and out temperature values will be pulled from.
temp_in_channel  = confs[Keys.temp_in]
temp_out_channel = confs[Keys.temp_out]

# Channel IDs that the in and out pressure values will be pulled from.
pressure_in_channel  = confs[Keys.pressure_in]
pressure_out_channel = confs[Keys.pressure_out]

# Connect to RDB
rdbHelper = RdbHelper()
conn = rdbHelper.getConnection()
channelHelper = ch.ChannelHelper(conn)

beam_power = None
if beam_power_channel is not None:
    beam_power = channelHelper.getChannelData(beam_power_channel)

mass_flow    = channelHelper.getChannelData(flow_rate_channel)
temp_in      = channelHelper.getChannelData(temp_in_channel)
temp_out     = channelHelper.getChannelData(temp_out_channel)
pressure_in  = channelHelper.getChannelData(pressure_in_channel)
pressure_out = channelHelper.getChannelData(pressure_out_channel)

if beam_power is None:
    times, data = channelHelper.align(mass_flow, temp_in, temp_out, pressure_in, pressure_out)
else:
    times, data = channelHelper.align(beam_power, mass_flow, temp_in, temp_out, pressure_in, pressure_out)
    
interp_beam_power = None

# Unpack the data tuple
if beam_power is None:
    interp_mass_flow, interp_temp_in, interp_temp_out, interp_pressure_in, interp_pressure_out = data
else:
    interp_beam_power, interp_mass_flow, interp_temp_in, interp_temp_out, interp_pressure_in, interp_pressure_out = data

print "{:>20} {:>20} {:>20} {:>20} {:>20}".format(flow_rate_channel, temp_in_channel, temp_out_channel, pressure_in_channel, pressure_out_channel)
for i in range(len(interp_mass_flow)):
    print "{:>20} {:>20} {:>20} {:>20} {:>20}".format(interp_mass_flow[i], interp_temp_in[i], interp_temp_out[i], interp_pressure_in[i], interp_pressure_out[i])



