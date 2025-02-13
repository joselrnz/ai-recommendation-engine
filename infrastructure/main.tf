# VPC Module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "ai-recommendation-vpc"
  cidr = var.vpc_cidr

  azs             = ["us-east-1a", "us-east-1b"]
  public_subnets  = var.public_subnets
  private_subnets = var.private_subnets

  enable_nat_gateway = true
  enable_vpn_gateway = false
}

# EKS Cluster
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "20.0.0"

  cluster_name    = var.eks_cluster_name
  cluster_version = "1.27"
  vpc_id         = module.vpc.vpc_id
  subnet_ids     = module.vpc.private_subnets

  enable_irsa    = true
}

# RDS Database
module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.0.0"

  identifier            = "ai-recommendation-db"
  engine               = "postgres"
  engine_version       = "14.2"
  instance_class       = var.db_instance_class
  allocated_storage    = 20
  db_name              = var.db_name
  username            = "admin"
  password            = "password123"  # Replace with AWS Secrets Manager
  subnet_ids         = module.vpc.private_subnets
  vpc_security_group_ids = [module.vpc.default_security_group_id]
}

# S3 Bucket
module "s3" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "4.0.0"

  bucket        = var.s3_bucket_name
  force_destroy = true
}

# API Gateway and Lambda
module "api_gateway" {
  source  = "terraform-aws-modules/api-gateway/aws"
  version = "3.0.0"

  name          = "ai-recommendation-api"
  description   = "API for AI Recommendation Engine"
  endpoint_type = "REGIONAL"
}

# AWS Glue
module "glue" {
  source  = "terraform-aws-modules/glue/aws"
  version = "1.0.0"

  database_name = "ai_recommendation"
}

# Amazon Personalize
module "personalize" {
  source  = "terraform-aws-modules/personalize/aws"
  version = "1.0.0"

  dataset_group_name = "recommendation-group"
}
