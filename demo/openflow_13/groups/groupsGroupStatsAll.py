"""
<title>GroupStatsAll</title>
<description>
    A packet sent to the group should increase byte/packet counters of group
    
</description>
"""

try:
    if('TWISTER_ENV' in globals()):
        from ce_libs.openflow.of_13.openflow_base import *
        testbed=currentTB
        from ce_libs import ra_proxy
        ra_service=ra_proxy                        
except:
    raise

class GroupStatsAll(GroupTest):
    """
    A packet sent to the group should increase byte/packet counters of group
    """

    def runTest(self):
        self.clear_switch()

        group_add_msg1 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 10, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_SET_FIELD, tcp_sport = 2000),
                testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 2)
            ]),
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_SET_FIELD, tcp_sport = 3000),
                testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 3)
            ])
        ])

        self.send_ctrl_exp_noerror(group_add_msg1, 'group add 1')

        group_add_msg2 = \
        testutils.create_group_mod_msg(ofp.OFPGC_ADD, ofp.OFPGT_ALL, group_id = 20, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_SET_FIELD, tcp_sport = 2000),
                testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 2)
            ]),
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action = ofp.OFPAT_SET_FIELD, tcp_sport = 3000),
                testutils.create_action(action = ofp.OFPAT_OUTPUT, port = 3)
            ])
        ])

        self.send_ctrl_exp_noerror(group_add_msg2, 'group add 2')

        packet_in  = testutils.simple_tcp_packet(tcp_sport=1000)

        flow_add_msg1 = \
        testutils.flow_msg_create(self,packet_in,ing_port = 1,action_list = [
            testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 10)
        ])

        self.send_ctrl_exp_noerror(flow_add_msg1, 'flow add 1')

        flow_add_msg2 = \
        testutils.flow_msg_create(self,packet_in,ing_port = 2,action_list = [
            testutils.create_action(action = ofp.OFPAT_GROUP, group_id = 20)
        ])

        self.send_ctrl_exp_noerror(flow_add_msg2, 'flow add 2')

        self.send_data(packet_in, 1)
        self.send_data(packet_in, 1)
        self.send_data(packet_in, 2)
        self.send_data(packet_in, 2)
        self.send_data(packet_in, 2)

        group_stats_req = \
        testutils.create_group_stats_req(ofp.OFPG_ALL)

        response = \
        self.send_ctrl_exp_reply(group_stats_req,
                                 ofp.OFPT_MULTIPART_REPLY, 'group stat', group_stats_req.header.xid)

        exp_len = ofp.OFP_HEADER_BYTES + \
                  ofp.OFP_MULTIPART_REPLY_BYTES + \
                  ofp.OFP_GROUP_STATS_BYTES + \
                  ofp.OFP_BUCKET_COUNTER_BYTES * 2 + \
                  ofp.OFP_GROUP_STATS_BYTES + \
                  ofp.OFP_BUCKET_COUNTER_BYTES * 2

        self.assertEqual(response.header.length, exp_len,
                         'Received packet length does not equal expected length')

    
tc = GroupStatsAll()
_RESULT = tc.run()
