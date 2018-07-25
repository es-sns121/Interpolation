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

# Channel ID that the mass flow rate values will be pulled from.
channel_flow_rate = confs['channel_flow_rate']

# Channel IDs that the in and out temperature values will be pulled from.
channel_temp_in  = confs['channel_temp_in']
channel_temp_out = confs['channel_temp_out']

# Channel IDs that the in and out pressure values will be pulled from.
channel_pressure_in  = confs['channel_pressure_in']
channel_pressure_out = confs['channel_pressure_out']

# Connect to RDB
rdbHelper = RdbHelper()
conn = rdbHelper.getConnection()
channelHelper = ch.ChannelHelper(conn)

mass_flow    = channelHelper.getChannelData(channel_flow_rate)
temp_in      = channelHelper.getChannelData(channel_temp_in)
temp_out     = channelHelper.getChannelData(channel_temp_out)
pressure_in  = channelHelper.getChannelData(channel_pressure_in)
pressure_out = channelHelper.getChannelData(channel_pressure_out)

times, data = channelHelper.align(mass_flow, temp_in, temp_out, pressure_in, pressure_out)
# Unpack the data tuple
interp_mass_flow, interp_temp_in, interp_temp_out, interp_pressure_in, interp_pressure_out = data

# Plot to verify
channelHelper.plot(   mass_flow[:, 0],    mass_flow[:, 1], times, interp_mass_flow,    "Mass Flow")
channelHelper.plot(     temp_in[:, 0],      temp_in[:, 1], times, interp_temp_in,      "Temp In")
channelHelper.plot(    temp_out[:, 0],     temp_out[:, 1], times, interp_temp_out,     "Temp Out")
channelHelper.plot( pressure_in[:, 0],  pressure_in[:, 1], times, interp_pressure_in,  "Pressure In")
channelHelper.plot(pressure_out[:, 0], pressure_out[:, 1], times, interp_pressure_out, "Pressure Out")
