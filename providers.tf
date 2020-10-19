terraform {
  required_providers {
    kafka = {
      source  = "Mongey/kafka"
      version = "0.2.10"
    }
    google-beta = {
      source = "hashicorp/google-beta"
    }
  }
}
