#!/usr/bin/python3
import nxos 

switch = nxos.Switch('198.19.36.167', 'cisco', 'cisco')
switch.feature('interface-vlan')
switch.feature('hsrp')
switch.hostname('tres-python')
switch.vrf('chiefs')
switch.network('mahomes', '15', '192.168.15.2/24', 'chiefs')
switch.network('kelce', '87', '192.168.87.2/24', 'chiefs')
switch.network('jones', '95', '192.168.95.2/24', 'chiefs')
switch.hsrp('15', '192.168.15.1', 110)
switch.hsrp('87', '192.168.87.1', 110)
switch.hsrp('95', '192.168.95.1', 110)
switch.access_interface('eth1/5', '15', 'Mahomes')
switch.access_interface('eth1/6', '87', 'Kelce')
switch.access_interface('eth1/7', '95', 'Jones')
switch.close()
