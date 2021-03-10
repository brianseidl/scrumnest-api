terraform {
  required_version = ">= 0.12"
  backend "s3" {
    key = "scrumnest-api"
  }
}

provider "aws" {
  region = var.region
}
