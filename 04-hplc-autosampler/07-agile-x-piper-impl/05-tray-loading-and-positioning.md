# Part 05 — Tray loading & positioning (AgileX PiPER simulation)

> **Sim goal:** Prove, entirely in open-source simulation, that the
> PiPER can place a carried vial into the *exact* autosampler-tray
> slot the worklist demands — fully seated, without nudging its
> neighbours — by modelling the tray as a fixed-pitch grid of named
> tf frames and driving a MoveIt 2 place + seat sequence into each
> one.

A **tf frame** is a named 3-D coordinate marker that ROS 2 tracks
over time; here we give every slot its own frame so "go to A1" is a
single lookup. **MoveIt 2** is the motion planner that finds a
collision-free path for the arm. New to a term? See
`../../03-place-items-on-shelf/02-glossary.md`.

## What we can prove in simulation

The hard parts of tray loading are *geometry and logic*, and both
sit fully inside the simulator:

- **Reachability of a full tray.** The PiPER's ~600 mm reach (`~`,
  verify) comfortably covers a standard ~48–54-position tray from a
  single fixed base — a clear point in its favour versus the
  myCobot 280's ~280 mm reach, which forces a cramped layout. We
  confirm every slot is reachable with margin before buying
  anything.
- **Collision-free placement** into a dense grid: the planner must
  bring the carried vial down between already-placed neighbours
  without clipping them.
- **The place sequence** itself: approach pose above the slot, a
  short straight-down descent, optional compliance/search, release,
  and a clean straight-up retreat.
- **Worklist → slot mapping** — that worklist row N lands in the
  correct physical slot (A1, A2, …), tested end to end.
- **Sequencing and cycle time** across a whole tray fill.

**Honest limits (need hardware):** real **seating force** and the
sub-millimetre **mechanical tolerances** of a real slot, friction
of glass on the slot wall, and whether a vial perches on the rim
versus drops home. Sim *assumes* a clean seat once the attach fires;
the real read on insertion reliability only comes on the bench.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **Gazebo Harmonic** (`gz-sim`) | Physics world holding the tray model, vials, and bench | Primary simulator; per-slot frames live here |
| **MoveIt 2** (config from PiPER URDF) | Plans the approach, straight-down descent, and retreat | Core motion planner for placement |
| **`ros2_control` + `gz_ros2_control`** | Executes planned joint trajectories on the URDF | Drives the simulated arm |
| **grasp-fix plugin** | "Attaches" the vial to the slot frame on seat (sim stand-in for friction-held seating) | Lets us model a successful seat without real contact physics |
| **MuJoCo** (optional) | Contact-rich tuning of the descent/search if Gazebo contact is too coarse | Use only if insertion feel matters |
| **tf2** | Publishes and looks up the per-slot frames (A1, A2, …) | Turns slot names into poses |
| **RViz2 / Foxglove** | Visualise frames, planned paths, and occupancy | Debugging and demo |

## How to simulate it now

1. **Build the tray model + per-slot frames (sim teach step).**
   Add a static tray model to the Gazebo world at a known pose. Then
   mimic the real **teach** calibration: jog the simulated arm to
   three corner slots (e.g. A1, the far-row corner, and the opposite
   corner), record those poses, and *derive the full grid* from the
   tray's fixed **pitch** (constant centre-to-centre spacing). A
   small node publishes one tf frame per slot — `tray/A1`,
   `tray/A2`, … — as static transforms relative to a `tray_origin`
   frame. This is the sim analogue of the fiducial/teach calibration
   in the high-level doc, and it makes the layout portable: change
   the pitch constant and every frame moves.

2. **Plan the place pose.** Given a target slot frame, compute an
   **approach pose** a few cm directly above it, ask MoveIt 2 for a
   collision-free plan to that pose, then a **short straight-down
   Cartesian move** to the seat height.

3. **Optional compliance / search.** For v1 keep it simple:
   straight descent. As a fallback, run a small **spiral search**
   (tiny offsets around the slot centre) before declaring a miss —
   this exercises the same control path the real arm would use with
   passive compliance, even though sim contact is idealised.

4. **Seat via grasp-fix attach.** When the arm reaches seat height,
   detach the vial from the gripper and **attach it to the slot
   frame** with the grasp-fix plugin, then open the gripper and
   retreat straight up. The vial now rides the `tray/Ax` frame.

5. **Neighbour-collision checks.** Spawn already-placed vials as
   collision objects in the MoveIt planning scene so the planner
   routes the carried vial *between* neighbours; fail the place if a
   plan can't be found without contact.

6. **Verify occupancy/seating** via Part 07: a height check (gripper
   reaches the expected release height) plus a vision check that the
   slot is now occupied and the vial top is flush. A vial sitting
   proud means "not seated" → raise a placement failure (Part 08).

7. **Test worklist → slot mapping.** Drive a small worklist
   (sequential: row 1 → A1, row 2 → A2, …) and confirm each vial
   ends up on its assigned frame. Then deliberately scramble one row
   to confirm the mapping table — not luck — is what places vials.

**Key tf frames:** `tray_origin`, `tray/A1` … `tray/H6` (or the
chosen format), `arm_base`, `gripper_tip`. **Mock interfaces:** none
required for placement itself — the tray is passive geometry — but
the seat event publishes to the verification topic Part 07 watches.

## Additional hardware needed

Beyond the **PiPER arm + gripper**, the real system needs:

| Real hardware | Why | Mocked in sim as |
|---------------|-----|------------------|
| **HPLC autosampler + trays/racks** | The destination the vial is loaded into | Static tray model with per-slot tf frames |
| **Tray fixture / kinematic locator** | Holds the tray at a repeatable, known pose so the calibrated grid stays valid | Fixed model pose in the world file |
| **Compliant tool or F/T sensor** (later) | Real seating relies on self-centring / felt contact force | grasp-fix attach on seat; optional MuJoCo descent |

Real **seating force and slot tolerances** cannot be proven in sim —
they are the headline item to validate on the bench.

## How it connects

- `02-vial-handling-and-gripping.md` — the arm arrives here
  *carrying* a gripped vial; placement is the end of that carry.
- `06-identification-labeling-and-tracking.md` — defines which
  sample (vial ID) belongs in which slot; this part realises that
  mapping physically.
- `07-perception-and-verification.md` — supplies the occupancy and
  seating verification that confirms a good place.
- `08-orchestration-error-handling-and-safety.md` — handles
  placement failures (jam, miss, tipped neighbour): retry, search,
  or quarantine.
- Matching high-level doc:
  `../03-high-level-solution/05-tray-loading-and-positioning.md`.
- Back to the overview: `README.md`.
