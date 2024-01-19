#!/usr/bin/python3
from functions import *

# Do all the work
authenticate('cisco', 'cisco')
feature('interface-vlan', True)
feature('hsrp', True)
hostname('tres-python')
vrf('chiefs')
network('mahomes', '15', '192.168.15.2/24', 'chiefs')
network('kelce', '87', '192.168.87.2/24', 'chiefs')
network('jones', '95', '192.168.95.2/24', 'chiefs')
hsrp('15', '192.168.15.1', 110)
hsrp('87', '192.168.87.1', 110)
hsrp('95', '192.168.95.1', 110)
access_interface('eth1/5', '15', 'Mahomes')
access_interface('eth1/6', '87', 'Kelce')
access_interface('eth1/7', '95', 'Jones')
disconnect()
