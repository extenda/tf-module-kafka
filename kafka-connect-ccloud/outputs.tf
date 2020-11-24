output "connection_id" {
  description = "Connection ID"
  value       = shell_script.connection.output["id"]
}
