###############################################################################
# Bootstrap: create the S3 bucket that holds the main config's Terraform state.
#
# Chicken-and-egg: the state bucket must exist before the main config can use
# an S3 backend. So this tiny config runs with LOCAL state (just this one
# bucket) and creates it once. You rarely touch it again.
#
#   terraform init
#   terraform apply -var state_bucket_name=isaac-sim-tfstate-<unique-suffix>
#
# Then put that bucket name in ../backend.hcl and init the main config.
###############################################################################

terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
  }
  # Local state on purpose — this is what bootstraps the remote state bucket.
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = "isaac-sim"
      ManagedBy = "terraform"
      Purpose   = "tfstate"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "state_bucket_name" {
  description = "Globally-unique S3 bucket name for Terraform state."
  type        = string
}

resource "aws_s3_bucket" "state" {
  bucket = var.state_bucket_name

  # Guard rail: don't let an accidental `terraform destroy` here nuke history.
  lifecycle {
    prevent_destroy = true
  }
}

# Keep every state revision so a bad apply can be rolled back.
resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Encrypt state at rest (SSE-S3 — no KMS key to manage; keep it simple).
resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# State can contain secrets (the teammate's credentials) — never public.
resource "aws_s3_bucket_public_access_block" "state" {
  bucket                  = aws_s3_bucket.state.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

output "state_bucket_name" {
  description = "Put this in ../backend.hcl as `bucket`."
  value       = aws_s3_bucket.state.id
}
