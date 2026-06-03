# Arms comparison — which arm to simulate first, before buying

> **The question.** We have three candidate arms with full
> implementation notes — the **reBot B601-DM**
> (`03-reBot-implementation/`), the **Elephant myCobot 280**
> (`04-mycobot-280-impl/`), and the **AgileX PiPER**
> (`05-agile-x-piper-impl/`). Which is best **for developing the
> simulated prototype before we spend money on hardware?** This note
> scores them on **30 parameters** through exactly that lens.

> **Disclaimer.** Specs, prices, and especially "tooling readiness as of
> early 2026" drift fast and several are approximate (`~`) or marked
> *verify*. Re-check vendor pages before quoting or buying. This is a
> decision aid, not a datasheet.

---

## How to read this

We are **not** picking the best arm in general — we are picking the best
arm for a **simulate-first, then buy** workflow. That shifts the weight
onto two things most buyers ignore:

1. **Sim-readiness** — can we stand up a working digital twin *now*, with
   little friction (URDF, MoveIt config, Gazebo assets, docs)?
2. **Representativeness** — does the twin actually predict the *real*
   arm's behaviour in a multi-station HPLC cell, so the simulation
   de-risks the purchase rather than misleading us?

Raw capability and price still matter, but they're secondary here.
Remember the architecture is **~90% arm-agnostic** (world, stations,
perception, orchestration, compliance) — so the arm choice really only
moves these two dials plus cost.

Each row names a **"Best for sim-first"** winner; ties are marked. A
weighted tally follows the table.

---

## The 30-parameter comparison

Legend: ✅ = best of the three for this parameter (sim-first lens);
"tie" = no meaningful difference. All figures `~`approximate / *verify*.

### A. Simulation-readiness & software ecosystem (build the twin now)

| # | Parameter | reBot B601-DM | myCobot 280 | AgileX PiPER | Best for sim-first |
|---|-----------|---------------|-------------|--------------|--------------------|
| 1 | Official URDF available | Yes | Yes | Yes | tie |
| 2 | Ready-made **MoveIt 2** config | In development | **Yes, mature** | Partial / *verify* | myCobot ✅ |
| 3 | Ready-made **Gazebo** sim assets | Emerging | **Yes** | Partial / *verify* | myCobot ✅ |
| 4 | `ros2_control` / `gz_ros2_control` path | Workable via URDF | **Well-trodden** | Workable via URDF | myCobot ✅ |
| 5 | ROS 2 maturity / stability | New (2026) | **Years of use** | Native, growing | myCobot ✅ |
| 6 | Pinocchio / kinematics lib support | **Shipped adaptation** | Generic | Generic | reBot ✅ |
| 7 | Isaac Sim / USD path | Being added | Community | Community | reBot ✅ |
| 8 | LeRobot / imitation-learning support | Yes | Community | Yes | reBot / PiPER |
| 9 | Vendor SDK quality | New SDK | **`pymycobot`, mature** | `piper_sdk`, solid | myCobot ✅ |
| 10 | Community size & examples | Tiny (brand new) | **Very large** | Growing | myCobot ✅ |
| 11 | Documentation quality | Launching | **Extensive** | Decent | myCobot ✅ |
| 12 | Openness of assets (HW + SW) | **Fully open HW+SW** | Open SW | Open SW | reBot ✅ |
| 13 | Time-to-first-sim (lowest friction) | Higher | **Lowest** | Medium | myCobot ✅ |
| 14 | Multi-simulator breadth (Gazebo/MuJoCo/Isaac) | Isaac-leaning | Gazebo-strong | Gazebo/Isaac (community) | tie |

### B. Hardware realism & representativeness (will the twin transfer?)

| # | Parameter | reBot B601-DM | myCobot 280 | AgileX PiPER | Best for sim-first |
|---|-----------|---------------|-------------|--------------|--------------------|
| 15 | Degrees of freedom | 6 (+gripper) | 6 | 6 | tie |
| 16 | Reach / working radius | **~767 mm** | ~280 mm | ~600 mm | reBot ✅ |
| 17 | Payload | ~1.5 kg | ~0.25 kg | ~1.5 kg | reBot / PiPER |
| 18 | Repeatability (stated) | **~0.2 mm** | ~±0.5 mm | sub-mm / *verify* | reBot ✅ |
| 19 | Reaches a full autosampler tray **+** stations | **Yes** | **No** (too short) | **Yes** | reBot / PiPER |
| 20 | Bench footprint vs cell needs | Suits a cell | Desk-only | Suits a cell | reBot / PiPER |
| 21 | Gripper / end-effector ecosystem | Gripper included | **Many options** | Gripper included | myCobot ✅ |
| 22 | Tool-changer support | Limited | Limited | Limited | tie (none strong) |
| 23 | Control interface (real arm) | Serial/CAN *(verify)* | USB/serial | **CAN bus** (robust) | PiPER ✅ |
| 24 | Speed / cycle-time potential | Good | Modest (small) | Good | reBot / PiPER |
| 25 | Rigidity for precise slot insertion | Good | Light/flexy | Good | reBot / PiPER |

### C. Cost, availability & purchase risk

| # | Parameter | reBot B601-DM | myCobot 280 | AgileX PiPER | Best for sim-first |
|---|-----------|---------------|-------------|--------------|--------------------|
| 26 | Arm purchase price | ~$1,499 | **~$700** | ~$1.5–2.5k | myCobot ✅ |
| 27 | Cost incl. gripper + accessories | Mid | **Lowest** | Mid | myCobot ✅ |
| 28 | Availability / ease to buy now | New / pre-order | **Widely available** | Available | myCobot ✅ |
| 29 | **Sim-to-real transfer fidelity** (twin → arm you'd deploy) | Good (if tooling matures) | Poor (reach gap) | **Best balance** | PiPER ✅ |
| 30 | **Representativeness for a real HPLC cell** | Yes | No | **Yes, affordably** | PiPER ✅ |

---

## Scoring

**Raw tally of "best" marks** (ties not counted): myCobot **~11**,
reBot **~6**, PiPER **~4**. On a naive count the myCobot 280 looks like
the winner — *because* it dominates the "start a sim today, cheaply"
rows. But that count under-weights the two rows that decide whether the
exercise was worth doing (#29–#30, transfer & representativeness), where
the myCobot loses badly on reach.

**Weighted score** (0–5 per category, weights tuned for *simulate-first,
then buy*):

| Category (weight) | reBot | myCobot 280 | PiPER |
|-------------------|:----:|:----:|:----:|
| Sim-readiness today (30%) | 3.0 | **5.0** | 3.5 |
| Representativeness / transfer (30%) | 4.5 | 2.0 | **5.0** |
| Cost / availability / risk (20%) | 3.5 | **5.0** | 4.0 |
| Raw capability / specs (20%) | **5.0** | 2.5 | 4.5 |
| **Weighted total** | **3.95** | 3.60 | **4.25** |

PiPER comes out on top, reBot second, myCobot third — *under this
weighting*. Note the ranking is weight-sensitive: if you value "fastest
cheapest start" over "twin that transfers," push the first and third
category weights up and the **myCobot 280 wins instead**.

---

## Verdict

**Best overall for developing the prototype before buying: the
AgileX PiPER.** It is the only candidate that is **both** representative
of a deployable multi-station HPLC cell (~600 mm reach, ~1.5 kg payload,
reaches a full tray) **and** ROS-2-native and cheap enough (~$1.5–2.5k)
that the purchase you de-risk in sim is the purchase you actually make.
The twin you build means something. *Caveat:* confirm its MoveIt 2 /
Gazebo asset maturity — if not ready, generate a MoveIt config from the
URDF (a standard, ~half-day task).

**Pick the myCobot 280 instead if** your priority is *getting a sim
running this week with zero friction* (its `mycobot_ros` ships Gazebo +
MoveIt today) and lowest cost — accepting that its ~280 mm reach means
the layout won't transfer to a real cell, so you'd re-do the geometry on
a bigger arm later.

**Pick the reBot B601-DM if** you want the best raw reach/payload/
repeatability and fully open hardware, and you're willing to absorb more
setup friction while its official MoveIt/Gazebo/Isaac tooling matures.

**The pragmatic play** (since the stack is ~90% arm-agnostic): start the
toolchain **today on the myCobot 280 assets** (or a rock-solid UR5e URDF)
to prove the prep→load loop *logic*, then **swap in the PiPER URDF** for
the reachability/cycle-time/layout decisions, and **buy the PiPER** for
bench validation.

---

## See also

- Per-arm simulation notes: [`03-reBot-implementation/`](03-reBot-implementation/README.md),
  [`04-mycobot-280-impl/`](04-mycobot-280-impl/README.md),
  [`05-agile-x-piper-impl/`](05-agile-x-piper-impl/README.md)
- The problem & solution being simulated:
  [`01-high-level-solution/`](01-high-level-solution/README.md)
