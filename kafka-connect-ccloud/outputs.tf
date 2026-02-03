output "connection_ids" {
  description = "Map of connector names to connection IDs"
  value       = { for k, v in confluent_connector.connector : k => v.id }
}
