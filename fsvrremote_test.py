# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyvisa
from time import sleep

class Test:
    inst = None
    f_span = 5
    f_channels = []
    freq_metric = "MHz"
    time_metric = "s"
    
    def write(self, cmd):
        self.inst.write(cmd)
        sleep(1)
    
    def connect(self):
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource('TCPIP0::mess03.lb02.hft-leipzig.de::inst0::INSTR')
        self.inst.timeout = 5000
        self.f_channels = list(range(2412,2477,5))
        self.f_channels.append(2484)
        self.write("*IDN?\n")
        self.write("SYStem:DISPlay:UPDate ON\n")
        self.write("CALC3:SGR:HDEP 5000")

    def set_channel(self, ch):
        f_middle = self.f_channels[ch-1]
        f_start = f_middle - self.f_span
        f_end = f_middle + self.f_span
        self.write("SENSe:FREQuency:START "+str(f_start)+self.freq_metric+"\n")
        self.write("SENSe:FREQuency:STOP "+str(f_end)+self.freq_metric+"\n")
        
    def clear(self, screens=[1,3]):
        for i in screens:
            self.write("CALCulate"+str(i)+":SGRam:CLEar:IMMediate")
            
    def store(self, filename):
        self.write("MMEMory:STORe3:TRACe 1, '"+filename+"'")
        
    def store_sgram(self, filename):
        self.write("MMEM:STOR3:SGR '"+filename+"'")
        
t = Test()
t.connect()
t.set_channel(1)
# t.clear()
# t.store_sgram("C:/trace1test.ASC")