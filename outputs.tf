output "kafka_key" {
  description = "API Key for the Kafka cluster"
  value       = local.kafka_api_key
  sensitive   = true
}

output "kafka_secret" {
  description = "API Secret for the Kafka cluster"
  value       = local.kafka_api_secret
  sensitive   = true
}

output "confluent_key" {
  description = "API Key for confluent"
  value       = local.confluent_api_key
  sensitive   = true
}

output "confluent_secret" {
  description = "API Secret for confluent"
  value       = local.confluent_api_secret
  sensitive   = true
}
