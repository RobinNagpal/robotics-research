# Isaac Sim on AWS — Deployment (run book)

Terraform for a single NVIDIA GPU server that runs **NVIDIA Isaac Sim**,
operated by one teammate (`issac-sim-user-1`) who can start / stop / log
in but **cannot resize or rebuild** it. The teammate **starts it
manually**; it **auto-stops at 16:00 EST** so it never runs overnight.

> The teammate starts the box on demand (see "Day-to-day" below); there
> is no scheduled start. The only schedule is the safety-net stop.

**Read [`00-plan.md`](00-plan.md) first** — it explains the design, the
GPU-instance choice, the IAM allow/deny split, and why EC2 over
Lightsail. This file is just the commands.

## What gets created

- 1 × EC2 `g5.xlarge` (NVIDIA A10G) Ubuntu 22.04 GPU instance
- IAM user `issac-sim-user-1` + scoped start/stop/connect policy
- 1 × EventBridge Scheduler schedule (auto **stop** 16:00 NY; start is manual)
- A security group + break-glass key pair

Services involved: **EC2, IAM, EventBridge Scheduler.** Nothing else.

## Files

| File | What |
|------|------|
| `00-plan.md` | The detailed plan — start here |
| `versions.tf` | Terraform + AWS provider pins, default tags |
| `variables.tf` | All inputs (only `allowed_ssh_cidr` is required) |
| `main.tf` | The GPU instance, SG, AMI lookup, key pair |
| `iam.tf` | Teammate user + allow/deny operator policy |
| `scheduler.tf` | 16:00 auto-stop schedule + role (manual start) |
| `outputs.tf` | Instance id/IP + teammate credentials (sensitive) |
| `scripts/bootstrap.sh` | First-boot NVIDIA driver install |
| `terraform.tfvars.example` | Copy to `terraform.tfvars` and edit |

## Prerequisites

- Terraform ≥ 1.5 and AWS credentials (you, the admin) with rights to
  create EC2/IAM/Scheduler resources.
- An SSH keypair for break-glass access:
  ```bash
  ssh-keygen -t ed25519 -f ~/.ssh/isaac-sim-key -C isaac-sim
  ```
- Your teammate's public IP (for the firewall): `curl ifconfig.me`

## Deploy

```bash
cd 05-isaac-sim/01-deployment
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars: set allowed_ssh_cidr to "<their-ip>/32"

terraform init
terraform plan
terraform apply
```

## Hand off to the teammate

```bash
terraform output iam_user_name
terraform output -raw iam_user_initial_password   # they reset on first login
terraform output -raw iam_access_key_id
terraform output -raw iam_secret_access_key
```

Give them these over a secure channel. Console sign-in URL is
`https://<account-id>.signin.aws.amazon.com/console`.

## Day-to-day (what the teammate can do)

Start / stop on demand (also works from the EC2 console buttons):

```bash
aws ec2 start-instances --instance-ids <instance_id>
aws ec2 stop-instances  --instance-ids <instance_id>
aws ec2 describe-instances --instance-ids <instance_id> \
  --query 'Reservations[].Instances[].State.Name' --output text
```

Connect (EC2 Instance Connect — no shared key needed):

```bash
aws ec2-instance-connect send-ssh-public-key \
  --instance-id <instance_id> --instance-os-user ubuntu \
  --ssh-public-key file://~/.ssh/isaac-sim-key.pub
ssh ubuntu@<public-ip>
```

They have full `sudo` on the box (OS updates, package installs) but the
IAM policy blocks resize / rebuild / terminate — try
`aws ec2 modify-instance-attribute ...` and it returns
`AccessDenied`, by design.

## Install Isaac Sim (one-time, on the box)

The driver is installed at first boot; Isaac Sim itself is installed by
the teammate after logging in. Two common paths:

1. **Container (simplest):** uncomment the Docker / NVIDIA Container
   Toolkit block in `scripts/bootstrap.sh` (or install it by hand), then
   pull and run the Isaac Sim container from NVIDIA NGC per NVIDIA's
   current instructions.
2. **Omniverse / native:** download the Isaac Sim package from NVIDIA and
   run headless or via NICE DCV (port 8443 is already open to
   `allowed_ssh_cidr`) for the GUI.

Check the GPU is live: `nvidia-smi`.

> Isaac Sim install steps and asset downloads are licence-gated and
> change often — follow NVIDIA's current docs rather than pinning
> commands here.

## Tear down

```bash
terraform destroy
```

This deletes the instance **and its root volume** — back up any scenes
or assets first (see plan §9 on persistent storage).
