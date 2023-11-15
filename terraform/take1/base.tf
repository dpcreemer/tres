####### Enable features #######
resource "nxos_feature_interface_vlan" "interface_vlan" {
  admin_state = "enabled"
}

resource "nxos_feature_hsrp" "hsrp" {
  admin_state = "enabled"
}

####### Create "Chiefs" VRF #######
resource "nxos_vrf" "vrf_chiefs" {
  name = "chiefs"
  description = "The KC Chiefs"
}

####### Create VLANs #######
resource "nxos_bridge_domain" "vlan15" {
  fabric_encap = "vlan-15"
  access_encap = "unknown"
  name = "mahomes"
}

resource "nxos_bridge_domain" "vlan87" {
  fabric_encap = "vlan-87"
  access_encap = "unknown"
  name = "kelce"
}

resource "nxos_bridge_domain" "vlan95" {
  fabric_encap = "vlan-95"
  access_encap = "unknown"
  name = "jones"
}

####### Create SVIs #######
resource "nxos_svi_interface" "svi15" {
  interface_id = "vlan15"
  admin_state = "up"
  description = "Mahomes"
}

resource "nxos_svi_interface" "svi87" {
  interface_id = "vlan87"
  admin_state = "up"
  description = "kelce"
}

resource "nxos_svi_interface" "svi95" {
  interface_id = "vlan95"
  admin_state = "up"
  description = "jones"
}

####### Add SVIs to VRF ####### 
resource "nxos_svi_interface_vrf" "svi15_vrf" {
  interface_id = "vlan15"
  vrf_dn = "sys/inst-chiefs"
}

resource "nxos_svi_interface_vrf" "svi87_vrf" {
  interface_id = "vlan87"
  vrf_dn = "sys/inst-chiefs"
}

resource "nxos_svi_interface_vrf" "svi95_vrf" {
  interface_id = "vlan95"
  vrf_dn = "sys/inst-chiefs"
}

####### Configure Access Interfaces #######
resource "nxos_physical_interface" "eth1_5" {
  interface_id = "eth1/5"
  mode = "access"
  layer = "Layer2"
  admin_state = "up"
  description = "Mahomes"
  access_vlan = "vlan-15"
}

resource "nxos_physical_interface" "eth1_6" {
  interface_id = "eth1/6"
  mode = "access"
  layer = "Layer2"
  admin_state = "up"
  description = "kelce"
  access_vlan = "vlan-87"
}

resource "nxos_physical_interface" "eth1_7" {
  interface_id = "eth1/7"
  mode = "access"
  layer = "Layer2"
  admin_state = "up"
  description = "jones"
  access_vlan = "vlan-95"
}

