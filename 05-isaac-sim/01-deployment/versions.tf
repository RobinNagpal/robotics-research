terraform {
  # 1.10+ for native S3 state locking (use_lockfile) — no DynamoDB table needed.
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = "isaac-sim"
      ManagedBy = "terraform"
      Owner     = var.iam_user_name
    }
  }
}
