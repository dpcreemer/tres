locals {
  model_string = file("n9k.yaml")
  model = yamldecode(local.model_string)
}

module "nxos_config" {
  source = "netascode/config/nxos"
  version = ">= 0.1.0"
  model = local.model
}
