####### Set Hostname #######
resource "nxos_system" "topSystem" {
  name = var.hostname 
}

####### Enable Features #######
resource "nxos_feature_interface_vlan" "interface_vlan" {
  admin_state = "enabled"
}

resource "nxos_feature_hsrp" "hsrp" {
  admin_state = "enabled"
}

####### Create VRF #######
resource "nxos_vrf" "vrf" {
  name = var.vrf
}

####### Create VLANs #######
resource "nxos_bridge_domain" "vlan_net1_vlan" {
  fabric_encap = "vlan-${var.net1_vlan}"
  name = var.net1_name
}

resource "nxos_bridge_domain" "vlan_87" {
  fabric_encap = "vlan-87"
  name = "kelce"
}

resource "nxos_bridge_domain" "vlan_95" {
  fabric_encap = "vlan-95"
  name = "jones"
}

####### Create SVIs #######

########### Net 1 ##
resource "nxos_svi_interface" "svi_net1" {
  interface_id = "vlan${var.net1_vlan}"
  admin_state = "up"
  description = var.net1_name
  mtu = "9216"
  depends_on = [nxos_feature_interface_vlan.interface_vlan]
}

resource "nxos_svi_interface_vrf" "svi_net1_vrf" {
  interface_id = "vlan${var.net1_vlan}"
  vrf_dn = "sys/inst-${var.vrf}"
  depends_on = [nxos_svi_interface.svi_net1]
}

resource "nxos_ipv4_interface" "svi_net1_l3" {
  interface_id = "vlan${var.net1_vlan}"
  vrf = var.vrf
  depends_on = [nxos_svi_interface_vrf.svi_net1_vrf]
}

resource "nxos_ipv4_interface_address" "svi_net1_ip" {
  interface_id = "vlan${var.net1_vlan}"
  vrf = var.vrf
  address = "192.168.${var.net1_vlan}.2/24"
  depends_on = [nxos_ipv4_interface.svi_net1_l3]
}

########### Net 2 ##
resource "nxos_svi_interface" "svi_net2" {
  interface_id = "vlan${var.net2_vlan}"
  admin_state = "up"
  description = var.net2_name
  mtu = "9216"
  depends_on = [nxos_feature_interface_vlan.interface_vlan]
}

resource "nxos_svi_interface_vrf" "svi_net2_vrf" {
  interface_id = "vlan${var.net2_vlan}"
  vrf_dn = "sys/inst-${var.vrf}"
  depends_on = [nxos_svi_interface.svi_net2]
}

resource "nxos_ipv4_interface" "svi_net2_l3" {
  interface_id = "vlan${var.net2_vlan}"
  vrf = var.vrf
  depends_on = [nxos_svi_interface_vrf.svi_net2_vrf]
}

resource "nxos_ipv4_interface_address" "svi_net2_ip" {
  interface_id = "vlan${var.net2_vlan}"
  vrf = var.vrf
  address = "192.168.${var.net2_vlan}.2/24"
  depends_on = [nxos_ipv4_interface.svi_net2_l3]
}

########### net 3 ##
resource "nxos_svi_interface" "svi_net3" {
  interface_id = "vlan${var.net3_vlan}"
  admin_state = "up"
  description = var.net3_name
  mtu = "9216"
  depends_on = [nxos_feature_interface_vlan.interface_vlan]
}

resource "nxos_svi_interface_vrf" "svi_net3_vrf" {
  interface_id = "vlan${var.net3_vlan}"
  vrf_dn = "sys/inst-${var.vrf}"
  depends_on = [nxos_svi_interface.svi_net3]
}

resource "nxos_ipv4_interface" "svi_net3_l3" {
  interface_id = "vlan${var.net3_vlan}"
  vrf = var.vrf
  depends_on = [nxos_svi_interface_vrf.svi_net3_vrf]
}

resource "nxos_ipv4_interface_address" "svi_net3_ip" {
  interface_id = "vlan${var.net3_vlan}"
  vrf = var.vrf
  address = "192.168.${var.net3_vlan}.2/24"
  depends_on = [nxos_ipv4_interface.svi_net3_l3]
}

####### Configure Ethernet Interfaces #######
resource "nxos_physical_interface" "eth1_5" {
  interface_id = "eth1/5"
  layer = "Layer2"
  access_vlan = "vlan-${var.net1_vlan}"
  description = var.net1_name
  admin_state = "up"
}

resource "nxos_physical_interface" "eth1_6" {
  interface_id = "eth1/6"
  layer = "Layer2"
  access_vlan = "vlan-${var.net2_vlan}"
  description = var.net2_name
  admin_state = "up"
}

resource "nxos_physical_interface" "eth1_7" {
  interface_id = "eth1/7"
  layer = "Layer2"
  access_vlan = "vlan-${var.net3_vlan}"
  description = var.net3_name
  admin_state = "up"
}
