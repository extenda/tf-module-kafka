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

data "google_secret_manager_secret_version" "connection_secret_config" {
  provider = google-beta

  for_each = var.connection_gcp_secret_config
  project  = var.connection_gcp_secret_project
  secret   = each.value
}

locals {
  confluent_api_key    = var.confluent_api_key != "" ? var.confluent_api_key : data.google_secret_manager_secret_version.confluent_api_key[0].secret_data
  confluent_api_secret = var.confluent_api_secret != "" ? var.confluent_api_secret : data.google_secret_manager_secret_version.confluent_api_secret[0].secret_data
}

provider "confluent" {
  cloud_api_key    = local.confluent_api_key
  cloud_api_secret = local.confluent_api_secret
}

resource "confluent_connector" "connector" {
  environment {
    id = var.confluent_environment
  }
  kafka_cluster {
    id = var.confluent_cluster
  }

  // Block for custom *sensitive* configuration properties that are labelled with "Type: password" under "Configuration Properties" section in the docs:
  // https://docs.confluent.io/cloud/current/connectors/cc-elasticsearch-service-sink.html#configuration-properties
  config_sensitive = merge(
    var.connection_sensitive_config,
    {
      for k, v in var.connection_gcp_secret_config : k => data.google_secret_manager_secret_version.connection_secret_config[k].secret_data
    }
  )

  // Block for custom *nonsensitive* configuration properties that are *not* labelled with "Type: password" under "Configuration Properties" section in the docs:
  // https://docs.confluent.io/cloud/current/connectors/cc-elasticsearch-service-sink.html#configuration-properties
  config_nonsensitive = var.connection_config

  lifecycle {
    prevent_destroy = false
  }
}
