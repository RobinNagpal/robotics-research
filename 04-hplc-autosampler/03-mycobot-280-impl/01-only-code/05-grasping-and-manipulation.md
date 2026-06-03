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
the recommended v1 path.

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

## See also

- [`README.md`](README.md) — the only-code layer guide and the other
  seven development layers.
- [`../02-code-plus-hardware/05-grasping-and-manipulation.md`](../02-code-plus-hardware/05-grasping-and-manipulation.md)
  — the same layer once the grasp must **execute on the real
  gripper** (slip, grip force, closing width, hold verification).
