# Layer 05 — Grasping & manipulation (code plus hardware)

> **Job:** Decide where and how to grip a 2 mL HPLC vial *and actually
> close the real gripper on it* — then verify the vial is truly held
> on the physical myCobot 280.

Same vocabulary as the only-code file, repeated because it matters
even more once the hardware is real:

- **Grasp pose** — the full 3D position and orientation of the gripper
  at the moment it closes. "Where to put the hand."
- **Antipodal grasp** — a grip where the two jaws press on two roughly
  opposite, roughly parallel faces, so contact forces cancel and the
  object cannot slip out. For a vial: two jaws on opposite sides of the
  glass body.
- **Parallel-jaw gripper** — the simple two-finger gripper (here the
  Elephant Robotics adaptive/parallel gripper on the myCobot 280) that
  opens and closes along one axis.

What changes versus only-code: the grasp must **execute** on a real,
**light, low-payload** gripper, on **smooth glass**, and we can no
longer *assume* the pick worked — we have to **verify** it. So two of
the five options below are about **execution and verification**, not
about *finding* a grasp. The physical headaches that drive the picks:

- **Slip on glass.** A 2 mL vial is smooth borosilicate; low friction
  means it can rotate or slide in the jaws even when nominally gripped.
- **Grip force on a light gripper.** The myCobot 280 is a desktop arm
  with a small gripper; it has limited, not always finely controllable,
  closing force. Too little and the vial slips; too much risks cracking
  glass or stalling the gripper motor.
- **Closing width.** The jaws must close to *just* under the vial
  diameter (~12 mm body). Command the wrong target width and you either
  miss the glass or crush against it.
- **Verifying it is held.** After closing, is the vial actually in the
  jaws, at the expected width, not dropped or askew? On hardware this
  must be *checked*, not assumed.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| Contact-GraspNet (+ real RGB-D) | Learned 6-DoF grasp predictor on live depth | Best-in-class | Predicts 6-DoF grasps from a real depth camera; strongest, GPU + calibration cost, overkill for one vial. |
| Analytical / antipodal (Open3D) | Geometric grasp from known shape | Cheapest | Computes the antipodal pinch from the vial's known cylinder; free, exact, deterministic. |
| ros2_control GripperCommand / Elephant driver (via pymycobot) | Real gripper execution | Best-practical | The actual driver that closes the physical jaws to a target width/force; the only way a grasp *happens*. |
| MoveIt Task Constructor (MTC) | Pick-place stage sequencer | Alternative | Sequences pick → lift → place stages and drives the gripper action; reusable, but infrastructure not a grasper. |
| Grasp verification via gripper feedback (width/current) | Did-we-get-it check | Alternative | Reads jaw width / motor current after closing to confirm a vial is actually held. |

> Note on tiers: the best-practical pick here is the **execution
> driver**, because on hardware a grasp that cannot be *commanded* and
> *verified* is worthless. MTC (the best-practical pick in only-code)
> drops to Alternative — it is still recommended as the sequencer, but
> on hardware the load-bearing new component is the gripper driver plus
> the feedback check, so those take the named tiers.

---

## Contact-GraspNet (+ real RGB-D)

Contact-GraspNet is a deep network that takes a **point cloud** — the
3D dot-cloud from a depth camera — and proposes a dense set of scored
**6-DoF grasp poses** ("6-DoF" = free in all six degrees of freedom, so
it can approach from any angle). On hardware it runs on **real RGB-D**:
a depth camera (RealSense / OAK / Orbbec, per Layer 04) sees the actual
vial in the actual tray, and the net returns grips in camera
coordinates that you transform into the arm's frame and execute.

Its strength is **capability and robustness to the real world**. Live
depth is noisier and more occluded than synthetic depth, and a learned
predictor trained on clutter copes with that far better than rigid
geometry — it is the closest open option to "look at whatever is there
and grab it." For a lab that later handles varied vials, caps, racks or
tip boxes, this is the ceiling. The commercial step beyond it,
**AnyGrasp**, is faster and more robust on live sensor data but is
licensed; treat AnyGrasp as the paid upgrade when one-off geometry
stops being enough.

Its weaknesses sharpen on hardware. It needs a **GPU on or near the
cell**, a trained checkpoint, and — critically — accurate **hand-eye
calibration** (knowing exactly where the camera is relative to the arm)
or its excellent grasps land in the wrong place. It also still does not
*execute* anything: its output is a pose that must be handed to the
gripper driver, and it does not know whether glass will slip or how
hard to squeeze. For one known upright vial it spends real money and
calibration effort rediscovering the pinch the analytical method gives
for free, and can pick a valid-but-wrong target (the cap). Best-in-class
on capability; genuine overkill for v1.

## Analytical / antipodal (Open3D)

The analytical approach computes the grasp from **known geometry**
instead of learning it. The vial is a ~12 mm cylinder; the preferred
pinch is "jaws perpendicular to the vial axis, centered on the body,
a few mm below the cap." From the vial axis and centroid (from tray
geometry or Layer 04 perception, mapped into the arm frame via the same
hand-eye calibration) you build a grasp pose square to the axis and a
target jaw width just under the glass diameter. **Open3D**, the
open-source 3D geometry library, provides the point-cloud and mesh
tooling to find the axis, sample contacts, and visualize the result.

Its strength on hardware is being **free, exact, and deterministic** —
the same correct pinch every time, no GPU, no model to deploy. Because
it emits an explicit target width and approach, it pairs naturally with
the gripper driver: the analytical method says *where and how wide*, the
driver *does it*, and the feedback check *confirms it*. For one known
rigid vial this is not a compromise; it is the right grasp source, and
it is cheap enough to run on the arm's own controller.

Its weaknesses are the real-world ones it cannot sense. It assumes the
vial is exactly where geometry says; if calibration drifts, the tray
shifts, or a vial leans, the computed pinch is silently wrong and — by
itself — it has **no feedback** to notice. It does not model **slip on
glass** or choose **grip force**; it just names a pose and width, so it
leans entirely on the driver and verification step to handle the
physics. Against Contact-GraspNet it has no graceful fallback for the
unknown. Cheapest and correct for v1, but only safe when paired with
execution feedback.

## ros2_control GripperCommand / Elephant gripper driver (via pymycobot)

This is the layer that makes a grasp **physically happen**. The myCobot
280's gripper is commanded either through **`pymycobot`** (Elephant
Robotics' Python SDK, which exposes set-gripper-value / -state / -speed
calls over serial) or, wrapped for ROS 2, through a **`ros2_control`**
hardware interface exposing the standard **`GripperCommand`** action — a
ROS action where you request a target **position (jaw width)** and
**max effort (force)** and get back the reached state. Whatever finds
the grasp upstream, *this* is what closes the jaws on the real vial.

Its strength is that it is **the only option that executes**, and it is
the natural home for the hardware-specific tuning the glass vial
demands. You set the **closing width** to just under ~12 mm so the jaws
bite the body; you cap the **grip force** low enough not to crack glass
or stall the small motor, but high enough to resist **slip** — a
tuning loop you can only close on hardware. Through `GripperCommand`'s
returned state (or `pymycobot`'s read-back) it also surfaces the
**width and motor current/effort** that the verification step consumes.
It is mandatory, lightweight, and ships with the arm.

Its weakness is that it is **purely an actuator interface — it finds no
grasp and plans no motion.** It must be fed a pose and width by the
analytical or learned method, and is best driven inside MTC so the
gripper action is sequenced with the arm motion rather than fired
blindly. Its force control is **coarse** (a desktop gripper, not a
force-torque research hand), so fine slip-avoidance is limited — you
manage it with width/force tuning and verification, not precise
servoing. Named **best-practical** here because on hardware the grasp
that cannot be commanded does not exist, and this is what commands it.

## MoveIt Task Constructor (MTC)

MoveIt Task Constructor, layered on **MoveIt 2** (Layer 03), describes a
manipulation **task as a sequence of stages** — pre-grasp, approach,
**close gripper**, lift, move-to-tray, place, retreat — and searches for
a consistent, collision-checked plan across them, attaching the vial to
the gripper in the planning scene once grasped so later motions know
the arm is carrying glass. On hardware its "close gripper" stage fires
the real **`GripperCommand`** action above, so MTC is the conductor that
ties the grasp pose, the arm motion, and the gripper actuation into one
restartable pick-place.

Its strength is being the **clean, reusable, collision-aware** way to
run pick-place on the real arm. It keeps the approach and retreat clear
of the tray and neighboring vials, restarts gracefully when a stage
fails, and lets you slot in a "verify hold" stage right after closing —
all inside the ROS 2 / MoveIt 2 stack the cell already runs. The
recommended hardware loop is still **MTC + analytical pinch + the
gripper driver + the feedback check** working together.

Its weakness, and why it is only **Alternative** here rather than
best-practical, is that it is **infrastructure, not the new
hardware-critical piece**. On the real cell the components that actually
determine success — that *close the jaws* and *confirm the vial is
held* — are the driver and the verification check; MTC orchestrates
them but adds no grip force, no slip handling, and no held/not-held
signal of its own. It also carries the full MoveIt 2 calibration and
config burden. Indispensable as the sequencer, but it is not what the
hardware risk lives in.

## Grasp verification via gripper feedback (width/current)

This option answers the question hardware forces on you that simulation
never did: **did we actually get the vial?** After the jaws close, you
read back two cheap signals the gripper already provides — the
**achieved jaw width** and the **motor current / effort** (how hard the
motor is working). If the jaws closed **all the way to fully shut**,
nothing is between them: the grasp **missed or dropped**. If they
stopped at roughly the expected ~12 mm width *and* the motor is holding
a steady current, something solid is held. A simple width-and-current
window turns "I sent a close command" into "a vial is verifiably in the
gripper."

Its strength is that it directly attacks the failure modes the others
cannot see. **Slip on glass** and a **missed pick** both show up as a
wrong final width or a collapsing holding current, so this is the gate
that lets orchestration (Layer 07) safely retry or abort instead of
driving an empty gripper to the tray. It needs no extra hardware on the
myCobot — it reuses the same `pymycobot` / `GripperCommand` read-back
the driver already exposes — and it is what makes the cheap analytical
pinch *trustworthy* in the real world.

Its weakness is that it is **a check, not a grasp** — it finds nothing
and moves nothing, and it is only as good as the signals a light
desktop gripper exposes. Width/current feedback confirms *that* glass
is held but not *how securely*; it will not catch a vial held slightly
crooked but at the right width, and the small gripper's current
reading is coarse. For higher assurance you add a confirmation
**camera glance** (Layer 04) after lift — which is exactly the
**two-witness** rule from [`../sensor-suite.md`](../sensor-suite.md):
"vial is held" = gripper feedback (**#4**) **and** a wrist-camera glance
(**#3**), two independent sensors that rarely lie the same way. Note the
heavier force sensing lives **off the light wrist**: the decapper load
cell / torque sensor (**#5**) belongs to the decap *station*, not the
gripper, because the 280's ~250 g payload can't carry a wrist
force-torque sensor. Essential glue, but **Alternative** because it rides
on the driver rather than standing alone.

## Verdict

- **Best-in-class:** **Contact-GraspNet (+ real RGB-D)** — strongest
  open learned 6-DoF grasping on live depth, the right ceiling for
  varied objects (with **AnyGrasp** as the licensed step beyond). For
  one known upright vial it is overkill and adds GPU + calibration cost.
- **Cheapest:** **Analytical / antipodal pinch (Open3D)** — free,
  exact, deterministic; the correct grasp *source* for a known vial,
  provided it is paired with execution feedback.
- **Best-practical:** **ros2_control GripperCommand / Elephant driver
  (via pymycobot), with the gripper-feedback hold check** — the actual
  way the grasp *executes* on the real myCobot and the way you *confirm*
  the vial is held, tuned for closing width, grip force, and slip on
  glass. In practice run it as **MTC + analytical pinch + this driver +
  the width/current check** together.

The hardware recommendation keeps the cheap analytical grasp *source*,
sequences it with MTC, **executes** it through the gripper driver, and
**verifies** it with width/current feedback; Contact-GraspNet remains
the deliberate later upgrade, not the v1 starting point.

## The learned upgrade path — VLA / generalist policies

Beyond the five sits the frontier: **Vision-Language-Action (VLA)**
foundation models that map camera frames + a text instruction straight
to robot actions, learned from demonstrations. On **real hardware** their
appeal is concrete — instead of hand-coding each new vial/labware case,
you **teleoperate a few demos and fine-tune**. The full comparison
(open vs closed, GPU, data needs, compliance) is in
[`../foundation-models.md`](../foundation-models.md); the short version:

| Model / ecosystem | Who | Open? | On real hardware you'd… |
|---|---|---|---|
| **π0 / π0.5 / π0.6** (openpi) | Physical Intelligence | Open | Fine-tune the strongest open flagship on real teleop demos |
| **Gemini Robotics On-Device / -ER** | Google DeepMind | Mostly closed | Adapt On-Device with **~50–100 demos**; run locally, low-latency |
| **OpenVLA (+ OFT)** | Stanford/Berkeley/TRI | Open | Fine-tune (LoRA); **OFT** gives real-time, multi-image inference |
| **Isaac GR00T N1.5 / N1.7** | NVIDIA | Open (Apache-2.0) | Sim-train + sim-to-real transfer onto the arm (needs Isaac + GPU) |
| **LeRobot + SmolVLA** | Hugging Face | Open | Record demos with LeRobot, train a ~450M model on a consumer GPU |

The hardware concerns these add on top of the analytical path: real
**inference latency** and **GPU placement** (on-arm compute vs a nearby
box), **data collection** (teleoperating enough clean demos), and — the
big one — **safety and trust**. A black-box policy driving a real arm
near glass must be wrapped in the same **safety gates** from the
[sensor suite](../sensor-suite.md): gripper-feedback hold check (#4),
wrist-camera confirm (#3), force/torque limits (#5), and the light
curtain / e-stop (#10/#11) that can halt it regardless of what it
"intends." Note **myCobot 280 support in LeRobot is community-dependent**
(verify) — you may need a custom data/driver bridge versus the
SO-100/SO-101-class arms LeRobot targets first.

**Compliance reality:** a non-deterministic learned policy is hard to
validate under **21 CFR Part 11 / IQ-OQ-PQ**. The honest deployment
pattern is **analytical/deterministic on the validated critical path,
VLA on flexible or non-GxP steps** — keep the cheap, exact, *executable*
pinch as v1 and treat the VLA as the generalization upgrade.

## See also

- [`README.md`](README.md) — the code-plus-hardware layer guide and the
  other seven development layers.
- [`../foundation-models.md`](../foundation-models.md) — the full VLA /
  generalist-policy comparison this section summarizes.
- [`../01-only-code/05-grasping-and-manipulation.md`](../01-only-code/05-grasping-and-manipulation.md)
  — the same layer proven **in simulation only**, before any real
  gripper, slip, or grip-force concerns enter.
