#http://librosweb.es/libro/python/capitulo_12/conectarse_a_la_base_de_datos_y_ejecutar_consultas.html
import sys
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import settings
#import mysql.connector
#coding=utf-8
 


def run_query(query=''): 
	datos = [settings.DB_HOST, settings.DB_USER, settings.DB_PASS, settings.DB_NAME] 
	 
	conn = MySQLdb.connect(*datos) # Conectar a la base de datos 
	cursor = conn.cursor()         # Crear un cursor 
	cursor.execute(query)          # Ejecutar una consulta 
	 
	if query.upper().startswith('SELECT'): 
	    data = cursor.fetchall()   # Traer los resultados de un select 
	else: 
	    conn.commit()              # Hacer efectiva la escritura de datos 
	    data = None 
	 
	cursor.close()                 # Cerrar el cursor 
	conn.close()                   # Cerrar la conexión 
	 
	return data

dato = input("Dato: ")
query = "INSERT INTO tbl_prueba (valor_campo) VALUES ('%s')" % dato
run_query(query)