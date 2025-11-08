# tf-module-kafka

## Description

This Terraform module provides resources for managing Kafka infrastructure in Confluent Cloud:

- **Main module**: Creates topics and ACLs in Kafka cluster
- **kafka-connect-ccloud submodule**: Creates and manages Kafka Connect connectors with advanced features including offset configuration


## Requirements

| Name | Version |
|------|---------|
| confluent | 2.51.0 |


## Providers

| Name | Version |
|------|---------|
| confluent | 2.51.0 |
| google-beta | n/a |


## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| acls | Kafka ACL list | `any` | n/a | yes |
| confluent\_api\_key | Cloud API key to control access to Confluent Cloud resources | `string` | `""` | no |
| confluent\_api\_secret | Cloud API secret to control access to Confluent Cloud resources | `string` | `""` | no |
| kafka\_id | The ID the the Kafka cluster of the form 'lkc-' | `string` | `""` | no |
| kafka\_key | API Key for the Kafka cluster | `string` | `""` | no |
| kafka\_rest\_endpoint | The REST Endpoint of the Kafka cluster | `string` | `""` | no |
| kafka\_secret | API Secret for the Kafka cluster | `string` | `""` | no |
| project\_id | The ID of the project in which Kafka secrets stored (if no kafka credentials provided) | `string` | `""` | no |
| topics | Kafka topic list | `any` | n/a | yes |


## Outputs

| Name | Description |
|------|-------------|
| confluent\_key | API Key for confluent |
| confluent\_secret | API Secret for confluent |
| kafka\_key | API Key for the Kafka cluster |
| kafka\_secret | API Secret for the Kafka cluster |

## Submodules

### kafka-connect-ccloud

A submodule for managing Kafka Connect connectors in Confluent Cloud.

**Features:**
- Connector configuration with sensitive and non-sensitive properties
- GCP Secret Manager integration for secure credential management
- **Offset configuration support** - Set specific partition offsets for connector replay scenarios

**Usage:**
```hcl
module "kafka_connector" {
  source = "./kafka-connect-ccloud"
  
  confluent_environment = "env-abc123"
  confluent_cluster     = "lkc-abc123"
  
  connection_config = {
    "connector.class" = "ElasticsearchSink"
    "topics"         = "my-topic"
    # ... other config
  }
  
  # Optional: Configure connector offsets for replay scenarios
  offsets = [
    {
      kafka_partition = 0
      kafka_topic     = "my-topic"
      kafka_offset    = 1000000
    }
  ]
}
```

For detailed documentation, see [kafka-connect-ccloud/README.md](./kafka-connect-ccloud/README.md).

## Changelog

### v3.0.0
- **BREAKING CHANGE**: Upgraded Confluent provider from 1.x to 2.51.0
- **NEW FEATURE**: Added offset configuration support in kafka-connect-ccloud module
- Added comprehensive .gitignore for Terraform projects
- Updated documentation with usage examples

### Previous versions
See git tags for historical releases.
