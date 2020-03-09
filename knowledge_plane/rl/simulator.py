from random import randint
import signal
import cpu_usage as cpu
from subprocess import Popen, PIPE, call
import time
import sys
sys.path.insert(0, '/home/ryu/ryu/ryu/app/intelligentProbing/database/')
sys.path.insert(0, '/home/ryu/ryu/ryu/app/intelligentProbing/tools/')
import ConnectionBD_v2
from write_csv import *
from bytes_to import *
import os.path as path
#from write_csv import *
#import time
#import os.path as path

class Simulator(object):

	def __init__(self, env, size=None, frame_delay=1, update_delay=1.0):
		self.env = env
		self.size = size if size is not None else ((self.env.grid_size[0] + 1) * self.env.block_size, (self.env.grid_size[1] + 1) * self.env.block_size)
		self.width, self.height = self.size
		self.frame_delay = frame_delay

		self.start_time = None
		self.current_time = 0.0
		self.last_updated = 0.0
		self.update_delay = update_delay

		self.quit = False

		self.devname = "enp0s3"
		self.timestep = 1  # Seconds

		self.load_tx = 0.0
		self.load_rx = 0.0
		self.cpu_controller = 0.0
		self.probing_f = 3
		self.bandwith_channel = 1000

		self.count_iteration = 1
		self.csv_file = "/home/ryu/ryu/ryu/app/intelligentProbing/results/network_state.csv"
		self.csv_columns = ['row','load_tx','load_rx','cpu','frequency', 'reward']

		if (path.exists(self.csv_file)):
			os.remove(self.csv_file)

	def run(self, n_trials=1):
		for trial in xrange(n_trials):
			#print ("Simulator.run(): Trial {}".format(trial))
			self.env.reset()
			self.current_time = 0.0
			self.last_updated = 0.0
			self.start_time = time.time()
			while True:
				self.current_time = time.time() - self.start_time
				try:
					# Handle events
					signal.signal(signal.SIGINT, self.signal_handler)
					#signal.pause()

					# Update environment
					if self.current_time - self.last_updated >= self.update_delay:
						self.env.step()
						self.last_updated = self.current_time

					self.render()
					#time.sleep(randint(0,9))
					self.probing_f = ConnectionBD_v2.getProbingFrequency()
					print("PROBING_F ",self.probing_f)
					self.env.set_probing_frequency(self.probing_f)
					# run load and cpu module
					self.save_load_cpu()

					time.sleep(self.probing_f)#get probing frequency from DB

				except KeyboardInterrupt:
					break
				finally:
					if self.env.done:
						break
			if self.quit:
				break
	def render(self):
		print("Updated Probing Frequency")

	def signal_handler(self,sig, frame):
		print('The Agent was stopped!')
		sys.exit(0)

	def transmission_rate(self, dev, direction, timestep):
		path = "/sys/class/net/{}/statistics/{}_bytes".format(dev, direction)
		f = open(path, "r")
		bytes_before = int(f.read())
		f.close()
		time.sleep(timestep)
		f = open(path, "r")
		bytes_after = int(f.read())
		f.close()
		return (bytes_after - bytes_before) / timestep

	def cpu_usage(self):
		ryu_procces = "ps -ef | grep '/usr/bin/python /home/ryu/.local/bin/ryu-manager ryu/app/intelligentProbing/control_plane/intelligent_probing.py' | grep -v grep | awk '{print $2}'"
		#ryu_procces = "ps -ef | grep '/home/efcastillo/miniconda2/bin/python /home/efcastillo/miniconda2/bin/ryu-manager ryu/app/intelligentProbing/control_plane/intelligent_probing.py' | grep -v grep | awk '{print $2}'"
		ryu_pip = Popen(ryu_procces, shell=True, stdin=PIPE, stderr=PIPE, stdout=PIPE)
		cpu_usage = 0
		# proc = Popen(["ryu-manager", "/home/efcastillo/ryu/ryu/app/simple_switch_13.py"], shell=True, stdin=PIPE, stderr=PIPE,stdout=PIPE)
		output = ryu_pip.communicate()[0]
		print "ryu process with pid %s" % int(output)

		if output == 0:
			pass
		else:
			cpu_usage = cpu.main(output,5,1,0.5)

		return cpu_usage

	def save_load_cpu(self):
		self.load_tx = self.transmission_rate(self.devname, "tx", self.timestep)
		self.load_rx = self.transmission_rate(self.devname, "rx", self.timestep)
		self.cpu_controller = round(self.cpu_usage(),2)

		#CPU STATES
		cpu_state = "cpu_g"
		if self.inRange(self.cpu_controller,90,100):
			cpu_state = "cpu_error"
		elif self.inRange(self.cpu_controller, 80, 89):
			cpu_state = "cpu_a"
		elif self.inRange(self.cpu_controller, 70, 79):
			cpu_state = "cpu_b"
		elif self.inRange(self.cpu_controller, 60, 69):
			cpu_state = "cpu_c"
		elif self.inRange(self.cpu_controller, 50, 59):
			cpu_state = "cpu_d"
		elif self.inRange(self.cpu_controller, 40, 49):
			cpu_state = "cpu_e"
		elif self.inRange(self.cpu_controller, 30, 39):
			cpu_state = "cpu_f"

		#LOAD STATES
		load_state = "load_i"
		if self.inRange_load(self.load_rx+self.load_tx,75,80):
			load_state = "load_a"
		elif self.inRange_load(self.load_rx+self.load_tx,70,74):
			load_state = "load_b"
		elif self.inRange_load(self.load_rx+self.load_tx,65,69):
			load_state = "load_c"
		elif self.inRange_load(self.load_rx+self.load_tx,60,64):
			load_state = "load_d"
		elif self.inRange_load(self.load_rx+self.load_tx,55,59):
			load_state = "load_e"
		elif self.inRange_load(self.load_rx+self.load_tx,50,54):
			load_state = "load_f"
		elif self.inRange_load(self.load_rx+self.load_tx,45,49):
			load_state = "load_g"
		elif self.inRange_load(self.load_rx+self.load_tx,1,44):
			load_state = "load_h"
		else:
			load_state = "load_error"

		#current_network_state = {'load_tx':self.load_tx,'load_rx':self.load_rx,'cpu':self.cpu_controller,'frequency':self.probing_f}
		current_network_state = {'load':load_state,'cpu':cpu_state,'frequency':self.probing_f}
		self.env.set_current_network_state(current_network_state)

		current_value_network_state = {'load_tx':Bytes_to(self.load_tx),'load_rx':Bytes_to(self.load_rx),'cpu':self.cpu_controller,'frequency':self.probing_f}
		self.env.set_value_current_network_state(current_value_network_state)

		dict_data = [{'row':self.count_iteration,'load_tx':self.load_tx,'load_rx':self.load_rx,'cpu':self.cpu_controller,'frequency':self.probing_f,'reward':self.env.cumulative_reward}]
		#print(dict_data)
		WriteDictToCSV(self.csv_file, self.csv_columns, dict_data)
		self.count_iteration += 1
		ConnectionBD_v2.insertNetworkState(current_network_state)

	def inRange(self,x,lowerbound, upperbound):
	    if x >= lowerbound and x <= upperbound:
	        return True
	    else :
	        return False
	def speed_nic(self):
		#Mbits/s
		speed_nic = "cat /sys/class/net/enp0s3/speed"
		ryu_nic = Popen(speed_nic, shell=True, stdin=PIPE, stderr=PIPE, stdout=PIPE)
		return ryu_nic.communicate()[0]

	def inRange_load(self,x_bytes,lowerbound, upperbound):

		x = Bytes_to(x_bytes)
		speed = int(self.speed_nic()) * 2
		print("Bytes ",x_bytes," LOAD...", x, " NIC...", speed)

		if x >= (lowerbound * speed)/100 and x <= (upperbound * speed)/100:
			return True
		else:
			return False
