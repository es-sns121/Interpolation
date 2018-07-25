# Connect to RDB and pull data from channel.

This package serves to facilitate pulling data from an RDB using a python client.
The data is then aligned chonologically and interpolated so that each channel that 
data is pulled from has the same amount of data points. Data is only interpolated
over channel overlaps.

## Install Oracle python client.

Install Oracle client by any of these, depending on python version:
    
    easy_install cx_Oracle
    pip install cx_Oracle
    python -m pip install cx_Oracle

Download the Oracle instant client binary from

    http://www.oracle.com/technetwork/database/database-technologies/instant-client/downloads/index.html

On Linux, unpack the instantclient-basiclite-linux.x64-12.2.0.1.0.zip
and add the resulting directory to LD_LIBRARY_PATH
    
## Install other python RDB client

Install your python RDB client of choice.


[MySQL](https://pypi.org/project/MySQL-python/) and [PostgreSQL](https://wiki.postgresql.org/wiki/Python) are good options...

## Setting up the program

The program only needs a single file to read input from...

### connection.conf

'connection.conf' is a connection configuration file. The file contains six fields:
    
    # Example channel
    # channel_id=RTBT_Diag:BCM25I:Power60

    # All fields except 'beam_power_channel_name' are required.
    # Beam power.
    beam_power_channel_name=
    
    # Mass flow rate
    flow_rate_channel_name=

    # Temperature in
    temp_in_channel_name=

    # Temperature out
    temp_out_channel_name=

    # Pressure in
    pressure_in_channel_name=

    # Pressure out
    pressure_out_channel_name=

The fields should have the respective PV names (channels) that data is to be pulled from.

### Running the script
    
    python easy_conn.py


