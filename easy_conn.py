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
from datetime import datetime, timedelta

prod = "(DESCRIPTION=(LOAD_BALANCE=OFF)(FAILOVER=ON)(ADDRESS=(PROTOCOL=TCP)(HOST=snsappa.sns.ornl.gov)(PORT=1610))(ADDRESS=(PROTOCOL=TCP)(HOST=snsappb.sns.ornl.gov)(PORT=1610))(CONNECT_DATA=(SERVICE_NAME=prod_controls)))"
conn = cx_Oracle.connect("sns_reports", "sns", prod)

print(conn.version)

# Get the last hour.
end = datetime.now()
start = end - timedelta(hours=1)

cursor = conn.cursor()
cursor.execute("""
    SELECT s.smpl_time AS Time, s.float_val AS Value, e.name AS Severity, m.name as Status
    FROM chan_arch.sample s
    JOIN chan_arch.channel c  ON c.channel_id = s.channel_id
    JOIN chan_arch.severity e ON e.severity_id = s.severity_id
    JOIN chan_arch.status m   ON m.status_id = s.status_id
    WHERE c.name = :1
    AND s.smpl_time BETWEEN :2 AND :3
    """,
    ( "RTBT_Diag:BCM25I:Power60", start, end ))
#   ( "RTBT_Diag:BCM25I:Power60", datetime(2018, 5, 21), datetime(2018, 5, 21, 1, 0, 0) ))
for time, value, sevr, stat in cursor:
    print(time, value, sevr, stat)



conn.close()
