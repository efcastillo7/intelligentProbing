import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from collections import defaultdict
from os import scandir, getcwd
import os.path as path
import numpy as np
from numpy import *
import csv
def replace_all(text):
    dic = { "Type: OFPT": "OPENFLOW",
    		"MULTIPART_REPLY, ": "REPLY_",
    		"MULTIPART_REQUEST, ": "REQUEST_",
    		"[TCP Spurious Retransmission] ": "",
    		"[TCP ZeroWindow] ": "",
    		"[TCP segment of a reassembled PDU]": "",
    		"[TCP Window Full] ": ""
            }
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def csvRead(csv_file):
    data = defaultdict(list)
    dict_data = defaultdict(list)    

    if not path.exists(csv_file):
            print("The file does not exist")
            sys.exit()
    for i, row in enumerate(csv.reader(open(csv_file, 'rt', encoding='utf-8'))):
        if not i or not row:
            continue    
        _,_,_,_,_,Length,Info = row    
        data[Info].append(float(Length))
    
    num_msg_reply     = 0
    num_msg_packet_in = 0
    num_msg_flow_mod  = 0
    num_msg_packet_out= 0
    
    for packet_cod, levels in data.items():
        packet_cod_filter = replace_all(packet_cod)
        if packet_cod_filter.find("OPENFLOW") != -1:
        	#print (packet_cod_filter)
        	if packet_cod_filter.find("REPLY_OFPMP") != -1:
        		num_msg_reply += float(len(levels))
        		#print (levels)
        	elif packet_cod_filter.find("PACKET_IN") != -1:	            
	            num_msg_packet_in += float(len(levels))
	        elif packet_cod_filter.find("PACKET_OUT") != -1:
	            num_msg_packet_out += float(len(levels))
	        elif packet_cod_filter.find("FLOW_MOD") != -1:
	            num_msg_flow_mod += float(len(levels))  

    #print("PacketIn ", num_msg_packet_in, " FlowMod ",num_msg_flow_mod, " Packet_out ",num_msg_packet_out, " Reply ", num_msg_reply)    
    print("Reply ", num_msg_reply)
    """
    openflow_msg            = num_msg_overhead + num_msg_cost + num_msg_sdn + num_msg_error + num_msg_packet_in
    openflow_total_traffic  = overhead_traffic + cost_traffic + sdn_functions_traffic + error_traffic + packet_in_traffic

    overhead_traffic        = (overhead_traffic *100) / openflow_total_traffic
    cost_traffic            = (cost_traffic *100) / openflow_total_traffic
    sdn_functions_traffic   = (sdn_functions_traffic *100) / openflow_total_traffic
    error_traffic           = (error_traffic *100) / openflow_total_traffic
    packet_in_traffic       = (packet_in_traffic *100) / openflow_total_traffic

    num_msg_sdn      = (num_msg_sdn * 100) / openflow_msg
    num_msg_error    = (num_msg_error * 100) / openflow_msg
    num_msg_overhead = (num_msg_overhead * 100) / openflow_msg
    num_msg_cost     = (num_msg_cost * 100) / openflow_msg
    num_msg_packet_in= (num_msg_packet_in *100) / openflow_msg
    """

    
    return [num_msg_packet_in,           #0
            num_msg_packet_out,          #1
            num_msg_flow_mod,			 #2
            num_msg_reply]          	 #3

currentPath = getcwd()
print(currentPath)

#csv_file = currentPath + '/probing_'+ sys.argv[1] + 's/speed_' + sys.argv[1] + '.csv'
state_05 = csvRead(currentPath + '/pcap/probing_05s.csv')
state_1 = csvRead(currentPath + '/pcap/probing_1s.csv')
state_2 = csvRead(currentPath + '/pcap/probing_2s.csv')
state_3 = csvRead(currentPath + '/pcap/probing_3s.csv')
state_4 = csvRead(currentPath + '/pcap/probing_4s.csv')
state_5 = csvRead(currentPath + '/pcap/probing_5s.csv')
state_6 = csvRead(currentPath + '/pcap/probing_6s.csv')
state_7 = csvRead(currentPath + '/pcap/probing_7s.csv')
state_8 = csvRead(currentPath + '/pcap/probing_8s.csv')
state_9 = csvRead(currentPath + '/pcap/probing_9s.csv')
state_10 = csvRead(currentPath + '/pcap/probing_10s.csv')
state_11 = csvRead(currentPath + '/pcap/probing_11s.csv')
state_12 = csvRead(currentPath + '/pcap/probing_12s.csv')
state_13 = csvRead(currentPath + '/pcap/probing_13s.csv')
state_14 = csvRead(currentPath + '/pcap/probing_14s.csv')
state_15 = csvRead(currentPath + '/pcap/probing_15s.csv')

############################### Packet Number #########################################
green_data = [state_05[0], state_1[0], state_2[0], state_3[0], state_4[0], state_5[0], 
                state_6[0], state_7[0],state_8[0],state_9[0],state_10[0],state_11[0],
                state_12[0],state_13[0],state_14[0],state_15[0]]

blue_data =  [state_05[1], state_1[1], state_2[1], state_3[1], state_4[1], state_5[1], 
                state_6[1], state_7[1],state_8[1],state_9[1],state_10[1],state_11[1],
                state_12[1],state_13[1],state_14[1],state_15[1]]

red_data =   [state_05[2], state_1[2], state_2[2], state_3[2], state_4[2], state_5[2], 
                state_6[2], state_7[2],state_8[2],state_9[2],state_10[2],state_11[2],
                state_12[2],state_13[2],state_14[2],state_15[2]]

black_data = [state_05[3], state_1[3], state_2[3], state_3[3], state_4[3], state_5[3], 
                state_6[3], state_7[3],state_8[3],state_9[3],state_10[3],state_11[3],
                state_12[3],state_13[3],state_14[3],state_15[3]]

labels = ['0.5','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

legend = ['PacketIn', 'PacketOut', 'FlowMod', 'Reply']

# Setting the positions and width for the bars
pos = list(range(len(green_data)))
width = 0.15 # the width of a bar

# Plotting the bars
fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(10,5))
patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')
bar1=plt.bar(pos, green_data, width,
                 alpha=0.5,
                 color='w',
                 edgecolor='black',
                 hatch='xxx', # this one defines the fill pattern
                 label=labels[0])

plt.bar([p + width for p in pos], blue_data, width,
                 alpha=0.9,
                 color='w',
                 edgecolor='black',
                 hatch='OO',
                 label=labels[1])
    
plt.bar([p + width*2 for p in pos], red_data, width,
                 alpha=0.5,
                 color='w',
                 edgecolor='black',
                 hatch='**',
                 label=labels[2])

plt.bar([p + width*3 for p in pos], black_data, width,
                 alpha=0.5,
                 color='#d62728',
                 edgecolor='black',
                 hatch='...',
                 label=labels[3])            


# Setting axis labels and ticks
plt.sca(ax1)
ax1.set_ylabel('Control channel Messages (%)')
ax1.set_xlabel('(a) Monitoring Interval (s)')
#ax.set_title('Grouped bar plot')
ax1.set_xticks([p + 1.5 * width for p in pos])
ax1.set_xticklabels(labels)

# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*5)
plt.ylim([0., max(green_data)*1.2])
plt.legend(legend, bbox_to_anchor=(1, -0.1), loc="upper right", columnspacing=0.5, ncol=2)
plt.tight_layout()
plt.grid()
plt.show()