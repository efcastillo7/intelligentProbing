#http://librosweb.es/libro/python/capitulo_12/conectarse_a_la_base_de_datos_y_ejecutar_consultas.html
import sys
import os
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

class DB(object):

	def __init__(self):
		#db_config = read_db_config()
		try:
			#self.conn = MySQLdb.connect(**db_config)
			self.conn = pymysql.connect(host='localhost',
                             user='ipro',
                             password='ryu',
                             db='ipro')
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

def createTableFlow():

	sql = DB()
	cursor = sql.cursor

	cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_stats_flow (id_datapath text, in_port text, eth_dst text,
		out_port text, packets text, bytes text, idle_timeout text, hard_timeout text, duration_sec text)''')

	sql.close()

	return True

def createTableAggregateFlow():

	sql = DB()
	cursor = sql.cursor

	cursor.execute('''CREATE TABLE IF NOT EXISTS tbl_stats_aggregate_flow (byte_count text, flow_count text, packet_count text)''')

	sql.close()

	return True	

def insertStatPort(statPort):
	sql = DB()
	query = "INSERT INTO `tbl_stats_port` (`id_datapath`, `port_number`, `rx_packets`, `rx_bytes`, `rx_errors`, `tx_packets`, `tx_bytes`, `tx_errors`) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"

	sql.cursor.execute(query, (statPort['id_datapath'],statPort['port_number'],statPort['rx_packets'],
		statPort['rx_bytes'],statPort['rx_errors'],statPort['tx_packets'],statPort['tx_bytes'],statPort['tx_errors']))
	
	if statPort['port_number'] != 4294967294:
		sql.conn.commit()
	sql.close()

def insertStatFlow(statFlow):
	sql = DB()
	query = "INSERT INTO `tbl_stats_flow` (`id_datapath`, `in_port`, `eth_dst`, `out_port`, `packets`, `bytes`, `idle_timeout`, `hard_timeout`, `duration_sec`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"

	sql.cursor.execute(query, (statFlow['id_datapath'],statFlow['in_port'],statFlow['eth_dst'],
		statFlow['out_port'],statFlow['packets'],statFlow['bytes'],statFlow['idle_timeout'],statFlow['hard_timeout'],statFlow['duration_sec']))
	
	sql.conn.commit()
	sql.close()

def insertStatAggregateFlow(statFlow):
	sql = DB()
	query = "INSERT INTO `tbl_stats_aggregate_flow` (`byte_count`, `flow_count`, `packet_count`) VALUES (%s,%s,%s)"

	sql.cursor.execute(query, (statFlow['byte_count'],statFlow['flow_count'],statFlow['packet_count']))
	
	sql.conn.commit()
	sql.close()	

def getProbingFrequency():
	sql = DB()
	query = "SELECT * FROM monitoring_interval ORDER by ID DESC LIMIT 1"
	sql.cursor.execute(query)	
	data = sql.cursor.fetchone()
	
	sql.close()
	return data[1]

def clean_table_cpu():
	sql = DB()
	query1 = "SELECT * FROM tbl_cpu"
	sql.cursor.execute(query1)
	registers = sql.cursor.rowcount

	if registers > 5:
		query = "DELETE FROM tbl_cpu WHERE insert_at < NOW() ORDER BY id LIMIT 1"
		sql.cursor.execute(query)
	sql.conn.commit()
	sql.close()

def insertStatcpu(statcpu):
	sql = DB()
	query = "INSERT INTO `tbl_cpu` (`time_`, `cpu`, `real_mb`, `virtual_mb`) VALUES (%s,%s,%s,%s)"

	sql.cursor.execute(query, (statcpu['times'],statcpu['cpu'],statcpu['real_mb'],statcpu['virtual_mb']))
	
	sql.conn.commit()
	sql.close()

def updateProbingFrequency(probing_f):
	sql = DB()
	query = "UPDATE `monitoring_interval` SET `interval_time`= %s, `aux` = %s WHERE `id` = 12"

	sql.cursor.execute(query, (probing_f,probing_f))
	
	sql.conn.commit()
	sql.close()

def insertNetworkState(net_stat):
	sql = DB()
	query = "INSERT INTO `tbl_network_state` (`load`, `cpu`, `frequency`) VALUES (%s,%s,%s)"

	sql.cursor.execute(query, (net_stat['load'],net_stat['cpu'],net_stat['frequency']))
	
	sql.conn.commit()
	sql.close()	