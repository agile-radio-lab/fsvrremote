# -*- coding: utf-8 -*-
"""
Author: Igor Kim
E-mail: igor.skh@gmail.com
Repository: https://bitbucket.org/igorkim/fsvrremote

Module for remote controlling of Rohde und Schwarz FSVR

April 2017
"""

import pyvisa
from time import sleep

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

    def connect(self):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource('TCPIP0::mess03.lb02.hft-leipzig.de::inst0::INSTR')
        self.inst.timeout = 5000
        self.f_channels = list(range(2412, 2477, 5))
        self.f_channels.append(2484)
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
