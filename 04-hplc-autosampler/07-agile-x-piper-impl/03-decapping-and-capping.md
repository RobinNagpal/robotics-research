# Part 03 — Decapping & capping (AgileX PiPER simulation)

> **Sim goal:** Prove the *logic and choreography* of opening and
> re-closing a vial with the **AgileX PiPER** arm — present, decap,
> work, recap, verify — without pretending to simulate threaded-cap
> physics, which we deliberately abstract away.

## What we can prove in simulation

Decapping is the hardest *physics* in the whole system (controlled
torque, cross-threading, septum integrity — see the matching
[`../03-high-level-solution/03-decapping-and-capping.md`](../03-high-level-solution/03-decapping-and-capping.md)).
A *septum* is the silicone/PTFE disc in the cap that the sampling
needle later pierces. None of that real physics is honestly
simulatable, so we do **not** try. Instead we simulate everything
*around* the torque event and treat the torque event itself as an
abstract, mockable action.

**Can prove in open-source sim:**

- The **PiPER reaches the station** with the held vial and presents it
  at the correct pose and orientation (vial axis aligned, upright). The
  arm's ~600 mm reach (`~`, verify) means the decapper station can sit
  comfortably away from the other stations without a cramped layout.
- The **sequencing**: grip vial → move to station → call `/decap` →
  confirm cap removed → (later) call `/cap` → confirm cap seated → carry
  on. This is the load-bearing logic and it runs end to end.
- The **state bookkeeping**: which vial is open, which cap belongs to
  which vial, where a parked cap sits — all tracked as ROS 2 state.
- The **failure branches** in software: what the behavior tree does when
  the station reports `success: false` or a bad-torque flag (retry,
  quarantine, safe-stop — see Part 08). A *behavior tree* is a tree of
  tasks the robot walks through to decide what to do next.
- The **perception checks** that gate the next step: "is the cap gone?"
  / "is the cap seated?" run against the rendered scene in Part 07.

**Cannot be proven in sim (needs hardware):** real **decap/recap
torque**, **cross-threading** detection, **glass cracking** under
over-torque, and **septum integrity**. These are friction/material
effects we abstract; they must be validated on the real station/tool.
Sim still de-risks them by proving the surrounding choreography is
correct *before* you spend the torque budget on hardware bring-up.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **Gazebo Harmonic** (`gz-sim`) | Hosts the vial+cap model and the station frame; toggles the cap joint | Primary; where the abstraction lives. |
| **`gz_ros2_control`** | Drives the **PiPER URDF** joints in sim (no real driver needed) | Same joint interface as the real arm via `piper_ros`. |
| **MoveIt 2** | Plans the collision-free move to the station presentation pose | Config generated from the PiPER URDF. |
| **ROS 2** (Humble/Jazzy) | Carries the `/decap` and `/cap` services + cap-present state | Identical interface on real hardware. |
| **BehaviorTree.CPP** (+ Groot2) | Sequences present → decap → work → recap → verify, with fault branches | Orchestration lives here (Part 08). |
| **RViz2 / Foxglove** | Visualise the station frame, the cap link, and service calls | Debugging and demos. |

## How to simulate it now

**The core abstraction.** A real screw cap *threads* onto the vial. We
do **not** model threads. We model the **cap as a separate link** joined
to the **vial link** by a joint that a station service can break
(detach) or remake (attach). A *link* is one rigid body in the model; a
*joint* connects two links. "Decap" = detach + announce
`cap_present:false`; "cap" = re-attach + announce `cap_present:true`.
No torque, no rotation, no contact dynamics are simulated.

1. **Add a cap link to the vial model.** Extend the vial SDF/URDF used
   in [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
   with a child `cap` link sitting on the vial mouth. Join it to the
   vial body with a **fixed joint** (the "breakable" joint we toggle).
   Give the cap its own visual so Part 07 perception can see it present
   or absent. (*tf* is the ROS 2 system of named coordinate frames that
   tracks where every part is.)

2. **Write the mock decapper-station node.** A single ROS 2 node that
   advertises two services at a fixed tf frame `decap_station`:
   - `/decap` (e.g. `std_srvs/Trigger` or a small custom srv) — detaches
     the cap link from the vial (delete/disable the fixed joint via the
     Gazebo model API, or re-parent the cap to a parking nest link),
     then publishes `cap_present:false` for that `vial_id` and returns
     `success:true` with a `torque_ok:true` flag.
   - `/cap` — re-attaches the cap to the vial (recreate the fixed
     joint), publishes `cap_present:true`, returns `success` +
     `torque_ok`.
   The station also owns a **per-vial cap registry** (which cap link is
   parked where) so the *same* cap returns to the *same* vial.

3. **Expose station tf frames.** Publish a static transform for
   `decap_station` (and a `cap_nest_<vial_id>` parking frame). The PiPER
   plans to a **presentation pose** defined relative to `decap_station`.

4. **Drive the sequence (behavior tree).** With the vial already gripped
   (Part 02): `MoveToPose` → presentation pose at `decap_station` →
   call `/decap` → on `success` and Part 07 confirming the cap is gone,
   proceed to dispensing (Part 04). After prep: return to the station →
   call `/cap` → Part 07 confirms the cap is seated.

5. **Inject the abstraction's "physics" as parameters.** To exercise
   failure handling, let the station node return `success:false` /
   `torque_ok:false` on demand (a parameter or a fault-injection
   service). This lets Part 08 prove the cross-thread / won't-release
   branches *without* simulating the actual torque.

6. **Verify with perception, not physics.** Don't trust the service's
   word alone — gate on Part 07 reading the rendered scene (cap link
   present vs absent, cap seating height). This mirrors the real
   recap-integrity check.

Optionally, if you want a contact-rich *grip-against-rotation* study
(the vial trying to spin while held), move just that sub-scene into
**MuJoCo** — but treat results as qualitative; real glass friction is
hardware-only.

## Additional hardware needed

Beyond the **PiPER arm + its gripper**, the real bench needs **one** of:

- a **dedicated decapper/capper station** (calibrated torque motor,
  purpose-built jaws) that the arm feeds vials into — the recommended v1
  approach; or
- a **torque-controlled decapping end-effector** the arm picks up from a
  **tool changer** (a quick-connect interface that lets the arm swap
  tools) and uses to decap in place. Note the PiPER's ~1.5 kg payload
  (`~`, verify) bounds how heavy such a tool can be.

Either way the bench also needs **cap parking nests** (clean, upright,
one-per-vial) and **torque sensing** for the real seal/cross-thread
checks.

**How it's mocked in sim:** all of the above collapse to the single
**mock decapper-station node** with its `/decap` and `/cap` services and
the breakable cap joint. The tool changer, if chosen, is an
attach/detach of an end-effector model. **No real torque, cross-
threading, glass-crack, or septum behaviour is represented** — those are
explicitly deferred to hardware validation.

## How it connects

- [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
  — the PiPER must already hold the vial (grasp-fix plugin) before it
  can present it to the station; the cap link is added to that same vial
  model.
- [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md)
  — a successful `/decap` is what makes the vial *open* so the dispenser
  service can change its fill-volume state; `/cap` runs after prep.
- [`07-perception-and-verification.md`](07-perception-and-verification.md)
  — confirms (from the rendered scene) that the cap is actually removed
  before dispensing and properly seated after recap.
- [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md)
  — defines what the behavior tree does on a decap/cap failure
  (`torque_ok:false`): retry, quarantine the vial, or safe-stop.
- Back to the index: [`README.md`](README.md).
