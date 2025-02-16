terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0"
    }
  }

  backend "s3" {
    bucket         = ""
    key            = ""
    region         = "us-east-1"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}
