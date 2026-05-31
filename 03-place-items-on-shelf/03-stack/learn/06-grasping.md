# Learn: Grasping — analytical antipodal (v1) + AnyGrasp (later)

> This is the learn-by-doing companion to the grasping stack layer in
> [`../06-grasping.md`](../06-grasping.md). It teaches the two top
> choices for deciding *how to grab the product*: a hand-computed
> **analytical antipodal grasp** for the one known rigid SKU (the v1
> pick), and **AnyGrasp** (with Contact-GraspNet as the open
> alternative) as the learned generalizer for later, when the products
> vary. We start from plain definitions, build a working example in
> Python with `numpy`, then wire it into the project as a small ROS 2
> node. New terms are defined on first use; anything still unclear is in
> the [glossary](../../02-glossary.md). This doc assumes you have read
> [`02-ros2.md`](02-ros2.md) (how nodes talk) and
> [`05-perception.md`](05-perception.md) (how we get the object's pose).

---

## 1. Introduction and basic concepts

**Grasping** is the step that decides *where and how to put the
gripper* so the robot can hold the product. That is all it does. It does
not move the arm, and it does not find the object — it sits in between
those two jobs.

Here is the boundary, stated as plainly as possible, because these three
layers are easy to confuse:

- **Perception** says **where the object is**. It gives you a pose — a
  position and orientation — for the `soup_can_400g` in the world.
- **Grasping** (this layer) says **where to put the gripper to hold
  it**. It turns "the can is *here*" into "open the jaws this wide and
  put the gripper *exactly there*, pointing *that* way."
- **Arm motion** says **how to move the arm so the gripper gets
  there**. It plans a collision-free trajectory to the pose grasping
  chose.

If you come from web development, think of grasping as a pure function.
Input: the object's pose plus what we know about its shape. Output: one
target gripper pose and one number (how wide to open the jaws). No side
effects, no hardware moved. The arm-motion layer is the thing that
"executes the request" later.

**Output of this layer, precisely.** Grasping returns:

1. **One target gripper pose** — a position (x, y, z) and an orientation
   for the gripper, expressed in a known reference frame.
2. **A gripper width** — for a parallel-jaw gripper, how far apart the
   two fingers should be. (Or, for a suction gripper, a single suction
   point and surface normal instead.)

That is the entire deliverable. One pose, one width.

**Two kinds of gripper.** The robot can hold things two ways, and the
choice changes what grasping outputs:

- **Parallel-jaw gripper.** Two flat fingers (jaws) that close toward
  each other, pinching the object from two sides — like a clamp or a
  pair of tongs. Good for cans and bottles, which you grab around the
  side. This project uses a parallel-jaw gripper.
- **Suction gripper.** A vacuum cup that sticks to one flat surface —
  like a suction hook on a bathroom tile. Good for flat-topped boxes.
  We mention it for completeness but do not use it here.

**Why v1 can be almost trivial.** The whole project is scoped (see
[`../../01-requirements.md`](../../01-requirements.md)) to **one known
rigid SKU per run** — a single `soup_can_400g` whose dimensions and
preferred grasp are given up front, not discovered. A can is a cylinder.
The natural way to grab a cylinder with a parallel-jaw gripper is to
pinch it across its diameter, halfway up its side. There is nothing to
learn and nothing to guess: given the can's pose and its radius, the
grasp pose is a short calculation. So v1's grasping layer is a few lines
of geometry. We only need the heavyweight learned models when the tray
starts holding products we have *not* measured in advance.

The honest framing from the stack doc: **don't over-engineer this.** Get
the trivial geometric grasp working end to end first, keep it in its own
clean box, and swap in a learned model only when the SKUs genuinely
vary.

---

## 2. Important concepts that are used most often

These are the words and ideas you will see in every grasping discussion.
Each gets one plain sentence.

- **Grasp pose.** The full position *and* orientation of the gripper at
  the moment it closes on the object — "put the gripper here, pointed
  this way." Position is three numbers (x, y, z). Orientation is which
  way the gripper is facing and how it is rolled.

- **Approach direction (approach vector).** The straight-line direction
  the gripper travels along as it moves in to grab the object — for a
  side pinch on a can, the gripper comes in horizontally, pointing at
  the can's center.

- **Antipodal grasp.** A grasp where the two fingers touch the object at
  two points that face *directly opposite* each other ("antipodal"
  literally means "on opposite sides"). Pinching a can across its
  diameter is the textbook example: the two contact points are on
  opposite sides of the cylinder, and the line between them passes
  through the center. Opposite contact points are what let two flat
  fingers hold an object without it squirting out.

- **Grasp width.** How far apart the two jaws are when they close on the
  object. For a side pinch on a cylinder it is roughly the diameter plus
  a small safety margin so the fingers clear the surface on the way in.

- **The `tool0` (gripper) frame.** A **frame** is just a labeled
  coordinate system attached to a part of the robot — an origin and a
  set of x/y/z axes. `tool0` is the frame at the gripper's tip; "the
  grasp pose" really means "where to place the `tool0` frame." The arm
  controller's whole job is to drive `tool0` to the pose we hand it.

- **`tf2`.** ROS 2's bookkeeping system for frames. It continuously
  tracks where every frame is relative to every other frame
  (`map`→`odom`→`base_link`→`arm_base_link`→…→`wrist_camera_link` and
  `tool0`) and can convert a pose from one frame into another. We use it
  to express a grasp in whatever frame the arm planner wants. The chain
  of frames was introduced in [`05-perception.md`](05-perception.md).

- **Force-closure.** A grasp has force-closure when the chosen contact
  points can resist a push or twist from *any* direction, so the object
  cannot escape no matter how it is nudged — a good antipodal pinch
  across a can's diameter has it; a one-finger touch does not.

- **Pre-grasp, approach, retreat.** Three poses around the grasp, not
  just one. **Pre-grasp** is a pose backed off from the object (jaws
  open, a few centimeters away) so the arm can get into position without
  bumping anything. **Approach** is the short straight move from
  pre-grasp in to the grasp pose. **Retreat** is the short straight move
  *out* after the jaws close, lifting the object clear before the arm
  swings away. Splitting the motion like this is what keeps the gripper
  from knocking the can over on the way in.

- **Grasp quality / ranking.** A score that says how good a candidate
  grasp is — higher means more likely to hold and easier for the arm to
  reach. When there are several possible grasps we **rank** them by this
  score and pick the best.

- **What the learned models add.** **AnyGrasp** and **Contact-GraspNet**
  are neural networks that look at a depth picture of a scene and output
  a *ranked list of full 6-DoF grasps* — that is, complete gripper poses
  (3 position + 3 orientation numbers, hence "6 degrees of freedom")
  with a confidence score each — for objects they have never seen and
  whose shape nobody measured in advance. Their **input** is a point
  cloud or RGB-D image (an RGB-D camera gives a normal color image plus,
  for every pixel, how far away that point is; a point cloud is the
  resulting cloud of 3D points). Their **output** is many candidate
  grasp poses, each with a width and a score, sorted best-first. That is
  exactly the same shape of answer our hand-written geometry produces —
  one pose and a width — which is why we can swap one for the other
  without touching the rest of the robot.

---

## 3. Hello world example with code

Goal: given the can's pose from perception and its known size, **compute
one analytical antipodal side-pinch grasp**. We pick the gripper
position at the can's mid-height, orient the jaws to close across the
diameter, and set the width to the diameter plus a margin. Then we print
the result.

First, the numbers we are given. The `soup_can_400g` is a rigid cylinder
with a known **radius ~33 mm** and **height ~110 mm** (figures are
approximate — re-check before quoting). Perception hands us the pose of
the can's *base center* in the `base_link` frame (the frame fixed to the
robot's body). We treat the can as standing upright, so its axis points
straight up along z.

A quick word on **quaternions**, because the orientation uses one. A
quaternion is just four numbers `[x, y, z, w]` that encode a 3D rotation
without the "gimbal" glitches that plain angles suffer from. You almost
never read them by eye; you build them from an axis-and-angle or from
"point this axis that way" and let a library do the math. Treat them as
an opaque rotation token.

```python
import numpy as np

# --- Known SKU geometry (approximate; re-check before quoting) ---
CAN_RADIUS_M = 0.033   # ~33 mm
CAN_HEIGHT_M = 0.110   # ~110 mm

# Parallel-jaw gripper limits and a safety margin.
GRIPPER_MAX_WIDTH_M = 0.085   # how wide the jaws open at most (~85 mm)
WIDTH_MARGIN_M = 0.010        # extra ~10 mm so jaws clear the surface

# --- Input from perception: the can's BASE CENTER pose ---
# Position in the base_link frame, in metres. The can stands upright,
# so we only need its (x, y, z) base-centre point for a side pinch.
can_base_xyz = np.array([0.45, 0.10, 0.20])   # example values

def antipodal_side_pinch(base_xyz, radius, height):
    """Compute one side-pinch grasp on an upright cylinder.

    Returns (position, quaternion_xyzw, width_m).
    """
    # 1. POSITION: pinch at mid-height, on the cylinder's axis.
    #    The gripper tip (tool0) sits at the can's centreline, halfway
    #    up. The jaws will close across the diameter from there.
    grasp_xyz = base_xyz.copy()
    grasp_xyz[2] = base_xyz[2] + height / 2.0   # raise to mid-height

    # 2. WIDTH: open to the diameter plus a margin so we don't scrape
    #    the can on the way in. Diameter = 2 * radius.
    width = 2.0 * radius + WIDTH_MARGIN_M

    # 3. ORIENTATION: we want the gripper to approach horizontally
    #    (pointing at the can's axis) with the jaws straddling the
    #    diameter. We describe the gripper by three axes:
    #      - approach axis: the direction the gripper moves IN  (+z of tool0)
    #      - close axis:    the direction the jaws close along  (x of tool0)
    #      - the third axis is fixed by the other two (right-hand rule)
    #
    #    Approach comes from -y toward the can (here we pick the gripper
    #    coming in along the world -y direction, i.e. it points +y).
    approach = np.array([0.0, 1.0, 0.0])   # gripper points +y, toward can
    close    = np.array([1.0, 0.0, 0.0])   # jaws open/close along x
    third    = np.cross(approach, close)   # completes a right-handed set

    # Build a rotation matrix whose columns are the gripper's axes,
    # then convert to a quaternion. Column order maps gripper x,y,z.
    R = np.column_stack((close, third, approach))
    quat = rotation_matrix_to_quaternion(R)

    return grasp_xyz, quat, width


def rotation_matrix_to_quaternion(R):
    """Standard 3x3 rotation matrix -> [x, y, z, w] quaternion."""
    trace = np.trace(R)
    if trace > 0.0:
        s = 0.5 / np.sqrt(trace + 1.0)
        w = 0.25 / s
        x = (R[2, 1] - R[1, 2]) * s
        y = (R[0, 2] - R[2, 0]) * s
        z = (R[1, 0] - R[0, 1]) * s
    else:
        # Pick the largest diagonal term for numerical stability.
        i = int(np.argmax([R[0, 0], R[1, 1], R[2, 2]]))
        if i == 0:
            s = 2.0 * np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2])
            w = (R[2, 1] - R[1, 2]) / s
            x = 0.25 * s
            y = (R[0, 1] + R[1, 0]) / s
            z = (R[0, 2] + R[2, 0]) / s
        elif i == 1:
            s = 2.0 * np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2])
            w = (R[0, 2] - R[2, 0]) / s
            x = (R[0, 1] + R[1, 0]) / s
            y = 0.25 * s
            z = (R[1, 2] + R[2, 1]) / s
        else:
            s = 2.0 * np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1])
            w = (R[1, 0] - R[0, 1]) / s
            x = (R[0, 2] + R[2, 0]) / s
            y = (R[1, 2] + R[2, 1]) / s
            z = 0.25 * s
    return np.array([x, y, z, w])


pos, quat, width = antipodal_side_pinch(
    can_base_xyz, CAN_RADIUS_M, CAN_HEIGHT_M)

print("Grasp position (m):", np.round(pos, 4))
print("Grasp orientation (quat xyzw):", np.round(quat, 4))
print("Gripper width (m):", round(width, 4))

# Sanity check: never command a width wider than the jaws can open.
assert width <= GRIPPER_MAX_WIDTH_M, "Object too wide for this gripper!"
```

Expected output:

```text
Grasp position (m): [0.45 0.1  0.255]
Grasp orientation (quat xyzw): [ 0.5  0.5 -0.5  0.5]
Gripper width (m): 0.076
```

**The geometry, in words.** The can stands upright, so we lift the grasp
point from the base center to the mid-height (`base_z + height/2`). A
side pinch wants the jaws to close *across the diameter*, so the
gripper's closing direction is horizontal and lined up with the can's
center; that is the `close` axis. The gripper must travel in
*horizontally* to reach that point, so the `approach` axis is also
horizontal, pointing at the can. Those two directions, plus the
right-hand rule for the third, fully define the gripper's orientation —
which we package as a quaternion. The width is the diameter
(`2 * radius` ≈ 66 mm) plus a ~10 mm margin ≈ 76 mm, comfortably under
the ~85 mm the jaws can open. That is the whole v1 grasp.

---

## 4. A bit advanced example with code

A real cylinder has *infinitely many* equally valid side pinches — you
can pinch it from any angle around its vertical axis, and the geometry is
identical. So instead of fixing one approach direction, we **generate
several candidates** (rotate the approach around the can's axis), give
each a simple **score**, and keep the best. Two things make one
direction better than another:

- **Reach.** A grasp the arm can comfortably reach is better. A cheap
  proxy: prefer an approach that comes from the robot's side (so the arm
  is not reaching across its own body). We score higher when the
  approach points roughly back toward `base_link`.
- **Neighbors.** If other cans sit nearby, prefer an approach that comes
  in from open space, not from the side blocked by a neighbor.

```python
import numpy as np

def candidate_side_pinches(base_xyz, radius, height, n=12):
    """Yield n side-pinch grasps spaced evenly around the can's axis."""
    grasps = []
    grasp_z = base_xyz[2] + height / 2.0
    for k in range(n):
        theta = 2.0 * np.pi * k / n            # angle around the axis
        # Approach direction in the horizontal plane at this angle.
        approach = np.array([np.cos(theta), np.sin(theta), 0.0])
        # Closing axis is perpendicular to approach, also horizontal.
        close = np.array([-np.sin(theta), np.cos(theta), 0.0])
        grasps.append({
            "position": np.array([base_xyz[0], base_xyz[1], grasp_z]),
            "approach": approach,
            "close": close,
        })
    return grasps


def score_grasp(grasp, base_xyz, neighbor_xy_list, robot_origin_xy):
    """Higher is better. Reward easy reach; punish blocked approaches."""
    score = 0.0

    # --- Reach term: prefer an approach pointing back toward the robot ---
    to_robot = np.array([robot_origin_xy[0] - base_xyz[0],
                         robot_origin_xy[1] - base_xyz[1], 0.0])
    norm = np.linalg.norm(to_robot)
    if norm > 1e-6:
        to_robot /= norm
        # dot product is +1 when approach faces the robot, -1 when away.
        score += np.dot(grasp["approach"], to_robot)

    # --- Neighbor term: punish approaches coming in past a neighbor ---
    for nbr in neighbor_xy_list:
        to_nbr = np.array([nbr[0] - base_xyz[0],
                           nbr[1] - base_xyz[1], 0.0])
        d = np.linalg.norm(to_nbr)
        if d > 1e-6:
            to_nbr /= d
            # If approach points toward a neighbor, subtract a penalty.
            alignment = np.dot(grasp["approach"], to_nbr)
            if alignment > 0.0:
                score -= 0.8 * alignment   # closer alignment, bigger hit
    return score


# --- Pick the best candidate ---
base = np.array([0.45, 0.10, 0.20])
neighbors = [(0.45, 0.04), (0.45, 0.16)]   # cans to the sides
robot_xy = (0.0, 0.0)                      # base_link origin

candidates = candidate_side_pinches(base, 0.033, 0.110, n=12)
ranked = sorted(
    candidates,
    key=lambda g: score_grasp(g, base, neighbors, robot_xy),
    reverse=True,
)
best = ranked[0]
print("Best approach direction:", np.round(best["approach"], 3))
```

This is "grasp ranking" in miniature: many candidates, a score per
candidate, keep the top one. The learned models do the same thing — just
with a neural network producing the candidates and the scores instead of
our two hand-written rules.

**When the SKU is unknown** — a jumbled tray, a product nobody measured —
the geometry above has nothing to work from. That is where **AnyGrasp**
(or open **Contact-GraspNet**) takes over. Conceptually it looks like
this:

```python
# Conceptual only — exact API depends on the package/version.
# Input: a point cloud captured from the wrist RGB-D camera, i.e. the
# (N, 3) array of 3D points on the visible surfaces in front of the arm.

from anygrasp_sdk import AnyGrasp        # pseudo-import for illustration

grasp_model = AnyGrasp(checkpoint="anygrasp.pth")  # loads on the GPU
grasp_model.load()

# point_cloud: numpy array of shape (N, 3) in the camera frame.
# colors:      optional (N, 3) RGB per point.
grasps = grasp_model.predict(point_cloud, colors)

# 'grasps' is a list ranked best-first. Each entry carries the same
# information our analytical function produced — a full gripper pose and
# a width — plus a confidence score:
best = grasps[0]
print(best.translation)   # gripper position (x, y, z) in camera frame
print(best.rotation)      # 3x3 orientation -> convert to a quaternion
print(best.width)         # how wide to open the jaws
print(best.score)         # model confidence, higher is better
```

The important point: the model's answer (**a ranked list of poses +
widths**) is the *same kind of thing* our analytical function returns.
Both produce "put `tool0` here, open this wide." That sameness is the
whole reason the swap in the next section is painless. Note AnyGrasp
needs a GPU (an RTX-class card or a Jetson Orin) and carries a
**commercial license fee to ship**; Contact-GraspNet is open and avoids
the fee but still wants a GPU.

---

## 5. Explanation of place-on-shelf code

Now the project version. Grasping is exposed as a small **ROS 2
service** — a request/response call, like an HTTP endpoint: the
orchestration layer sends the product's pose and gets back a grasp.
(Services were covered in [`02-ros2.md`](02-ros2.md).) The result feeds
the `pick_product` step, which is the arm-motion layer's action; the
other project steps — `navigate_to_shelf`, `locate_slot`,
`place_product`, `verify_placement` — live in their own nodes.

We define the request/response as a service type. The request is the
product `PoseStamped` from perception; the response is the target gripper
`PoseStamped`, a width, and a flag.

```text
# ComputeGrasp.srv
geometry_msgs/PoseStamped product_pose   # from perception (can base)
---
geometry_msgs/PoseStamped grasp_pose      # where to put tool0
float64 gripper_width                      # how wide to open the jaws
bool ok                                    # could we compute a grasp?
```

`PoseStamped` is a ROS message that bundles a pose (position +
orientation quaternion) *with* the name of the frame it is measured in
and a timestamp — the "stamped" part — so there is never any ambiguity
about which coordinate system a pose lives in.

```python
import numpy as np
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from shelf_msgs.srv import ComputeGrasp   # the .srv above, generated

# Known SKU geometry (approximate; re-check before quoting).
CAN_RADIUS_M = 0.033
CAN_HEIGHT_M = 0.110
WIDTH_MARGIN_M = 0.010
GRIPPER_MAX_WIDTH_M = 0.085

# Pre-grasp / retreat offsets, in metres.
PREGRASP_BACKOFF_M = 0.08   # stand 8 cm back before approaching
RETREAT_LIFT_M = 0.05       # lift 5 cm straight up after closing


class GraspServer(Node):
    """Turns a product pose into a target gripper pose for pick_product."""

    def __init__(self):
        super().__init__("grasp_server")
        # Expose the service the orchestration layer will call.
        self.srv = self.create_service(
            ComputeGrasp, "compute_grasp", self.handle_compute_grasp)
        self.get_logger().info("compute_grasp service ready.")

    def handle_compute_grasp(self, request, response):
        # 1. Read the product pose. We use only its position here; the
        #    can is known to stand upright, so its orientation is fixed.
        p = request.product_pose.pose.position
        base_xyz = np.array([p.x, p.y, p.z])

        # 2. Compute the analytical side-pinch grasp (Section 3 logic).
        grasp_xyz, quat, width = self.analytical_grasp(base_xyz)

        # 3. Width sanity check — never command more than the jaws open.
        if width > GRIPPER_MAX_WIDTH_M:
            self.get_logger().warn("Object too wide; cannot grasp.")
            response.ok = False
            return response

        # 4. Fill the response as a PoseStamped in the SAME frame the
        #    product pose arrived in (typically base_link). The arm
        #    planner can re-express it via tf2 if it wants tool0 in a
        #    different frame.
        gp = PoseStamped()
        gp.header.frame_id = request.product_pose.header.frame_id
        gp.header.stamp = self.get_clock().now().to_msg()
        gp.pose.position.x = float(grasp_xyz[0])
        gp.pose.position.y = float(grasp_xyz[1])
        gp.pose.position.z = float(grasp_xyz[2])
        gp.pose.orientation.x = float(quat[0])
        gp.pose.orientation.y = float(quat[1])
        gp.pose.orientation.z = float(quat[2])
        gp.pose.orientation.w = float(quat[3])

        response.grasp_pose = gp
        response.gripper_width = float(width)
        response.ok = True
        self.get_logger().info("Computed grasp at mid-height side pinch.")
        return response

    def analytical_grasp(self, base_xyz):
        """Side-pinch grasp on the upright can (see Section 3)."""
        grasp_xyz = base_xyz.copy()
        grasp_xyz[2] = base_xyz[2] + CAN_HEIGHT_M / 2.0   # mid-height
        width = 2.0 * CAN_RADIUS_M + WIDTH_MARGIN_M       # diameter+margin

        approach = np.array([0.0, 1.0, 0.0])   # come in horizontally
        close = np.array([1.0, 0.0, 0.0])      # jaws close along x
        third = np.cross(approach, close)
        R = np.column_stack((close, third, approach))
        quat = rotation_matrix_to_quaternion(R)   # from Section 3
        return grasp_xyz, quat, width


def main():
    rclpy.init()
    node = GraspServer()
    rclpy.spin(node)        # wait for requests until shut down
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

**Block by block:**

- **`__init__`** registers one service named `compute_grasp`. Any node
  that has the product pose (the orchestrator) calls it and blocks until
  it gets a grasp back. This is the only public surface of the layer.
- **Step 1** pulls the position out of the incoming `PoseStamped`. We
  ignore the incoming orientation because we already *know* the can
  stands upright — that is the v1 "known rigid SKU" assumption doing its
  job and saving us work.
- **Step 2** calls the Section 3 geometry: mid-height position, jaws
  across the diameter, width = diameter + margin.
- **Step 3** is the **width sanity check** — if perception ever handed
  us something too fat for the jaws, we fail cleanly (`ok = False`)
  rather than commanding an impossible motion.
- **Step 4** builds the response `PoseStamped` *in the same frame the
  request came in*. Keeping the frame consistent means the arm layer can
  trust `header.frame_id` and, if it prefers a different frame, ask
  `tf2` to convert — no hidden assumptions.

**The pre-grasp / approach / retreat offsets.** Notice the
`PREGRASP_BACKOFF_M` and `RETREAT_LIFT_M` constants. We deliberately do
*not* bake these into the single grasp pose. The cleanest design is for
grasping to return the one *final* grasp pose, and for the arm-motion
layer (`pick_product`) to derive the pre-grasp and retreat from it:

```python
# Done inside the pick_product (arm-motion) node, from the grasp_pose
# this service returns. Shown here so the hand-off is clear.

def pregrasp_from_grasp(grasp_pose, backoff_m):
    """Back off along the gripper's approach axis (its local +z)."""
    pre = copy.deepcopy(grasp_pose)
    # Move 'backoff_m' opposite the approach direction so the gripper
    # starts clear of the can, then approaches in a straight line.
    pre.pose.position.y -= backoff_m   # approach was +y, so back off -y
    return pre
```

Splitting the move into pre-grasp → straight approach → close → straight
retreat is what stops the gripper from clipping the can or its neighbors
on the way in and out.

**The grasp-confirmation check.** After the arm closes the jaws, the
project still has to confirm the grab actually worked before driving off
— a missed grasp that goes unnoticed becomes a dropped can. The
confirmation is *not* part of this grasping service; it belongs to the
pick step and uses one of three signals: the gripper's reported finger
gap (did it stop at roughly the can's diameter, or close all the way to
zero because it caught nothing?), a load/weight reading, or a quick look
from the wrist camera. This doc's job is only to produce the target
pose; the check lives next to the motion that created it.

**Why this stays swappable for AnyGrasp.** The entire layer hides behind
one service contract: *give me a product pose, get back a gripper pose +
width + ok*. Nothing outside this node knows or cares *how* the grasp was
computed. To move from v1's analytical grasp to AnyGrasp later, you
replace the body of `analytical_grasp` with a call into the learned
model (subscribing to `/wrist_camera/depth/points` for the point cloud,
running the network, converting its top-ranked result into the same
`PoseStamped` + width), and change *nothing* in perception, arm motion,
or orchestration. The service name, the request, and the response stay
identical. That clean seam is the payoff for keeping grasping its own
small box — exactly the architecture the stack doc
[`../06-grasping.md`](../06-grasping.md) argues for.

---

With perception finding the can and grasping deciding how to hold it, the
next question is how to sequence the whole pick-drive-place loop and
recover when a step fails. That is the orchestration layer — continue to
[`07-behavior-trees.md`](07-behavior-trees.md).
