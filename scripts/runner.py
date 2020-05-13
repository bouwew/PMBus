#!/usr/bin/env python

import time
from pmbus import PMBus

print("Initializing PMBUS... \n")

HEP = PMBus(0x40) #New pmbus object with device address 0x40

time.sleep(1)

#HEP.setVinUVLimit(36.0)

time.sleep(1)

while True:
    print("Temperature: " + str(HEP.getTempurature()))
    print("Input Voltage: " + str(HEP.getVoltageIn()))
    print("Output Voltage: " + str(HEP.getVoltageOut()))
    print("Output Current: " + str(HEP.getCurrent()))
    print("Output Power: " + str(HEP.getPowerOut(False)) + "\n\n") #False is caclulated from given values of current and voltage while True gets values from DRQ1250
    print("Status: " + str(HEP.getStatusSummary()) + "\n")
    print("CURVE_CC: " + str(HEP.getCURVE_CC()) + "\n")
    print("CURVE_CV: " + str(HEP.getCURVE_CV()) + "\n")
    print("CURVE_FC: " + str(HEP.getCURVE_FV()) + "\n")
    print("CURVE_TC: " + str(HEP.getCURVE_TC()) + "\n")
    print("Charger Status: " + str(HEP.getCHGStatus()) + "\n")
    print("Curve_Config: " + str(HEP.getCurveConfig()) + "\n")
    print("System Status: " + str(HEP.getSystemStatus()) + "\n")
    print("Systen Config: " + str(HEP.getSystemConfig()) + "\n")
    #DRQ.encodePMBus(34.0)

    time.sleep(5)
