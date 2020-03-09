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
    error_traffic = 0
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
    print("SDN ",sdn_functions_traffic, " IN ", packet_in_traffic,"BW ",(cost_traffic+overhead_traffic), "Error ", error_traffic, "Total traffic ", openflow_total_traffic, "Probing ",Path(csv_file).name)


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
#state_05    = [11.77  , 88.23]
state_1     = [29.17  , 70.83]
state_2     = [36.9  ,  63.1]
state_3     = [70.86  , 29.14]
state_4     = [77.86  , 22.14]
state_5     = [88.09  , 11.91]
state_6     = [89.33  , 10.67]
state_7     = [90.02 ,  9.98]
state_8     = [91.13 ,  8.87]
state_9     = [91.73 ,  8.27]
state_10    = [92.75  , 7.25]
state_11    = [93.1 ,   6.9]
state_12    = [93.86 ,  6.14]
state_13    = [93.62 ,  6.38]
state_14    = [94.63 ,  5.37]
state_15    = [96.4 ,   3.6]

#state_ipro = csvRead(currentPath + '/pcap/delay/ipro_v4.csv')

#print(total_traffic, "---", overhead_traffic, "---", num_msg_cost)

# Input data; groupwise

############################### Packet Number #########################################
green_data = [state_1[0], state_2[0], state_3[0], state_4[0], state_5[0], 
                state_6[0], state_7[0],state_8[0],state_9[0],state_10[0],state_11[0],
                state_12[0],state_13[0],state_14[0],state_15[0]]

blue_data =  [state_1[1], state_2[1], state_3[1], state_4[1], state_5[1], 
                state_6[1], state_7[1],state_8[1],state_9[1],state_10[1],state_11[1],
                state_12[1],state_13[1],state_14[1],state_15[1]]
   

# Setting the positions and width for the bars
pos = list(range(len(green_data))) 
width = 0.15 # the width of a bar

# Plotting the bars
#fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10,5))
f, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')

# Setting axis labels and ticks
fontsize_label = 26
fontsize_tick = 18

############################### Traffic #########################################

labels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

# Setting the positions and width for the bars
pos = list(range(len(green_data))) 
width = 0.15 # the width of a bar
print(pos)
# Plotting the bars
#fig, ax = plt.subplots(figsize=(10,6))
patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')
#ax2 = plt.subplot(2,1,2)
bar2=plt.bar(green_data, width,
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

ax1.set_ylabel('Bandwidth (%)', fontsize=fontsize_label)
ax1.set_xlabel('Probing interval (s)', fontsize=fontsize_label)
#ax.set_title('Grouped bar plot')
ax1.set_xticks([p + 1.5 * width for p in pos])
ax1.set_xticklabels(labels)
ax1.tick_params(direction='out', labelsize=fontsize_tick)

# Setting the x-axis and y-axis limits
plt.xlim(min(pos)-width, max(pos)+width*5)
plt.ylim([0., 100*1])

# Adding the legend and showing the plot
legend = ['SDN functions messages', 'Overhead']
plt.legend(legend, bbox_to_anchor=(1.0, 1.1), loc="upper right", columnspacing=0.5, ncol=4, fontsize=17)
plt.tight_layout()
plt.grid()
plt.axhline(y=12, label='', c='#d62728', linestyle=':')
plt.show()