import sys
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/database/')
import ConnectionBD_v2

ConnectionBD_v2.clean_table_cpu()

