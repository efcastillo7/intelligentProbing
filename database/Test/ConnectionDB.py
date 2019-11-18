#http://librosweb.es/libro/python/capitulo_12/conectarse_a_la_base_de_datos_y_ejecutar_consultas.html
import sys
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import settings

class opendb():
	"""docstring for opendb"""
	def __init__(self):
		datos = [settings.DB_HOST, settings.DB_USER, settings.DB_PASS, settings.DB_NAME,settings.CHARSET,settings.CURSORCLASS]	 
		self.connection = MySQLdb.connect(*datos) # Conectar a la base de datos 
		self.cursor = self.connection.cursor()         # Crear un cursor 
	
	@staticmethod
	def close(self):
		self.connection.close	

def createTable():

    sql = opendb()
    cursor = sql.cursor

    cursor.execute('''CREATE TABLE IF NOT EXISTS sensors (date real, address text, rssi integer,
        locationX real, locationY real, gatewayID text)''')

    sql.close()
    return True

# To insert a statistic reply event from switch in the DB
def insertSensorEvent(sensor):
	sql = opendb()
	
    try:
    	with sql.cursor() as cursor:
	        # Create a new record
	        user ={}
	        user['email']="dos@python.org."
	        user['password']="123456"
	        sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
	        cursor.execute(sql, (user['email'], user['password']))

	    # connection is not autocommit by default. So you must commit to save
	    # your changes.
	    sql.connection.commit()    
	finally:
    	sql.close()