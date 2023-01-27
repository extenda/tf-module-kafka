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
  default     = {}
}

variable connection_sensitive_config {
  description = "Map of connection configuration with sensitive data"
  type        = map(string)
  default     = {}
}

variable confluent_api_key {
  description = "Cloud API key to control access to Confluent Cloud resources"
  type        = string
  default     = ""
}

variable confluent_api_secret {
  description = "Cloud API secret to control access to Confluent Cloud resources"
  type        = string
  default     = ""
  sensitive   = true
}

variable project_id {
  description = "The ID of the project in which Kafka secrets stored (if no kafka credentials provided)"
  type        = string
  default     = ""
}

variable connection_gcp_secret_project {
  description = "GCP project ID having secrets for connection_gcp_secret_config"
  type        = string
  default     = ""
}

variable connection_gcp_secret_config {
  description = "Map of connection configuration with gcp secret names, from which values are taken"
  type        = map(string)
  default     = {}
}
