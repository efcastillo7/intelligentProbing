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


class IntelligentProbing(simple_switch_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(IntelligentProbing, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self._monitor)

    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
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
