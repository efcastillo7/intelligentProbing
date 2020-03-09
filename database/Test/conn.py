#http://librosweb.es/libro/python/capitulo_12/conectarse_a_la_base_de_datos_y_ejecutar_consultas.html
import sys
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import settings

def connect():
    datos = [settings.DB_HOST, settings.DB_USER, settings.DB_PASS, settings.DB_NAME]    

    try:
        conn = MySQLdb.connect(*datos)
        print('Connected to MySQL database')
 
    except TypeError as e:
        print(e)
 
    finally:
        conn.close()


if __name__ == '__main__':
    connect()