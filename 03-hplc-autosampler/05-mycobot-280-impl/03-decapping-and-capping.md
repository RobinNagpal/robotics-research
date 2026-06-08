# Part 03 — Decapping & capping (myCobot 280 simulation)

> **Sim goal:** Prove the *logic and choreography* of opening and
> re-closing a vial — present, decap, work, recap, verify — on the
> myCobot 280, without pretending to simulate threaded-cap physics,
> which we deliberately abstract away.

## What we can prove in simulation

Decapping is the hardest *physics* in the whole system (controlled
torque, cross-threading, septum integrity).
None of that real physics is honestly simulatable, so we do **not** try.
Instead we simulate everything *around* the torque event and treat the
torque event itself as an abstract, mockable action that a **mock
decapper-station node** performs on command.

**Can prove in open-source sim:**

- The **arm reaches the station** with the held vial and presents it at
  the correct pose and orientation (vial axis aligned, upright). On the
  myCobot 280 this reachability check matters most: with only a
  **~280 mm working radius** (`~` figure — verify), the `decap_station`
  must sit *inside* the arm's compact workspace, close to the supply
  rack and dispenser. The digital twin is where you confirm the station
  is reachable before committing to a bench layout (see Part 10).
- The **sequencing**: grip vial → drive to station → call `/decap` →
  confirm cap removed → (later) call `/cap` → confirm cap seated → carry
  on. This is the load-bearing logic and it runs end to end.
- The **state bookkeeping**: which vial is open, which cap belongs to
  which vial, where a parked cap sits — all tracked as ROS 2 state.
- The **failure branches** in software: what the behavior tree does when
  the station reports `success:false` or a bad-torque flag (retry,
  quarantine, safe-stop — see Part 08).
- The **perception checks** that gate the next step: "is the cap gone?"
  / "is the cap seated?" run against the rendered scene in Part 07.

**Cannot be proven in sim (needs hardware):** real **decap/recap
torque**, **cross-threading** detection, **glass cracking** under
over-torque, and **septum integrity** (the silicone/PTFE disc the needle
pierces). A *septum* is the thin pierceable disc in the cap; *cross-
threading* is when the cap bites the threads at an angle and jams. These
are friction/material effects we abstract; they must be validated on the
real station/tool — and the 280's **~250 g payload** means the real arm
contributes little holding force, so the station must do the gripping
and twisting. Sim still de-risks the work by proving the surrounding
choreography is correct *before* hardware bring-up.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **Gazebo Harmonic** (`gz-sim`) | Hosts the vial+cap model and the station frame; toggles the cap joint | Primary; where the abstraction lives. |
| **`mycobot_ros`** | Supplies the ready-made myCobot 280 URDF + MoveIt config used to drive the arm in sim | BSD; saves building the model. |
| **`gz_ros2_control`** | Drives the myCobot 280 URDF joints in sim (no `pymycobot`, no real driver) | Same joint interface as the real arm. |
| **MoveIt 2** | Plans the collision-free move to the station presentation pose | Config from `mycobot_ros`. |
| **ROS 2** (Humble/Jazzy) | Carries the `/decap` and `/cap` services + cap-present state | Identical interface on real hardware. |
| **BehaviorTree.CPP** (+ Groot2) | Sequences present → decap → work → recap → verify, with fault branches | Orchestration lives here (Part 08). |
| **RViz2 / Foxglove** | Visualise the station frame, the cap link, and service calls | Debugging and demos. |

## How to simulate it now

**The core abstraction.** A real screw cap *threads* onto the vial. We
do **not** model threads. We model the **cap as a separate link** joined
to the **vial link** by a joint that a station service can break
(detach) or remake (attach). "Decap" = detach + announce
`cap_present:false`; "cap" = re-attach + announce `cap_present:true`.
No torque, no rotation, no contact dynamics are simulated.

1. **Add a cap link to the vial model.** Extend the vial SDF/URDF used
   in [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
   with a child `cap` link sitting on the vial mouth. Join it to the
   vial body with a **fixed joint** (the "breakable" joint we toggle).
   Give the cap its own visual so Part 07 perception can see it present
   or absent.

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

3. **Expose station tf frames — close to the arm.** Publish a static
   transform for `decap_station` (and a `cap_nest_<vial_id>` parking
   frame). Because the 280's reach is short, place this frame
   deliberately near the arm base and sanity-check in RViz2 that the
   presentation pose is inside the reachable workspace. The arm plans to
   a **presentation pose** defined relative to `decap_station`.

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

### The two sensors that gate a decap/recap

On the real bench the `torque_ok` flag is not a guess — it comes from
sensors in the station, cross-checked by a camera (see the canonical
[`sensor-suite.md`](sensor-suite.md)). Two witnesses gate this step:

- **Decapper load cell / torque sense (#5).** The station's torque
  motor reports the **decap / cap torque**, which is how the real cell
  detects **cross-threading** (torque climbs abnormally as the cap
  bites at an angle) and a **stuck cap** (torque hits a ceiling without
  the cap breaking free). This is the sensor behind the abstract
  `torque_ok` flag — and it lives in the station, not on the arm,
  precisely because the 280 has no joint F/T sensing. *Sim stand-in:* a
  Gazebo **force-torque sensor on the cap joint**; the mock station
  reads it (or an injected fault value) to set `torque_ok` instead of
  always returning `true`.
- **Station camera (#2) — the second witness.** A fixed, side-on
  RGB/RGB-D camera at the station confirms **cap-off** after `/decap`
  and **cap-seated** (correct seating height, square on the mouth)
  after `/cap`. *Sim stand-in:* a Gazebo `camera` at the
  `decap_station` frame feeding the Part 07 check.

Per the **two-witness habit**, "cap is off" / "cap is seated" is
trusted only when the load-cell torque (#5) **and** the station camera
(#2) agree, so a torque sensor that reads fine on a cap that visibly
isn't seated still fails the gate.

Optionally, if you want a contact-rich *grip-against-rotation* study
(the vial trying to spin while held), move just that sub-scene into
**MuJoCo** — but treat results as qualitative; real glass friction is
hardware-only, and on the 280 the holding force is too small to rely on.

## Additional hardware needed

Beyond the **myCobot 280 + its gripper**, the real bench needs **one**
of the following — and, because the 280 cannot supply meaningful
holding torque itself, the station-based option is strongly preferred:

- a **dedicated decapper/capper station** (calibrated torque motor,
  purpose-built jaws) that the arm feeds vials into — the recommended v1
  approach; or
- a **torque-controlled decapping end-effector** the arm picks up from a
  **tool changer** (a quick-connect interface) and uses to decap in
  place — heavier and harder for a 250 g-payload arm, so a later option.

Either way the bench also needs **cap parking nests** (clean, upright,
one-per-vial) and **torque sensing** for the real seal/cross-thread
checks. All of this must fit the **compact 280 workspace**, clustered
tightly around the arm.

**How it's mocked in sim:** all of the above collapse to the single
**mock decapper-station node** with its `/decap` and `/cap` services and
the breakable cap joint. The tool changer, if chosen, is an
attach/detach of an end-effector model. **No real torque, cross-
threading, glass-crack, or septum behaviour is represented** — those are
explicitly deferred to hardware validation.

## How it connects

- [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
  — the arm must already hold the vial (grasp-fix plugin) before it can
  present it to the station; the cap link is added to that same vial
  model.
- [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md)
  — a successful `/decap` is what makes the vial *open* so the dispenser
  service can change its fill-volume state; `/cap` runs after prep.
- [`sensor-suite.md`](sensor-suite.md) — the canonical sensor list;
  the decapper load cell / torque sense (#5) behind `torque_ok` and the
  station camera (#2) used to confirm cap-off / cap-seated are defined
  there with costs and sim stand-ins.
- [`07-perception-and-verification.md`](07-perception-and-verification.md)
  — confirms (from the rendered scene) that the cap is actually removed
  before dispensing and properly seated after recap.
- [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md)
  — defines what the behavior tree does on a decap/cap failure
  (`torque_ok:false`): retry, quarantine the vial, or safe-stop.
- Back to the index: [`README.md`](README.md).
