#sudo pip install PyMySQL  

import sys
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/database/')
import ConnectionBD_v2

#ConnectionBD_v2.createTablePort()
#ConnectionBD_v2.createTableFlow()
#ConnectionBD_v2.createTableAggregateFlow()
#probing = ConnectionBD_v2.getProbingFrequency()

#print(probing)