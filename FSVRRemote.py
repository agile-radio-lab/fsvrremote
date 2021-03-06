# -*- coding: utf-8 -*-
"""
Author: Igor Kim
E-mail: igor.skh@gmail.com
Repository: https://github.com/igorskh/fsvrremote

Module for remote controlling of Rohde und Schwarz FSVR

(c) Igor Kim 2017-2020
"""

import pyvisa
from time import sleep

DEFAULT_TIMEOUT = 5000
WIFI_CHANNELS = list(range(2412, 2477, 5))
WIFI_CHANNELS.append(2484)

class FSVRRemote:
    inst = None
    f_span = 5
    f_channels = []
    freq_metric = "MHz"
    time_metric = "s"
    hdepth = 5000
    swptime = 0.001

    @staticmethod
    def bool_to_str(value):
        return "ON" if value else "OFF"

    def set_fspan(self, value):
        self.f_span = float(value)

    def set_reflevel(self, value):
        self.reflevel = float(value)
        self.write('DISP:TRAC:Y:RLEV ' + str(self.reflevel) + "dBm")

    def set_swptime(self, value):
        self.swptime = float(value)
        self.write("SWE:TIME " + str(self.swptime) + self.time_metric)

    def set_hdepth(self, value):
        self.hdepth = int(value)
        self.write("CALC3:SGR:HDEP " + str(self.hdepth))

    def write(self, cmd):
        self.inst.write(cmd + "\n")
        sleep(1)

    def connect(self, device_str):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(device_str)
        self.inst.timeout = DEFAULT_TIMEOUT
        self.f_channels = WIFI_CHANNELS
        self.write("*IDN?")
        self.write("SYStem:DISPlay:UPDate ON")
        self.set_hdepth(self.hdepth)
        self.set_swptime(self.swptime)

    def set_f_middle(self, freq):
        f_start = freq - self.f_span
        f_end = freq + self.f_span
        self.write("SENSe:FREQuency:START " + str(f_start) + self.freq_metric)
        self.write("SENSe:FREQuency:STOP " + str(f_end) + self.freq_metric)

    def set_channel(self, ch):
        f_middle = self.f_channels[ch - 1]
        self.set_f_middle(f_middle)

    def clear(self, screens=[1, 3]):
        for i in screens:
            self.write("CALCulate" + str(i) + ":SGRam:CLEar:IMMediate")

    def store(self, filename):
        self.write("MMEMory:STORe3:TRACe 1, '" + filename + "'")

    def store_sgram(self, filename):
        self.write("MMEM:STOR3:SGR '" + filename + "'")
