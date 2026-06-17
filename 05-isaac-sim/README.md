# 05 — Isaac Sim on AWS

Infrastructure for running **NVIDIA Isaac Sim** in the cloud for the
team, separate from the simulation-first work in
[`../02-hplc-autosampler/`](../02-hplc-autosampler/). Isaac Sim is
NVIDIA's robotics simulator / synthetic-data generator; this folder is
about *standing up a GPU box to run it on*, cheaply and safely.

## Contents

```
01-deployment/   Terraform + plan for a single GPU server one teammate can
                 start/stop/log-into (but not resize or rebuild). Manual start,
                 automatic 16:00 EST stop. Read 01-deployment/00-plan.md first.
```

## At a glance

- **One** EC2 `g5.xlarge` (NVIDIA A10G) — the smallest instance that runs
  Isaac Sim comfortably; `g4dn.xlarge` (T4) is the cost floor.
- Teammate IAM user **`issac-sim-user-1`**: start / stop / connect only;
  resize, rebuild, and terminate are explicitly denied.
- **Manual start**, **automatic stop at 16:00** New-York time (DST-safe),
  plus on-demand stop whenever they're done.
- Minimal service footprint: **EC2 + IAM + EventBridge Scheduler.**

See [`01-deployment/00-plan.md`](01-deployment/00-plan.md) for the full
rationale (including why EC2 over Lightsail) and
[`01-deployment/README.md`](01-deployment/README.md) for the run book.

> Cost/spec figures in these files are approximate (`~`) and drift —
> re-check current EC2 pricing and Isaac Sim system requirements before
> quoting.
