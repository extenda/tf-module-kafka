# tf-module-kafka

## Description

This provider creates topics and ACLs in Kafka cluster.


## Requirements

| Name | Version |
|------|---------|
| kafka | 0.2.10 |

## Providers

| Name | Version |
|------|---------|
| google-beta | n/a |
| kafka | 0.2.10 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| kafka\_url | URL of the kafka cluster (comma-separated list of kafka bootstrap servers) | `string` | `""` | no |
| kafka\_key | API Key for the Kafka cluster | `string` | `""` | no |
| kafka\_secret | API Secret for the Kafka cluster | `string` | `""` | no |
| project\_id | The ID of the project in which Kafka secrets stored (if no kafka credentials provided) | `string` | n/a | no |
| topics | Kafka topic list | `any` | n/a | yes |
| acls | Kafka ACL list | `any` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| kafka\_url | URL of the kafka cluster |
| key | API Key for the Kafka cluster |
| secret | API Secret for the Kafka cluster |

