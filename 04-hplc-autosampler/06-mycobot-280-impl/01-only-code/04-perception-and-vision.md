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

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for
perception & vision.

## Known-pose localization of tray and vials

A lab assistant always knows where things are — they glance at a rack and
instantly register which nest holds which vial, and their hand goes to the
right spot even if the rack was set down a little crooked. This use case
gives the cell that spatial sense: from a single fiducial marker on the
tray, it works out the precise 3-D position of every nest, so the arm
reaches each one on centre even after a human nudged the rack.

The bigger experiment is the HPLC batch, where each vial must end up in
the exact tray slot its worklist row names. Everything downstream —
reaching, gripping, placing — depends on knowing where each nest actually
is, not where the CAD said it should be. This localization is the first
step of every per-vial cycle, so an error here cascades into a missed pick
later.

The assistant's "where is it?" judgment happens on every reach — hundreds
of times a day — and re-anchors instantly whenever a rack is moved. The
cell recomputes nest positions from the marker on every frame the camera
sees, so the grid follows the rack continuously through the run.

- **The moment:** an operator nudged the rack 5 mm and rotated it 2°; the
  arm must still reach each nest centre exactly.
- **How, in depth:** an **AprilTag** on the tray gives a full 6-DoF pose
  via PnP, and every nest is a fixed offset from it, so the whole grid
  moves with the tag — a shift/rotation is absorbed with no re-teaching.
- **Edge case it survives:** a partially occluded tag — the detector
  rejects a low-confidence read and waits for a clean frame rather than
  publishing a wrong pose the arm would act on.
- **Walkthrough:** (1) detect the tray AprilTag in the overhead frame; (2)
  solve its 6-DoF pose via PnP; (3) add the fixed per-nest offsets; (4)
  publish a `PoseStamped` per nest for Layer 03 to reach.
- **In the scene:** an operator sets the rack down a touch crooked; the
  overhead camera catches the AprilTag on the tray, and in software the
  entire 96-nest grid quietly rotates and shifts to follow it, so every
  reach target lands back on centre.
- **Why it's done this way:** demanding micron-perfect fixturing would
  make the cell impractical for a real lab where humans place racks by
  hand; anchoring everything to a fiducial lets the cell absorb that human
  imprecision instead of failing on it.
- **In the full loop:** this is the first step of every per-vial cycle —
  it tells Layer 03 where to reach and Layer 05 where to grasp, so a wrong
  pose here cascades into a missed pick downstream.
- **Value:** the cell tolerates a hand-placed rack instead of demanding
  micron-perfect fixturing.

### Meta code

This meta turns "where is everything?" into a single, well-conditioned
measurement: find one printed fiducial marker — an AprilTag — on the tray,
and derive everything else from it. The pipeline subscribes to the
overhead camera image and the camera's intrinsic parameters (its focal
lengths and image centre), which together are what let a flat picture be
turned into 3-D geometry.

On each frame it detects any AprilTags and, for the specific tag known to
be stuck on the tray, solves the tag's full six-degree-of-freedom pose
relative to the camera using the geometry of its four corners. That
camera-relative pose is then transformed into the arm's base frame using
the known, fixed mounting of the camera — giving the tray's position and
orientation in the coordinates the arm actually plans in.

Because every nest sits at a fixed, known offset from the tray tag, the
pipeline can now place all 96 nests by simply applying each offset to the
tag pose. The whole grid therefore moves and rotates rigidly with the tag,
so a rack nudged 5 mm and rotated 2° is absorbed automatically — no
position has to be re-taught.

A guard runs throughout: if the tag is missing, partly occluded, or
detected with low confidence, the frame is skipped rather than publishing
a pose the arm would act on. Only a clean, confident detection produces
nest poses for Layer 03. The localizer in pseudocode:

```text
# subscribe to the overhead RGB image + the camera intrinsics
# on each frame:
#     detect AprilTag markers -> (id, corners)
#     for the tray's tag id:
#         solve its 6-DoF pose via PnP (corners + tag size + intrinsics)  (T_cam_tag)
#         T_base_tag = camera_mount * T_cam_tag                            (into the arm frame)
#         for each nest: pose = T_base_tag * fixed_offset[nest]            (grid follows the tag)
#         publish a PoseStamped per nest                                   (-> Layer 03)
#     low-confidence / occluded tag -> skip the frame                      (never publish a guess)
```

### Real code

An OpenCV + AprilTag node that turns the tray tag into a pose for every
nest. **Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from sensor_msgs.msg import Image                       # the overhead camera frame
from geometry_msgs.msg import PoseStamped               # the per-nest pose we publish
from cv_bridge import CvBridge                          # converts a ROS Image <-> an OpenCV array
import numpy as np                                      # arrays + the camera matrix / transforms
from pupil_apriltags import Detector                    # finds the printed AprilTags in the image

CAM_MTX = np.array([[600., 0., 320.], [0., 600., 240.], [0., 0., 1.]])  # fx,fy + image centre
TAG_SIZE = 0.03                                          # the tray tag is 3 cm wide (printed size)
TRAY_TAG = 0                                             # the tag id stuck on the tray
NEST_OFFSETS = {"A1": (0.00, 0.00, 0.00),               # each nest's fixed offset from the tag...
                "A2": (0.02, 0.00, 0.00)}               # ...(only two shown; all 96 in practice)


class TrayLocalizer(Node):                              # publishes a pose per nest from the tray tag
    def __init__(self):                                 # one-time setup
        super().__init__("tray_localizer")              # register on the ROS 2 graph
        self.bridge = CvBridge()                        # the one image converter we reuse
        self.det = Detector(families="tag36h11")        # the AprilTag family our tags use
        self.pub = self.create_publisher(PoseStamped, "/nest/pose", 10)  # per-nest poses out
        self.create_subscription(                       # listen to the overhead camera...
            Image, "/overhead/image_raw", self.on_frame, 10)

    def on_frame(self, msg):                            # runs on each overhead frame
        gray = self.bridge.imgmsg_to_cv2(msg, "mono8")  # ROS Image -> grayscale OpenCV array
        fx, fy, cx, cy = CAM_MTX[0,0], CAM_MTX[1,1], CAM_MTX[0,2], CAM_MTX[1,2]  # intrinsics
        tags = self.det.detect(gray, estimate_tag_pose=True,  # detect tags AND solve their pose...
                               camera_params=(fx, fy, cx, cy), tag_size=TAG_SIZE)
        for t in tags:                                  # consider every detected tag
            if t.tag_id != TRAY_TAG or t.decision_margin < 30:  # not the tray tag, or low-confidence?
                continue                                # skip it -> never publish a guessed pose
            for nest, off in NEST_OFFSETS.items():      # turn the tag pose into each nest's pose
                p = PoseStamped()                       # the message for this nest
                p.header.frame_id = "base_link"         # poses are expressed in the arm frame
                p.pose.position.x = float(t.pose_t[0] + off[0])  # tag X + the nest's fixed X offset
                p.pose.position.y = float(t.pose_t[1] + off[1])  # tag Y + the nest's fixed Y offset
                p.pose.position.z = float(t.pose_t[2] + off[2])  # tag Z + the nest's fixed Z offset
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

## Hand-eye calibration and its verification

A lab assistant's hand-eye coordination is so practised they never think
about it — they see a vial and their hand goes exactly there, the brain
having long since learned the offset between eye and hand. A robot has to
*measure* that offset explicitly: the transform between what the camera
sees and where the arm actually is. This use case establishes and,
crucially, *checks* that camera-to-arm calibration, because a few
millimetres of error turns every reach into a near-miss.

The bigger experiment is the HPLC batch, every vial of which is reached
for using poses the camera reports. If the calibration is wrong, that
error is baked silently into all 60–100 reaches — the arm consistently
grips a few millimetres off, dropping or crushing vials. Calibration is
the foundation the whole perception-to-motion chain stands on, which is
why this use case also verifies it rather than trusting it.

A human's hand-eye coordination is continuous and self-correcting; the
robot's calibration is a periodic procedure — run at bring-up and
re-checked routinely (say, daily or after any bump to the camera) because
it can drift. The verification step runs more often than the full
recalibration, quietly confirming on a regular cadence that the cell is
still reaching true.

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
- **Walkthrough:** (1) drive the arm to several known tag poses; (2)
  collect tag-in-camera and arm-in-base pairs; (3) solve `calibrateHandEye`
  for the camera↔arm transform; (4) cross-check against depth and flag any
  offset over tolerance.
- **In the scene:** the arm taps out a little choreography, touching
  several known marker poses while the camera watches, and from that dance
  the exact camera-to-arm offset is solved — then a deliberately planted
  3 mm error is caught by the depth check, proving the safeguard bites.
- **Why it's done this way:** every reach is only as accurate as the
  camera-to-arm transform, and a few millimetres of calibration error
  turns each grasp into a near-miss; building and *verifying* the
  calibration is the foundation the whole perception-to-motion chain
  stands on.
- **In the full loop:** this underwrites accuracy for the whole loop —
  every pose the perception layer publishes inherits the calibration, so
  it connects perception's outputs to motion's inputs for every reach in
  the run.
- **Value:** the calibration *procedure* is proven in sim and transfers to
  hardware, where it's the difference between reaching the vial and
  reaching past it.

### Meta code

This meta is the classic eye-in-hand calibration: recover the unknown
rigid transform between the camera and the gripper by moving the arm to
several known poses and watching how a fixed marker appears to move in the
camera. Each sample pairs two measurements taken at the same instant —
where the gripper is relative to the arm base (from forward kinematics),
and where the marker is relative to the camera (from the tag's pose).

With a handful of such pairs spanning different orientations, a standard
solver (OpenCV's `calibrateHandEye`) computes the camera-to-gripper
transform that is consistent with all of them. That single transform is
what lets any future tag detection be expressed correctly in the arm's
frame.

The pipeline does not stop at solving — it verifies. Holding out a sample
the solve didn't use, it predicts where the marker should appear given the
computed transform and compares that to where the marker was actually
measured. A residual error above a small tolerance means the calibration
is wrong or has drifted, and the result is rejected rather than trusted.

In only-code the true transform is known, so a deliberate few-millimetre
error is injected to prove the verification step actually catches it — the
safeguard is tested, not assumed. The calibration in pseudocode:

```text
# collect N samples: drive the arm to a known pose, detect the tray tag, record:
#     (R_grip2base, t_grip2base)   from forward kinematics / tf
#     (R_tag2cam,   t_tag2cam)     from the tag PnP
# solve calibrateHandEye(...) -> (R_cam2grip, t_cam2grip)   (the eye-in-hand transform)
# verify on a held-out sample:
#     predict the tag pose using the solved transform
#     error vs the measured pose > tol -> FAIL              (bad / drifted calibration)
# (sim) inject a deliberate 3 mm offset -> the check MUST flag it
```

### Real code

An OpenCV `calibrateHandEye` solve plus a residual check that catches a
bad calibration. **Illustrative teaching code** — re-verify before use;
every line is commented.

```python
import cv2                                              # OpenCV: hand-eye calibration + geometry
import numpy as np                                      # arrays for the rotations / translations

TOL_M = 0.002                                           # fail the check above a 2 mm residual


def calibrate(samples):                                 # samples: list of (R_g2b,t_g2b,R_t2c,t_t2c)
    R_g2b = [s[0] for s in samples]                     # gripper->base rotations (from FK / tf)
    t_g2b = [s[1] for s in samples]                     # gripper->base translations
    R_t2c = [s[2] for s in samples]                     # tag->camera rotations (from PnP)
    t_t2c = [s[3] for s in samples]                     # tag->camera translations
    R_c2g, t_c2g = cv2.calibrateHandEye(                # solve the eye-in-hand transform...
        R_g2b, t_g2b, R_t2c, t_t2c,                     # ...from the paired motions
        method=cv2.CALIB_HAND_EYE_TSAI)                 # Tsai's classic solver
    return R_c2g, t_c2g                                 # camera->gripper rotation + translation


def verify(R_c2g, t_c2g, holdout):                      # check the transform on an unseen sample
    R_g2b, t_g2b, R_t2c, t_t2c = holdout                # the held-out measured sample
    # predicted tag-in-base via the solved chain: base<-grip<-cam<-tag
    cam_in_base = t_g2b + R_g2b @ t_c2g                 # camera position in the base frame
    pred_tag = cam_in_base + (R_g2b @ R_c2g) @ t_t2c    # predicted tag position in the base frame
    meas_tag = t_g2b + R_g2b @ (t_c2g + R_c2g @ t_t2c)  # the same chain from the measured sample
    err = float(np.linalg.norm(pred_tag - meas_tag))    # residual distance between them (metres)
    return err <= TOL_M, err                            # (passed?, the residual) for the report


if __name__ == "__main__":                              # run directly on recorded samples
    data = np.load("handeye_samples.npy", allow_pickle=True)  # the N driven-pose + tag samples
    R, t = calibrate(list(data[:-1]))                   # calibrate on all but the last sample
    ok, err = verify(R, t, data[-1])                    # verify on the held-out last sample
    print(f"calibration {'OK' if ok else 'FAILED'} (residual {err*1000:.1f} mm)")  # the verdict
```

## See also

- [`README.md`](README.md) — the only-code folder overview and the full
  list of development layers.
- [`../02-code-plus-hardware/04-perception-and-vision.md`](../02-code-plus-hardware/04-perception-and-vision.md)
  — the same layer once **real cameras** feed the pipeline (camera SDKs,
  hand-eye calibration, glass glare, real noise, latency).
- [`../foundation-models.md`](../foundation-models.md) — VLA models can
  **subsume this perception layer**, mapping camera frames straight to
  actions; the learned-upgrade alternative to the explicit pipeline here.
