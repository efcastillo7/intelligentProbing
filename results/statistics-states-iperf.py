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
    print("SDN ",sdn_functions_traffic, " Overhead ", overhead_traffic*100,"Cost ",(cost_traffic+overhead_traffic), "Error ", error_traffic, "Total traffic ", openflow_total_traffic,"file ", Path(csv_file).name)


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
state_4 = csvRead(currentPath + '/iperf_results/probing_4s.csv')
state_5 = csvRead(currentPath + '/iperf_results/probing_5s.csv')
state_6 = csvRead(currentPath + '/iperf_results/probing_6s.csv')
state_ipro = csvRead(currentPath + '/iperf_results/ipro.csv')

#print(total_traffic, "---", overhead_traffic, "---", num_msg_cost)