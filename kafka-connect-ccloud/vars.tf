variable confluent_environment {
  description = "ID of confluent environment"
  type        = string
}

variable confluent_cluster {
  description = "ID of confluent cluster"
  type        = string
}

variable connectors {
  description = "Map of connector configurations keyed by connector name"
  type = map(object({
    config             = optional(map(string), {})
    sensitive_config   = optional(map(string), {})
    gcp_secret_project = optional(string, "")
    gcp_secret_config  = optional(map(string), {})
    status             = optional(string)
    offsets = optional(list(object({
      kafka_partition = number
      kafka_topic     = string
      kafka_offset    = number
    })), [])
  }))
  default = {}
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
