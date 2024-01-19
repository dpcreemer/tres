#!/usr/bin/python3
import nxos 

print("Welcome to the switch configuration tool.")

address = input("Switch address: ")
switch = nxos.Switch(address)

features = {
  'v': 'interface-vlan',
  'h': 'hsrp'
}
feature = ""
while feature.lower() != "q":
  print("\nWhat feature would you like to activate?:")
  for key in list(features.keys()):
    print(f"  {key} - {features[key]}")
  print("  q - Done")
  feature = input("feature: ")
  if feature in list(features.keys()):
    switch.feature(features[feature])

switch.hostname(input('\nhostname: '))

vrf = input('\nVRF: ')

switch.vrf(vrf)

network = "none"
while network != "":
  print("\nCreate a network. (enter a blank name to when done.)")
  network = input("  name: ")
  if network == "": break
  vlan = input("  VLAN id: ")
  ip = input("  IP address: ")
  hsrp_ip = input("  HSRP address: ")
  hsrp_priority = input("  HSRP priority: ")  
  switch.network(network, vlan, ip, vrf)
  switch.hsrp(vlan, hsrp_ip, hsrp_priority)

interface = "none"
while interface != "":
  print("\nConfigure and access interface: (enter a blank line when done.)")
  interface = input("  interface: ")
  if interface == "": break
  vlan = input("  VLAN: ")
  descr = input("  description: ")
  switch.access_interface(interface, vlan, descr)

switch.disconnect()
