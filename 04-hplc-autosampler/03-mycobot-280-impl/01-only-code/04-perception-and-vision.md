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

## See also

- [`README.md`](README.md) — the only-code folder overview and the full
  list of development layers.
- [`../02-code-plus-hardware/04-perception-and-vision.md`](../02-code-plus-hardware/04-perception-and-vision.md)
  — the same layer once **real cameras** feed the pipeline (camera SDKs,
  hand-eye calibration, glass glare, real noise, latency).
