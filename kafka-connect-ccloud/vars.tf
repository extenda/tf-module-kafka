variable confluent_project_gcp_secret {
  description = "GCP project ID having secret for confluentcloud credentials"
  type        = string
  default     = "tf-admin-90301274"
}

variable confluent_username {
  description = "Confluentcloud username or GCP secretname to extract username if var.confluent_project_gcp_secret provided"
  type        = string
  default     = "confluent-username"
}

variable confluent_password {
  description = "Confluentcloud password or GCP secretname to extract password if var.confluent_project_gcp_secret provided"
  type        = string
  default     = "confluent-password"
}


variable confluent_environment {
  description = "ID of confluent environment"
  type        = string
}

variable confluent_cluster {
  description = "ID of confluent cluster"
  type        = string
}


variable connection_config {
  description = "Map of connection configuration"
  type        = map(string)
}

variable connection_sensitive_config {
  description = "Map of connection configuration with sensitive data"
  type        = map(string)
}
