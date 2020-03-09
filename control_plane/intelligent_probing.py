from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

from operator import attrgetter
from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER, CONFIG_DISPATCHER, HANDSHAKE_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.controller.ofp_event import EventOFPErrorMsg
from ryu.lib import hub
import json
import sys
sys.path.insert(0, '/home/ryu/ryu/ryu/app/intelligentProbing/database/')
import ConnectionBD_v2

import random


class IntelligentProbing(simple_switch_13.SimpleSwitch13):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(IntelligentProbing, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

        self.mac_to_port = {}
    """    
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        idle = hard = random.randint(0, 10)

        #print("SET IDLE_TIMEOUT")

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    idle_timeout=idle, hard_timeout=hard,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    idle_timeout=idle, hard_timeout=hard,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})

        self.logger.info("Packet IN %s %s %s %s", dpid, src, dst, in_port)

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)
"""
    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

    def _monitor(self):        
        while True:
            probing_frequency = ConnectionBD_v2.getProbingFrequency()
            #probing_frequency = 6
            print("PROBING TO...",probing_frequency)    
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(probing_frequency)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

        cookie = cookie_mask = 0
        match = parser.OFPMatch(in_port=1)

        req = parser.OFPAggregateStatsRequest(datapath, 0,
                                              ofproto.OFPTT_ALL,
                                              ofproto.OFPP_ANY,
                                              ofproto.OFPG_ANY,
                                              cookie, cookie_mask,
                                              match)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        flow_statistics = {}
        self.logger.debug('FLOWS----:')
        
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            
            flow_statistics['id_datapath'] = ev.msg.datapath.id
            flow_statistics['in_port'] = stat.match['in_port']
            flow_statistics['eth_dst'] = stat.match['eth_dst']
            flow_statistics['out_port'] = stat.instructions[0].actions[0].port
            flow_statistics['packets'] = stat.packet_count
            flow_statistics['bytes'] = stat.byte_count
            flow_statistics['idle_timeout'] = stat.idle_timeout
            flow_statistics['hard_timeout'] = stat.hard_timeout
            flow_statistics['duration_sec'] = stat.duration_sec
            self.logger.debug('IDLE TIMEOUT: %016x', stat.idle_timeout)     
            #ConnectionBD_v2.insertStatFlow(flow_statistics)

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        body = ev.msg.body
        port_statistics = {}
                
        for stat in sorted(body, key=attrgetter('port_no')):            
            port_statistics['id_datapath'] = ev.msg.datapath.id
            port_statistics['port_number'] = stat.port_no
            port_statistics['rx_packets']  = stat.rx_packets
            port_statistics['rx_bytes']    = stat.rx_bytes
            port_statistics['rx_errors']   = stat.rx_errors
            port_statistics['tx_packets']  = stat.tx_packets
            port_statistics['tx_bytes']    = stat.tx_bytes
            port_statistics['tx_errors']   = stat.tx_errors
            #self.logger.debug('IDLE TIMEOUT: %016x', stat.rx_packets)

            #ConnectionBD_v2.insertStatPort(port_statistics)

    @set_ev_cls(ofp_event.EventOFPAggregateStatsReply, MAIN_DISPATCHER)
    def aggregate_stats_reply_handler(self, ev):
        body = ev.msg.body
        aggregate_flow_statistics = {}

        aggregate_flow_statistics['byte_count'] =  body.byte_count
        aggregate_flow_statistics['flow_count'] = body.flow_count
        aggregate_flow_statistics['packet_count'] = body.packet_count

        if body.flow_count > 0:
            ConnectionBD_v2.insertStatAggregateFlow(aggregate_flow_statistics)

        #ConnectionBD_v2.insertStatAggregateFlow(aggregate_flow_statistics)


    @set_ev_cls(EventOFPErrorMsg,
                [HANDSHAKE_DISPATCHER, CONFIG_DISPATCHER, MAIN_DISPATCHER])
    def error_msg_handler(self, ev):
        msg = ev.msg
        self.logger.info('OFPErrorMsg received: type=0x%02x code=0x%02x '
                         'message=%s',
                        msg.type, msg.code, hex_array(msg.data))        
