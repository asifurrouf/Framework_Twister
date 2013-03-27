"""
<title>GroupModInvalidID</title>
<description>
    A modification for reserved group should result in OFPET_BAD_ACTION/OFPGMFC_INVALID_GROUP
    
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

class GroupModInvalidID(GroupTest):
    """
    A modification for reserved group should result in OFPET_BAD_ACTION/OFPGMFC_INVALID_GROUP
    """

    def runTest(self):
        self.clear_switch()

        group_mod_msg = \
        testutils.create_group_mod_msg(ofp.OFPGC_MODIFY, ofp.OFPGT_ALL, group_id = ofp.OFPG_ALL, buckets = [
            testutils.create_bucket(0, 0, 0, [
                testutils.create_action(action= ofp.OFPAT_OUTPUT, port= 1)
            ])
        ])
        self.send_ctrl_exp_error(group_mod_msg, 'group mod',
                                 ofp.OFPET_GROUP_MOD_FAILED,
                                 ofp.OFPGMFC_INVALID_GROUP)

    
tc = GroupModInvalidID()
_RESULT = tc.run()
