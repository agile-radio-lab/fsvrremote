# -*- coding: utf-8 -*-
"""
Author: Igor Kim
E-mail: igor.skh@gmail.com
Repository: https://bitbucket.org/igorkim/fsvrremote

Example for remote controlling of Rohde und Schwarz FSVR

April 2017
"""

from FSVRRemote import FSVRRemote

t = FSVRRemote()
t.connect('TCPIP0::192.168.0.4::inst0::INSTR')
t.set_f_middle(1815)
t.set_reflevel(-40)
t.set_hdepth(10000)
t.set_fspan(5)
t.set_swptime(0.00005)
t.clear()
# t.store_sgram("D:/LTE.DAT")