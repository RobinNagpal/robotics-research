# Learn: Perception — RGB-D geometric (Open3D) + FoundationPose

> This is the hands-on companion to the perception layer
> (`../05-perception.md`). It teaches the v1 top choices: a
> **geometric pipeline** built on the **Open3D** library (point
> clouds, plane fitting, mesh registration) as the primary tool,
> with **FoundationPose** as the step up when the tray's position is
> uncertain. We assume you have read the ROS 2 learn doc
> (`02-ros2.md`) and know how nodes, topics, and messages work. Any
> unfamiliar term is defined here on first use or in the glossary
> (`../../02-glossary.md`). Audience: a programmer who has never
> touched robotics or computer vision. Next stop after this:
> grasping (`06-grasping.md`).

---

## 1. Introduction and basic concepts

Perception is the part of the robot that **looks and understands**.
In this project it never moves a motor. It produces *information*
and hands that information to other layers. Think of it like a
read-only API endpoint: other parts of the system call it, it
returns data, and that is all it does.

For the shelf-stocking robot, perception answers exactly two
questions, over and over:

1. **Where is the product I want to pick?** Not just "roughly over
   there," but its full **6-DoF pose**. "DoF" means *degrees of
   freedom*. **6-DoF pose** = three numbers for **position**
   (x, y, z — where the object is in space) plus three numbers for
   **orientation** (how it is rotated — tilt, roll, which way it
   faces). Six numbers fully describe where a rigid object sits and
   how it is turned. The arm needs all six to grab the can without
   fumbling.
2. **Where is the empty slot on the shelf?** Also a 6-DoF pose: the
   exact spot and orientation to set the product down.

Both answers are poses. Both are computed from what a camera sees.

### What an RGB-D camera is

A normal camera gives you a **color image**: a grid of pixels, each
with a red, green, and blue value. That is the "RGB" part.

An **RGB-D camera** adds one more channel: **depth**. For every
pixel it also reports **how far away** that point in the world is,
in meters. That is the "D" (depth). So each pixel carries both a
color and a distance. The wrist camera on our robot
(`/wrist_camera/...` topics) is an RGB-D camera.

Why does depth matter? A plain color image is flat — it cannot tell
you that the can is 38 cm away and the shelf behind it is 55 cm
away. Depth turns a flat picture into something you can measure in
3D. That is what lets us compute real-world poses instead of just
2D bounding boxes.

### What a point cloud is

A **point cloud** is the most useful way to think about RGB-D data.
It is simply **a big list of 3D points** — each point is an
(x, y, z) coordinate in meters, often with a color attached. If the
camera sees 300,000 pixels with valid depth, you get a point cloud
of 300,000 points floating in space, shaped like whatever the
camera is looking at: the tray, the cans, the shelf face.

If you have ever worked with an array of `{x, y, z}` objects in
JavaScript, a point cloud is literally that, just very large. In
ROS 2 it travels as a message type called `sensor_msgs/PointCloud2`,
published on `/wrist_camera/depth/points`.

Everything in the geometric pipeline is **math on this list of
points**: throw away points we don't need, find the flat plane that
is the shelf, find the clump of points that is the can, and figure
out the can's pose by fitting its known shape to that clump.

### The one rule to remember

Perception **outputs information, never motion**. It publishes poses
and detections. The grasping layer (`06-grasping.md`) and the
arm-motion layer (`04-arm-motion-planning.md`) are the ones that
turn those poses into movement. Keeping that boundary clean is why
the system stays understandable.

---

## 2. Important concepts that are used most often

These are the building blocks every perception node in this project
reuses. Read them once; the code sections below assume them.

### Depth images vs. point clouds

There are two ways the same depth data shows up:

- A **depth image** is a grid, like a grayscale photo, where each
  pixel's value is a distance in meters. It is compact and easy to
  store, but the points are still organized by pixel, not by where
  they are in space.
- A **point cloud** is the same data converted into explicit 3D
  (x, y, z) points. This is what we actually compute with.

You convert from a depth image to a point cloud using the camera's
**intrinsics** (next). In our stack the simulator and the camera
driver usually publish the point cloud directly on
`/wrist_camera/depth/points`, so we often skip the conversion.

### Camera intrinsics

**Intrinsics** are a small set of numbers that describe the
camera's own optics: its **focal length** (how "zoomed in" it is)
and its **principal point** (where the lens center lands on the
image). With the intrinsics you can take a pixel plus its depth and
compute the real 3D point it corresponds to. Without them, a depth
image is just numbers with no scale.

In ROS 2 the intrinsics arrive on `/wrist_camera/depth/camera_info`
as a `sensor_msgs/CameraInfo` message. You rarely do this math by
hand — Open3D and the camera driver handle it — but you should know
the word, because "wrong intrinsics" is a classic reason a point
cloud comes out distorted.

### Coordinate frames and tf2

Every 3D point is measured **relative to something**. The camera
reports points relative to itself — in the **`wrist_camera_link`**
frame. But the arm plans in the robot's body frame, **`base_link`**.
A pose is meaningless until you say *which frame* it is in.

A **coordinate frame** is just an origin and a set of axes — a local
"here is zero, here is which way is forward." Our robot has a chain
of them:

```
map -> odom -> base_link -> arm_base_link -> ... -> wrist_camera_link
                                                 -> tool0
```

- `map` is the fixed world.
- `odom` and `base_link` track the moving base.
- `wrist_camera_link` is where the camera physically sits.
- `tool0` is the gripper's tool tip.

**tf2** is the ROS 2 system that constantly tracks how all these
frames relate, so you can ask "given this point in
`wrist_camera_link`, what are its coordinates in `base_link`?" and
get a correct answer even as the arm moves. The math behind it is a
**transform**: a 4x4 matrix that, when multiplied with a point,
moves it from one frame into another. You will see those 4x4
matrices in the code. For now: tf2 gives you the matrix, you apply
it, the point is now in the frame you wanted.

This matters because perception sees things in the camera frame, but
must publish answers in `base_link` so the arm can use them.

### Downsampling and voxel grids

A raw point cloud is huge (hundreds of thousands of points) and most
of those points are redundant. **Downsampling** means keeping fewer
points without losing the shape. The standard method is a **voxel
grid**: imagine slicing 3D space into tiny cubes ("voxels," like 3D
pixels) of, say, 5 mm on a side, and replacing all the points inside
each cube with a single average point. The result is a cloud maybe
10x smaller that looks the same but processes far faster. Open3D's
function for this is `voxel_down_sample`.

### Plane segmentation with RANSAC

The shelf face and the tabletop are **flat planes**. Finding them
lets us separate "the shelf" from "the stuff on the shelf."

**Plane segmentation** = finding the points that all lie on one flat
surface. The standard algorithm is **RANSAC** (*Random Sample
Consensus*). Plain explanation: RANSAC repeatedly picks a few random
points, guesses a plane through them, then counts how many of all
the points lie close to that guessed plane. After many tries it
keeps the guess with the most points agreeing (the most "inliers").
This is robust because random clutter rarely agrees on the same
plane, so the true dominant surface wins. Open3D's function is
`segment_plane`. It returns the **plane equation**
(four numbers a, b, c, d describing the plane) and the list of point
indices that lie on it.

### Clustering

Once the big plane is removed, what remains are the objects sitting
on it — cans, boxes. **Clustering** groups nearby points into
separate clumps, so each clump is one object. Open3D's
`cluster_dbscan` does this. We use it to isolate "the can" before
estimating its pose.

### ICP — fitting a known shape to what we see

**ICP** stands for **Iterative Closest Point**. It is the workhorse
for pose estimation when you already know the object's shape.

The idea: we have a **model** of the can (a mesh or a clean point
cloud of `soup_can_400g`, since dimensions are known) and we have
the **observed** points the camera saw. ICP slides and rotates the
model until it best overlaps the observed points. "Iterative"
because it repeats: for each model point, find the closest observed
point, compute the rotation+translation that reduces the total gap,
apply it, repeat until the fit stops improving. The output is a 4x4
transform — and that transform *is* the object's 6-DoF pose.

The catch: ICP needs a **decent starting guess**. If the model
starts far from the observed cluster, ICP can lock onto the wrong
alignment. In v1 this is fine because the tray layout is known, so
we always have a good initial guess. Open3D's function is
`registration_icp`.

### What FoundationPose adds

ICP's weakness — needing a good initial guess — is exactly what
**FoundationPose** removes. FoundationPose is a learned,
**model-based, zero-shot 6-DoF pose estimator**. Unpacking that:

- **Model-based**: you give it the object's CAD model / mesh (we
  have `soup_can_400g`'s mesh).
- **Zero-shot**: it works on a new object *without per-object
  training* — you don't have to collect and label thousands of
  images of your can first.
- It takes an RGB-D image plus the mesh and outputs the full 6-DoF
  pose, even with **no good initial guess**.

So the trade is clear: ICP is free, fast, CPU-only, and perfect when
the tray pose is known. FoundationPose needs a GPU but stays robust
when the tray gets bumped or jumbled. v1 starts with ICP; you swap
in FoundationPose the moment "known tray position" stops holding.

### A note on detection / segmentation (finding the empty slot)

Plane fitting tells you where the shelf *surface* is, but not which
part of it is **empty** versus already stocked. For that you use
2D detection and segmentation. **YOLO-World** is an
**open-vocabulary** object detector — you give it a text prompt like
`"soup can"` and it draws boxes around matching objects, with no
per-SKU training. **SAM 2** (*Segment Anything Model 2*) turns a box
or a click into a precise pixel **mask** (the exact outline of an
object or region). Used together — YOLO-World finds the cans on the
shelf, SAM 2 outlines them — you can subtract the occupied regions
from the shelf face and measure the empty gap for the next facing.
In v1 we mostly compute the empty slot straight from the planogram
(a known file), so these models are a later upgrade, not a v1
requirement.

---

## 3. Hello world example with code

Goal: take a point cloud, shrink it with a voxel grid, then find the
dominant flat surface (the shelf face or the table) and print the
plane and how many points sit on it. This is pure Open3D, no ROS 2
yet, so you can run it standalone.

First, install Open3D:

```bash
pip install open3d numpy
```

Now the script. Read the comments — each step maps to a concept
from section 2.

```python
import open3d as o3d
import numpy as np

# 1. Load a point cloud from a file. In a real run this comes from
#    the camera topic; here we read a saved .pcd/.ply for practice.
#    A point cloud is just a long list of (x, y, z) points.
pcd = o3d.io.read_point_cloud("shelf_scene.ply")
print(f"Loaded cloud with {len(pcd.points)} points")

# 2. Downsample with a voxel grid. We slice space into 5 mm cubes
#    and keep one averaged point per cube. The cloud gets much
#    smaller but keeps its shape, so everything after this is faster.
voxel_size = 0.005  # 5 mm, in meters
pcd_small = pcd.voxel_down_sample(voxel_size)
print(f"After downsampling: {len(pcd_small.points)} points")

# 3. Plane segmentation with RANSAC. This finds the single flat
#    surface that the most points agree on -- our shelf face / table.
#    - distance_threshold: how close (meters) a point must be to the
#      plane to count as "on" it (here 1 cm).
#    - ransac_n: how many random points each guess uses (3 defines a
#      plane).
#    - num_iterations: how many random guesses to try; more = more
#      reliable, slower.
plane_model, inlier_indices = pcd_small.segment_plane(
    distance_threshold=0.01,
    ransac_n=3,
    num_iterations=1000,
)

# 4. Unpack the result.
#    plane_model is [a, b, c, d] for the plane equation
#        a*x + b*y + c*z + d = 0.
#    (a, b, c) is the plane's normal -- the direction it faces.
#    inlier_indices lists which points lie on that plane.
a, b, c, d = plane_model
print(f"Plane equation: {a:.3f} x + {b:.3f} y + {c:.3f} z + {d:.3f} = 0")
print(f"Points on the plane (inliers): {len(inlier_indices)}")

# 5. (Optional) split the cloud into "the plane" vs "everything
#    else." The leftover points are the objects sitting on the
#    surface -- the cans we care about.
plane_cloud = pcd_small.select_by_index(inlier_indices)
objects_cloud = pcd_small.select_by_index(inlier_indices, invert=True)
print(f"Objects (off the plane): {len(objects_cloud.points)} points")
```

What just happened, step by step:

- **Step 1** loads the points. The count tells you the camera saw
  something — a count near zero means a bad depth frame.
- **Step 2** is the speed move. Hundreds of thousands of points down
  to tens of thousands, same shape.
- **Step 3** is the heart of it. RANSAC tries 1000 random planes and
  returns the one most points agree with. For a shelf scene that is
  the shelf face; for a tray scene it is the tray floor.
- **Step 4** prints the answer. The four numbers `[a, b, c, d]` are
  the plane; `(a, b, c)` is the **normal vector** — the direction
  the surface faces, which later tells the arm which way "into the
  shelf" is.
- **Step 5** separates surface from objects. We keep
  `objects_cloud` for the next example, where we find the can.

If you have a display, add
`o3d.visualization.draw_geometries([plane_cloud])` to actually see
the detected plane. Seeing it is the fastest way to build intuition.

---

## 4. A bit advanced example with code

Goal: estimate the 6-DoF pose of one `soup_can_400g`. The plan:

1. Crop the cloud to just the tray region (we know roughly where the
   tray is, because it is loaded in a fixed fixture).
2. Remove the tray floor plane, cluster the rest, take the can-sized
   clump.
3. Run ICP to align the can's known model to that clump.
4. Read off the 4x4 transform — that *is* the pose.

```python
import open3d as o3d
import numpy as np

# --- Inputs we already have ---
# The observed scene from the wrist camera (already a point cloud).
scene = o3d.io.read_point_cloud("tray_scene.ply")

# The KNOWN model of the can. Because soup_can_400g has known
# dimensions and a known mesh, we can load it and sample points off
# its surface to get a model point cloud to match against.
can_mesh = o3d.io.read_triangle_mesh("soup_can_400g.obj")
can_model = can_mesh.sample_points_uniformly(number_of_points=5000)

# 1. Crop to the tray region. We know the tray sits in a fixed
#    fixture, so we can define a 3D box (min corner, max corner) in
#    meters and keep only points inside it. This removes the shelf,
#    the floor, and other clutter cheaply.
tray_box = o3d.geometry.AxisAlignedBoundingBox(
    min_bound=(-0.20, -0.15, 0.30),   # x, y, z lower corner
    max_bound=( 0.20,  0.15, 0.60),   # x, y, z upper corner
)
tray_cloud = scene.crop(tray_box)

# 2a. Remove the tray floor with the same RANSAC plane fit as before,
#     so only the objects sitting in the tray remain.
_, floor_idx = tray_cloud.segment_plane(
    distance_threshold=0.005, ransac_n=3, num_iterations=500
)
objects = tray_cloud.select_by_index(floor_idx, invert=True)

# 2b. Cluster the leftover points into separate objects. DBSCAN
#     groups points that are within `eps` meters of each other and
#     need at least `min_points` to count as a cluster (not noise).
labels = np.array(
    objects.cluster_dbscan(eps=0.02, min_points=30)
)
# Pick the largest cluster as "the can to pick" (v1: one obvious
# product in front). label -1 means "noise", so we ignore it.
valid = labels[labels >= 0]
biggest_label = np.bincount(valid).argmax()
can_observed = objects.select_by_index(
    np.where(labels == biggest_label)[0]
)

# 3. ICP registration: slide/rotate the known can model until it
#    best overlaps the observed can cluster.
#    - We give it an initial guess `init`: place the model at the
#      cluster's center. In v1 the tray layout is known, so this
#      guess is good -- which is exactly what ICP needs.
init = np.eye(4)  # 4x4 identity = "no movement yet"
init[:3, 3] = can_observed.get_center()  # move model to cluster center

icp_result = o3d.pipelines.registration.registration_icp(
    can_model,          # source: the known model
    can_observed,       # target: what the camera saw
    max_correspondence_distance=0.02,  # only match points within 2 cm
    init=init,
    estimation_method=
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
)

# 4. The result. `transformation` is the 4x4 matrix that places the
#    can model onto the observed can -- i.e. the can's 6-DoF pose in
#    the camera frame. `fitness` (0..1) is how much of the model
#    found a match; higher is a more trustworthy fit.
pose_in_camera = icp_result.transformation
print("Can 6-DoF pose (camera frame), 4x4 transform:")
print(np.round(pose_in_camera, 3))
print(f"ICP fitness (overlap quality): {icp_result.fitness:.2f}")
```

Reading the output: the top-left 3x3 block of the 4x4 matrix is the
**rotation** (orientation), and the right-hand column's top three
numbers are the **translation** (x, y, z position). Together: the
6-DoF pose. The `fitness` number is your quality gate — if it is
low (say under ~0.5), the fit is bad and the node should report
failure rather than hand a wrong pose to the arm.

One important note: this pose is in the **camera frame**. Before the
arm can use it, you transform it into `base_link` using tf2 (shown
in the next section).

### When the tray pose is unknown: FoundationPose instead of ICP

ICP above leaned on `init` — a good initial guess from the known
tray layout. The day the tray gets bumped, shuffled, or you allow a
jumbled tray, that guess disappears and ICP becomes unreliable.
**FoundationPose** is the drop-in replacement: give it the RGB-D
frame plus the known mesh, and it returns the 6-DoF pose with no
initial guess. Conceptually it slots in like this:

```python
# Conceptual -- FoundationPose runs as its own GPU-backed estimator.
# It needs: the color image, the depth image, the camera intrinsics,
# the object mesh, and a mask of where the object roughly is (e.g.
# from YOLO-World + SAM 2). It returns the full 6-DoF pose directly.

from foundationpose import FoundationPose   # pseudo-import for clarity

estimator = FoundationPose(mesh=can_mesh)   # load the known SKU mesh

pose_in_camera = estimator.estimate(
    color=color_image,        # from /wrist_camera/color/image_raw
    depth=depth_image,        # from the depth stream
    intrinsics=camera_K,      # from /wrist_camera/depth/camera_info
    object_mask=can_mask,     # rough mask, e.g. from SAM 2
)
# Same kind of output as ICP: a 4x4 transform = the 6-DoF pose.
# No `init` guess required -- that is the whole point.
```

The interface is deliberately the same shape — a 4x4 pose in the
camera frame — so the rest of the system (the transform to
`base_link`, the handoff to grasping) does not change when you swap
the estimator. That is what "step up" means here: you replace one
box, not the pipeline.

---

## 5. Explanation of the place-on-shelf perception node

Now the real thing: a ROS 2 perception node for this project. It
serves two of the project actions. On a **`locate_slot`** request it
returns where the next product should go. On a **`pick_product`**
request it returns the product's 6-DoF pose. Both answers come back
as a `geometry_msgs/PoseStamped` (a pose tagged with its frame and a
timestamp) in `base_link`.

To keep this readable we use two simple ROS 2 services — one per
question — rather than full action servers. The orchestration layer
(`07-orchestration.md`) calls them; perception only ever answers.

```python
import rclpy
from rclpy.node import Node
import numpy as np
import open3d as o3d

# ROS 2 message types.
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import PoseStamped
from std_srvs.srv import Trigger        # simple request/response service

# tf2 for converting poses between coordinate frames.
import tf2_ros
from tf2_geometry_msgs import do_transform_pose_stamped

# Helper (from earlier sections / a small utils module) that turns a
# ROS PointCloud2 message into an Open3D point cloud.
from pcl_helpers import ros_cloud_to_open3d


class ShelfPerceptionNode(Node):
    def __init__(self):
        super().__init__("shelf_perception")

        # --- The planogram: a small static file we were given. ---
        # slot_origin is the pose of the first facing on the shelf,
        # spacing is how far apart facings sit, and `placed` counts
        # how many products we have already put down this run.
        self.planogram = {
            "sku": "soup_can_400g",
            "slot_origin": np.array([0.55, 0.10, 0.95]),  # x,y,z in map
            "spacing": 0.09,        # 9 cm between facings, along +y
            "facings": 6,
        }
        self.placed = 0

        # --- Subscribe to the wrist camera's point cloud. ---
        # We cache the latest cloud so a service call can use it
        # immediately instead of waiting for a fresh frame.
        self.latest_cloud = None
        self.create_subscription(
            PointCloud2,
            "/wrist_camera/depth/points",
            self._cloud_cb,
            10,                       # queue depth
        )

        # --- tf2 buffer + listener: keeps the frame tree up to date
        #     so we can convert camera-frame poses to base_link. ---
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # --- The two services we offer. ---
        self.create_service(Trigger, "locate_slot", self.locate_slot_cb)
        self.create_service(Trigger, "pick_product", self.pick_product_cb)

        # Where we publish the latest computed slot pose, so tools
        # like RViz can visualize what perception decided.
        self.slot_pub = self.create_publisher(
            PoseStamped, "perception/slot_pose", 10
        )
        self.get_logger().info("shelf_perception ready")

    # Called every time a new point cloud arrives. Just store it.
    def _cloud_cb(self, msg: PointCloud2):
        self.latest_cloud = msg

    # ---------------- locate_slot ----------------
    def locate_slot_cb(self, request, response):
        """Return where the NEXT empty facing is, in base_link."""
        if self.latest_cloud is None:
            response.success = False
            response.message = "no point cloud yet"
            return response

        # 1. Convert the ROS cloud to Open3D and fit the shelf face.
        #    We re-fit the plane each call so the slot rides on the
        #    real, observed shelf height -- not a stale assumption.
        cloud = ros_cloud_to_open3d(self.latest_cloud)
        cloud = cloud.voxel_down_sample(0.005)
        plane_model, inliers = cloud.segment_plane(
            distance_threshold=0.01, ransac_n=3, num_iterations=1000
        )
        # plane_model = [a, b, c, d]; (a,b,c) is the shelf's normal,
        # i.e. the direction the shelf face points outward.
        self.get_logger().info(f"shelf plane: {np.round(plane_model, 3)}")

        # 2. Compute the next slot from the planogram. The Nth facing
        #    sits `placed * spacing` along the shelf from the origin.
        slot_xyz = self.planogram["slot_origin"].copy()
        slot_xyz[1] += self.placed * self.planogram["spacing"]  # +y

        # 3. Build a PoseStamped. The planogram is defined in `map`,
        #    so we tag the pose with frame_id "map" first.
        slot_in_map = PoseStamped()
        slot_in_map.header.frame_id = "map"
        slot_in_map.header.stamp = self.get_clock().now().to_msg()
        slot_in_map.pose.position.x = float(slot_xyz[0])
        slot_in_map.pose.position.y = float(slot_xyz[1])
        slot_in_map.pose.position.z = float(slot_xyz[2])
        # Upright orientation: identity quaternion (w=1) = "no
        # rotation," which for our setup means the can stands up.
        slot_in_map.pose.orientation.w = 1.0

        # 4. Convert map -> base_link with tf2, because the arm plans
        #    in base_link. tf2 looks up the current transform between
        #    the two frames and applies it.
        try:
            tf = self.tf_buffer.lookup_transform(
                "base_link", "map", rclpy.time.Time()
            )
            slot_in_base = do_transform_pose_stamped(slot_in_map, tf)
        except tf2_ros.TransformException as e:
            response.success = False
            response.message = f"tf lookup failed: {e}"
            return response

        # 5. Publish for visualization and return success. The actual
        #    pose goes back through a richer interface in the real
        #    system; Trigger just carries success + a message here.
        self.slot_pub.publish(slot_in_base)
        response.success = True
        response.message = (
            f"slot {self.placed} at base_link "
            f"({slot_in_base.pose.position.x:.3f}, "
            f"{slot_in_base.pose.position.y:.3f}, "
            f"{slot_in_base.pose.position.z:.3f})"
        )
        return response

    # ---------------- pick_product ----------------
    def pick_product_cb(self, request, response):
        """Return the product's 6-DoF pose, in base_link."""
        if self.latest_cloud is None:
            response.success = False
            response.message = "no point cloud yet"
            return response

        # 1. Estimate the can pose in the camera frame. In v1 this is
        #    the ICP routine from section 4 (known tray, good init).
        #    Swap in FoundationPose here when the tray pose is unknown
        #    -- same 4x4 output, so nothing below changes.
        cloud = ros_cloud_to_open3d(self.latest_cloud)
        pose_in_camera = self._estimate_can_pose_icp(cloud)  # 4x4 matrix
        if pose_in_camera is None:
            response.success = False
            response.message = "pose estimate failed (low fit)"
            return response

        # 2. Wrap the 4x4 transform as a PoseStamped in the camera
        #    frame, then convert to base_link with tf2 -- same idea as
        #    locate_slot, just starting from wrist_camera_link.
        product_in_cam = self._matrix_to_pose_stamped(
            pose_in_camera, frame_id="wrist_camera_link"
        )
        try:
            tf = self.tf_buffer.lookup_transform(
                "base_link", "wrist_camera_link", rclpy.time.Time()
            )
            product_in_base = do_transform_pose_stamped(product_in_cam, tf)
        except tf2_ros.TransformException as e:
            response.success = False
            response.message = f"tf lookup failed: {e}"
            return response

        # 3. This product pose is what the grasping layer consumes
        #    (06-grasping.md) to plan how to actually grab the can.
        response.success = True
        response.message = (
            f"product at base_link "
            f"({product_in_base.pose.position.x:.3f}, "
            f"{product_in_base.pose.position.y:.3f}, "
            f"{product_in_base.pose.position.z:.3f})"
        )
        return response

    # --- helpers (bodies omitted; see section 4 for the ICP math) ---
    def _estimate_can_pose_icp(self, cloud):
        """Crop tray, cluster, ICP-align the known soup_can_400g mesh.
        Returns a 4x4 numpy transform, or None if the fit is poor."""
        ...

    def _matrix_to_pose_stamped(self, matrix, frame_id):
        """Convert a 4x4 transform into a PoseStamped (position +
        quaternion) tagged with the given frame_id."""
        ...

    def mark_placed(self):
        """Orchestration calls this after a successful place so the
        next locate_slot points at the next empty facing."""
        self.placed += 1


def main():
    rclpy.init()
    node = ShelfPerceptionNode()
    rclpy.spin(node)        # process callbacks until shut down
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

Walking through the node block by block:

- **`__init__` — planogram.** The planogram is the static file from
  the requirements: which SKU, where the first facing sits, how far
  apart facings are, and how many fit. `self.placed` is the running
  count of products already set down this run. This is the entire
  reason `locate_slot` can compute "the *next* empty slot" by simple
  arithmetic — no learned perception needed in v1.

- **`__init__` — subscription.** We subscribe to
  `/wrist_camera/depth/points` and cache the most recent cloud in
  `self.latest_cloud`. Caching means a service call answers from the
  newest frame instantly instead of blocking for a fresh one.

- **`__init__` — tf2.** The `Buffer` and `TransformListener`
  together keep a live picture of the frame tree. We need them
  because perception computes in `map` (the planogram) or
  `wrist_camera_link` (the camera), but must answer in `base_link`.

- **`__init__` — services.** Two services, one per question:
  `locate_slot` and `pick_product`. Orchestration calls them; this
  node only answers. That is the "information, not motion" rule made
  concrete.

- **`_cloud_cb`.** A one-liner: every incoming cloud overwrites the
  cached one. Cheap and always current.

- **`locate_slot_cb`, step 1.** We re-fit the shelf-face plane with
  RANSAC on every call. Re-fitting (instead of trusting a stored
  height) keeps the slot pose pinned to the *observed* shelf, so
  small navigation errors in where the robot parked do not push the
  place pose off the real shelf.

- **`locate_slot_cb`, step 2.** Pure planogram arithmetic: the Nth
  facing is the origin shifted by `placed * spacing` along the
  shelf. This is the "slot origin + offset by how many already
  placed" rule from requirements §6, step 5.

- **`locate_slot_cb`, steps 3-4.** Build the pose in `map` (where the
  planogram lives), then use tf2 to convert it into `base_link`. The
  identity quaternion (`w = 1.0`) means "upright," matching the
  requirement that products go down standing up.

- **`locate_slot_cb`, step 5.** Publish the pose for visualization
  and return success. In the full system the pose travels back over a
  richer action interface to the arm-motion layer
  (`04-arm-motion-planning.md`); here `Trigger` keeps the example
  small.

- **`pick_product_cb`, step 1.** This is where section 4's ICP runs
  (in `_estimate_can_pose_icp`) and returns a 4x4 pose in the camera
  frame. The comment marks the exact spot you swap in FoundationPose
  when the tray pose becomes uncertain — because the output shape is
  identical, nothing downstream changes.

- **`pick_product_cb`, steps 2-3.** Wrap the 4x4 as a `PoseStamped`
  in `wrist_camera_link`, convert to `base_link` with tf2, and hand
  it off. That product pose is exactly what the grasping layer
  (`06-grasping.md`) needs to plan the grab.

- **`mark_placed`.** After a successful place, orchestration bumps
  the counter so the next `locate_slot` returns the next empty
  facing. This is the loop closing — perception's two answers,
  driven by the planogram, keep the pick-drive-place cycle moving
  until the row is full.

Notice what is *not* here: no motor commands, no trajectories, no
arm control. Perception fit a plane, did some arithmetic, estimated
one pose, and converted frames. That restraint is the whole design.

---

## Where to go next

You now have the v1 perception toolkit: Open3D for geometric pose
and plane fitting, ICP for known-pose registration, FoundationPose
as the GPU step-up, and a clean ROS 2 node that answers
`locate_slot` and `pick_product` in `base_link`. The product pose
this layer produces is the input to grasping — how the robot decides
*where and how to actually grip* the can. Continue with
`06-grasping.md`. For the layer-level comparison and the cost/hardware
breakdown, see `../05-perception.md`; for any term, the glossary is
`../../02-glossary.md`.
