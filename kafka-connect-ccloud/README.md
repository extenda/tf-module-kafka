## Description

This is Terraform module for creating kafka-connect connections in Confluent Cloud


Example of `connection_config` and `connection_sensitive_config` for create managed sink to Elasticsearch:

```json
"connection_config": {
    "topics": "pnp.external.output.products.0",
    "name": "sink-products-elastic"
    "connector.class": "ElasticsearchSink",
    "input.data.format": "AVRO",
    "connection.url": "https://2c462688f1144c6e836ca9e83674b1f9.europe-west3.gcp.cloud.es.io:9243",
    "type.name": "pnp.external.output.products.0",
    "connection.username": "elastic",
    "key.ignore": "false",
    "schema.ignore": "true",
    "compact.map.entries": "true",
    "behavior.on.null.values": "delete",
    "drop.invalid.message": "false",
    "auto.create.indices.at.start": "true",
    "tasks.max": "1",
}

"connection_sensitive_config": {
    "kafka.api.key": "***********",
    "kafka.api.secret": "*********************************************************",
    "connection.password": "**************",
}
```

## Requirements

## Providers

| Name | Version |
|------|---------|
| google-beta | n/a |
| confluentinc/confluent | 1.25.0 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| confluent\_api\_key | Cloud API key to control access to Confluent Cloud resources | `string` | `""` | no |
| confluent\_api\_secret | Cloud API secret to control access to Confluent Cloud resources | `string` | `""` | no |
| confluent\_cluster | ID of confluent cluster | `string` | n/a | yes |
| confluent\_environment | ID of confluent environment | `string` | n/a | yes |
| connection\_config | Map of connection configuration | `map(string)` | `{}` | no |
| connection\_gcp\_secret\_config | Map of connection configuration with gcp secret names, from which values are taken | `map(string)` | `{}` | no |
| connection\_gcp\_secret\_project | GCP project ID having secrets for connection\_gcp\_secret\_config | `string` | `""` | no |
| connection\_sensitive\_config | Map of connection configuration with sensitive data | `map(string)` | `{}` | no |
| project\_id | The ID of the project in which Kafka secrets stored (if no kafka credentials provided) | `string` | `""` | no |
| status | (Optional String) The status of the connector (one of `NONE`, `PROVISIONING`, `RUNNING`, `DEGRADED`, `FAILED`, `PAUSED`, `DELETED`). Pausing (`RUNNING` -> `PAUSED`) and resuming (`PAUSED` -> `RUNNING`) a connector is supported via an update operation. | `string` | `null` | no |

## Outputs

| Name | Description |
|------|-------------|
| connection\_id | Connection ID |

