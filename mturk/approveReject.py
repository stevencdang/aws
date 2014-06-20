#!/usr/bin/env python2

import mturk

if __name__ == '__main__':
    m = mturk.MechanicalTurk()
    r = m.request("GetAccountBalance")
    if r.valid:
        print r.get_response_element("AvailableBalance")
    else:
        print "failed"
        print r.get_response_element("AvailableBalance")
