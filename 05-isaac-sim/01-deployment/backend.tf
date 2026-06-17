###############################################################################
# Remote Terraform state in S3, with native state locking (use_lockfile —
# requires Terraform >= 1.10, so no separate DynamoDB lock table).
#
# This uses PARTIAL configuration: the block is intentionally empty here and
# the real values live in backend.hcl (gitignored) so the globally-unique
# bucket name stays out of version control.
#
# One-time setup (see README "Remote state"):
#   1. cd bootstrap && terraform init && terraform apply   # creates the bucket
#   2. cp backend.hcl.example backend.hcl ; edit the bucket name
#   3. terraform init -backend-config=backend.hcl          # back in this dir
###############################################################################
terraform {
  backend "s3" {
    # bucket, key, region, encrypt, use_lockfile all come from backend.hcl
  }
}
