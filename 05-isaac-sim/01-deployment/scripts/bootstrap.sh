#!/bin/bash
###############################################################################
# First-boot bootstrap for the Isaac Sim GPU server.
#
# Installs the NVIDIA driver so the A10G/T4/L4 is usable. It does NOT install
# Isaac Sim itself — that download is large and licence-gated, so the teammate
# does it after logging in (see ../README.md). Keeping it out of Terraform
# keeps apply fast and avoids baking credentials into user_data.
###############################################################################
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get upgrade -y
apt-get install -y build-essential gcc make linux-headers-"$(uname -r)" \
  ubuntu-drivers-common curl ca-certificates

# Install the recommended NVIDIA driver for the attached GPU.
ubuntu-drivers autoinstall

# Optional: Docker + NVIDIA Container Toolkit, the easiest way to run the
# Isaac Sim container after reboot. Commented out — uncomment if you want the
# container path ready on first boot.
#
# install -m0755 -d /etc/apt/keyrings
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
#   | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
# echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] \
#   https://download.docker.com/linux/ubuntu jammy stable" \
#   > /etc/apt/sources.list.d/docker.list
# curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
#   | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
# curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
#   | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
#   > /etc/apt/sources.list.d/nvidia-container-toolkit.list
# apt-get update -y
# apt-get install -y docker.ce nvidia-container-toolkit
# nvidia-ctk runtime configure --runtime=docker
# systemctl restart docker
# usermod -aG docker ubuntu

# The driver needs a reboot to load.
touch /var/log/isaac-bootstrap-done
reboot
