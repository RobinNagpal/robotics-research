# Layer 04 — Perception & 3D vision (only-code)

> **Job:** Turn the simulator's synthetic camera output into the
> numbers the rest of the cell needs — *where* each vial and tray slot
> is — entirely in software, with no real camera attached.

In "only-code" mode the camera is part of the digital twin. Gazebo (or
whichever simulator from Layer 01 you run) renders **RGB** frames — plain
colour images, three channels, no distance information — and, if you add
a depth-camera plugin, **RGB-D** frames, which pair each colour pixel
with a *depth* value (how far that pixel is from the camera). From a
depth image you can compute a **point cloud**: a set of 3-D points
`(x, y, z)`, the raw geometry of the scene. The end product perception
must deliver is a **pose** for each object — its position *and*
orientation in space, six numbers — so the arm in Layer 03 knows exactly
where to reach.

Because the scene is synthetic, the data is clean: no lens smudges, no
glass glare, perfect knowledge of where the simulated camera sits. That
makes this the right place to prove the *algorithms* before real-world
noise (handled in the sibling hardware file) is allowed to complicate
them.

These simulated cameras are sensors **#1–#3** (overhead, station, and
wrist) of a wider suite — see [`../sensor-suite.md`](../sensor-suite.md).
The non-camera sim sensors are deliberate **co-witnesses**: the
verification gates fuse a camera check with a force-torque reading (#5),
the base IMU (#12), or a logical-camera presence check (#7) so that no
fact rests on vision alone (the **two-witness** habit). Perception's job
here is to deliver one of the two witnesses, not the whole verdict.

## The five at a glance

| Framework | Role | Tier | One-liner |
|---|---|---|---|
| Ultralytics YOLO (PyTorch) | Learned object detection / segmentation | Best-in-class | Trained neural net finds and outlines vials in RGB; strongest, but needs data + GPU. |
| OpenCV | Classic 2-D image processing | Cheapest | Free, CPU-only, everywhere — the workhorse for edges, blobs, colour, contours. |
| OpenCV + Open3D + AprilTag | Geometry + fiducials for known objects | Best-practical | Combine 2-D vision, 3-D point clouds, and printed markers for reliable known-pose pickup. |
| Open3D | 3-D point-cloud processing | Alternative | Modern, friendly library for filtering, fitting, and registering point clouds. |
| PCL (Point Cloud Library) | Heavy-duty 3-D point-cloud processing | Alternative | Exhaustive, battle-tested C++ point-cloud toolkit — powerful but heavy and dated. |

A **fiducial** is a printed pattern designed to be easy for a camera to
find and measure; an **AprilTag** is a specific, widely-used fiducial —
a small black-and-white square (like a chunky QR code) whose four
corners let software recover the tag's full 6-number pose from a single
image. Stick one on a tray, and "where is the tray?" becomes trivial.

## Ultralytics YOLO (PyTorch)

Ultralytics YOLO ("You Only Look Once") is a family of neural networks
for **object detection** (draw a box around each vial and label it) and
**instance segmentation** (outline its exact silhouette). It is built on
**PyTorch**, the dominant deep-learning framework, and ships as a Python
package with pre-trained models you fine-tune on your own images. In
only-code mode you train it on synthetic frames rendered by the
simulator, which can churn out thousands of perfectly-labelled images for
free.

Its strength is robustness to *variety*. A learned detector copes with
clutter, partial occlusion, odd lighting, and vials it has only loosely
seen before — situations where hand-tuned rules fall apart. It is the
only one of the five that genuinely *recognises* objects rather than
matching geometry or markers, so it scales to "find any vial in a messy
rack" far better than the others. For a v2 that must handle unlabelled or
varied consumables, this is the ceiling.

Its weakness, versus the other four, is cost and discipline. It needs a
**GPU** to train and to run fast (OpenCV, Open3D, PCL, and AprilTag all
run happily on a plain CPU), and it needs a *dataset* — even synthetic
data must be generated and curated, whereas AprilTag needs only a printed
marker and OpenCV needs only a few lines of code. It also returns 2-D
boxes or masks, not a 6-number pose; you still bolt on Open3D or PCL to
lift its output into 3-D. For a v1 whose vials and trays are **known and
fixed**, that is more machinery than the job requires — which is exactly
why it is best-in-class but not best-practical here.

## OpenCV

OpenCV is the standard open-source **computer-vision** library: decades
old, available in C++ and Python, and present in virtually every robotics
project. It handles the classic 2-D operations — reading images,
correcting lens distortion, finding edges and contours, thresholding by
colour, detecting blobs and circles, and basic camera calibration. In
simulation it ingests Gazebo's rendered RGB frames directly through a ROS
2 image topic.

It is the **cheapest** option by a wide margin: free, permissively
licensed, CPU-only, and so ubiquitous that almost any vision question has
a worked answer online. For a tidy synthetic scene, simple OpenCV tricks
go a long way — a vial's circular rim is a near-perfect target for
Hough-circle detection, and a tray's grid can be located by colour and
contour. It is also the glue everyone reaches for: the AprilTag and YOLO
pipelines both lean on OpenCV for image handling and calibration.

Its weakness, against the other four, is that on its own it is **2-D and
hand-tuned**. It has no native point-cloud or 3-D-registration tools the
way Open3D and PCL do, so it cannot by itself turn a depth image into a
fitted object pose. And unlike YOLO it does not *learn* — every rule is
written and tweaked by hand, so it grows brittle as the scene gets
varied or cluttered. It is indispensable plumbing, but rarely the whole
answer; that is why the practical pick *includes* OpenCV rather than
relying on it alone.

## OpenCV + Open3D + AprilTag

This is not one tool but the **recommended combination** for v1, and it
earns its own section because the whole is the point. **AprilTag**
markers, stuck on the tray (and optionally on a vial caddy), give an
instant, rock-solid 6-number pose for those known fixtures from a single
RGB frame. **OpenCV** handles the 2-D work around them — reading frames,
camera calibration, finding vial rims by shape and colour. **Open3D**
takes the simulator's depth/point-cloud data and fits clean geometry
(planes for the tray surface, cylinders for vials) to confirm heights and
catch a missing or tipped vial.

It is the **best-practical** pick because it matches the v1 philosophy:
the vials and trays are *known* objects at *known-ish* poses, so you
solve the problem with **geometry and fiducials** instead of training a
network. Every piece is free, open-source, and CPU-friendly, so it runs
on the same modest machine as the simulator with no GPU. It is also far
more *debuggable* than a neural net: when a pose is wrong you can see
which marker or which fitted cylinder went astray, rather than squinting
at a black box.

Its limit, versus YOLO, is that it leans on *structure you control* —
markers you placed, shapes you expect. It will not recognise an
unexpected object or a vial type it was never told about, and it asks you
to physically tag fixtures, which YOLO does not. Against bare OpenCV it is
more moving parts; against PCL it deliberately swaps raw power for
Open3D's simplicity. For the constrained HPLC cell those trade-offs are
all in its favour, but they are real trade-offs.

## Open3D

Open3D is a modern open-source library for **3-D data** — point clouds
and meshes. It loads a point cloud (from the simulator's depth camera),
cleans it (remove stray points, downsample), and fits or matches geometry:
plane segmentation to find the tray surface, **registration** (aligning
two point clouds, e.g. a vial model to the observed points) to recover
pose, and clustering to separate one vial from its neighbours. Its Python
API is clean and its built-in 3-D viewer makes debugging genuinely
pleasant.

Its appeal over the others is the sweet spot it hits: it does real 3-D
geometry that OpenCV and AprilTag cannot, while being dramatically
**lighter and friendlier than PCL**. A point-cloud filtering-and-fitting
task that is a paragraph of Python in Open3D is a much larger C++ build in
PCL. For the modest 3-D needs of this cell — confirm the tray plane,
verify vial presence and height — it is right-sized.

Its weakness is breadth and ecosystem depth. **PCL** still carries more
exotic algorithms and a longer track record in heavy industrial 3-D work;
**OpenCV** owns 2-D far more completely; **YOLO** owns recognition; and
**AprilTag** beats Open3D outright for the specific job of pose-from-a-
marker (faster, simpler, more reliable than fitting a cloud). On its own
Open3D answers "what is the geometry here?" but not "which object is
this?" — so it is a strong *component*, which is why it rides inside the
practical combo rather than standing alone.

## PCL (Point Cloud Library)

PCL is the long-established, comprehensive C++ library for **point-cloud
processing**. If an operation on 3-D points exists, PCL probably
implements it: filtering, surface normals, segmentation, feature
descriptors, registration, and model fitting (RANSAC plane/cylinder
fitting, useful for trays and vials). It has deep historical ties to ROS
and was for years *the* answer for 3-D perception in robotics.

Its strength is sheer **completeness and pedigree**. For an unusual or
demanding 3-D algorithm not found in Open3D, PCL likely has it, and its
implementations are well-worn from years of industrial use. Where raw
algorithmic coverage is what you need, nothing else on this list matches
it.

Its weakness, against the other four, is that it is **heavy and dated**.
It is C++-first with comparatively awkward Python bindings, slow and
fiddly to build and link, and its documentation has aged poorly compared
to Open3D's clean modern API. For this cell's simple 3-D needs it is
overkill: Open3D does the same fitting with far less friction, OpenCV
handles the 2-D, AprilTag handles the known-pose problem outright, and
YOLO handles recognition. So PCL stays an **Alternative** — reach for it
only if a specific 3-D algorithm you need lives only there.

## Verdict

- **Best-in-class:** **Ultralytics YOLO (PyTorch)** — learned detection
  and segmentation is the most powerful and general perception on offer,
  the right tool once vials and racks become varied or unlabelled. It
  pays for that power with a GPU and a dataset.
- **Cheapest:** **OpenCV** — free, CPU-only, ubiquitous, and good enough
  on its own for the clean, simple synthetic scenes you start with.
- **Best-practical:** **OpenCV + Open3D + AprilTag** — geometry plus
  fiducials for the *known* vials and trays. It matches the v1
  "known-pose first" rule, needs no GPU and no training data, runs beside
  the simulator, and stays easy to debug. Defer YOLO to a later milestone
  when variety demands it.

## Realistic scenario & use cases

> **Why this matters for automation.** Perception is the cell's eyes:
> it turns camera pixels into the **6-DoF poses** the arm reaches for and
> the **yes/no checks** that stop the arm wasting a move on an empty nest.
> Its automation value is letting the cell cope with a bench that is never
> *exactly* where the CAD said — a nudged rack, a missing vial, a glare —
> instead of demanding a perfectly fixtured world.

**The scenario.** The overhead camera must locate the tray and the vials
in a rack that an operator **nudged 5 mm and rotated 2°** while a blind
was opened, **changing the lighting**. Two nests are empty, one vial is
**under-filled** (a low meniscus), and another shows a **curved glass
reflection** that could fool a naive detector. The arm must only reach
real, full vials; the **wrist camera** must confirm each vial is actually
in the gripper before transit; and all of this rests on the **camera-to-
arm (hand-eye) calibration** being right — a 3 mm calibration error would
silently bias every reach. Perception has to hold all of that together.

The layer must therefore serve several **distinct use cases**:

1. **Known-pose localization of tray and vials.** Give Layer 03 the
   6-DoF pose of the tray and each nest, even after the rack shifts and
   rotates.
   - *How the solution handles it:* an **AprilTag** fiducial on the tray
     yields a full 6-DoF pose via PnP, and the nests are fixed offsets
     from it — so a 5 mm/2° move is absorbed automatically, no re-teaching.

2. **Presence / absence and fill verification.** Spot the two empty nests
   and the under-filled vial *before* the arm moves.
   - *How:* **Open3D** fits vial cylinders and meniscus height in the
     depth cloud — a missing cylinder means an empty nest, a low meniscus
     means under-filled — and the result feeds the Layer 10 gate.

3. **Grasp confirmation from the wrist camera.** Confirm a vial is truly
   in the jaws before retreat and transit.
   - *How:* the wrist camera checks for the vial's edge/tag at the gripper
     line; this is the visual half of a two-witness check with the gripper
     `JointState` from Layer 05.

4. **Hand-eye / workcell calibration and its verification.** Establish and
   *check* the camera↔arm↔bench transforms so a detected pose is correct
   in the arm's frame.
   - *How:* in only-code the transforms are known, but the **calibration
     procedure** (drive the arm to several known tag poses, solve
     `calibrateHandEye`) is rehearsed here so it transfers to hardware; a
     deliberate 3 mm offset is injected to prove the depth cross-check
     flags the disagreement rather than reaching blindly.

5. **Lighting and reflection robustness.** Keep detection stable when the
   light changes and glass glares.
   - *How:* AprilTag is high-contrast and robust; the **two-witness**
     depth cross-check rejects a spurious RGB hit; and when variety grows,
     Layer 01's domain-randomized (Isaac Sim) frames harden the learned
     **YOLO** path.

**Where the pick flexes.** OpenCV + Open3D + AprilTag (best-practical)
covers use cases 1–4 and the geometry side of 5 with no GPU and no
training data — the v1 "known-pose first" rule. Only when vials, labels,
or racks become genuinely varied or unlabelled (an extreme of use cases 2
and 5) does the learned **Ultralytics YOLO** path earn its GPU and
dataset, trained on the synthetic frames the digital twin already
generates.

### Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for
perception & vision.

#### Known-pose localization of tray and vials

- **The moment:** an operator nudged the rack 5 mm and rotated it 2°; the
  arm must still reach each nest centre exactly.
- **How, in depth:** an **AprilTag** on the tray gives a full 6-DoF pose
  via PnP, and every nest is a fixed offset from it, so the whole grid
  moves with the tag — a shift/rotation is absorbed with no re-teaching.
- **Edge case it survives:** a partially occluded tag — the detector
  rejects a low-confidence read and waits for a clean frame rather than
  publishing a wrong pose the arm would act on.
- **Value:** the cell tolerates a hand-placed rack instead of demanding
  micron-perfect fixturing.

#### Presence/absence and fill verification

- **The moment:** two nests are empty and one vial is under-filled; the arm
  must skip the empties and flag the low one *before* wasting a move.
- **How, in depth:** **Open3D** fits vial cylinders and meniscus height in
  the depth cloud — a missing cylinder is an empty nest, a low meniscus is
  under-filled — and the result feeds the Layer 10 fill gate.
- **Edge case it survives:** a clear-liquid meniscus that's hard to see —
  the depth/geometry fit doesn't depend on liquid colour, so water-clear
  diluent is measured as reliably as a tinted sample.
- **Value:** the cell never picks an empty nest or loads an under-filled
  vial, catching prep errors a human would miss at 2 a.m.

#### Hand-eye calibration and its verification

- **The moment:** if the camera-to-arm transform is off by 3 mm, every
  reach inherits the error; the cell must establish *and check* the
  calibration.
- **How, in depth:** the arm is driven to several known tag poses and
  `calibrateHandEye` solves the camera↔arm transform; in only-code the
  truth is known, so a deliberate 3 mm offset is injected to prove the
  depth cross-check flags the disagreement.
- **Edge case it survives:** calibration drift over time — the periodic
  re-check against the depth witness catches a slowly creeping offset
  before it causes a missed grasp.
- **Value:** the calibration *procedure* is proven in sim and transfers to
  hardware, where it's the difference between reaching the vial and
  reaching past it.

## Meta code

The shape of the best-practical pipeline (OpenCV + AprilTag for the
fiducial pose, Open3D for the depth cross-check), before any
library-specific detail:

```text
# subscribe to the simulator's overhead RGB image topic   (sensor #1)
# subscribe to the matching depth / point-cloud topic       (optional)
# on every camera frame:
#     detect AprilTag markers in the RGB image            (fiducial -> id + corners)
#     for the tag id stuck on the tray:
#         solve the tag's 6-DoF pose relative to the camera (PnP from its corners)
#         transform that pose into the world frame          (known camera mount)
#         (depth) fit the tray plane / vial cylinders        (confirm height, presence)
#         if the marker pose and the depth fit agree:        (two-witness check)
#             publish one PoseStamped for the object         (-> Layer 03 reaches it)
```

## Real code

A minimal but complete ROS 2 (`rclpy`) node implementing that pipeline.
This is **illustrative teaching code**: library and message names drift
between versions, so re-verify before relying on it. Every line carries
an inline comment explaining exactly what it does.

```python
import rclpy                                    # ROS 2 Python client library (the robot framework)
from rclpy.node import Node                     # base class every ROS 2 program ("node") builds on
from sensor_msgs.msg import Image               # the message type a camera publishes one frame as
from geometry_msgs.msg import PoseStamped       # a 6-DoF pose + which frame + what time it is for
from cv_bridge import CvBridge                  # converts a ROS Image message <-> an OpenCV array
import cv2                                       # OpenCV: 2-D image processing and camera geometry
import numpy as np                               # arrays + linear algebra, used for the camera matrix
from pupil_apriltags import Detector            # the AprilTag detector that finds the printed markers

# --- fixed, known facts about the simulated camera and the marker ---
CAMERA_MATRIX = np.array([[600.0,   0.0, 320.0],  # fx, 0, cx: x focal length and image-centre column
                          [  0.0, 600.0, 240.0],  # 0, fy, cy: y focal length and image-centre row
                          [  0.0,   0.0,   1.0]])  # bottom row of the standard pinhole camera matrix
TAG_SIZE_M = 0.03                                  # the AprilTag is 3 cm wide (its real printed size)
TRAY_TAG_ID = 0                                     # the specific tag id we stuck on the sample tray


class TrayPoseNode(Node):                          # our perception node, built on the ROS 2 Node class
    def __init__(self):                            # set-up that runs once, when the node is created
        super().__init__("tray_pose")              # register on the ROS 2 graph under the name "tray_pose"
        self.bridge = CvBridge()                   # build the one image converter we reuse every frame
        self.detector = Detector(families="tag36h11")  # the AprilTag family our markers are printed in
        self.sub = self.create_subscription(       # start listening to the overhead camera (sensor #1)
            Image, "/overhead/image_raw",          # message type, then the topic name the sim publishes on
            self.on_frame, 10)                      # call self.on_frame per frame; 10 = inbox queue depth
        self.pub = self.create_publisher(          # open an outgoing channel for the tray's pose
            PoseStamped, "/tray/pose", 10)         # type, topic name Layer 03 will read, queue depth

    def on_frame(self, msg):                        # runs automatically each time a camera frame arrives
        gray = self.bridge.imgmsg_to_cv2(msg, "mono8")  # ROS Image -> a grayscale OpenCV image array
        fx, fy = CAMERA_MATRIX[0, 0], CAMERA_MATRIX[1, 1]  # read the two focal lengths from the matrix
        cx, cy = CAMERA_MATRIX[0, 2], CAMERA_MATRIX[1, 2]  # read the image-centre point from the matrix
        tags = self.detector.detect(               # run AprilTag detection on this grayscale frame
            gray, estimate_tag_pose=True,          # also solve each found tag's full 6-DoF pose
            camera_params=(fx, fy, cx, cy),        # the camera intrinsics the pose solver needs
            tag_size=TAG_SIZE_M)                    # plus the marker's real size, to recover true scale
        for tag in tags:                            # walk through every marker found in this frame
            if tag.tag_id != TRAY_TAG_ID:          # is this the tag we care about (the tray's)?
                continue                            # no -> ignore it and check the next detected tag
            self.publish_pose(tag, msg.header)     # yes -> turn this detection into a published pose

    def publish_pose(self, tag, header):            # convert one detected tag into a PoseStamped message
        out = PoseStamped()                         # make the empty message we are about to fill in
        out.header = header                         # copy the frame id + timestamp from the source image
        out.pose.position.x = float(tag.pose_t[0])  # tag centre, left-right vs camera, in metres
        out.pose.position.y = float(tag.pose_t[1])  # tag centre, up-down vs camera, in metres
        out.pose.position.z = float(tag.pose_t[2])  # tag centre, distance from camera, in metres
        out.pose.orientation.w = 1.0                # leave orientation as "no rotation" for this sketch
        self.pub.publish(out)                       # send the finished pose out on /tray/pose
        self.get_logger().info(                     # print a tidy, time-stamped status line
            f"tray seen at z={out.pose.position.z:.3f} m")  # show the measured distance for sanity


def main():                                         # the standard ROS 2 program entry point
    rclpy.init()                                    # start up the ROS 2 client library (must come first)
    node = TrayPoseNode()                           # build our node, which runs its __init__ set-up
    rclpy.spin(node)                                # keep handling camera frames until you press Ctrl-C
    node.destroy_node()                             # remove the node from the graph on shutdown
    rclpy.shutdown()                                # close the ROS 2 client library cleanly


if __name__ == "__main__":                          # only run if this file is launched directly
    main()                                          # ...then start everything above
```

The depth cross-check named in the meta code is a few extra lines of
Open3D — load the depth topic as a point cloud, call
`segment_plane(...)` to fit the tray surface, and confirm the marker's
height matches the fitted plane before trusting the pose. It is left out
of the node above to keep the one published path clear, but it is the
second of the **two witnesses** [`../sensor-suite.md`](../sensor-suite.md)
asks for.

## See also

- [`README.md`](README.md) — the only-code folder overview and the full
  list of development layers.
- [`../02-code-plus-hardware/04-perception-and-vision.md`](../02-code-plus-hardware/04-perception-and-vision.md)
  — the same layer once **real cameras** feed the pipeline (camera SDKs,
  hand-eye calibration, glass glare, real noise, latency).
- [`../foundation-models.md`](../foundation-models.md) — VLA models can
  **subsume this perception layer**, mapping camera frames straight to
  actions; the learned-upgrade alternative to the explicit pipeline here.
