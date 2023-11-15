terraform {
  required_providers {
    nxos = {
      source = "ciscodevnet/nxos"
    }
  }
}

provider "nxos" {
  username = "cisco"
  password = "cisco"
  url = "https://198.19.36.167"
}
