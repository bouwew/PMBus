#!/usr/bin/env python

import time
from pmbus import PMBus

print("Initializing PMBUS... \n")

HEP = PMBus(0x40) #New pmbus object with device address 0x40

time.sleep(1)

#HEP.setVinUVLimit(36.0)
#HEP.setCURVE_CC(17.0)
#HEP.setCURVE_CV(59.0)
HEP.setCURVE_FV(54.6)
#HEP.setCURVE_TC(3.0)

#HEP.setChargerMode()
#HEP.setPSUMode()

#HEP.setPMBusMode()
#HEP.setUserMode()


