data "google_secret_manager_secret_version" "kafka_url" {
  provider = google-beta

  count   = (var.kafka_url == "" && var.project_id != "") ? 1 : 0
  project = var.project_id
  secret  = "kafka_url"
}

data "google_secret_manager_secret_version" "kafka_key" {
  provider = google-beta

  count   = (var.kafka_key == "" && var.project_id != "") ? 1 : 0
  project = var.project_id
  secret  = "kafka_key"
}

data "google_secret_manager_secret_version" "kafka_secret" {
  provider = google-beta

  count   = (var.kafka_secret == "" && var.project_id != "") ? 1 : 0
  project = var.project_id
  secret  = "kafka_secret"
}


locals {
  bootstrap_servers = split(",", var.kafka_url != "" ? var.kafka_url : data.google_secret_manager_secret_version.kafka_url[0].secret_data)
  kafka_key         = var.kafka_key != "" ? var.kafka_key : data.google_secret_manager_secret_version.kafka_key[0].secret_data
  kafka_secret      = var.kafka_secret != "" ? var.kafka_secret : data.google_secret_manager_secret_version.kafka_secret[0].secret_data
}

provider "kafka" {
  bootstrap_servers = local.bootstrap_servers

  tls_enabled    = true
  sasl_username  = local.kafka_key
  sasl_password  = local.kafka_secret
  sasl_mechanism = "plain"
  timeout        = 2
}

resource "kafka_topic" "topic" {
  for_each = { for topic in var.topics : topic.name => topic }

  name               = each.value.name
  replication_factor = each.value.replication_factor
  partitions         = each.value.partitions
  config             = each.value.config
}

resource "kafka_acl" "acl" {
  count = length(var.topics)

  resource_name       = var.acls[count.index].resource_name
  resource_type       = var.acls[count.index].resource_type
  acl_principal       = var.acls[count.index].acl_principal
  acl_host            = var.acls[count.index].acl_host
  acl_operation       = var.acls[count.index].acl_operation
  acl_permission_type = var.acls[count.index].acl_permission_type
}
