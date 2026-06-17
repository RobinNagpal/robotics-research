###############################################################################
# The one GPU server. Smallest NVIDIA box that runs Isaac Sim (see 00-plan.md
# §3). Lives in the default VPC to keep the service list tiny.
###############################################################################

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

data "aws_vpc" "default" {
  default = true
}

# Latest Ubuntu 22.04 LTS (Canonical). NVIDIA driver is installed on first
# boot by scripts/bootstrap.sh; Isaac Sim itself is installed manually after
# (large, licence-gated download) — see README.
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_key_pair" "break_glass" {
  key_name   = var.key_pair_name
  public_key = file(var.public_key_path)
}

resource "aws_security_group" "isaac" {
  name        = "isaac-sim-sg"
  description = "Isaac Sim server: SSH + NICE DCV from the teammate only"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  ingress {
    description = "NICE DCV (Isaac Sim remote desktop)"
    from_port   = 8443
    to_port     = 8443
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ssh_cidr]
  }

  egress {
    description = "All outbound (driver + Isaac Sim downloads)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = { Name = "isaac-sim-sg" }
}

resource "aws_instance" "isaac" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.break_glass.key_name
  vpc_security_group_ids = [aws_security_group.isaac.id]
  user_data              = file("${path.module}/scripts/bootstrap.sh")

  root_block_device {
    volume_size           = var.root_volume_size_gb
    volume_type           = "gp3"
    delete_on_termination = true
  }

  tags = {
    Name = "isaac-sim-server"
    Role = "isaac-sim"
  }
}

# Canonical ARN of this one instance — every scoped policy below points here.
locals {
  instance_arn = "arn:aws:ec2:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:instance/${aws_instance.isaac.id}"
}
