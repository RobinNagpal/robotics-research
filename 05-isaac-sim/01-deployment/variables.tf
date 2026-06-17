###############################################################################
# Inputs. Sensible defaults everywhere except `allowed_ssh_cidr`, which you
# MUST set (your teammate's public IP) so the box isn't open to the world.
###############################################################################

variable "aws_region" {
  description = "Region to deploy into. us-east-1 = US East, matches the EST schedule."
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = <<-EOT
    Smallest NVIDIA instance that runs Isaac Sim comfortably.
      g5.xlarge  -> A10G 24GB  (recommended default)
      g6.xlarge  -> L4   24GB  (newer, often similar/cheaper)
      g4dn.xlarge-> T4   16GB  (cost floor; light/headless only)
  EOT
  type        = string
  default     = "g5.xlarge"
}

variable "root_volume_size_gb" {
  description = "Root EBS size. Isaac Sim + Omniverse assets are large."
  type        = number
  default     = 250
}

variable "iam_user_name" {
  description = "Teammate's IAM user name. Kept as the literally requested spelling."
  type        = string
  default     = "issac-sim-user-1"
}

variable "allowed_ssh_cidr" {
  description = "CIDR allowed to reach SSH (22) and NICE DCV (8443). Use a /32, e.g. \"203.0.113.4/32\". No default on purpose."
  type        = string
}

variable "key_pair_name" {
  description = "Name for the break-glass EC2 key pair."
  type        = string
  default     = "isaac-sim-key"
}

variable "public_key_path" {
  description = "Path to the public SSH key uploaded as the break-glass key pair."
  type        = string
  default     = "~/.ssh/isaac-sim-key.pub"
}

variable "schedule_start_cron" {
  description = "When to auto-START. Default 06:00, weekdays."
  type        = string
  default     = "cron(0 6 ? * MON-FRI *)"
}

variable "schedule_stop_cron" {
  description = "When to auto-STOP. Default 16:00, weekdays."
  type        = string
  default     = "cron(0 16 ? * MON-FRI *)"
}

variable "schedule_timezone" {
  description = "IANA tz for the schedules. New York = true EST/EDT with automatic DST."
  type        = string
  default     = "America/New_York"
}
