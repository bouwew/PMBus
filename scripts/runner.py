#!/usr/bin/env python

import time
from pmbus import PMBus

print("Initializing PMBUS... \n")

HEP = PMBus(0x40) #New pmbus object with device address 0x40

time.sleep(1)

# Let's initialize the unit:
# Set it to bulk-charging: 48.0+11.0 = 59.0V; max 17A
v_stop_float = 50.0
v_trim_cv = (57.6-48.0)
v_trim_float = (54.8-48.0)
i_out_bulk = 7.5
i_out_float = 0.2

HEP.setVoutTrim(v_trim_cv) 
HEP.setIoutOCLimit(i_out_bulk)

time.sleep(1)

HEP.setOn()
in_bulk = True
in_float = False

print("Initialised to BULK mode and starting, waiting 10 secs...")

time.sleep(1)

print("Temperature: " + str(HEP.getTemperature()))
print("Input Voltage: " + str(HEP.getVoltageIn()))
print("Output Voltage: " + str(HEP.getVoltageOut()))
print("Output Current: " + str(HEP.getCurrent()))
print("Output Power: " + str(HEP.getPowerOut(False))) #False is caclulated from given values of current$
if in_bulk:
    print("Charger status: BULK/ABS mode \n")
if in_float:
    print("Charger status: FLOAT mode \n") 
print("Status: " + str(HEP.getStatusSummary()) + "\n")
#print("CURVE_CC: " + str(HEP.getCURVE_CC()) + "\n")
#print("CURVE_CV: " + str(HEP.getCURVE_CV()) + "\n")
#print("CURVE_FC: " + str(HEP.getCURVE_FV()) + "\n")
#print("CURVE_TC: " + str(HEP.getCURVE_TC()) + "\n")
#print("Charger Status: " + str(HEP.getCHGStatus()) + "\n")
#print("Curve_Config: " + str(HEP.getCurveConfig()) + "\n")
#print("System Status: " + str(HEP.getSystemStatus()) + "\n")
#print("Systen Config: " + str(HEP.getSystemConfig()) + "\n")

time.sleep(5)

while True:
    print("Temperature: " + str(HEP.getTemperature()))
    print("Input Voltage: " + str(HEP.getVoltageIn()))
    print("Output Voltage: " + str(HEP.getVoltageOut()))
    print("Output Current: " + str(HEP.getCurrent()))
    print("Output Power: " + str(HEP.getPowerOut(False))) #False is caclulated from given values of current$
    if in_bulk:
        print("Charger status: BULK/ABS mode \n")
    if in_float:
        print("Charger status: FLOAT mode \n")
    print("Status: " + str(HEP.getStatusSummary()) + "\n")
    #print("CURVE_CC: " + str(HEP.getCURVE_CC()) + "\n")
    #print("CURVE_CV: " + str(HEP.getCURVE_CV()) + "\n")
    #print("CURVE_FC: " + str(HEP.getCURVE_FV()) + "\n")
    #print("CURVE_TC: " + str(HEP.getCURVE_TC()) + "\n")
    #print("Charger Status: " + str(HEP.getCHGStatus()) + "\n")
    #print("Curve_Config: " + str(HEP.getCurveConfig()) + "\n")
    #print("System Status: " + str(HEP.getSystemStatus()) + "\n")
    #print("Systen Config: " + str(HEP.getSystemConfig()) + "\n")
    #DRQ.encodePMBus(34.0)

    if in_bulk and HEP.getCurrent() < i_out_float:
        HEP.setVoutTrim(v_trim_float)
        in_bulk = False
        in_float = True
        print("Switched to FLOAT mode")

    if in_float and HEP.getVoltageOut() < v_stop_float:
        HEP.setVoutTrim(v_trim_cv)
        in_bulk = True
        in_float = False
        print("Switched back to BULK mode")

    time.sleep(5)
