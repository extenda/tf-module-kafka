data "google_secret_manager_secret_version" "confluent_api_key" {
  provider = google-beta

  count   = (var.confluent_api_key == "" && var.project_id != "") ? 1 : 0
  project = var.project_id
  secret  = "confluent_api_key"
}

data "google_secret_manager_secret_version" "confluent_api_secret" {
  provider = google-beta

  count   = (var.confluent_api_secret == "" && var.project_id != "") ? 1 : 0
  project = var.project_id
  secret  = "confluent_api_secret"
}

locals {
  confluent_api_key    = var.confluent_api_key != "" ? var.confluent_api_key : data.google_secret_manager_secret_version.confluent_api_key[0].secret_data
  confluent_api_secret = var.confluent_api_secret != "" ? var.confluent_api_secret : data.google_secret_manager_secret_version.confluent_api_secret[0].secret_data

  # Flatten all GCP secret references across all connectors into a single map for lookup
  all_gcp_secrets = merge([
    for name, connector in var.connectors : {
      for config_key, secret_name in connector.gcp_secret_config :
      "${name}/${config_key}" => {
        project     = connector.gcp_secret_project
        secret_name = secret_name
      }
    }
  ]...)
}

provider "confluent" {
  cloud_api_key    = local.confluent_api_key
  cloud_api_secret = local.confluent_api_secret
}

data "google_secret_manager_secret_version" "connection_secret_config" {
  provider = google-beta

  for_each = local.all_gcp_secrets
  project  = each.value.project
  secret   = each.value.secret_name
}

resource "confluent_connector" "connector" {
  for_each = var.connectors

  environment {
    id = var.confluent_environment
  }
  kafka_cluster {
    id = var.confluent_cluster
  }

  config_sensitive = merge(
    each.value.sensitive_config,
    {
      for config_key, secret_name in each.value.gcp_secret_config :
      config_key => data.google_secret_manager_secret_version.connection_secret_config["${each.key}/${config_key}"].secret_data
    }
  )

  config_nonsensitive = each.value.config

  status = each.value.status

  dynamic "offsets" {
    for_each = each.value.offsets
    content {
      partition = jsonencode({
        kafka_partition = offsets.value.kafka_partition
        kafka_topic     = offsets.value.kafka_topic
      })
      offset = jsonencode({
        kafka_offset = offsets.value.kafka_offset
      })
    }
  }

  lifecycle {
    prevent_destroy = false
  }
}
