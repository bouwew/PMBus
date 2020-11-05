#!/usr/bin/env python

import time
from pmbus import PMBus

print("Initializing PMBUS... \n")

HEP = PMBus(0x40) #New pmbus object with device address 0x40

time.sleep(1)

HEP.setOff(True)

print("Set to Hard off")
