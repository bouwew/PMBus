# PMBus
A python library for interfacing with devices that are based on the PMBus Specification.

The code from the Michael-Equi/PMBus github was taken as a basis and made to work with the MeanWell HEP-1000:

```
Temperature: 43.375
Input Voltage: 236.0
Output Voltage: 54.609375
Output Current: 1.5625
Output Power: 85.3271484375

Status: ({'busy': False, 'off': False, 'vout_ov_fault': False, 'iout_oc_fault': False, 'vin_uv_fault': False, 'temp_fault': False, 'cml_fault': False, 'vout_fault': False, 'iout_fault': False, 'input_fault': False, 'pwr_gd': True, 'fan_fault': False, 'other': False, 'unknown': False}, 0)

CURVE_CC: 17.5
CURVE_CV: 59.0
CURVE_FC: 54.599609375
CURVE_TC: 3.0

Charger Status: ({'FULLM': True, 'CCM': False, 'CVM': False, 'FVM': True, 'NTCER': False, 'BTNC': False, 'CCTOF': False, 'CVTOF': False, 'FVTOF': False}, 9)

Curve_Config: ({'CUVS_A': False, 'CUVS_B': False, 'TCS_A': True, 'TCS_B': False, 'STGS': False, 'CUVE': True, 'CCTOE': False, 'CVTOE': False, 'FVTOE': False}, 132)

System Status: ({'DC_OK': True, 'ADL_ON': True, 'INITIAL_STATE': False, 'EEPER': False}, 18)

Systen Config: ({'PM_CTL': True, 'OPER_INIT_A': True, 'OPER_INIT_B': False}, 3)
```
Commands to use:

`python3 test.py` to obtain the above output.

`python3 program.py` to program the HEP-1000, I have only tested with one programming-line uncommented at a time.

Note: there could be bugs, Status is not tested. Charger Status, Curve Config, System Status and System Config are tested and appear to be correct.
