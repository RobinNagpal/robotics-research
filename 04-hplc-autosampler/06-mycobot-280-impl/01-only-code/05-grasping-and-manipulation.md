# Layer 05 — Grasping & manipulation (only code)

> **Job:** Decide *where and how* the arm should grip a 2 mL HPLC
> vial, and sequence the pick-and-place — proven entirely in
> simulation, with no real gripper in the loop.

A quick vocabulary note before the options, because three terms recur:

- **Grasp pose** — the full 3D position *and* orientation of the
  gripper at the moment it closes on the object. "Where to put the
  hand."
- **Antipodal grasp** — a grip where the two jaws press on two
  roughly opposite, roughly parallel faces of the object, so the
  contact forces cancel and the object does not squirt out. For a
  cylinder like a vial, an antipodal pinch is just "two jaws on
  opposite sides of the glass."
- **Parallel-jaw gripper** — the simple two-finger gripper (the
  myCobot 280's adaptive/parallel gripper) that opens and closes
  along one axis. All five options below ultimately output a grip
  this kind of gripper can execute.

The v1 reality that shapes every choice here: there is **one known,
rigid vial** with a **preferred pinch** (grab the glass body just
below the cap, jaws square to the vial axis). The pose of the vial is
known from the tray geometry or from perception (Layer 04). That means
**heavy learned grasp prediction is overkill** — but we still survey
it, because it is the path to handling messier objects later.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| Contact-GraspNet | Learned 6-DoF grasp predictor | Best-in-class | Deep net proposes full 6-DoF grasps from a depth cloud; strong, GPU-hungry, overkill for one vial. |
| Analytical / antipodal (custom + Open3D) | Geometric grasp from known shape | Cheapest | Pure geometry: compute the antipodal pinch from the vial's known cylinder; free, instant, exact. |
| MoveIt Task Constructor (MTC) | Pick-place stage sequencer | Best-practical | Wraps an analytical pinch in clean, reusable pick → lift → place stages inside MoveIt 2. |
| GraspIt! | Classic grasp simulator | Alternative | Veteran simulator for grasp synthesis and quality metrics; powerful but aging and standalone. |
| Dex-Net / GQ-CNN | Learned grasp-quality scorer | Alternative | Scores top-down parallel-jaw grasps from depth; great for bins, mismatched to a fixed vial. |

---

## Contact-GraspNet

Contact-GraspNet is a deep neural network (from NVIDIA research) that
takes a **point cloud** — the 3D dot-cloud a depth camera produces —
and directly proposes a dense set of **6-DoF grasp poses**, each with
a confidence score. "6-DoF" means the grasp is free in all six
degrees of freedom (3 for position, 3 for orientation), so it can
approach from any angle, not just straight down. In an only-code
setting you feed it synthetic depth rendered from your simulator, and
it returns candidate grips you can rank and execute on the simulated
gripper.

Where it shines is **generality**. It was trained to grasp clutter and
novel shapes it never saw, so it degrades gracefully when objects are
unknown, partly occluded, or jumbled. For a lab cell that might later
handle assorted vials, caps, tube racks, or pipette tips, this is the
ceiling of capability among the five — the closest open option to a
"just look and grab anything" system. The commercial step beyond it is
**AnyGrasp** (from the same lineage of dense 6-DoF grasping), which is
faster and more robust but is licensed, not free; treat AnyGrasp as the
upgrade you buy once one-off geometry stops being enough.

Its weakness against the other four is **mismatch to the v1 problem**.
It needs a GPU, a trained checkpoint, and a depth pipeline, and it
predicts grasps for objects it does not *know* — but here we *do* know
the object exactly. So it spends a lot of compute rediscovering the
one pinch the analytical method gives us for free, and it can return a
physically valid but *procedurally wrong* grasp (e.g. gripping the cap
instead of the body) that a hard-coded rule would never make. Versus
MTC it is only a grasp *source*, not a sequencer — you still need
something to stage the pick-place. Versus Dex-Net it is heavier but
genuinely 6-DoF rather than top-down. Best-in-class on capability,
but parked behind the analytical method for v1.

## Analytical / antipodal (custom + Open3D)

The analytical approach throws out learning entirely and computes the
grasp from **known geometry**. A 2 mL vial is a ~12 mm diameter
cylinder; the preferred pinch is "jaws perpendicular to the vial axis,
centered on the body, a few mm below the cap." That is a handful of
lines of math: take the vial's axis and centroid (known from the tray
or from Layer 04), build a grasp pose square to that axis at the
chosen height, and check the jaw opening clears the glass. **Open3D**
— an open-source 3D geometry library — supplies the point-cloud and
mesh tooling (load the vial mesh, find its axis, sample contact
points, visualize the grasp) so you are not writing linear algebra
from scratch.

Its strength is being **free, instant, deterministic, and exact** for
exactly this case. No GPU, no training data, no model to ship; the
same pinch comes out every time, which makes it trivial to test and
to reason about. For one known rigid vial with a preferred pinch, this
is not a compromise — it is arguably the *correct* answer, and it is
the engine the best-practical pick wraps. It also doubles as ground
truth when you later want to check whether a learned method agrees.

Its weakness against the others is **brittleness to the unknown**. The
moment the object is not the vial you hard-coded — a different cap, a
toppled vial, a cluttered tray, a novel consumable — the geometry
assumptions break and you get no graceful fallback, whereas
Contact-GraspNet and Dex-Net were *built* for novelty. Compared to
MTC, raw analytical code is just a grasp *calculator*; it does not
manage collision-aware approach, retreat, or attach/detach of the
object in the planning scene — you would hand-roll all of that.
Compared to GraspIt! it has no built-in grasp-quality metrics or
multi-finger synthesis. Cheapest by a mile, and perfect for v1, but it
does not scale to variety on its own.

## MoveIt Task Constructor (MTC)

MoveIt Task Constructor is a planning framework layered on **MoveIt 2**
(the arm motion-planning stack from Layer 03). Instead of planning one
motion at a time, you describe a **task as a sequence of stages** —
"move to pre-grasp," "approach," "close gripper," "lift," "move to
tray," "place," "retreat" — and MTC searches for a consistent plan
across all of them, backtracking if a later stage fails. It does not
*invent* grasps; you give it the grasp pose (from the analytical
method above) and it builds the collision-aware pick-and-place around
it, including attaching the vial to the gripper in the planning scene
so subsequent motions know the arm is now carrying something.

Its strength is being the **clean, reusable, production-shaped** way to
express manipulation. The pick-place pattern is exactly what MTC was
designed for, it lives inside the ROS 2 / MoveIt ecosystem the rest of
the cell already uses, and the stages are reconfigurable — swap the
grasp source, change approach distances, or add a "scan label" stage
without rewriting the loop. Pairing MTC with the analytical pinch
gives you the best of both: trivial, exact grasp computation *plus* a
robust, collision-checked, restartable sequence. That combination is
the recommended v1 path. In sim, MTC's "close gripper" stage does not
just assume success — a **two-witness "did we get it?" check** confirms
it: simulated gripper feedback (#4 — `ros2_control` jaw width plus joint
effort) and the grasp-fix contact say the jaws closed on glass, and a
**wrist-camera glance** (#3) confirms a vial is in hand. Both agree
before the lift stage fires; either one dissenting branches to a retry.
The decap stage similarly reads decap torque from the Gazebo
force-torque sensor (#5) on the cap joint. See
[`../sensor-suite.md`](../sensor-suite.md).

Its weakness against the others is that it is **infrastructure, not a
grasper**. On its own MTC produces nothing — point it at no grasp
source and it has nothing to sequence, so it is strictly complementary
to the analytical / Contact-GraspNet options rather than a competitor
for *finding* grips. It also carries the full MoveIt 2 learning curve
and config burden, which is heavier than a 20-line analytical script
if all you ever do is the one pinch. Versus GraspIt! and Dex-Net it
makes no grasp-quality judgment of its own. Best-practical because it
turns the cheap analytical pinch into a real, maintainable pick-place.

## GraspIt!

GraspIt! is the veteran **grasp-planning simulator** from academia: you
load a hand model and an object, and it synthesizes grasps and scores
them with **grasp-quality metrics** — numeric measures of how
stable/secure a grip is (e.g. how well it resists being pushed out of
the hand). It pioneered a lot of the field and still appears in
courses and papers as the reference tool for understanding *why* one
grip is better than another, including for multi-finger hands.

Its strength is **analysis depth**. If you genuinely needed to study
grasp stability — compare candidate pinches on a vial, reason about
friction and contact quality, or design a custom gripper — GraspIt!'s
metrics and force analysis are richer than anything the analytical
script computes by hand. It is a good *teaching and exploration* tool
for the manipulation layer.

Its weakness against the others is **age and fit**. It is an older,
largely standalone C++/Qt application with thin, unofficial ROS 2
integration, so wiring it into a modern ROS 2 cell is friction the
other options avoid. For a single known vial and a simple parallel-jaw
pinch, its multi-finger synthesis is capability you will never use —
the analytical method answers the same question in a few lines, MTC
handles the sequencing GraspIt! does not, and Contact-GraspNet /
Dex-Net cover the learned, perception-driven case it predates. Useful
to understand grasp quality; not on the v1 build path. Alternative.

## Dex-Net / GQ-CNN

Dex-Net (and its **GQ-CNN** — Grasp-Quality Convolutional Neural
Network) is a learned system that looks at a **depth image** and scores
candidate **top-down parallel-jaw grasps**, picking the one most likely
to hold. It was famously effective at **bin-picking**: reach into a
tote of mixed objects and reliably pull one out. The model is trained
on a massive synthetic dataset of grasps and their success, so it
generalizes well to novel objects seen from above.

Its strength is **robust top-down picking of unknown clutter** with a
plain two-finger gripper — exactly the parallel-jaw hardware the
myCobot uses. If the lab problem were "a tray of randomly dumped
vials, grab any one," Dex-Net would be a strong, well-proven fit, and
it is lighter to run than full 6-DoF prediction.

Its weakness against the others is that it is **top-down only and
clutter-oriented**, which mismatches a fixed, known vial standing
upright in a precise tray slot. The approach angle for a vial in a rack
is often *not* straight down (the cap or neighbors may block a vertical
descent), and Dex-Net does not reason about full 6-DoF approach the way
Contact-GraspNet does. Against the analytical method it is wildly
heavier for a grasp we already know exactly; against MTC it is, like
the other predictors, only a grasp source needing a sequencer; against
GraspIt! it trades interpretable metrics for a black-box score. A great
tool for the wrong problem here. Alternative.

## Verdict

- **Best-in-class:** **Contact-GraspNet** — strongest open,
  learned 6-DoF grasping, the right ceiling if vials/objects become
  varied and known-pose tricks stop working (with **AnyGrasp** as the
  commercial step beyond). For v1's single known vial it is genuine
  overkill.
- **Cheapest:** **Analytical / antipodal pinch (custom + Open3D)** —
  free, no GPU, deterministic, and exactly right for one rigid vial
  with a preferred pinch.
- **Best-practical:** **MoveIt Task Constructor wrapping the
  analytical pinch** — keeps the cheap exact grasp but gives it clean,
  collision-aware, reusable pick → lift → place stages in the ROS 2 /
  MoveIt 2 stack the rest of the cell uses.

The v1 recommendation is the cheapest grasp *source* (analytical)
driven by the best-practical *sequencer* (MTC); Contact-GraspNet is the
deliberate later upgrade, not the starting point.

## Realistic scenario & use cases

> **Why this matters for automation.** Grasping is the one layer where
> the cell physically *touches* the sample, so its automation value is
> trust: pick a smooth glass vial **firmly enough never to drop it but
> gently enough never to crack it**, every time, across vial variants —
> the single most failure-prone motion in the loop, and the one a human
> currently babysits.

**The scenario.** The gripper must lift a 2 mL glass vial from a **tight
rack nest** whose neighbours sit only ~16 mm away, carry it to the
decapper and **hold it against the twisting torque** while the cap comes
off, then place it precisely in **tray slot A3** with a straight retreat.
Along the way it meets an **under-filled vial** (off-centre mass that
wants to tip), a **crimp-cap vial seated slightly proud**, and one pick
where the vial **slips** on first contact and must be re-grasped. The grip
has to handle all of it without a crush or a drop.

The layer must therefore serve several **distinct use cases**:

1. **Secure pinch of a smooth glass vial — no crush, no slip.** Close on
   the vial with a force inside the narrow safe window for thin glass.
   - *How the solution handles it:* an **analytical antipodal pinch** on
     the vial's cylinder axis with a **force-limited** close; the safe
     force window is validated in **MuJoCo** (Layer 01's best-contacts
     pick) before it ever runs on hardware.

2. **Tight-nest pick and place with collision-aware stages.** Enter a
   16 mm-clearance nest, lift straight, transit, and seat in slot A3.
   - *How:* **MoveIt Task Constructor** sequences reusable
     `approach → grasp → lift → place → retreat` stages with the
     neighbouring vials as collision objects, reusing Layer 03's Cartesian
     approach for the straight entry/exit.

3. **Slip detection and re-grasp.** Catch the failed/slipped pick and
   retry instead of carrying nothing.
   - *How:* the gripper `JointState` (jaws closing past the expected vial
     width ⇒ empty/slip) is **two-witnessed** with the wrist camera
     (Layer 04); on disagreement MTC re-enters the pick stage.

4. **Anti-rotation hold for decap / recap.** Grip firmly enough that the
   vial doesn't spin while the decapper applies torque.
   - *How:* a higher-force "hold" grasp mode, gated by the **force-torque**
     witness on the cap joint (sensor #5), with orchestration sequencing
     hold → twist → release.

5. **Adapt to vial variants.** Handle the under-filled off-balance vial,
   the proud crimp-cap, and screw-cap differences.
   - *How:* the analytical grasp is **parameterized by vial type** read
     from the worklist (diameter, grip height, force); the off-balance
     case is exactly what MuJoCo validates, and genuinely novel labware is
     the trigger to escalate.

**Where the pick flexes.** MTC wrapping the analytical pinch
(best-practical) covers all five for the known v1 vial set. The moment
vials, caps, or labware become **varied or unlabelled** — an extreme of
use case 5 — is when **Contact-GraspNet** (best-in-class) or a **VLA
policy** earns its GPU and demonstrations, which is the upgrade path the
next section lays out.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for grasping
& manipulation — the layer that physically touches the glass.

## Force-safe pinch of a glass vial

- **The moment:** the gripper closes on a smooth 2 mL glass vial — too soft
  and it slips, too hard and it cracks.
- **How, in depth:** an **analytical antipodal pinch** on the cylinder axis
  closes with a **force limit** inside the safe glass window; that window
  is validated in **MuJoCo** (best contacts) before it ever runs, so the
  number isn't guessed.
- **Edge case it survives:** a vial slightly larger or smaller than nominal
  — the force target, not a fixed jaw width, governs the close, so a vial
  at the edge of tolerance is still held safely.
- **Walkthrough:** (1) read the vial's diameter and grip height from the
  worklist; (2) align the jaws to the cylinder axis; (3) close to the
  force target validated in MuJoCo; (4) confirm jaw width matches the vial
  before lifting.
- **In the scene:** two gripper fingers close on a smooth glass cylinder
  and stop at a precise squeeze — firm enough that the vial won't slide,
  light enough that the thin wall won't craze. The number behind that
  squeeze was settled earlier in a contact simulator, not guessed at the
  bench.
- **Why it's done this way:** glass vials are at once fragile and
  slippery, so the safe grip is a narrow band between drop and crack;
  controlling to a validated force rather than a fixed jaw position is
  what keeps the cell inside that band across normal vial tolerance.
- **In the full loop:** this is the pick at the heart of each cycle — it
  follows Layer 04's localization and Layer 03's approach, and it is the
  precondition for the decap, dispense, scan, and place steps that follow;
  nothing downstream happens until the vial is safely held.
- **Value:** the most failure-prone touch in the loop is made repeatable,
  removing the drop-or-crack risk a human babysits.

### Meta code

The shape of the force-limited pinch, before any library detail:

```text
# read the vial type from the worklist -> diameter, grip height, safe force (MuJoCo-validated)
# align the gripper to the vial's cylinder axis at the grip height
# close the jaws toward the target FORCE (not a fixed width):
#     stop as soon as measured force >= safe force          (force-limited, won't crush glass)
# confirm the closed jaw width ~ vial diameter              (we hold glass, not air)
#     mismatch -> report a failed grasp                      (-> slip / re-grasp path)
```

### Real code

A node that closes the gripper to a safe force, then checks the jaw width
confirms a vial is held. **Illustrative teaching code** — re-verify before
use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from rclpy.action import ActionClient                   # to send a gripper command goal
from control_msgs.action import GripperCommand          # position + max-effort gripper action
from sensor_msgs.msg import JointState                  # to read the actual jaw width back

VIALS = {"2mL_screw": {"dia": 0.0118, "force": 5.0},    # per-type diameter (m) + safe force (N)...
         "2mL_crimp": {"dia": 0.0115, "force": 4.5}}    # ...both validated in MuJoCo beforehand
WIDTH_TOL = 0.002                                       # jaw width must match the vial within 2 mm


class ForceSafePinch(Node):                             # closes on a vial to a force, then verifies
    def __init__(self):                                 # one-time setup
        super().__init__("force_safe_pinch")            # register on the ROS 2 graph
        self.cli = ActionClient(self, GripperCommand,   # action client to the gripper controller
                                "/gripper_controller/gripper_cmd")
        self.jaw = None                                 # latest measured jaw width (metres)
        self.create_subscription(                       # read the gripper's joint state...
            JointState, "/joint_states", self.on_js, 10)  # ...to learn the actual jaw width

    def on_js(self, msg):                               # runs on each joint-state update
        if "gripper_finger_joint" in msg.name:          # is the finger joint reported here?
            i = msg.name.index("gripper_finger_joint")  # find its index...
            self.jaw = msg.position[i] * 2.0            # ...total width ~ 2x one finger's travel

    def pinch(self, vial_type: str) -> bool:            # close on a vial of this type; True if held
        spec = VIALS[vial_type]                         # diameter + safe force for this vial
        goal = GripperCommand.Goal()                    # the command we send the gripper
        goal.command.position = spec["dia"] - 0.004     # aim just inside the diameter (a squeeze)
        goal.command.max_effort = spec["force"]         # but never exceed the safe glass force
        self.cli.wait_for_server()                      # ensure the gripper controller is up
        self.cli.send_goal_async(goal)                  # close to that position OR force, first wins
        rclpy.spin_once(self, timeout_sec=1.0)          # let a fresh /joint_states arrive
        if self.jaw is None or abs(self.jaw - spec["dia"]) > WIDTH_TOL:  # closed on air, not glass?
            self.get_logger().warn("grasp width off -> failed pinch")  # likely empty / slipped
            return False                                # -> hand to the slip / re-grasp use case
        return True                                     # jaw width matches the vial: we hold glass
```

## Slip detection and re-grasp

- **The moment:** vial 61 shifts on first contact and the pick fails; the
  arm must notice and retry, not carry nothing to the dispenser.
- **How, in depth:** the gripper `JointState` (jaws closing past the
  expected vial width ⇒ empty/slip) is **two-witnessed** with the wrist
  camera; on disagreement MoveIt Task Constructor re-enters the pick stage.
- **Edge case it survives:** a *partial* grasp that holds at first then
  slips in transit — the wrist-camera witness is re-checked before the
  place, catching a vial lost en route.
- **Walkthrough:** (1) close and read jaw width; (2) cross-check with the
  wrist camera; (3) on disagreement re-enter the MTC pick stage; (4)
  re-verify before transit, and flag the vial after *N* failed tries.
- **In the scene:** the fingers close but meet less resistance than a vial
  should give — the jaws have shut on air, or the vial twisted away. The
  wrist camera confirms the miss, and the arm calmly backs off and tries
  the pick again instead of carrying nothing onward.
- **Why it's done this way:** even a good grasp occasionally misses, and a
  cell that didn't notice would carry on placing nothing — corrupting the
  tray order; detecting the miss and retrying is what makes the pick
  reliable enough to leave unattended.
- **In the full loop:** this protects the rest of the cycle — by
  confirming the hold before transit, it ensures Layers 03/06/07 aren't
  operating on an empty gripper, so a slip is caught here rather than
  discovered at the place step.
- **Value:** a failed pick becomes a retry, not a dropped sample and a
  halted run.

### Meta code

The shape of the two-witness slip guard, before any library detail:

```text
# after a pinch attempt, gather two witnesses, time-matched:
#     gripper: jaw width ~ vial diameter?    (closed on glass vs closed on air)
#     wrist camera: is a vial at the gripper line?
# both agree "held" -> tell MTC to PROCEED to transit
# disagree / both empty:
#     tries < N -> tell MTC to REPICK (re-enter the pick stage)
#     tries >= N -> FLAG the vial for human review (don't loop forever)
```

### Real code

A node that two-witnesses the grasp (gripper width + wrist camera) and
drives a bounded retry. **Illustrative teaching code** — re-verify before
use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from sensor_msgs.msg import JointState                  # witness 1: the gripper jaw width
from std_msgs.msg import Bool, String                   # witness 2: wrist "vial present"; + command
from message_filters import Subscriber, ApproximateTimeSynchronizer  # pair the witnesses in time

VIAL_DIA = 0.0118                                       # expected jaw width when holding a vial (m)
WIDTH_TOL = 0.002                                       # within 2 mm counts as "holding glass"
MAX_TRIES = 3                                           # give up (flag) after this many retries


class SlipGuard(Node):                                  # two-witness grasp check with bounded retry
    def __init__(self):                                 # one-time setup
        super().__init__("slip_guard")                  # register on the ROS 2 graph
        self.tries = 0                                  # how many pick attempts on this vial so far
        self.cmd = self.create_publisher(String, "/mtc/command", 10)  # PROCEED / REPICK / FLAG
        jaw = Subscriber(self, JointState, "/joint_states")   # witness 1: the gripper
        cam = Subscriber(self, Bool, "/wrist/vial_present")   # witness 2: the wrist camera
        self.sync = ApproximateTimeSynchronizer(        # pair the two witnesses in time...
            [jaw, cam], queue_size=10, slop=0.1, allow_headerless=True)
        self.sync.registerCallback(self.on_pair)        # ...and judge each matched pair

    def on_pair(self, js, present):                     # runs on a time-matched (gripper, camera) pair
        held = ("gripper_finger_joint" in js.name and   # the gripper says "holding glass" when...
                abs(js.position[js.name.index("gripper_finger_joint")] * 2 - VIAL_DIA) <= WIDTH_TOL)
        if held and present.data:                       # BOTH witnesses agree a vial is held
            self.tries = 0                              # reset the counter for the next vial
            self.cmd.publish(String(data="PROCEED"))    # tell MTC to carry on to transit
        elif self.tries < MAX_TRIES:                    # they disagree / both empty -> retry
            self.tries += 1                             # count this failed attempt
            self.cmd.publish(String(data="REPICK"))     # tell MTC to re-enter the pick stage
        else:                                           # too many failures on this vial
            self.cmd.publish(String(data="FLAG"))       # park it for human review (never loop)


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(SlipGuard()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## Anti-rotation hold for decap/recap

- **The moment:** the decapper applies torque to unscrew a cap; if the vial
  spins in the jaws nothing comes off and the cap may strip.
- **How, in depth:** a higher-force **hold** grasp mode is engaged, gated
  by the **force-torque** witness on the cap joint (sensor #5), while
  orchestration sequences hold → twist → release.
- **Edge case it survives:** a stuck cap whose torque spikes past normal —
  the force-torque reading trips a limit, so the cell stops and flags
  rather than wrenching the vial out of the nest.
- **Walkthrough:** (1) engage the high-force hold grasp; (2) the decapper
  applies twist; (3) the cap-joint force-torque is watched throughout; (4)
  stop and flag on an over-torque, otherwise release after the cap is off.
- **In the scene:** the gripper clamps down hard and holds while the
  decapper grips the cap and twists; a torque gauge on the cap joint
  watches the strain, and if a stuck cap fights back too hard the whole
  move freezes rather than wrenching the vial out of its nest.
- **Why it's done this way:** removing a cap means fighting friction, and
  if the vial spins or the cap is stuck a blind twist can shatter glass or
  strip the cap; holding firmly and watching torque turns an open-loop
  wrench into a monitored, abortable step.
- **In the full loop:** this enables the decap sub-step between pick and
  dispense — holding against the decapper's torque is what lets the cap
  come off so the dispenser can fill, before a recap and the scan-and-place
  that follow.
- **Value:** decapping becomes a controlled, monitored action instead of a
  blind twist that risks shattering glass.

### Meta code

The shape of the monitored decap, before any library detail:

```text
# engage the high-force HOLD grasp (firmer than a transport pinch)
# tell the decapper to start twisting the cap
# while twisting, watch the cap-joint force-torque (sensor #5):
#     torque rose then collapsed below FREE -> cap broke free -> stop, release   (success)
#     torque exceeds STUCK limit -> stuck cap -> stop, flag, do NOT wrench        (abort safely)
# on success: release the hold; on abort: leave the vial in the nest + flag
```

### Real code

A node that holds the vial firmly and supervises the un-cap by torque,
aborting on a stuck cap. **Illustrative teaching code** — re-verify before
use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from rclpy.action import ActionClient                   # to command the gripper hold
from control_msgs.action import GripperCommand          # gripper position + max-effort
from geometry_msgs.msg import WrenchStamped             # the cap-joint force-torque (sensor #5)
from std_srvs.srv import Trigger                        # start/stop the decapper twisting

HOLD_FORCE = 8.0                                        # firmer than a transport pinch (N)
STUCK_NM = 4.0                                          # abort above this un-cap torque (N*m)
FREE_NM = 0.5                                           # torque falling below this -> cap is off


class AntiRotationDecap(Node):                          # holds the vial and supervises the un-cap
    def __init__(self):                                 # one-time setup
        super().__init__("anti_rotation_decap")         # register on the ROS 2 graph
        self.grip = ActionClient(self, GripperCommand,  # action client for the gripper hold
                                 "/gripper_controller/gripper_cmd")
        self.start = self.create_client(Trigger, "/decapper/start")  # start the decapper twist
        self.stop = self.create_client(Trigger, "/decapper/stop")    # stop it (success or abort)
        self.peak = 0.0                                 # highest torque seen this decap
        self.done = False                               # latch so we judge/stop only once
        self.create_subscription(                       # watch the cap-joint force-torque...
            WrenchStamped, "/decapper/wrench", self.on_wrench, 10)

    def decap(self):                                    # begin one monitored decap
        goal = GripperCommand.Goal()                    # the firm HOLD command
        goal.command.position = 0.010                   # close onto the vial body...
        goal.command.max_effort = HOLD_FORCE            # ...with the higher hold force
        self.grip.wait_for_server()                     # ensure the gripper controller is up
        self.grip.send_goal_async(goal)                 # engage and hold the vial against twist
        self.start.call_async(Trigger.Request())        # tell the decapper to start unscrewing

    def on_wrench(self, msg):                           # runs on each cap-joint torque sample
        if self.done:                                   # already finished this decap?
            return                                      # ignore further samples
        tz = abs(msg.wrench.torque.z)                   # the un-cap torque about the cap axis
        self.peak = max(self.peak, tz)                  # remember the peak for the success test
        if tz > STUCK_NM:                               # the cap is fighting back too hard
            self.done = True                            # latch: stop reacting
            self.stop.call_async(Trigger.Request())     # STOP twisting -> never wrench the vial out
            self.get_logger().error("stuck cap -> abort + flag")  # leave it in the nest, flag it
        elif self.peak > FREE_NM and tz < FREE_NM:      # torque rose then collapsed...
            self.done = True                            # latch: success path
            self.stop.call_async(Trigger.Request())     # stop the now freely-spinning decapper
            self.get_logger().info("cap free -> release hold")  # release the vial; decap done
```

## The learned upgrade path — VLA / generalist policies

The five above are the **v1 toolbox**. Beyond them sits the frontier:
**Vision-Language-Action (VLA)** foundation models that take camera
frames + a text instruction (*"pick the vial, place it in slot A3"*) and
emit robot actions **end-to-end**, learned from demonstrations rather
than hand-coded geometry. A strong VLA collapses perception (Layer 04),
grasp choice, and even some sequencing into one trained network — so it
belongs *primarily* here in manipulation, but cuts across several layers.
The full comparison (open vs closed, sim support, data/GPU needs,
compliance caveats) is in
[`../foundation-models.md`](../foundation-models.md); the short version:

| Model / ecosystem | Who | Open? | In only-code you can… |
|---|---|---|---|
| **π0 / π0.5 / π0.6** (openpi) | Physical Intelligence | Open | Roll out / fine-tune the strongest open flagship on sim demos |
| **Gemini Robotics 1.5 / -ER / On-Device** | Google DeepMind | Mostly closed | Prototype against the API/SDK; track the capability ceiling |
| **OpenVLA (+ OFT)** | Stanford/Berkeley/TRI | Open | Fine-tune the clean 7B baseline — the VLA "hello world" |
| **Isaac GR00T N1.5 / N1.7** | NVIDIA | Open (Apache-2.0) | Train sim-native in Isaac Lab with synthetic demos |
| **LeRobot + SmolVLA** | Hugging Face | Open | Start here: record sim demos, train a ~450M model on a normal GPU |

In **only-code** mode the appeal is that you can **prove the whole
learned workflow with zero hardware**: roll a pretrained policy out on a
simulation benchmark (LIBERO / SIMPLER / ManiSkill, or GR00T in Isaac
Lab), generate **synthetic demonstrations**, fine-tune, and measure
success on a simulated vial-pick — before buying anything.

Why this stays an *upgrade*, not the v1 plan: for **one known rigid vial
in a known slot**, a VLA spends a GPU and a pile of demonstrations
relearning the pinch the analytical method gives for free, and — being a
non-deterministic black box — is far harder to **validate** for a
regulated lab (21 CFR Part 11 / IQ-OQ-PQ; see
[`../foundation-models.md`](../foundation-models.md)). Its value arrives
when the lab needs **generalization** — many vial types, novel labware,
spoken instructions — which is exactly the later milestone this stack
defers learned methods to.

## See also

- [`README.md`](README.md) — the only-code layer guide and the other
  seven development layers.
- [`../foundation-models.md`](../foundation-models.md) — the full VLA /
  generalist-policy comparison this section summarizes.
- [`../02-code-plus-hardware/05-grasping-and-manipulation.md`](../02-code-plus-hardware/05-grasping-and-manipulation.md)
  — the same layer once the grasp must **execute on the real
  gripper** (slip, grip force, closing width, hold verification).
