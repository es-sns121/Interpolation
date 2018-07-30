# Connect to RDB and pull data from channel.

This package serves to facilitate pulling data from an RDB using a python client.
The data is then aligned chonologically and interpolated so that each channel that 
data is pulled from has the same amount of data points. Data is only interpolated
over channel overlaps.

## Linux

### Install Pip

Install pip. [Here.](https://pip.pypa.io/en/stable/installing/)

### Install needed Python Modules.

Install SciPy

    python -m pip install -U scipy

Install MatplotLib

    python -m pip install -U matplotlib

Install the oracle python client.

    python -m pip install cx_Oracle

Download the Oracle instant client binary from

    http://www.oracle.com/technetwork/database/database-technologies/instant-client/downloads/index.html

On Linux, unpack the instantclient-basic-linux.x64-12.2.0.1.0.zip
and add the resulting directory to LD_LIBRARY_PATH

Install Pandas

    python -m pip install -U pandas
    
Install OpenPxl

    python -m pip install -U openpyxl

## Windows

### Install Python 2

Install the latest stable version of [Python 2](https://www.python.org/downloads/windows/)

Run the installer with admin privileges.

You need to add the Python executable and 'Scripts' directory to your Path enviornment variable.

The default install location for Python on Windows is

    C:\Python27

Add this to your path variable.

The Scipts directory in the Python install location should also be added.

    C:\Python27\Scripts
    
Add this to your path variable.

### Install Pip

Install Pip. [Here.](https://pip.pypa.io/en/stable/installing/)

The easiest way on windows is to run the get-pip.py script available at the above link.

### Install needed Python Modules.

Install SciPy

    python -m pip install -U scipy

Install MatplotLib

    python -m pip install -U matplotlib

Install the oracle python client.

    python -m pip install -U cx_Oracle

Download the Oracle instant client binary from

    http://www.oracle.com/technetwork/database/database-technologies/instant-client/downloads/index.html

On Windows, unzip the instantclient-basic-Windows.x64-12.2.0.1.0.zip
and add the resulting directory to your Path enviornment variable.

Install Pandas

    python -m pip install -U pandas
    
Install OpenPxl

    python -m pip install -U openpyxl

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

    cd Interpolation/src

To retrieve data:

    python easy_conn.py

For help:

    python easy_conn.py -help

To set sampling:

    python easy_conn.py -sample [avg/up/down]
    
To print debug info:

    python easy_conn.py -verbose

