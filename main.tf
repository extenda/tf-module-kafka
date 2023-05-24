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

data "google_secret_manager_secret_version" "kafka_key" {
  provider = google-beta

  count   = (var.kafka_key == "" && var.project_id != "") ? 1 : 0
  project = var.project_id
  secret  = "kafka_cluster_api_key"
}

data "google_secret_manager_secret_version" "kafka_secret" {
  provider = google-beta

  count   = (var.kafka_secret == "" && var.project_id != "") ? 1 : 0
  project = var.project_id
  secret  = "kafka_cluster_api_secret"
}


locals {
  confluent_api_key    = var.confluent_api_key != "" ? var.confluent_api_key : data.google_secret_manager_secret_version.confluent_api_key[0].secret_data
  confluent_api_secret = var.confluent_api_secret != "" ? var.confluent_api_secret : data.google_secret_manager_secret_version.confluent_api_secret[0].secret_data
  kafka_api_key        = var.kafka_key != "" ? var.kafka_key : data.google_secret_manager_secret_version.kafka_key[0].secret_data
  kafka_api_secret     = var.kafka_secret != "" ? var.kafka_secret : data.google_secret_manager_secret_version.kafka_secret[0].secret_data
}

provider "confluent" {
  cloud_api_key       = local.confluent_api_key
  cloud_api_secret    = local.confluent_api_secret
  kafka_api_key       = local.kafka_api_key
  kafka_api_secret    = local.kafka_api_secret
  kafka_id            = var.kafka_id
  kafka_rest_endpoint = var.kafka_rest_endpoint
}

resource "confluent_kafka_topic" "topic" {
  for_each = { for topic in var.topics : topic.name => topic }

  topic_name       = each.value.name
  partitions_count = each.value.partitions
  config           = each.value.config

  lifecycle {
    prevent_destroy = false
  }
}

resource "confluent_kafka_acl" "acl" {
  count = length(var.acls)

  resource_name = var.acls[count.index].resource_name
  resource_type = var.acls[count.index].resource_type
  pattern_type  = var.acls[count.index].pattern_type
  principal     = var.acls[count.index].principal
  host          = var.acls[count.index].host
  operation     = var.acls[count.index].operation
  permission    = var.acls[count.index].permission

  lifecycle {
    prevent_destroy = false
  }
}
