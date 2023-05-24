variable project_id {
  description = "The ID of the project in which Kafka secrets stored (if no kafka credentials provided)"
  type        = string
  default     = ""
}

variable kafka_key {
  description = "API Key for the Kafka cluster"
  type        = string
  default     = ""
}

variable kafka_secret {
  description = "API Secret for the Kafka cluster"
  type        = string
  default     = ""
}

variable topics {
  description = "Kafka topic list"
  type        = any
}

variable acls {
  description = "Kafka ACL list"
  type        = any
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

variable kafka_id {
  description = "The ID the the Kafka cluster of the form 'lkc-'"
  type        = string
  default     = ""
}

variable kafka_rest_endpoint {
  description = "The REST Endpoint of the Kafka cluster"
  type        = string
  default     = ""
}
