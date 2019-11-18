#http://librosweb.es/libro/python/capitulo_12/conectarse_a_la_base_de_datos_y_ejecutar_consultas.html
import sys
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
#from python_mysql_dbconfig import read_db_config

class DB(object):

	def __init__(self):
		#db_config = read_db_config()
		try:
			#self.conn = MySQLdb.connect(**db_config)
			self.conn = pymysql.connect(host='localhost',
                             user='root',
                             password='Swsh123$',
                             db='PruebaDB')
			self.cursor = self.conn.cursor()
			if (self.conn):

				print("DB init success")

			else:
				print("DB init fail")
		except Exception as e:

			print("DB init fail %s " % str(e))


	#@staticmethod
	def close(self):
		self.conn.close

def createTable():

    sql = DB()
    cursor = sql.cursor

    cursor.execute('''CREATE TABLE IF NOT EXISTS sensors (date real, address text, rssi integer,
        locationX real, locationY real, gatewayID text)''')

    sql.close()
    return True

def createTablePort():

	sql = DB()
	cursor = sql.cursor

	cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_stats_port (id_datapath text, port_number text, rx_packets text,
		rx_bytes text, rx_errors text, tx_packets text, tx_bytes text, tx_errors text)''')

	sql.close()

	return True

# To insert a statistic reply event from switch in the DB
def insertSensorEvent(sensor):
	sql = DB()
	user ={}
	user['email']="666@python.org."
	user['password']="666"
	sql2 = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"

	sql.cursor.execute(sql2, (user['email'], user['password']))

	sql.conn.commit()
	sql.close()

def insertStatPort(statPort):
	sql = DB()
	query = "INSERT INTO `tbl_stats_port` (`id_datapath`, `port_number`, `rx_packets`, `rx_bytes`, `rx_errors`, `tx_packets`, `tx_bytes`, `tx_errors`) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"

	sql.cursor.execute(query, (statPort['id_datapath'],statPort['port_number'],statPort['rx_packets'],
		statPort['rx_bytes'],statPort['rx_errors'],statPort['tx_packets'],statPort['tx_bytes'],statPort['tx_errors']))
	
	if statPort['port_number'] != 4294967294:
		sql.conn.commit()
	sql.close()