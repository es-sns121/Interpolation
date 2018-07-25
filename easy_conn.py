# 
# Author(s): Evan Smith, smithej@ornl.gov
#

from RdbHelper import RdbHelper
import ChannelHelper as ch

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

beam_power_channel = None
if 'beam_power_channel_name' in confs and confs['beam_power_channel_name'].strip():
    print 'beam power supplied', '"' + confs['beam_power_channel_name'] + '"'
    beam_power_channel = confs['beam_power_channel_name']
    
# Channel ID that the mass flow rate values will be pulled from.
flow_rate_channel = confs['flow_rate_channel_name']

# Channel IDs that the in and out temperature values will be pulled from.
temp_in_channel  = confs['temp_in_channel_name']
temp_out_channel = confs['temp_out_channel_name']

# Channel IDs that the in and out pressure values will be pulled from.
pressure_in_channel  = confs['pressure_in_channel_name']
pressure_out_channel = confs['pressure_out_channel_name']

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
    
interp_beam_power, interp_mass_flow, interp_temp_in, interp_temp_out, interp_pressure_in, interp_pressure_out = None, None, None, None, None, None

# Unpack the data tuple
if beam_power is None:
    interp_mass_flow, interp_temp_in, interp_temp_out, interp_pressure_in, interp_pressure_out = data
else:
    interp_beam_power, interp_mass_flow, interp_temp_in, interp_temp_out, interp_pressure_in, interp_pressure_out = data

# Plot to verify
if interp_beam_power is not None:
   channelHelper.plot(beam_power[:, 0],  beam_power[:, 1], times, interp_beam_power,   "Beam Power") 
channelHelper.plot(   mass_flow[:, 0],    mass_flow[:, 1], times, interp_mass_flow,    "Mass Flow")
channelHelper.plot(     temp_in[:, 0],      temp_in[:, 1], times, interp_temp_in,      "Temp In")
channelHelper.plot(    temp_out[:, 0],     temp_out[:, 1], times, interp_temp_out,     "Temp Out")
channelHelper.plot( pressure_in[:, 0],  pressure_in[:, 1], times, interp_pressure_in,  "Pressure In")
channelHelper.plot(pressure_out[:, 0], pressure_out[:, 1], times, interp_pressure_out, "Pressure Out")



