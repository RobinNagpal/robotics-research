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

## Meta code

The best-practical pick wraps the analytical pinch in **MoveIt Task
Constructor** stages. The heart of the "close gripper" stage is the
**two-witness "did we get it?"** check: close the jaws, then read the
gripper's own servo feedback (#4 — jaw width + effort) to decide
*held* vs *empty* before the lift fires.

```text
# command the gripper to close on the vial             (the analytical pinch pose)
# read the gripper's servo feedback                    (sensor #4: joint state + effort)
#     jaw width  = how far apart the jaws ended up      (position of the gripper joint)
#     effort     = how hard the motor is pushing        (current/torque on that joint)
# decide held vs empty from a band:
#     if jaws closed all the way (width ~0):            (nothing between them)
#         -> EMPTY: the pinch missed                     (-> branch to retry)
#     if jaws stopped at ~vial width AND effort is high: (glass is resisting the squeeze)
#         -> HELD: a vial is in the jaws                  (-> lift stage may fire)
#     otherwise (too wide, or no resistance):           (slipped / wrong object)
#         -> EMPTY: do not trust the grasp               (-> branch to retry)
# (the wrist camera #3 is the second witness; both must agree before lifting)
```

## Real code

A minimal but complete ROS 2 (`rclpy`) node for the grasp-verification
witness — the analytical pinch is sequenced by **MoveIt Task
Constructor**, and this node reads **`ros2_control`** gripper feedback
(sensor #4) to confirm the catch. This is **illustrative teaching
code**: library and message names drift between versions, so re-verify
before relying on it. Every line carries an inline comment.

```python
import rclpy                                      # ROS 2 Python client library (the robot framework)
from rclpy.node import Node                       # base class every ROS 2 program ("node") builds on
from sensor_msgs.msg import JointState            # message carrying each joint's position + effort
from std_msgs.msg import String                   # simple text message we use to report held / empty

# --- known facts about the gripper and the 2 mL vial it pinches ---
GRIPPER_JOINT = "gripper_finger_joint"             # the joint whose position = how far the jaws are open
CLOSED_WIDTH = 0.002                                # jaws this closed (~2 mm) mean they met: nothing held
VIAL_WIDTH_LO = 0.010                               # a gripped ~12 mm vial leaves the jaws at least this open
VIAL_WIDTH_HI = 0.014                               # ...and at most this open: the expected jaw-width band
HOLD_EFFORT = 0.5                                   # this much motor effort (N·m-ish) means glass is resisting


class GraspWitness(Node):                          # our grasp-verification node, built on the ROS 2 Node class
    def __init__(self):                            # set-up that runs once, when the node is created
        super().__init__("grasp_witness")          # register on the ROS 2 graph under the name "grasp_witness"
        self.sub = self.create_subscription(       # start listening to the gripper's feedback (sensor #4)
            JointState, "/joint_states",           # message type, then the topic ros2_control publishes on
            self.on_joints, 10)                     # call self.on_joints per update; 10 = inbox queue depth
        self.pub = self.create_publisher(          # open an outgoing channel to report the verdict
            String, "/grasp/held", 10)             # type, topic the MTC "close" stage reads, queue depth

    def on_joints(self, msg):                       # runs automatically each time joint feedback arrives
        if GRIPPER_JOINT not in msg.name:          # does this update even mention the gripper joint?
            return                                  # no -> ignore it (it was about the arm joints)
        i = msg.name.index(GRIPPER_JOINT)          # find where the gripper joint sits in the parallel lists
        width = msg.position[i]                    # jaw opening right now, in metres (how far apart the jaws)
        effort = abs(msg.effort[i])                # how hard the gripper motor is pushing (its current/torque)
        verdict = self.classify(width, effort)     # turn those two numbers into "held" or "empty"
        self.pub.publish(String(data=verdict))     # send the verdict out for the MTC sequence to act on
        self.get_logger().info(                     # print a tidy status line for sanity
            f"{verdict}: width={width:.3f} m effort={effort:.2f}")  # show the numbers behind the call

    def classify(self, width, effort):              # the two-witness band: held vs empty from #4 alone
        if width <= CLOSED_WIDTH:                  # did the jaws shut all the way to nearly touching?
            return "empty"                          # yes -> nothing was between them: the pinch missed
        gripping = VIAL_WIDTH_LO <= width <= VIAL_WIDTH_HI  # did the jaws stop in the vial-width band?
        if gripping and effort >= HOLD_EFFORT:     # AND is the motor straining against the glass?
            return "held"                           # yes to both -> a vial is genuinely in the jaws
        return "empty"                              # otherwise: too wide, or no resistance -> don't trust it


def main():                                        # the standard ROS 2 program entry point
    rclpy.init()                                    # start up the ROS 2 client library (must come first)
    node = GraspWitness()                           # build our node, which runs its __init__ set-up
    rclpy.spin(node)                                # keep handling gripper feedback until you press Ctrl-C
    node.destroy_node()                             # remove the node from the graph on shutdown
    rclpy.shutdown()                                # close the ROS 2 client library cleanly


if __name__ == "__main__":                          # only run if this file is launched directly
    main()                                          # ...then start everything above
```

This node is only the *first* of the two witnesses. The MTC "close
gripper" stage waits for a `held` here **and** a wrist-camera glance
(#3) before firing the lift; either one dissenting branches to a retry.
See [`../sensor-suite.md`](../sensor-suite.md) for the full two-witness
habit.

## See also

- [`README.md`](README.md) — the only-code layer guide and the other
  seven development layers.
- [`../foundation-models.md`](../foundation-models.md) — the full VLA /
  generalist-policy comparison this section summarizes.
- [`../02-code-plus-hardware/05-grasping-and-manipulation.md`](../02-code-plus-hardware/05-grasping-and-manipulation.md)
  — the same layer once the grasp must **execute on the real
  gripper** (slip, grip force, closing width, hold verification).
