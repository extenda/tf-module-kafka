terraform {
  required_providers {
    confluent = {
      source  = "confluentinc/confluent"
      version = "1.25.0"
    }
    google-beta = {
      source = "hashicorp/google-beta"
    }
  }
}
