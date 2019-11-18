import pyshark
import os, platform, logging

rtp_list = []
cap = pyshark.FileCapture('probing_05.pcap', display_filter='openflow_v4.multipart_reply.type')

f = open('test.log', 'w')
flows_number = 0
total_flows = 0
for i in cap:    
    #print("Position", i[3])    
    if "<OPENFLOW_V4 Layer>" in str(i.layers):
        #print("Length ", i[len(i.layers)-1].length)
        #print("Length ", i[len(i.layers)-1])
        f.write(str(i[len(i.layers)-1]))
        f.write('\n')
        total_flows += 1
        #print("Total ", total_flows)
        if str(i[len(i.layers)-1]).find("Flow stats") != -1:
            flows_number += 1
            print("Flows ", flows_number)
            
print(total_flows)

# Number of flow stats -> openflow_v4.flow_stats.flags, openflow_v4.packet_out.in_port, 