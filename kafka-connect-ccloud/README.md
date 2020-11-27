## Description

This is Terraform module for creating kafka-connect connections in Confluent Cloud

Native Terraform Kafka-connect module can't authenticate, thats why this module was created.
It uses [shell](https://github.com/scottwinkler/terraform-provider-shell) provider and wrap `ccloud` commands for creating and deleting connections.

Example of `connection_config` and `connection_sensitive_config` for create managed sink to Elasticsearch:

```json
"connection_config": {
    "topics": "pnp.external.output.products.0",
    "name": "sink-products-elastic"
    "connector.class": "ElasticsearchSink",
    "input.data.format": "AVRO",
    "connection.url": "https://2c462688f1144c6e836ca9e83674b1f9.europe-west3.gcp.cloud.es.io:9243",
    "type.name": "pnp.external.output.products.0",
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
    "connection.username": "**************",
    "connection.password": "**************",
}

```


## Requirements

| Name | Version |
|------|---------|
| shell | 1.7.3 |

## Providers

| Name | Version |
|------|---------|
| google-beta | n/a |
| shell | 1.7.3 |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| confluent\_cluster | ID of confluent cluster | `string` | n/a | yes |
| confluent\_environment | ID of confluent environment | `string` | n/a | yes |
| confluent\_password | Confluentcloud password or GCP secretname to extract password if var.confluent\_project\_gcp\_secret provided | `string` | `"confluent-password"` | no |
| confluent\_project\_gcp\_secret | GCP project ID having secret for confluentcloud credentials | `string` | `"tf-admin-90301274"` | no |
| confluent\_username | Confluentcloud username or GCP secretname to extract username if var.confluent\_project\_gcp\_secret provided | `string` | `"confluent-username"` | no |
| connection\_sensitive\_config | Map of connection configuration with sensitive data | `map(string)` | n/a | yes |
| connection\_config | Map of connection configuration | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| connection\_id | Connection ID |

