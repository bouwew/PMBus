"""" Forked from https://github.com/Michael-Equi/PMBus and improved for use with the MEANWELL HEP-1000. """

from smbus import SMBus
import math

class PMBus:

    #constants initialized on object creation
    VOUT_MODE = 0b00000
    VOUT_N = 0b00000

    def __init__(self, addr, id=1):
        self.busID = id
        self.address = addr
        self.VOUT_MODE = self._readBytePMBus(0x20)
        voutN = self.VOUT_MODE & 0b00011111
        self.VOUT_N = self.twos_comp(voutN, 5)
        print("Succesfully connected to PMBus...")
        #print("Default N-value = " + str(self.VOUT_N) + "\n" )

    #Decode/encode Linear data format => X=Y*2^N
    def _decodePMBus(self, message):
        messageN = message >> 11
        messageY = message & 0b0000011111111111
        message = messageY*(2.0**(self.twos_comp(messageN, 5))) #calculate real values (everything but VOUT works)
        return message

    def _encodePMBus(self, message):
        YMAX = 1023.0
        #print(message)
        Nval = int(math.log(message/YMAX,2))
        #print("NVal: " + str(Nval))
        Yval = int(message/(2**-Nval))
        #print("YVal: " + str(Yval))
        message = ((Nval & 0b00011111)<<11) | Yval
        #print(message, bin(message))
        return message

    def _encodePMBusVout(self, value):
        Nval = -1 * self.VOUT_N
        #print("Nval: " + str(Nval))
        Vval = int(value/(2**-Nval))
        #print("Vval: " + str(Vval))
        return Vval

    def _encode_N_PMBus(self, value, N):
        #print(value)
        Nval = N
        #print("NVal: " + str(Nval))
        Yval = int(value/(2**Nval))
        #print("YVal: " + str(Yval))
        value = ((Nval & 0b00011111)<<11) | Yval
        #print(value, bin(value))
        return value

    def _encode_N_PMBusIout(self, value, N):
        #print(value)
        Nval = N
        #print("NVal: " + str(Nval))
        Ival = int(value/(2**Nval))
        #print("IVal: " + str(Ival))
        return Ival

    #wrapper functions for reading/writing a word/byte to an address with pec
    def _writeWordPMBus(self, cmd, word, pecByte=True):
        bus = SMBus(self.busID)
        bus.pec = pecByte
        bus.write_word_data(self.address, cmd, word)
        bus.close()

    def _readWordPMBus(self, cmd, pecByte=True):
        bus = SMBus(self.busID)
        bus.pec = pecByte
        data = bus.read_word_data(self.address, cmd)
        bus.close()
        return data

    def _writeBytePMBus(self, cmd, byte, pecByte=True):
        bus = SMBus(self.busID)
        bus.pec = pecByte
        bus.write_byte_data(self.address, cmd, byte)
        bus.close()

    def _readBytePMBus(self, cmd, pecByte=True):
        bus = SMBus(self.busID)
        bus.pec = pecByte
        data = bus.read_byte_data(self.address, cmd)
        bus.close()
        return data

    def _writeBlockPMBus(self, cmd, list, pecByte=True):
        bus = SMBus(self.busID)
        bus.pec = pecByte
        bus.write_i2c_block_data(self.address, cmd, list)
        bus.close()

    def _readBlockPMBus(self, cmd, pecByte=True):
        bus = SMBus(self.busID)
        bus.pec = pecByte
        data = bus.read_i2c_block_data(self.address, cmd)
        bus.close()
        return data

    ################################### Functions for setting PMBus values
    def setVoutTrim(self, value, minTrimVoltage=-24.0, maxTrimVoltage=12.0):
        """The VOUT_TRIM command sets the value of the output voltage related to the default voltage VOUT."""
        if value < minTrimVoltage:
            value = minTrimVoltage
        if value > maxTrimVoltage:
            value = maxTrimVoltage

        self._writeWordPMBus(0x22, self._encodePMBusVout(value))

    def setIoutOCLimit(self, ocLimit, maxOverCurrent=65.0):
        """The IOUT_OV_WARN_LIMIT command sets the value of the output current that causes
        an output overcurrent warning. The IOUT_OC_FAULT_LIMIT command sets the value of the output current, in
        amperes, that causes the overcurrent detector to indicate an overcurrent fault condition."""
        #min = 59, max = 65 for DRQ1250
        N = -4
        if ocLimit < maxOverCurrent:
            ocFaultLimit = float(ocLimit)
        else:
            ocFaultLimit = maxOverCurrent

        self._writeWordPMBus(0x46, self._encode_N_PMBus(ocFaultLimit, N))

    #See PMBus spec page 53-54 for information on the on/off functionality
    def setOff(self, hard=False):
        if hard:
            self._writeBytePMBus(0x01,0x00) #Hard off
        else:
            self._writeBytePMBus(0x01,0x40) #Soft off

    def setOn(self):
        self._writeBytePMBus(0x01,0x80)

    def setCURVE_CC(self, value):
        """Set CURVE_CC, max 17.5A."""
        N = -4
        maxCurrent = 17.5
        if value < maxCurrent:
            value = float(value)
        else:
            value = maxCurrent

        self._writeWordPMBus(0xB0, self._encode_N_PMBus(value, N))

    def setCURVE_CV(self, value):
        """Set CURVE_CV, max 60.0V."""
        maxVolt = 60.0
        if float(value) < maxVolt:
            value = float(value)
        else:
            value = maxVolt

        self._writeWordPMBus(0xB1, self._encodePMBusVout(value))

    def setCURVE_FV(self, value):
        """Set CURVE_FV, max 57.0V."""
        maxVolt = 57.0
        if float(value) < maxVolt:
            value = float(value)
        else:
            value = maxVolt

        self._writeWordPMBus(0xB2, self._encodePMBusVout(value))

    def setCURVE_TC(self, value):
        """Set CURVE_TC, max 5.0A."""
        N = -4
        maxCurrent = 5.0
        if value < maxCurrent:
            value = float(value)
        else:
            value = maxCurrent

        self._writeWordPMBus(0xB3, self._encode_N_PMBus(value, N))

    def setPMBusMode(self):
        """Set to PMBus Mode."""
        self._writeWordPMBus(0xBE, 3)

    def setUserMode(self):
        """Set to User Mode."""
        self._writeWordPMBus(0xBE, 2)

    def setChargerMode(self):
        """Set to Charger Mode."""
        self._writeWordPMBus(0xB4, 132)

    def setPSUMode(self):
        """Set to PSU Mode."""
        self._writeWordPMBus(0xB4, 4)

    ################################### Functions for getting PMBus values
    def getVoltageIn(self):
        self.voltageIn = self._decodePMBus(self._readWordPMBus(0x88))
        return self.voltageIn

    def getVoltageOut(self):
        voltageOutMessage = self._readWordPMBus(0x8B)
        #print(voltageOutMessage)
        #print(self.VOUT_N)
        self.voltageOut = voltageOutMessage*(2.0**self.VOUT_N)
        return self.voltageOut

    def getCurrent(self):
        bus = SMBus(1)
        self.current = self._decodePMBus(self._readWordPMBus(0x8C))
        bus.close()
        return self.current

    def getPowerOut(self, fromDRQ):
        if(fromDRQ == True):
            self.powerOut = self._decodePMBus(self._readWordPMBus(0x96))
        else:
            self.powerOut = self.voltageOut * self.current
        return self.powerOut

    def getTemperature(self):
        self.temperature = self._decodePMBus(self._readWordPMBus(0x8D))
        return self.temperature

    def getIoutOCLimit(self):
        #returns fault, warn
        return self._decodePMBus(self._readWordPMBus(0x46)), self._decodePMBus(self._readWordPMBus(0x4A))

    def getIoutFaultResponse(self):
        #see page 37-40 on PMBus spec for info on response bytes
        return self._readBytePMBus(0x47)

    def getFaultResponse(self, register):
        #see page 37-40 on PMBus spec for info on response bytes
        """
        DRQ1250 registers:
        VIN UV  = 0x5A
        VIN OV  = 0x56
        VOUT OV = 0x41
        OT      = 0x50
        """
        return self._readBytePMBus(register)

    #members for getting the status of the DRQ device
    #see PMBUS spec part two pages 77-79
    def getStatusSummary(self):
        """The STATUS_WORD command returns two bytes of information with a summary of the
        unit's fault condition. Based on the information in these bytes, the host can get more
        information by reading the appropriate status registers. The low byte of the STATUS_WORD
        is the same register as the STATUS_BYTE command."""
        # BUSY | OFF | VOUT_OV_Fault | IOUT_OC_FAULT | VIN_UV_FAULT | TEMPURATURE | CML (command memory logic) | None
        # VOUT Fault | IOUT Fault | POUT  Fault | INPUT Fault | MFR_Specific | PWR_GD | Fans | Other | Unknown
        # Note: if PWR_GD is set then pwr is not good (negative logic)
        self.statusSummary = self._readWordPMBus(0x79)
        status = {
            "busy" :          bool(self.statusSummary & (0b1<<7)),
            "off" :           bool(self.statusSummary & (0b1<<6)),
            "vout_ov_fault" : bool(self.statusSummary & (0b1<<5)),
            "iout_oc_fault" : bool(self.statusSummary & (0b1<<4)),
            "vin_uv_fault" :  bool(self.statusSummary & (0b1<<3)),
            "temp_fault" :    bool(self.statusSummary & (0b1<<2)),
            "cml_fault" :     bool(self.statusSummary & (0b1<<1)),
            "vout_fault" :    bool(self.statusSummary & (0b1<<15)),
            "iout_fault" :    bool(self.statusSummary & (0b1<<14)),
            "input_fault" :   bool(self.statusSummary & (0b1<<13)),
            "pwr_gd" :        not bool(self.statusSummary & (0b1<<11)),
            "fan_fault" :     bool(self.statusSummary & (0b1<<10)),
            "other" :         bool(self.statusSummary & (0b1<<9)),
            "unknown" :       bool(self.statusSummary & (0b1<<8)),
        }
        return status, self.statusSummary

    def getCURVE_CC(self):
        bus = SMBus(1)
        self.current = self._decodePMBus(self._readWordPMBus(0xB0))
        bus.close()
        return self.current

    def getCURVE_CV(self):
        voltageOutMessage = self._readWordPMBus(0xB1)
        self.voltageOut = voltageOutMessage*(2.0**self.VOUT_N)
        return self.voltageOut

    def getCURVE_FV(self):
        voltageOutMessage = self._readWordPMBus(0xB2)
        self.voltageOut = voltageOutMessage*(2.0**self.VOUT_N)
        return self.voltageOut

    def getCURVE_TC(self):
        bus = SMBus(1)
        self.current = self._decodePMBus(self._readWordPMBus(0xB3))
        bus.close()
        return self.current

    def getCurveConfig(self):
        """The charger status."""
        self.statusSummary = self._readWordPMBus(0xB4)
        status = {
            "CUVS_A" :        bool(self.statusSummary & (0b1)),
            "CUVS_B" :        bool(self.statusSummary & (0b1<<1)),
            "TCS_A" :         bool(self.statusSummary & (0b1<<2)),
            "TCS_B" :         bool(self.statusSummary & (0b1<<3)),
            "STGS" :          bool(self.statusSummary & (0b1<<6)),
            "CUVE" :          bool(self.statusSummary & (0b1<<7)),
            "CCTOE" :         bool(self.statusSummary & (0b1<<8)),
            "CVTOE" :         bool(self.statusSummary & (0b1<<9)),
            "FVTOE" :         bool(self.statusSummary & (0b1<<10)),
        }
        return status, self.statusSummary

    def getCHGStatus(self):
        """The charger status."""
        self.statusSummary = self._readWordPMBus(0xB8)
        status = {
            "FULLM" :         bool(self.statusSummary & (0b1)),
            "CCM" :           bool(self.statusSummary & (0b1<<1)),
            "CVM" :           bool(self.statusSummary & (0b1<<2)),
            "FVM" : 	         bool(self.statusSummary & (0b1<<3)),
            "NTCER" :         bool(self.statusSummary & (0b1<<10)),
            "BTNC" :          bool(self.statusSummary & (0b1<<11)),
            "CCTOF" :         bool(self.statusSummary & (0b1<<13)),
            "CVTOF" :         bool(self.statusSummary & (0b1<<14)),
            "FVTOF" :         bool(self.statusSummary & (0b1<<15)),
        }
        return status, self.statusSummary

    def getSystemConfig(self):
        """The charger status."""
        self.statusSummary = self._readWordPMBus(0xBE)
        status = {
            "PM_CTL" :        bool(self.statusSummary & (0b1)),
            "OPER_INIT_A" :   bool(self.statusSummary & (0b1<<1)),
            "OPER_INIT_B" :   bool(self.statusSummary & (0b1<<2)),
        }
        return status, self.statusSummary

    def getSystemStatus(self):
        """The charger status."""
        self.statusSummary = self._readWordPMBus(0xBF)
        status = {
            "DC_OK" :         bool(self.statusSummary & (0b1<<1)),
            "ADL_ON" :        bool(self.statusSummary & (0b1<<4)),
            "INITIAL_STATE" : bool(self.statusSummary & (0b1<<5)),
            "EEPER" :         bool(self.statusSummary & (0b1<<6)),
        }
        return status, self.statusSummary

    #method for computing twos complement
    def twos_comp(self, val, bits):
        #compute the 2's complement of int value val
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val
