# Isaac Sim on AWS — Deployment Plan

> **Status:** plan + Terraform in this folder. Read this first, then
> `README.md` for the run book.
>
> **One-line goal:** give one teammate
> (`issac-sim-user-1`) a single cheap NVIDIA GPU server that runs
> NVIDIA **Isaac Sim**, that they **start manually** and log into on
> demand, that **auto-shuts-down at 16:00 EST** so it never runs
> overnight, and that they **cannot resize, rebuild, or destroy**.

A note on spelling: the product is **Isaac Sim** (one "a", then
"aac"). The request wrote "issac". We keep the *folder* and product
references spelled correctly as **isaac**, but we keep the IAM user
name exactly as requested — `issac-sim-user-1` — so it matches what
you typed and what your teammate will log in as. Change
`var.iam_user_name` if you'd rather fix the spelling.

---

## 1. Requirements, restated

| # | You asked for | How we deliver it |
|---|---------------|-------------------|
| 1 | A user `issac-sim-user-1` for a teammate | IAM user + console login + access keys |
| 1 | Smallest NVIDIA server that can run Isaac Sim | One `g5.xlarge` EC2 instance (NVIDIA A10G, 24 GB) — see §3 |
| 2 | User can **start** the server or **connect** to it | IAM allow on `ec2:StartInstances` / `StopInstances` + EC2 Instance Connect, scoped to this one instance |
| 2 | User **cannot** modify/create the server config or **increase size** | Explicit IAM **Deny** on `RunInstances`, `ModifyInstanceAttribute`, `TerminateInstances`, volume changes, tag changes |
| 2 | User **can** log in and update the OS | OS-level access (SSH / sudo) is independent of IAM — they get a shell, they can `apt upgrade` |
| 3 | Manual start, automatic shutdown | Teammate starts on demand; **one** EventBridge **Scheduler** stop at 16:00, timezone `America/New_York`. No auto-start |
| 4 | Start/stop on demand if needed | Same IAM start/stop rights → console button or one CLI command, any time |
| 5 | Keep it simple, minimal services, Lightsail if possible | EC2 + IAM + EventBridge only. No Lambda, no Instance Scheduler stack. Lightsail rejected — see §2 |

---

## 2. Why EC2 and not Lightsail (the "keep it simple" call)

You asked to prefer **Lightsail**. We looked, and chose **plain EC2**
instead. Honest reasoning:

- **GPU fit.** Isaac Sim is an RTX / Omniverse workload — it needs a
  specific class of NVIDIA GPU (RTX-capable, ray-tracing cores) plus a
  matching NVIDIA driver. EC2's `g5` / `g4dn` families are the
  documented, NVIDIA-blessed path for running Isaac Sim in the cloud.
  Lightsail's GPU plans are newer, fewer, and not documented by NVIDIA
  for Isaac Sim. Picking the platform Isaac Sim is *known* to run on is
  the simpler outcome even if the service name is less "simple".
- **The permission split you want.** Requirement 2 — "can start/stop and
  log in, but cannot resize or rebuild" — is expressed cleanly with
  standard EC2 IAM actions scoped to one instance ARN. Lightsail's IAM
  surface is coarser and would make that allow/deny split harder to
  prove.
- **Scheduling is identical either way.** Neither Lightsail nor EC2 has
  "run 6-to-4" as a built-in toggle. On EC2 we get it with two
  EventBridge Scheduler entries calling the EC2 API directly — **no
  Lambda, no extra moving parts**.

Net: the *service list* stays tiny (EC2 + IAM + EventBridge Scheduler),
and the GPU/driver story is the well-trodden one. That is the simplest
thing that actually works.

> If you specifically want to pilot Lightsail GPU instead, that's a
> swap of `main.tf` only; the IAM and scheduling design carries over.
> Flagged as an open question in §9.

---

## 3. Picking the "smallest NVIDIA server that runs Isaac Sim"

Isaac Sim's published minimum is an RTX GPU with **≥ 8 GB VRAM** (e.g.
RTX 3070 class); NVIDIA recommends more for comfortable use. Mapping
that to the cheapest AWS GPU instances that have RTX-class silicon:

| Instance | GPU | VRAM | vCPU / RAM | ~On-demand /hr (us-east-1) | Isaac Sim fit | Bottom line |
|----------|-----|------|------------|---------------------------|---------------|-------------|
| `g4dn.xlarge` | T4 (Turing) | 16 GB | 4 / 16 GB | ~$0.53 | Runs, but T4 is the floor — sluggish on heavy scenes / RTX rendering | Cheapest that boots Isaac Sim; OK for light/headless work |
| **`g5.xlarge`** | **A10G (Ampere)** | **24 GB** | **4 / 16 GB** | **~$1.01** | **Comfortable; the common "minimum recommended" cloud box** | **Pick this — smallest that runs Isaac Sim *well*** |
| `g6.xlarge` | L4 (Ada) | 24 GB | 4 / 16 GB | ~$0.80 | Newer gen, similar/better than A10G, sometimes cheaper | Good alt if `g5` is constrained or pricier in your AZ |

**Top pick: `g5.xlarge`.** It is the smallest single-GPU instance that
runs Isaac Sim *comfortably* (24 GB VRAM clears Omniverse/RTX headroom),
and it's the size most cloud Isaac Sim guides assume. `g4dn.xlarge` is
the true cost floor if your teammate only does light or headless runs —
it's exposed as `var.instance_type` so switching is a one-line change.
`g6.xlarge` is a fine drop-in if A10G capacity is tight.

> **Prices are approximate and drift** (`~`) — re-check the EC2 pricing
> page before quoting. All three are billed **per second while
> running**; a **stopped** instance costs only its EBS disk (~$20/mo
> for a 250 GB gp3 root). The 6-to-4 schedule is what keeps the bill
> small — see §6.

---

## 4. Architecture

```
                         ┌─────────────────────────────────────────┐
                         │  AWS account / region us-east-1          │
                         │                                          │
   EventBridge          │   ┌──────────────────────────────────┐   │
   Scheduler            │   │  EC2 g5.xlarge "isaac-sim-server" │   │
   ┌──────────┐         │   │  - NVIDIA A10G + driver           │   │
   │ 16:00 ET │  stop   │   │  - Ubuntu 22.04                   │   │
   │  (stop   ├─────────┼──▶│  - 250 GB gp3 root                │   │
   │  only)   │         │   │  - Isaac Sim (installed post-boot)│   │
   └────┬─────┘         │   └──────────────▲───────────────────┘   │
        │ assumes       │                  │ start/stop + connect    │
        ▼               │                  │ (scoped to THIS arn)    │
   scheduler role       │                  │ (manual start by user)  │
   (StopInstances on    │          ┌───────┴────────┐                │
    one instance)       │          │ IAM user        │                │
                         │          │ issac-sim-user-1│                │
                         │          │  ALLOW: start/  │                │
                         │          │   stop/connect  │                │
                         │          │  DENY: resize/  │                │
                         │          │   rebuild/del   │                │
                         │          └────────┬────────┘                │
                         └───────────────────┼─────────────────────────┘
                                              │ SSH / EC2 Instance Connect
                                              ▼
                                       teammate's laptop
                                       (allowed_ssh_cidr)
```

Total AWS services in play: **EC2, IAM, EventBridge Scheduler.** That's
it.

---

## 5. The IAM permission model (requirement 2 in detail)

The teammate's policy (`isaac-sim-operator`, see `iam.tf`) is built as
**allow a short list, then hard-deny the dangerous list**. An explicit
`Deny` always wins, so even a future broad attach can't let them resize.

| Capability | Action(s) | Effect | Scope |
|------------|-----------|--------|-------|
| See the server + its state | `ec2:DescribeInstances`, `DescribeInstanceStatus`, `DescribeInstanceTypes`, `DescribeTags` | **Allow** | `*` (Describe can't be resource-scoped) |
| Start the (stopped) server | `ec2:StartInstances` | **Allow** | this instance ARN only |
| Stop the server | `ec2:StopInstances` | **Allow** | this instance ARN only |
| Connect / get a shell | `ec2-instance-connect:SendSSHPublicKey` (osuser `ubuntu`) | **Allow** | this instance ARN only |
| **Create a new server** | `ec2:RunInstances` | **Deny** | `*` |
| **Resize / change config** | `ec2:ModifyInstanceAttribute`, `ModifyInstanceCreditSpecification` | **Deny** | `*` |
| **Destroy** | `ec2:TerminateInstances` | **Deny** | `*` |
| **Grow / swap disk** | `ec2:ModifyVolume`, `AttachVolume`, `DetachVolume`, `CreateImage` | **Deny** | `*` |
| **Re-tag to escape scoping** | `ec2:CreateTags`, `DeleteTags` | **Deny** | `*` |

Why this satisfies each clause of requirement 2:

- *"start a new server or connect to the running server"* → Start +
  Instance Connect allowed. ("Start a new server" = power on the
  existing stopped box; literally launching new instances is denied so
  costs can't sprawl.)
- *"not modify or create the server configuration"* → `RunInstances`
  and `ModifyInstanceAttribute` denied.
- *"can login and update it"* → SSH shell + `sudo apt upgrade` is
  OS-level, untouched by IAM. They fully own the machine's *software*.
- *"not be able to increase the size"* → changing instance type
  requires `stop → ModifyInstanceAttribute(instanceType) → start`; the
  `ModifyInstanceAttribute` Deny blocks it. Disk growth is denied too.

**Connection method.** Default is **EC2 Instance Connect** (push an
ephemeral SSH key via IAM, then SSH) so there are no long-lived shared
keys and access is fully IAM-governed. A static key pair is also created
for break-glass. For the Isaac Sim **GUI**, install NICE DCV on the box
(port 8443, locked to `allowed_ssh_cidr`) — noted in the README; the
security group already opens that port.

---

## 6. Scheduling — manual start, automatic shutdown (requirements 3 & 4)

The model is **manual on, automatic off**: the teammate powers the box
up only when they need it, and a single scheduled stop guarantees it is
never left running overnight.

- **No auto-start.** Nothing turns the box on for you — that's the point.
  The teammate starts it on demand (console button or one CLI command;
  they already hold `ec2:StartInstances`).
- **One auto-stop**, via **EventBridge Scheduler** (not Lambda, not the
  EC2 Instance Scheduler solution — both are heavier):
  - **stop** — `cron(0 16 ? * MON-FRI *)` → calls `ec2:StopInstances`
- It carries `schedule_expression_timezone = "America/New_York"`, so the
  platform handles **EST↔EDT (daylight saving) automatically** — you
  asked for "EST" and you get true New-York local time year round, no
  manual clock shifts.
- The schedule targets the EC2 API **directly** through the Scheduler
  *universal target* (`arn:aws:scheduler:::aws-sdk:ec2:stopInstances`),
  using a tiny dedicated role that can only **stop** this one instance.
  No function to maintain.
- **Weekdays only** by default (`MON-FRI`). Change to `* * *` in
  `var.schedule_stop_cron` if you want a weekend stop too.
- **On demand (requirement 4):** the teammate also holds
  `ec2:StopInstances`, so they can shut down early themselves whenever
  they're done — the 16:00 stop is the *safety net*, not the only way off.

> Edge cases to know:
> - **Box started after 16:00** (e.g. a 20:00 debugging session): it runs
>   until the teammate stops it, or until the **next** 16:00 stop the
>   following weekday. If you want a hard "auto-off N hours after any
>   manual start" regardless of clock time, that needs a small Lambda —
>   deliberately left out to keep things simple. Flagged in §9.
> - **Box left running from earlier:** the 16:00 stop is idempotent — if
>   it's already stopped, stopping again is a no-op.

---

## 7. Cost sketch (approximate — re-check before quoting)

Assuming `g5.xlarge`, weekdays, and a *worst case* of the teammate
starting early and the box running until the 16:00 auto-stop (~10 h/day):

- Compute: ~$1.01/hr × 10 h × ~22 weekdays ≈ **~$220/mo** (an upper
  bound — manual start means real usage is usually less, since they only
  turn it on when working).
- If left 24/7 it would be ~$730/mo — so the auto-stop saves **~70%**
  even before counting the days they don't start it at all.
- EBS root (250 GB gp3) while stopped/running: **~$20/mo** (always on).
- Elastic IP: none by default (uses the auto-assigned public IP, which
  changes on each stop/start — fine with Instance Connect, which
  resolves by instance ID). Add an EIP only if you need a stable
  address (~$3.6/mo while associated).
- Data egress: pay-as-you-go; small for headless work, larger if you
  stream the DCV desktop.

**Switching to `g4dn.xlarge` roughly halves the compute line** (~$115/mo)
if the teammate's work is light/headless.

---

## 8. Deploy / operate / tear down

Full commands live in `README.md`. In short:

1. `terraform init`
2. Set `allowed_ssh_cidr` (your teammate's IP/32) in
   `terraform.tfvars`; drop their public SSH key at
   `var.public_key_path`.
3. `terraform plan` → `terraform apply`.
4. Hand the teammate the outputs (console password + access keys —
   marked sensitive). They change the password on first login.
5. First boot installs the NVIDIA driver via `scripts/bootstrap.sh`;
   they then install Isaac Sim itself (container or Omniverse launcher)
   — that step is intentionally manual and documented in the README,
   not baked into Terraform (the asset download is large and
   licensing-gated).
6. Tear down: `terraform destroy`.

---

## 9. Open questions / deliberately out of scope

1. **Lightsail GPU pilot** — if you want to try it, it's a `main.tf`
   swap; IAM + scheduling carry over. Say the word.
2. **Auto-off after manual start** — capping a 22:00 ad-hoc session
   automatically needs a small Lambda; left out for simplicity.
3. **Persistent data** — root volume is wiped on `terraform destroy`.
   If Isaac assets/scenes must survive teardown, add a separate EBS
   data volume or S3 sync (not in v1).
4. **Stable IP / DNS** — add an Elastic IP if the teammate wants one
   unchanging address instead of resolving by instance ID.
5. **Spelling** — IAM user kept as literal `issac-sim-user-1`; flip
   `var.iam_user_name` to correct it.

---

*Cost and spec figures above are approximate and drift — hedge (`~`)
and re-check the current EC2 pricing / Isaac Sim system-requirements
pages before quoting them to anyone.*
