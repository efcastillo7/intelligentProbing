#!/usr/bin/python
#Autor: Jose Leonardo Henao Ramirez
#Crear carpeta Codigo (mkdir Codigo)
from mininet.net import Mininet
import sys, os, time
for elements in sys.argv:
	#numero de registros top a generar recibidos por consola
	num_regs=int(sys.argv[1])
	#tiempo de retraso entre cada registro top a generar recibidos por consola
	delay=int(sys.argv[2])
net = Mininet()
times = (num_regs*delay)
print "-----------------------------------------------------------------"
print "PRUEBA DE RECURSOS DEL SISTEMA CORRIENDO MININET PYTHON LATENCIA"
print "Resultado disponible en Codigo/test4_res2_systconapiping.txt"
print "-----------------------------------------------------------------"
#print 'Agregando Controller'
net.addController('c0')
#print "Agregando hosts"
net.addHost("h0")
net.addHost("h1")
#print "Agregando Switch"
net.addSwitch("s1")
#print "Agregando enlaces entre hosts y sw"
net.addLink("h0","s1")
net.addLink("h1","s1")
#print 'Iniciando red'
net.start()
fo = open("test4_res2_systconapiping.txt", "w")
while times > 0:
	if times%30==0:
		fo.write("PING "+str(times)+" segundos\n")
		fo.write(str(net.pingFull())+"\n\n")
print "Tiempo restante: "+str(times)+" segundos"
time.sleep(1)
times=times-1
fo.close()
net.stop()
print "Proceso en Python finalizado"