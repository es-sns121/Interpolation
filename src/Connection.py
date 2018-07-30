# 
# Author(s): Evan Smith, smithej@ornl.gov
#

import sys
from time import strftime, gmtime
from RdbConnection import Rdb
from ImportExcel import Importer
from datetime import datetime
import ChannelData as ch
import ExportToExcel as ex
import PlotHelper as ph

# ---------------- #
#     Globals      #
# ---------------- #

date_input_format = '%d/%m/%Y'

# ---------------- #
#   Subroutine(s)  #
# ---------------- #

def help():
    print 'usage: python Connection.py start_date end_date [-help] [-sample (up/down/avg)] [-export (filename)] [-plot] [-print]'
    print '\tdate format is "day/month/year". Ex: 10/31/2000'
    print '\toption "-help"       : Print this message'
    print '\toption "-verbose"    : Print debug information.'
    print '\toption "-sample"     : The default is to average the number of samples between the finest and coarsest data.'
    print '\t                     : Use "avg" for average, "up" to up sample to the finest level, or "down" to down sample to the coarsest level.'
    sys.exit(0)

# ---------------- #
#   Main routine   #
# ---------------- #

if '-help' in sys.argv:
    help()

start_date = None
end_date   = None

if 3 > len(sys.argv):
    help()
else:
    start_date = datetime.strptime(sys.argv[1], date_input_format)
    end_date   = datetime.strptime(sys.argv[2], date_input_format)

if start_date >= end_date:
    print 'Start date "{}" cannot be after or equal to end date "{}".\n'.format(sys.argv[1], sys.argv[2])
    help()
    
print start_date
print end_date

verbose = False
if '-verbose' in sys.argv:
    verbose = True
    print 'Verbose set. Printing debug info.'

channels = []
with open('../config/connection.conf') as channel_config_file:
    for line in channel_config_file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, value = line.split('=')
        value = value.strip()
        if value and value is not None:
            channels.append(value)

table_files = []
with open('../config/tables.conf') as table_config_file:
    for line in table_config_file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, value = line.split('=')
        value = value.strip()
        if value and value is not None:
            table_files.append(value)

if verbose:
    print 'Read channel names as: ', channels

rdb = Rdb()
conn = rdb.getConnection()

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

channelHelper = ch.ChannelHelper(conn, sample, verbose,)

unaligned_data = []
for channel in channels:
    unaligned_data.append(channelHelper.getChannelData(channel, start=start_date, end=end_date))
    if verbose:
        print len(unaligned_data[-1]), ' samples found for channel ', channel

aligned_data = channelHelper.alignChannelData(*unaligned_data)

data = {}

data['Time'] = aligned_data[0]
for i in range(0, len(channels)):
    data[channels[i]] = aligned_data[i + 1]

interpolationFunctions = []
importer = Importer()
for table_file in table_files:
    importer.readFile(table_file)
    interpolationFunctions.append(importer.get2dInterpolationFunction())

# 'data' now contains a map of data arrays keyed on their respective channel names.
# 'interpolationFunctions' now contains a list of 2D interpolation functions. Their order is the same as in the tables.conf file.

# EXAMPLE
# heEnthalpyFunction = interpolationFunctions[0]
# he_enthalpy_value = heEnthalpyFunction(he_pressure_value, he_temperature_value)
