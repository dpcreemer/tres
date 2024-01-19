####### Set Hostname #######
resource "nxos_system" "topSystem" {
  name = "tres-terraform"
}

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
  depends_on = [nxos_feature_interface_vlan.interface_vlan]
}

resource "nxos_svi_interface" "svi87" {
  interface_id = "vlan87"
  admin_state = "up"
  description = "kelce"
  depends_on = [nxos_feature_interface_vlan.interface_vlan]
}

resource "nxos_svi_interface" "svi95" {
  interface_id = "vlan95"
  admin_state = "up"
  description = "jones"
  depends_on = [nxos_feature_interface_vlan.interface_vlan]
}

####### Add SVIs to VRF ####### 
resource "nxos_svi_interface_vrf" "svi15_vrf" {
  interface_id = "vlan15"
  vrf_dn = "sys/inst-chiefs"
  depends_on = [nxos_svi_interface.svi15]
}

resource "nxos_svi_interface_vrf" "svi87_vrf" {
  interface_id = "vlan87"
  vrf_dn = "sys/inst-chiefs"
  depends_on = [nxos_svi_interface.svi87]
}

resource "nxos_svi_interface_vrf" "svi95_vrf" {
  interface_id = "vlan95"
  vrf_dn = "sys/inst-chiefs"
  depends_on = [nxos_svi_interface.svi95]
}

####### Add VRF to SVI #######
resource "nxos_ipv4_interface" "svi15_l3" {
  interface_id = "vlan15"
  vrf = "chiefs"
  depends_on = [nxos_svi_interface_vrf.svi15_vrf]
}

resource "nxos_ipv4_interface" "svi87_l3" {
  interface_id = "vlan87"
  vrf = "chiefs"
  depends_on = [nxos_svi_interface_vrf.svi87_vrf]
}

resource "nxos_ipv4_interface" "svi95_l3" {
  interface_id = "vlan95"
  vrf = "chiefs"
  depends_on = [nxos_svi_interface_vrf.svi95_vrf]
}

####### Add IP addresses to SVI #######
resource "nxos_ipv4_interface_address" "svi15_ip" {
  interface_id = "vlan15"
  vrf = "chiefs"
  address = "192.168.15.2/24"
  depends_on = [nxos_ipv4_interface.svi15_l3]
}

resource "nxos_ipv4_interface_address" "svi87_ip" {
  interface_id = "vlan87"
  vrf = "chiefs"
  address = "192.168.87.2/24"
  depends_on = [nxos_ipv4_interface.svi87_l3]
}

resource "nxos_ipv4_interface_address" "svi95_ip" {
  interface_id = "vlan95"
  vrf = "chiefs"
  address = "192.168.95.2/24"
  depends_on = [nxos_ipv4_interface.svi95_l3]
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
