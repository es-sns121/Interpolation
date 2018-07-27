# 
# Author(s): Evan Smith, smithej@ornl.gov
#

from time import strftime, gmtime
import sys
from RdbHelper import RdbHelper
import ChannelHelper as ch
import PlotHelper as ph
import ExportHelper as ex

# ---------------- #
#   Subroutine(s)  #
# ---------------- #

def help():
    print 'usage: python easy_conn.py [-h] [-sample (up/down/avg)] [-export (filename)] [-plot] [-print]'
    print '\toption "-help"       : Print this message'
    print '\toption "-verbose"    : Print debug information.'
    print '\toption "-sample"     : The default is to average the number of samples between the finest and coarsest data.'
    print '\t                     : Use "avg" for average, "up" to up sample to the finest level, or "down" to down sample to the coarsest level.'
    print '\toption "-export"     : Exports the data to an excel file.'
    print '\toption "-plot"       : Plot the interpolated data against the raw data.'
    print '\toption "-print"      : Print the interpolated data.'
    sys.exit(0)

# Convert an array of seconds since epoch to string timestamps.
def convertTimes(times):
    formattedTimes = []
    for time in times:
        formattedTime = strftime('%Y-%m-%d %H:%M:%S', gmtime(time))
        formattedTimes.append(formattedTime)
    return formattedTimes

# ---------------- #
#   Main routine   #
# ---------------- #

# Provides a central location for all non externalized key strings.
class Keys:
    config_file  = 'connection.conf'
    beam_power   = 'beam_power_channel_name'
    flow_rate    = 'flow_rate_channel_name'
    temp_in      = 'temp_in_channel_name'
    temp_out     = 'temp_out_channel_name'
    pressure_in  = 'pressure_in_channel_name'
    pressure_out = 'pressure_out_channel_name'

if '-help' in sys.argv:
    help()

verbose = False
if '-verbose' in sys.argv:
    verbose = True
    print 'Verbose set. Printing debug info.'

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

if verbose:
    print 'Read channel names as: ', channels

# Connect to RDB
rdbHelper = RdbHelper()
conn = rdbHelper.getConnection()
if verbose:
    print 'Server version: ', conn.version

sample = 'avg'
if '-sample' in sys.argv:
    index = sys.argv.index('-sample')
    sample = sys.argv[index + 1]
    if sample not in ('avg', 'up', 'down'):
        print 'Sample value must be either "avg", "up", or "down"'
        sys.exit(0)

if verbose:
    print 'Sample : ', sample

channelHelper = ch.ChannelHelper(conn, sample, verbose)

data = []
for channel in channels:
    data.append(channelHelper.getChannelData(channel))
    if verbose:
        print len(data[-1]), ' samples found for channel ', channel

# interpolated_data is a tuple containing five or six arrays depending on if beam power was used.
times, interpolated_data = channelHelper.align(*data)

# Print if given the command.
if '-print' in sys.argv:
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

# Plot if given the command.
if '-plot' in sys.argv:
    for i in range(len(data)):
        if interpolated_data[i] is not None:
            ph.plot(data[i][:, 0], data[i][:, 1], times, interpolated_data[i], channels[i])
        else:
            print 'Channel {} not plotted.'.format(channels[i])
            
# Export if given the command.
if '-export' in sys.argv:
    index = sys.argv.index('-export')
    filename = sys.argv[index + 1]
    print 'Exporting to file ', filename
    headers = ['Time']
    for channel in channels:
        headers.append(channel)
    converted_times = convertTimes(times)
    columns = [converted_times]
    for array in interpolated_data:
        columns.append(array)
    exporter = ex.Exporter(filename)
    exporter.export(headers, columns)
    
