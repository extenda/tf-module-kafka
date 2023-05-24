# tf-module-kafka

## Description

This provider creates topics and ACLs in Kafka cluster.


## Requirements

| Name | Version |
|------|---------|
| confluent | 1.29.0 |


## Providers

| Name | Version |
|------|---------|
| confluent | 1.29.0 |
| google-beta | n/a |


## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| acl\_prevent\_destroy | Set prevent destory lifecycle for the ACLs | `bool` | `true` | no |
| acls | Kafka ACL list | `any` | n/a | yes |
| confluent\_api\_key | Cloud API key to control access to Confluent Cloud resources | `string` | `""` | no |
| confluent\_api\_secret | Cloud API secret to control access to Confluent Cloud resources | `string` | `""` | no |
| kafka\_id | The ID the the Kafka cluster of the form 'lkc-' | `string` | `""` | no |
| kafka\_key | API Key for the Kafka cluster | `string` | `""` | no |
| kafka\_rest\_endpoint | The REST Endpoint of the Kafka cluster | `string` | `""` | no |
| kafka\_secret | API Secret for the Kafka cluster | `string` | `""` | no |
| project\_id | The ID of the project in which Kafka secrets stored (if no kafka credentials provided) | `string` | `""` | no |
| topic\_prevent\_destroy | Set prevent destory lifecycle for the topics | `bool` | `true` | no |
| topics | Kafka topic list | `any` | n/a | yes |


## Outputs

| Name | Description |
|------|-------------|
| confluent\_key | API Key for confluent |
| confluent\_secret | API Secret for confluent |
| kafka\_key | API Key for the Kafka cluster |
| kafka\_secret | API Secret for the Kafka cluster |
