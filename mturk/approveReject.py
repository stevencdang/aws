#!/usr/bin/env python2

import mturk

if __name__ == '__main__':
    m = mturk.MechanicalTurk()
    r = m.request("ApproveRejectedAssignment",
        {"AssignmentId": "3QHK8ZVMIMI8YD6B75F8M2F4ZQJBL8",
        "RequesterFeedback": "Late completion due to requester server technical difficulties, but finished after technical difficulties were finished"})
    if r.valid:
        print r.get_response_element("ApproveRejectedAssignmentResult")
    else:
        print "failed"
