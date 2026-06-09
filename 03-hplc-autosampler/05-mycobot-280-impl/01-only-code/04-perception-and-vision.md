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
| Ultralytics YOLO + OpenCV + RGB-D depth | Learned detection lifted to 3-D | Best-practical | YOLO finds vials/tray in RGB, depth lifts each detection to a 3-D pose — the real workflow. |
| Ultralytics YOLO (PyTorch) | Learned object detection / segmentation | Best-in-class | Trained neural net finds and outlines vials in RGB; the detector at the heart of the cell. |
| OpenCV | Classic 2-D image processing | Cheapest | Free, CPU-only, everywhere — the workhorse for image handling, edges, blobs, colour. |
| Open3D | 3-D point-cloud processing | Alternative | Modern, friendly library for filtering, fitting, and registering point clouds. |
| PCL (Point Cloud Library) | Heavy-duty 3-D point-cloud processing | Alternative | Exhaustive, battle-tested C++ point-cloud toolkit — powerful but heavy and dated. |

**Bottom line:** YOLO detection lifted to 3-D through the depth image is
the practical backbone here; OpenCV and Open3D are supporting tools for
image handling and point-cloud geometry.

A **detector** is software that finds and labels objects in an image —
it draws a box around each vial, the tray, a cap, a beaker, and tells you
what each box is. **YOLO** ("You Only Look Once") is a fast, widely-used
detector. It gives you a 2-D box in the picture; pairing that box with
the **depth** image (how far each pixel is) lets you recover the object's
3-D position. No printed markers are stuck on anything — the cell reads
the objects themselves.

## Ultralytics YOLO (PyTorch)

Ultralytics YOLO ("You Only Look Once") is a family of neural networks
for **object detection** (draw a box around each vial and label it) and
**instance segmentation** (outline its exact silhouette). It is built on
**PyTorch**, the dominant deep-learning framework, and ships as a Python
package (`ultralytics`) with pre-trained models you fine-tune on your own
images. In only-code mode you train it on **synthetic frames** rendered
by the simulator, which can churn out thousands of perfectly-labelled
images for free — see the synthetic-data note below.

Its strength is robustness to *variety*. A learned detector copes with
clutter, partial occlusion, odd lighting, and vials it has only loosely
seen before — situations where hand-tuned rules fall apart. It is the
only one of the five that genuinely *recognises* objects rather than
matching geometry, so it scales from "find this tray" to "find any vial
in a messy rack" far better than the others. That is why it sits at the
heart of the cell's perception rather than off to the side.

Its cost, versus the other four, is discipline. It runs fastest on a
**GPU** (OpenCV, Open3D, and PCL all run happily on a plain CPU, and a
small YOLO model can run on CPU too, just slower), and it needs a
*dataset* — synthetic frames must still be generated and curated. It also
returns 2-D boxes or masks, not a 6-number pose, so you pair it with the
**depth** image (or Open3D/PCL) to lift each detection into 3-D. Those
are real obligations, but they are obligations the project already plans
for: the simulator generates the training data, and the depth camera
supplies the lift. That is what makes the **YOLO + depth** pipeline the
practical backbone, not just the best-in-class detector.

**Bottom line:** the learned detector that does the real recognising —
paired with depth for 3-D, it is the cell's perception backbone.

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
contour. It is also the glue everyone reaches for: the **YOLO pipeline**
leans on OpenCV for image handling, cropping, and calibration, and on its
camera intrinsics to deproject a detection into 3-D.

Its weakness, against the other four, is that on its own it is **2-D and
hand-tuned**. It has no native point-cloud or 3-D-registration tools the
way Open3D and PCL do, so it cannot by itself turn a depth image into a
fitted object pose. And unlike YOLO it does not *learn* — every rule is
written and tweaked by hand, so it grows brittle as the scene gets
varied or cluttered. It is indispensable plumbing, but rarely the whole
answer; that is why the practical pick *includes* OpenCV rather than
relying on it alone.

**Bottom line:** the indispensable image-handling and calibration glue
the YOLO pipeline runs on — never the whole answer by itself.

## Ultralytics YOLO + OpenCV + RGB-D depth

This is not one tool but the **recommended combination** for the real
cell, and it earns its own section because the whole is the point.
**YOLO** runs on each RGB frame and finds the objects directly — the
tray, the vials, the caps, a beaker — returning a labelled box (and, with
a segmentation model, an outline) for each, with **no printed markers on
anything**. **OpenCV** handles the 2-D plumbing: receiving frames,
cropping to a detection, and holding the camera intrinsics. The **RGB-D
depth** image supplies the missing third dimension: take a detection's
box-centre pixel, read its depth, and **deproject** it through the
intrinsics to a 3-D point — turning a flat box into a real position in
space. For the tray, YOLO finds the tray, depth lifts it to a 3-D pose,
and the individual nests are indexed from the **known tray geometry**
relative to that pose.

It is the **best-practical** pick because it is the *real* workflow: a
working lab cell must read varied, unlabelled consumables that no fiducial
will ever be stuck to, and a learned detector is what actually does that.
The detector is trained and validated on **synthetic data** generated
from the Gazebo twin with **domain randomization** (varying lighting,
textures, and object poses), so the data cost is paid by the simulator,
not by a human labelling photographs — which is exactly the project's
synthetic-data services direction. Depth lifting keeps the 3-D side
simple: no point-cloud model-fitting is required just to get a pose, only
one depth read per detection.

Its obligations, versus a pure-geometry approach, are a **dataset** and a
detector to train, and a GPU to train comfortably (a small model infers
on CPU, just slower). When a pose looks wrong you debug two clear stages —
the detection (is the box on the right object?) and the lift (is the depth
read clean?) — rather than one black box. Open3D or PCL can still be added
where a fuller 3-D fit helps (confirming a tray plane, a tipped vial), but
they are supporting tools, not the backbone.

**Bottom line:** YOLO detection lifted to 3-D through depth is the cell's
practical perception backbone — the real workflow, backed by synthetic
training data from the twin.

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
geometry that OpenCV cannot, while being dramatically **lighter and
friendlier than PCL**. A point-cloud filtering-and-fitting task that is a
paragraph of Python in Open3D is a much larger C++ build in PCL. For the
modest 3-D needs of this cell — confirm the tray plane, verify vial
presence and height — it is right-sized.

Its weakness is breadth and ecosystem depth. **PCL** still carries more
exotic algorithms and a longer track record in heavy industrial 3-D work;
**OpenCV** owns 2-D far more completely; and **YOLO** owns recognition —
which object is this? On its own Open3D answers "what is the geometry
here?" but not "which object is this?" — so it is a strong *component*
that supports the YOLO backbone (a depth read or a confirming plane fit),
rather than standing alone.

**Bottom line:** the right-sized 3-D helper — supports the YOLO + depth
backbone with plane and cylinder fits, but does not recognise objects
itself.

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
handles the 2-D, depth lifting turns a YOLO box into a pose outright, and
YOLO handles recognition. So PCL stays an **Alternative** — reach for it
only if a specific 3-D algorithm you need lives only there.

**Bottom line:** the heavyweight 3-D toolkit held in reserve — reach for
it only when a niche point-cloud algorithm lives nowhere else.

## Verdict

- **Best-in-class:** **Ultralytics YOLO (PyTorch)** — learned detection
  and segmentation is the most powerful and general perception on offer,
  the detector that actually recognises varied, unlabelled vials and
  racks. It pays for that power with a dataset (synthetic, from the twin)
  and a GPU to train comfortably.
- **Cheapest:** **OpenCV** — free, CPU-only, ubiquitous; the image-
  handling and intrinsics glue the YOLO pipeline runs on.
- **Best-practical:** **Ultralytics YOLO + OpenCV + RGB-D depth** — the
  real workflow. YOLO finds the tray, vials, and caps directly in RGB
  with no printed markers; depth lifts each detection to a 3-D pose; tray
  nests are indexed from known geometry. It is trained and validated on
  synthetic data the Gazebo twin generates with domain randomization,
  tying perception straight to the project's synthetic-data services.

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

1. **YOLO detection + depth localization of tray and vials.** Give Layer
   03 the 6-DoF pose of the tray and each nest, even after the rack shifts
   and rotates.
   - *How the solution handles it:* **YOLO** detects the tray and vials in
     the RGB frame, the **depth** image lifts each detection to a 3-D
     point, and the nests are indexed as fixed offsets from the detected
     tray pose — so a 5 mm/2° move is absorbed automatically, no
     re-teaching and no printed marker.

2. **Presence / absence and fill verification.** Spot the two empty nests
   and the under-filled vial *before* the arm moves.
   - *How:* **Open3D** fits vial cylinders and meniscus height in the
     depth cloud — a missing cylinder means an empty nest, a low meniscus
     means under-filled — and the result feeds the Layer 10 gate.

3. **Grasp confirmation from the wrist camera.** Confirm a vial is truly
   in the jaws before retreat and transit.
   - *How:* the wrist camera checks for the vial's edge at the gripper
     line; this is the visual half of a two-witness check with the gripper
     `JointState` from Layer 05.

4. **Hand-eye / workcell calibration and its verification.** Establish and
   *check* the camera↔arm↔bench transforms so a detected pose is correct
   in the arm's frame.
   - *How:* in only-code the transforms are known, but the **calibration
     procedure** (drive the arm to several known calibration-target poses,
     solve `calibrateHandEye`) is rehearsed here so it transfers to
     hardware; a deliberate 3 mm offset is injected to prove the depth
     cross-check flags the disagreement rather than reaching blindly.

5. **Lighting and reflection robustness.** Keep detection stable when the
   light changes and glass glares.
   - *How:* the **YOLO** detector is trained on **domain-randomized**
     synthetic frames (varied lighting, textures, and glare) so it stays
     stable as the light changes; the **two-witness** depth cross-check
     then rejects a spurious RGB hit before the arm acts on it.

**Where the pick flexes.** Ultralytics YOLO + OpenCV + RGB-D depth
(best-practical) covers all five use cases: YOLO recognises the tray,
vials, and caps directly in RGB, depth lifts each detection to a 3-D
pose, and Open3D adds a confirming geometric fit where presence and fill
(use case 2) need one. The detector is trained on the synthetic frames
the digital twin generates with **domain randomization**, so the same
pipeline that handles a tidy scene also copes when vials, labels, or
racks become genuinely varied or unlabelled (an extreme of use cases 2
and 5) — no printed marker anywhere in the loop.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for
perception & vision.

## YOLO detection + depth localization of tray and vials

A lab assistant always knows where things are — they glance at a rack and
instantly register which nest holds which vial, and their hand goes to the
right spot even if the rack was set down a little crooked. This use case
gives the cell that spatial sense: it **detects** the tray and the vials
directly in the camera image with YOLO, **lifts** each detection to a 3-D
point through the depth image, and works out the precise 3-D position of
every nest, so the arm reaches each one on centre even after a human
nudged the rack — with no marker stuck to anything.

The bigger experiment is the HPLC batch, where each vial must end up in
the exact tray slot its worklist row names. Everything downstream —
reaching, gripping, placing — depends on knowing where each nest actually
is, not where the CAD said it should be. This localization is the first
step of every per-vial cycle, so an error here cascades into a missed pick
later.

The assistant's "where is it?" judgment happens on every reach — hundreds
of times a day — and re-anchors instantly whenever a rack is moved. The
cell re-detects the tray and recomputes nest positions on every frame the
camera sees, so the grid follows the rack continuously through the run.

- **The moment:** an operator nudged the rack 5 mm and rotated it 2°; the
  arm must still reach each nest centre exactly.
- **How, in depth:** **YOLO** detects the tray (and the vials) in the RGB
  frame, the **depth** image lifts the tray detection to a 3-D pose, and
  every nest is a fixed offset from that pose, so the whole grid moves
  with the detected tray — a shift/rotation is absorbed with no
  re-teaching and no printed marker.
- **Edge case it survives:** a partially occluded tray — YOLO rejects a
  low-confidence detection and waits for a clean frame rather than
  publishing a wrong pose the arm would act on.
- **Walkthrough:** (1) run YOLO on the overhead frame to detect the tray;
  (2) lift its box-centre to a 3-D point through the depth image and
  intrinsics; (3) add the fixed per-nest offsets in the tray frame; (4)
  publish a `PoseStamped` per nest for Layer 03 to reach.
- **In the scene:** an operator sets the rack down a touch crooked; the
  overhead camera frame runs through YOLO, the tray detection is lifted to
  3-D, and in software the entire 96-nest grid quietly rotates and shifts
  to follow it, so every reach target lands back on centre.
- **Why it's done this way:** demanding micron-perfect fixturing would
  make the cell impractical for a real lab where humans place racks by
  hand; a real lab also will not let anyone stick a printed marker on
  every consumable, so the cell detects the objects themselves and absorbs
  that human imprecision instead of failing on it.
- **In the full loop:** this is the first step of every per-vial cycle —
  it tells Layer 03 where to reach and Layer 05 where to grasp, so a wrong
  pose here cascades into a missed pick downstream.
- **Value:** the cell tolerates a hand-placed rack instead of demanding
  micron-perfect fixturing.

### Meta code

This meta turns "where is everything?" into a single, well-conditioned
measurement: **detect** the tray in the image with YOLO, **lift** that
detection to a 3-D pose through the depth image, and derive everything
else from it. The pipeline subscribes to the overhead camera's RGB image,
the matching depth image, and the camera's intrinsic parameters (its
focal lengths and image centre), which together are what let a flat
picture be turned into 3-D geometry.

On each frame it runs YOLO, which returns a labelled box for every object
it recognises — the tray, the vials, the caps. For the **tray** box it
takes the box-centre pixel, reads that pixel's depth, and **deprojects**
it through the intrinsics to a 3-D point in the camera frame. That
camera-relative point is then transformed into the arm's base frame using
the known, fixed mounting of the camera — giving the tray's position in
the coordinates the arm actually plans in. (The tray's in-plane rotation
comes from the detected box orientation, or from a quick plane fit on the
tray's depth points.)

Because every nest sits at a fixed, known offset from the tray, the
pipeline can now place all 96 nests by simply applying each offset to the
tray pose. The whole grid therefore moves and rotates rigidly with the
detected tray, so a rack nudged 5 mm and rotated 2° is absorbed
automatically — no position has to be re-taught.

The YOLO model doing the detecting is trained and validated entirely on
**synthetic frames** the Gazebo twin renders with **domain
randomization** — the tray, vials, and caps are varied in pose, texture,
and lighting so the detector generalises — which is the project's
synthetic-data services direction in action.

A guard runs throughout: if the tray is missing, partly occluded, or
detected with low confidence, the frame is skipped rather than publishing
a pose the arm would act on. Only a clean, confident detection produces
nest poses for Layer 03. The localizer in pseudocode:

```text
# subscribe to the overhead RGB image + the matching depth image + the camera intrinsics
# (the YOLO model was trained on domain-randomized synthetic frames from the Gazebo twin)
# on each frame:
#     run YOLO on the RGB frame -> detections (class, box, confidence)
#     for the tray detection:
#         low confidence / occluded -> skip the frame                      (never publish a guess)
#         (u, v) = box centre pixel                                        (where the tray is)
#         z = depth_image[v, u]                                            (how far the tray is)
#         P_cam = deproject(u, v, z, intrinsics)                          (lift 2-D box -> 3-D point)
#         T_base_tray = camera_mount * pose_from(P_cam, tray_rotation)    (into the arm frame)
#         for each nest: pose = T_base_tray * fixed_offset[nest]          (grid follows the tray)
#         publish a PoseStamped per nest                                   (-> Layer 03)
```

### Real code

A YOLO node that detects the tray, lifts its box-centre to a 3-D point
through the depth image, and publishes a pose for every nest.
**Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from message_filters import Subscriber, ApproximateTimeSynchronizer  # pair RGB + depth by timestamp
from sensor_msgs.msg import Image                       # the overhead RGB and depth frames
from geometry_msgs.msg import PoseStamped               # the per-nest pose we publish
from cv_bridge import CvBridge                          # converts a ROS Image <-> an OpenCV array
import numpy as np                                      # arrays + the camera matrix / transforms
from ultralytics import YOLO                            # the trained YOLO detector (PyTorch)

CAM_MTX = np.array([[600., 0., 320.], [0., 600., 240.], [0., 0., 1.]])  # fx,fy + image centre
TRAY_CLASS = "tray"                                      # the YOLO class name for the tray
MIN_CONF = 0.60                                          # ignore detections below this confidence
NEST_OFFSETS = {"A1": (0.00, 0.00, 0.00),               # each nest's fixed offset from the tray...
                "A2": (0.02, 0.00, 0.00)}               # ...(only two shown; all 96 in practice)
# weights trained on domain-randomized SYNTHETIC frames rendered by the Gazebo twin (no real photos)
MODEL = YOLO("tray_vials_synth.pt")                     # load those synthetic-trained weights


class TrayLocalizer(Node):                              # publishes a pose per nest from the detected tray
    def __init__(self):                                 # one-time setup
        super().__init__("tray_localizer")              # register on the ROS 2 graph
        self.bridge = CvBridge()                        # the one image converter we reuse
        self.pub = self.create_publisher(PoseStamped, "/nest/pose", 10)  # per-nest poses out
        rgb = Subscriber(self, Image, "/overhead/image_raw")    # the colour frame...
        depth = Subscriber(self, Image, "/overhead/depth")      # ...and the matching depth frame
        self.sync = ApproximateTimeSynchronizer(        # deliver an RGB + depth pair together...
            [rgb, depth], queue_size=10, slop=0.05)     # ...whose timestamps are within 50 ms
        self.sync.registerCallback(self.on_frame)       # call on_frame with each matched pair

    def deproject(self, u, v, z):                       # lift a pixel (u, v) at depth z into 3-D
        fx, fy = CAM_MTX[0, 0], CAM_MTX[1, 1]           # the camera's focal lengths
        cx, cy = CAM_MTX[0, 2], CAM_MTX[1, 2]           # the image centre
        x = (u - cx) * z / fx                           # back out the real X from the pixel column
        y = (v - cy) * z / fy                           # back out the real Y from the pixel row
        return np.array([x, y, z])                      # the 3-D point in the camera frame

    def on_frame(self, rgb_msg, depth_msg):             # runs on each matched RGB + depth pair
        img = self.bridge.imgmsg_to_cv2(rgb_msg, "bgr8")    # ROS Image -> an OpenCV colour array
        depth = self.bridge.imgmsg_to_cv2(depth_msg, "32FC1")  # depth in metres, one float per pixel
        results = MODEL(img, verbose=False)[0]          # run YOLO -> boxes + classes + confidences
        for box in results.boxes:                       # consider every detected object
            name = results.names[int(box.cls)]          # the class name for this detection
            if name != TRAY_CLASS or float(box.conf) < MIN_CONF:  # not the tray, or low-confidence?
                continue                                # skip it -> never publish a guessed pose
            x0, y0, x1, y1 = box.xyxy[0]                 # the tray box corners, in pixels
            u, v = int((x0 + x1) / 2), int((y0 + y1) / 2)   # the box-centre pixel
            z = float(depth[v, u])                       # read that pixel's depth (metres)
            if not z > 0.0:                              # no valid depth there?
                continue                                # skip -> wait for a clean frame
            tray = self.deproject(u, v, z)               # lift the tray centre into a 3-D point
            for nest, off in NEST_OFFSETS.items():      # turn the tray pose into each nest's pose
                p = PoseStamped()                       # the message for this nest
                p.header.frame_id = "base_link"         # poses are expressed in the arm frame
                p.pose.position.x = float(tray[0] + off[0])  # tray X + the nest's fixed X offset
                p.pose.position.y = float(tray[1] + off[1])  # tray Y + the nest's fixed Y offset
                p.pose.position.z = float(tray[2] + off[2])  # tray Z + the nest's fixed Z offset
                self.pub.publish(p)                     # hand this nest's pose to Layer 03


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(TrayLocalizer()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## Presence/absence and fill verification

Before loading a tray, a careful lab assistant scans it: is every position
that should hold a vial actually filled, and does each vial have enough
liquid in it? An empty nest or a half-filled vial is a problem caught best
*before* the instrument runs, not after a blank result comes back. This
use case is the cell making that same check — measuring, nest by nest,
whether a vial is present and whether its liquid level is high enough.

The bigger experiment is the HPLC batch, whose results are only
trustworthy if every vial actually contains what the worklist says it
does. A worklist describes the intended tray, but real trays are prepared
by people and are sometimes wrong — a skipped fill, a missed position.
Verifying presence and fill before the arm acts is what stops the cell
wasting a cycle on, or worse injecting, a bad vial.

The assistant makes this presence-and-fill check on essentially every vial
of every tray — dozens to a few hundred times a day — and it's exactly the
kind of tedious visual vigilance that slips at 2 a.m. The cell runs the
check on every nest, every run, without fatigue.

- **The moment:** two nests are empty and one vial is under-filled; the arm
  must skip the empties and flag the low one *before* wasting a move.
- **How, in depth:** **Open3D** fits vial cylinders and meniscus height in
  the depth cloud — a missing cylinder is an empty nest, a low meniscus is
  under-filled — and the result feeds the Layer 10 fill gate.
- **Edge case it survives:** a clear-liquid meniscus that's hard to see —
  the depth/geometry fit doesn't depend on liquid colour, so water-clear
  diluent is measured as reliably as a tinted sample.
- **Walkthrough:** (1) take the depth cloud over the rack; (2) fit a
  cylinder at each nest; (3) classify present vs empty and measure meniscus
  height; (4) emit per-nest presence and fill to the Layer 10 gate.
- **In the scene:** the depth camera sweeps the rack and, slot by slot,
  the software draws a cylinder where each vial should be and reads the
  liquid line inside it — spotting the two empty nests and the one
  suspiciously low meniscus before the arm wastes a single motion.
- **Why it's done this way:** a worklist says what *should* be in each
  nest, but trays are prepared by people and are sometimes wrong; checking
  presence and fill before acting is what stops the cell injecting an
  empty or under-filled vial and silently corrupting a result.
- **In the full loop:** this gates the cycle before work begins — its
  presence/fill verdict feeds Layer 10's gate, which decides whether the
  arm even attempts that nest, saving the pick/decap/dispense effort on a
  bad vial.
- **Value:** the cell never picks an empty nest or loads an under-filled
  vial, catching prep errors a human would miss at 2 a.m.

### Meta code

This meta works entirely in 3-D geometry, not appearance, which is what
makes it robust to colourless liquids and lighting changes. It takes the
depth camera's point cloud over the rack — a dense set of 3-D points — and
reasons about it nest by nest, using the known positions of the nests in
the tray frame.

For each nest it crops the cloud to a narrow vertical column centred on
that nest. The first verdict is simple presence: a column with almost no
points means no vial is there, so the nest is marked empty immediately and
the cell knows to skip it.

For a column that does contain a vial, the pipeline measures the height of
the highest points — the liquid surface, or meniscus — relative to the
known nest floor. That height is the fill level; comparing it to a minimum
threshold separates a properly-filled vial from an under-filled one,
regardless of whether the liquid is tinted or water-clear, because the
measurement is geometric.

The output is a per-nest verdict — empty, under-filled, or OK, plus the
measured fill — that feeds the Layer 10 fill gate, which decides whether
the arm should even attempt that nest. The check in pseudocode:

```text
# subscribe to the depth point cloud over the rack
# for each nest (known x, y in the tray frame):
#     crop the cloud to a small column around the nest centre
#     too few points -> EMPTY nest                         (no vial present)
#     else fit a vertical cylinder -> radius + top-z        (the vial + its liquid line)
#     fill = top_z - nest_floor                            (meniscus height)
#     present and fill >= min -> OK, else UNDER-FILLED
# publish {nest: status, fill} -> Layer 10 fill gate
```

### Real code

An Open3D check that crops the depth cloud per nest and measures presence
and fill from geometry alone. **Illustrative teaching code** — re-verify
before use; every line is commented.

```python
import open3d as o3d                                    # 3-D geometry: point clouds + fitting
import numpy as np                                      # array maths on the cropped points

NEST_XY = {"A1": (0.18, 0.10), "A2": (0.20, 0.10)}      # nest centres (x, y) in metres; ...all 96
NEST_FLOOR_Z = 0.80                                     # the z of an empty nest's bottom (metres)
MIN_POINTS = 50                                         # fewer points than this => the nest is empty
MIN_FILL = 0.015                                        # a vial below 15 mm of liquid is under-filled
RADIUS = 0.01                                           # crop a 1 cm column around each nest centre


def classify(cloud: o3d.geometry.PointCloud) -> dict:   # presence + fill verdict per nest
    pts = np.asarray(cloud.points)                      # the raw Nx3 array of depth points
    out = {}                                            # nest -> {"status", "fill"}
    for nest, (x, y) in NEST_XY.items():                # check each nest independently
        col = pts[(np.abs(pts[:, 0] - x) < RADIUS) &    # keep points within RADIUS in x...
                  (np.abs(pts[:, 1] - y) < RADIUS)]     # ...and within RADIUS in y (a column)
        if len(col) < MIN_POINTS:                       # almost no points in this column?
            out[nest] = {"status": "EMPTY", "fill": 0.0}  # -> no vial is present here
            continue                                    # nothing to measure; next nest
        top_z = float(col[:, 2].max())                  # the highest point = the liquid surface
        fill = top_z - NEST_FLOOR_Z                     # meniscus height above the nest floor
        status = "OK" if fill >= MIN_FILL else "UNDER_FILLED"  # enough liquid, or too little?
        out[nest] = {"status": status, "fill": round(fill, 3)}  # record the verdict + the level
    return out                                          # the per-nest map for the Layer 10 gate


if __name__ == "__main__":                              # run directly on a saved cloud
    pcd = o3d.io.read_point_cloud("rack.pcd")           # load a depth cloud captured over the rack
    print(classify(pcd))                                # print {nest: presence + fill} for inspection
```

## Grasp confirmation from the wrist camera

After a lab assistant grips a vial, they take a quick look to confirm it's
actually in their fingers before lifting it away — a glance that costs
nothing and catches an empty grab. This use case is the cell's version:
the wrist camera looks at the gripper right after a pick and confirms a
vial is held before the arm carries it off.

The bigger experiment is the HPLC batch, where every vial is picked before
it's moved, decapped, dispensed, scanned, and placed. A pick that grabbed
nothing, if uncaught, would send the arm carrying an empty gripper through
all those steps. The wrist-camera check is the visual confirmation that a
vial is really there — the other half of a two-witness grasp check, paired
with the gripper's own feel from Layer 05.

The assistant's confirming glance happens on every pick — hundreds of
times a day. The cell runs the wrist-camera grasp confirmation just as
often: once after every pick, on every vial, all run long. It's one of the
highest-frequency perception checks in the loop.

- **The moment:** the gripper has just closed on a nest; before the arm
  lifts and carries the vial, the wrist camera must confirm a vial is
  actually in the jaws.
- **How, in depth:** the wrist camera looks at the gripper line for the
  vial's edge, returning a "vial present" boolean that the Layer 10 grasp
  gate ANDs with the gripper's own width reading.
- **Edge case it survives:** a vial gripped but not properly seated — the
  camera sees no vial at the expected gripper line and reports absent, so
  the cell re-grasps rather than carrying a bad hold.
- **Walkthrough:** (1) after a pick, capture a wrist-camera frame; (2)
  detect the vial at the gripper line; (3) publish "vial present"
  true/false; (4) Layer 10 fuses it with the gripper width to allow or
  block transit.
- **In the scene:** the wrist camera, inches from the closed jaws, catches
  the bright edge of a held vial against the gripper — or empty space where
  a vial should be — and reports what it sees in a heartbeat.
- **Why it's done this way:** the gripper's feel can be fooled (a jammed
  jaw reads as "holding"), so an independent visual witness is needed
  before trusting a grasp; checking before transit catches the miss at its
  cheapest moment.
- **In the full loop:** this runs right after every Layer 05 pick and
  feeds the Layer 10 two-witness grasp gate, the checkpoint before every
  transit.
- **Value:** an empty or bad grasp is caught visually the instant it
  happens, before the arm carries nothing across the bench.

### Meta code

This meta is a small, fast, single-purpose detector aimed at one fixed
region: the gap between the gripper's fingers, where a held vial would
appear. Because the wrist camera is rigidly mounted near the gripper, the
vial — if present — always shows up in roughly the same place in the
frame, which makes the check simple and reliable.

Right after a pick, the pipeline grabs a wrist-camera frame and looks for
the vial's signature at the gripper line — the bright vertical edges of
the glass. It is not trying to identify the vial (that's the scan step
later), only to answer present-or-absent.

The result is published as a single boolean on a "vial present" topic.
Deliberately, this is only one witness: the pipeline doesn't act on it
alone, because a camera can be fooled by a reflection just as a gripper
can be fooled by a jam.

Instead the boolean is consumed by the Layer 10 grasp gate, which ANDs it
with the gripper's own width reading from Layer 05, so transit is allowed
only when both the camera and the gripper agree a vial is held. The check
in pseudocode:

```text
# the wrist camera is rigidly mounted, so a held vial appears at a fixed region of the frame
# right after a pick:
#     grab a wrist-camera frame
#     look at the gripper line for the vial's edges
#     vial seen there -> publish /wrist/vial_present = True
#     nothing there   -> publish /wrist/vial_present = False
# Layer 10 ANDs this with the gripper width -> the two-witness grasp gate
```

### Real code

A node that checks a fixed gripper-line region of the wrist frame for a
held vial. **Illustrative teaching code** — re-verify before use; every
line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from sensor_msgs.msg import Image                       # the wrist-camera frame
from std_msgs.msg import Bool                           # the "vial present" witness we publish
from cv_bridge import CvBridge                          # ROS Image <-> OpenCV array
import cv2                                              # OpenCV: crop + edge detection
import numpy as np                                      # count edge pixels in the region

# the fixed region of the wrist frame where a held vial appears (x0, y0, x1, y1), in pixels
GRIPPER_ROI = (270, 180, 370, 460)                     # a tall strip between the fingers
EDGE_PIXELS_MIN = 400                                  # this many edge pixels => a vial is there


class GraspConfirm(Node):                              # confirms a vial is in the jaws after a pick
    def __init__(self):                                 # one-time setup
        super().__init__("grasp_confirm")               # register on the ROS 2 graph
        self.bridge = CvBridge()                        # the one image converter we reuse
        self.pub = self.create_publisher(Bool, "/wrist/vial_present", 10)  # the visual witness
        self.create_subscription(                       # watch the wrist camera...
            Image, "/wrist/image_raw", self.on_frame, 10)

    def on_frame(self, msg):                            # runs on each wrist-camera frame
        img = self.bridge.imgmsg_to_cv2(msg, "mono8")   # ROS Image -> a grayscale OpenCV array
        x0, y0, x1, y1 = GRIPPER_ROI                    # the fixed strip between the fingers
        roi = img[y0:y1, x0:x1]                         # crop to just that region
        edges = cv2.Canny(roi, 50, 150)                 # find strong edges (the vial's glass walls)
        present = int(np.count_nonzero(edges)) > EDGE_PIXELS_MIN  # enough edge => a vial is held
        self.pub.publish(Bool(data=bool(present)))      # publish the present/absent witness


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(GraspConfirm()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## See also

- [`README.md`](README.md) — the only-code folder overview and the full
  list of development layers.
- [`../foundation-models.md`](../foundation-models.md) — VLA models can
  **subsume this perception layer**, mapping camera frames straight to
  actions; the learned-upgrade alternative to the explicit pipeline here.
