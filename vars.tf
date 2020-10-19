variable project_id {
  description = "The ID of the project in which Kafka secrets stored (if no kafka credentials provided)"
  type        = string
  default     = ""
}

variable kafka_url {
  description = "URL of the kafka cluster (comma-separated list of kafka bootstrap servers)"
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
