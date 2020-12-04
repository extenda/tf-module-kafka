data "google_secret_manager_secret_version" "confluent_username" {
  provider = google-beta

  count   = (var.confluent_project_gcp_secret != "") ? 1 : 0
  project = var.confluent_project_gcp_secret
  secret  = var.confluent_username
}

data "google_secret_manager_secret_version" "confluent_password" {
  provider = google-beta

  count   = (var.confluent_project_gcp_secret != "") ? 1 : 0
  project = var.confluent_project_gcp_secret
  secret  = var.confluent_password
}


data "google_secret_manager_secret_version" "connection_secret_config" {
  provider = google-beta

  for_each = var.connection_gcp_secret_config
  project  = var.connection_gcp_secret_project
  secret   = each.value
}

resource "shell_script" "connection" {
  lifecycle_commands {
    create = "python3 ccloud.py create"
    delete = "python3 ccloud.py delete"
    read   = "python3 ccloud.py read"
    update = "python3 ccloud.py update"
  }

  environment = merge(
    {
      CONFLUENT_ENVIRONMENT = var.confluent_environment,
      CONFLUENT_CLUSTER     = var.confluent_cluster,
    },
    { for k, v in var.connection_config : "CONNECTION_${k}" => v }
  )

  sensitive_environment = merge(
    {
      CONFLUENT_USERNAME = (var.confluent_project_gcp_secret != "") ? data.google_secret_manager_secret_version.confluent_username[0].secret_data : var.confluent_username
      CONFLUENT_PASSWORD = (var.confluent_project_gcp_secret != "") ? data.google_secret_manager_secret_version.confluent_password[0].secret_data : var.confluent_password
    },
    { for k, v in var.connection_sensitive_config : "CONNECTION_${k}" => v },
    { for k, v in var.connection_gcp_secret_config : "CONNECTION_${k}" => data.google_secret_manager_secret_version.connection_secret_config[k].secret_data }
  )
}
