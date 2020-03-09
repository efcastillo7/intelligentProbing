#http://librosweb.es/libro/python/capitulo_12/conectarse_a_la_base_de_datos_y_ejecutar_consultas.html
import sys
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import settings
from python_mysql_dbconfig import read_db_config

# def connect():
# 	try:
# 		db_config = read_db_config()
# 		conn = MySQLdb.connect(**db_config)
# 		if (conn):
# 			print ("Connection successful")
# 		else:
# 			print ("Error")
# 	except Exception as e:
# 		print(e)

class DB(object):

	def __init__(self):
		db_config = read_db_config()
		try:
			self.conn = MySQLdb.connect(**db_config)
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


# To insert a statistic reply event from switch in the DB
def insertSensorEvent(sensor):
	sql = DB()
	user ={}
	user['email']="666@python.org."
	user['password']="666"
	sql2 = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"

	sql.cursor.execute(sql2, (user['email'], user['password']))

	#sql.conn.commit()
	sql.close()