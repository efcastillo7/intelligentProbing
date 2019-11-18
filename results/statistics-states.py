import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
from collections import defaultdict
from os import scandir, getcwd
from pathlib import Path
import os.path as path
import numpy as np
from numpy import *
import csv
def replace_all(text):
    dic = { "Type: ": "", 
            "OFPT_MULTIPART_REQUEST, OFPMP_": "REQUEST_",
            "OFPT_MULTIPART_REPLY, OFPMP_": "REPLY_",
            "OFPT_PACKET_IN": "PACKET_IN",
            "OFPT_PACKET_OUT": "PACKET_OUT",
            "OFPT_FLOW_MOD": "FLOW_MOD",
            "OFPT_HELLO": "HELLO",
            "OFPT_FEATURES_REQUEST": "FEATURES_REQUEST",
            "[TCP ZeroWindow] ": "ZERO_WINDOW_",
            "[TCP Window Full] ": "WINDOW_FULL_",
            "[TCP segment of a reassembled PDU]":"",
            "[TCP Spurious Retransmission] ": "SPURIOUS_",
            "[TCP Window Update] 6653": "TCP_FLAGS_C_S",
            "6653 [PSH, ACK]": "TCP_FLAGS_S_C"
            #"OFPMP_":""
            }
    for i, j in dic.items():
        text = text.replace(i, j)
    return text.replace("PACKET_INPACKET_IN","PACKET_IN").replace("REPLY_PORT_STATSREPLY_AGGREGATE","REPLY_PORT_AGGREGATE")

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
    
    total_traffic     = 0
    num_msg_traffic   = i
    overhead_traffic  = 0
    sdn_functions_traffic     = 0
    error_traffic     = 0
    num_msg_overhead  = 0
    num_msg_cost      = 0
    num_msg_sdn       = 0  
    cost_traffic      = 0
    list_msg_overhead = ["REQUEST_FLOW","REQUEST_PORT_STATS", "REQUEST_AGGREGATE"]
    list_msg_cost     = ["REPLY_PORT_AGGREGATE","REPLY_FLOW"]
    list_msg_sdn      = ["PACKET_OUT", "FLOW_MOD","REQUEST_PORT_DESC","OFPT_PORT_STATUS"]

    num_msg_error     = 0
    num_msg_packet_in = 0
    packet_in_traffic = 0

    #print("Items ", data.items())
    for packet_cod, levels in data.items():
        packet_cod_filter = replace_all(packet_cod)
        #print(packet_cod_filter)
        #total_traffic += sum(levels)
        if packet_cod_filter in list_msg_overhead:
            overhead_traffic += float(sum(levels))
            num_msg_overhead += float(len(levels))
            dict_data[packet_cod_filter].append(float(sum(levels)))
        elif packet_cod_filter in list_msg_cost or packet_cod_filter.find("Type: OFPT_MULTIPART_REPLY, OFPMP_PORT_STATSType: OFPT_MULTIPART_REPLY, OFPMP_AGGREGATE") != -1:
            cost_traffic += float(sum(levels))
            num_msg_cost += float(len(levels))
        elif packet_cod_filter in list_msg_sdn:
            sdn_functions_traffic += float(sum(levels))
            num_msg_sdn += float(len(levels))
        elif packet_cod_filter.find("SPURIOUS") != -1 or packet_cod_filter.find("ZERO") != -1 or packet_cod_filter.find("WINDOW_FULL") != -1 or packet_cod_filter.find("TCP_FLAGS") != -1:
            error_traffic += float(sum(levels))
            num_msg_error += float(len(levels))
        elif packet_cod_filter.find("PACKET_IN") != -1:
            pass
            #packet_in_traffic += float(sum(levels))
            #num_msg_packet_in += float(len(levels))
            
        #print (packet_cod, sum(levels), len(levels))
    #print("ERROR ", num_msg_traffic, total_traffic)
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

    #print("Total ", num_msg_traffic, " OpenFLow ",openflow_msg, " SDN ",num_msg_sdn, " Overhead ", overhead_traffic,"Error ",error_traffic, "Cost ", overhead_traffic)
    print("SDN ",sdn_functions_traffic, " Overhead ", overhead_traffic,"Cost ",(cost_traffic+overhead_traffic),
     "Error ", error_traffic, "Total traffic ", openflow_total_traffic, "file ", Path(csv_file).name)


    return [overhead_traffic,           #0
            num_msg_overhead,           #1
            cost_traffic,               #2
            num_msg_cost,               #3
            sdn_functions_traffic,      #4
            num_msg_sdn,                #5
            error_traffic,              #6
            num_msg_error,              #7
            packet_in_traffic,          #8
            num_msg_packet_in]          #9

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
state_ipro = csvRead(currentPath + '/pcap/delay/ipro_v4.csv')

#print(total_traffic, "---", overhead_traffic, "---", num_msg_cost)

# Input data; groupwise

############################### Packet Number #########################################
green_data = [state_05[1], state_1[1], state_2[1], state_3[1], state_4[1], state_5[1], 
                state_6[1], state_7[1],state_8[1],state_9[1],state_10[1],state_11[1],
                state_12[1],state_13[1],state_14[1],state_15[1]]

blue_data =  [state_05[3], state_1[3], state_2[3], state_3[3], state_4[3], state_5[3], 
                state_6[3], state_7[3],state_8[3],state_9[3],state_10[3],state_11[3],
                state_12[3],state_13[3],state_14[3],state_15[3]]

red_data =   [state_05[5], state_1[5], state_2[5], state_3[5], state_4[5], state_5[5], 
                state_6[5], state_7[5],state_8[5],state_9[5],state_10[5],state_11[5],
                state_12[5],state_13[5],state_14[5],state_15[5]]

black_data = [state_05[7], state_1[7], state_2[7], state_3[7], state_4[7], state_5[7], 
                state_6[7], state_7[7],state_8[7],state_9[7],state_10[7],state_11[7],
                state_12[7],state_13[7],state_14[7],state_15[7]]
"""
orange_data = [state_05[9], state_1[9], state_2[9], state_3[9], state_4[9], state_5[9], 
                state_6[9], state_7[9],state_8[9],state_9[9],state_10[9],state_11[9],
                state_12[9],state_13[9],state_14[9],state_15[9]]
"""
labels = ['0.5','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
"""
legend = ['Read-State Request messages', 'Read-State Reply messages', 'SDN functions messages', 
            'TCP Error', 'Packet-In']
            """
legend = ['Read-State Request messages', 'Read-State Reply messages', 'SDN functions messages', 
            'TCP Error']            

# Setting the positions and width for the bars
pos = list(range(len(green_data))) 
width = 0.15 # the width of a bar

# Plotting the bars
#fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10,5))
ax1 = plt.subplot(2,1,1)
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
"""
plt.bar([p + width*4 for p in pos], orange_data, width,
                 alpha=0.5,
                 color='w',
                 edgecolor='black',
                 hatch='++',
                 label=labels[4])
                 """

# Setting axis labels and ticks
fontsize_label = 26
fontsize_tick = 18
plt.sca(ax1)
ax1.set_ylabel('Messages (%)', fontsize=fontsize_label)
ax1.set_xlabel('(a) Probing interval (s)', fontsize=fontsize_label)
#ax.set_title('Grouped bar plot')
ax1.set_xticks([p + 1.5 * width for p in pos])
ax1.set_xticklabels(labels)
ax1.tick_params(direction='out', labelsize=fontsize_tick)

# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*5)
plt.ylim([0., 100*1.2])

# Adding the legend and showing the plot
#plt.legend(legend, loc='upper right')
#bbox_to_anchor=(0.5, -0.2)
#plt.tight_layout()
plt.grid()
plt.legend(legend, bbox_to_anchor=(1.0, 1.2), loc="upper right", columnspacing=0.5, ncol=4, fontsize=17)
#plt.show()

#Filter wireshark "tcp.analysis.flags and ip.src == 192.168.0.22 and ip.dst == 192.168.0.28"
# tcp.analysis.flags && tcp.analysis.lost_segment

############################### Traffic #########################################
green_data = [state_05[0], state_1[0], state_2[0], state_3[0], state_4[0], state_5[0], 
                state_6[0], state_7[0],state_8[0],state_9[0],state_10[0],state_11[0],
                state_12[0],state_13[0],state_14[0],state_15[0]]

blue_data =  [state_05[2], state_1[2], state_2[2], state_3[2], state_4[2], state_5[2], 
                state_6[2], state_7[2],state_8[2],state_9[2],state_10[2],state_11[2],
                state_12[2],state_13[2],state_14[2],state_15[2]]

red_data =   [state_05[4], state_1[4], state_2[4], state_3[4], state_4[4], state_5[4], 
                state_6[4], state_7[4],state_8[4],state_9[4],state_10[4],state_11[4],
                state_12[4],state_13[4],state_14[4],state_15[4]]

black_data = [state_05[6], state_1[6], state_2[6], state_3[6], state_4[6], state_5[6], 
                state_6[6], state_7[6],state_8[6],state_9[6],state_10[6],state_11[6],
                state_12[6],state_13[6],state_14[6],state_15[6]]
"""
orange_data = [state_05[8], state_1[8], state_2[8], state_3[8], state_4[8], state_5[8], 
                state_6[8], state_7[8],state_8[8],state_9[8],state_10[8],state_11[8],
                state_12[8],state_13[8],state_14[8],state_15[8]]
"""
labels = ['0.5','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

legend = ['Read-State Request messages', 'Read-State Reply messages', 'SDN functions messages', 
            'TCP Error']

# Setting the positions and width for the bars
pos = list(range(len(green_data))) 
width = 0.15 # the width of a bar
    
# Plotting the bars
#fig, ax = plt.subplots(figsize=(10,6))
patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')
ax2 = plt.subplot(2,1,2)
bar2=plt.bar(pos, green_data, width,
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
"""
plt.bar([p + width*4 for p in pos], orange_data, width,
                 alpha=0.5,
                 color='w',
                 edgecolor='black',
                 hatch='++',
                 label=labels[4])
                 """
# Setting axis labels and ticks
#plt.sca(ax2)
ax2.set_ylabel('Bandwidth (%)', fontsize=fontsize_label)
ax2.set_xlabel('(b) Probing interval (s)', fontsize=fontsize_label)
#ax.set_title('Grouped bar plot')
ax2.set_xticks([p + 1.5 * width for p in pos])
ax2.set_xticklabels(labels)
ax2.tick_params(direction='out', labelsize=fontsize_tick)

# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*5)
plt.ylim([0., 100*1.2])

# Adding the legend and showing the plot
# plt.legend(legend, bbox_to_anchor=(1, -0.23), loc="upper right", columnspacing=0.5, ncol=2, fontsize=14)
plt.tight_layout()
plt.grid()
plt.show()