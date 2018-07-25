# 
# Author(s): Evan Smith, smithej@ornl.gov
#
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

class RdbHelper:
    def getConnection(self):
        # Connect to RDB
        prod = "(DESCRIPTION=(LOAD_BALANCE=OFF)(FAILOVER=ON)(ADDRESS=(PROTOCOL=TCP)(HOST=snsappa.sns.ornl.gov)(PORT=1610))(ADDRESS=(PROTOCOL=TCP)(HOST=snsappb.sns.ornl.gov)(PORT=1610))(CONNECT_DATA=(SERVICE_NAME=prod_controls)))"
        connection = cx_Oracle.connect("sns_reports", "sns", prod)
        
        return connection
