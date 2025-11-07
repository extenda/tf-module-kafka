terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "2.51.0"
    }
    google-beta = {
      source = "hashicorp/google-beta"
    }
  }
}
