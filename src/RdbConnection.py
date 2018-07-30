# 
# Author(s): Evan Smith, smithej@ornl.gov
#

import cx_Oracle

class Rdb:
    def getConnection(self):
        # Connect to RDB
        prod = "(DESCRIPTION=(LOAD_BALANCE=OFF)(FAILOVER=ON)(ADDRESS=(PROTOCOL=TCP)(HOST=snsappa.sns.ornl.gov)(PORT=1610))(ADDRESS=(PROTOCOL=TCP)(HOST=snsappb.sns.ornl.gov)(PORT=1610))(CONNECT_DATA=(SERVICE_NAME=prod_controls)))"
        connection = cx_Oracle.connect("sns_reports", "sns", prod)
        
        return connection
