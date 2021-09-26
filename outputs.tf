output "kafka_url" {
  description = "URL of the kafka cluster"
  value       = local.bootstrap_servers
  sensitive   = true
}

output "key" {
  description = "API Key for the Kafka cluster"
  value       = local.kafka_key
  sensitive   = true
}

output "secret" {
  description = "API Secret for the Kafka cluster"
  value       = local.kafka_secret
  sensitive   = true
}
