# 02 — Top three 6-DoF pose estimation models (with code)

> **Goal of this page.** Name three of the best-known *open* 6-DoF pose
> estimation models you can actually download and run, compare them, and
> give a short, commented code sample for each. Builds on
> [`00-introduction.md`](00-introduction.md) and
> [`01-working.md`](01-working.md).
>
> **Read me first — all numbers are approximate and drift fast.**
> Speeds, licences and especially install/run commands change often.
> These are research repositories, so their Python interfaces (the exact
> function and argument names) shift between versions. Treat every code
> block as a *teaching sketch* that shows the *shape* of the call, not a
> guaranteed-runnable script — always check the project's current
> documentation. Most of these want an NVIDIA GPU and a depth camera (see
> [`01-working.md`](01-working.md)).

Reminders from the earlier pages, so this one stands on its own:

- **6-DoF** = **six degrees of freedom** = three position numbers + three
  orientation numbers = a **pose**.
- **RGB-D** = **red-green-blue-plus-depth**: a colour image plus a
  per-pixel distance image, usually from a depth camera such as an Intel
  RealSense.
- **CAD model** = **computer-aided-design model**: a precise 3D drawing of
  an object's shape, stored as a *mesh* file (a surface made of many small
  triangles, e.g. `.obj` / `.ply` / `.stl`).
- **Mask** = a per-pixel outline marking which pixels belong to the
  object.

## Why these three

These are three of the most famous pose estimators with **open** code and
weights, spanning the useful range: a state-of-the-art all-rounder, a
render-and-compare novel-object model, and an old lightweight RGB-only
favourite.

| Model | Needs a CAD model? | Needs depth? | ~Speed | Licence | Bottom line |
|---|---|---|---|---|---|
| **FoundationPose** (NVIDIA, 2024) | Optional (works model-based *or* model-free) | Yes (RGB-D) | ~real-time when *tracking*, slower for a fresh estimate | Open (research-leaning) | State of the art; one model does both estimation and tracking, known or novel objects |
| **MegaPose** (Inria, in HappyPose) | Yes, at run time (no per-object retraining) | Optional but recommended | Slow-ish (render-and-compare) | Open (permissive) | Best for *novel* known-shape objects you can supply a mesh for, without retraining |
| **DOPE** (NVIDIA) | Pre-trained per object | **No** (RGB only) | Fast, lightweight | Open (permissive) | Old, famous, runs on cheap hardware — but only for the specific objects it was trained on |

"Model-based" and "model-free" are explained in
[`00-introduction.md`](00-introduction.md); "single-shot versus
tracking" in [`01-working.md`](01-working.md).

---

## 1. FoundationPose

**What it is.** A 2024 model from NVIDIA that unifies **6-DoF pose
estimation *and* tracking** in one system, and works for **novel
objects** — either **model-based** (you give it a CAD mesh) or
**model-free** (you give it a handful of reference images instead). It is
widely regarded as state of the art. It is distributed as a GitHub
repository you clone and build, not a one-line `pip install`.

**Install.**

```bash
# A recent NVIDIA GPU is expected. The repo ships heavier build steps
# (CUDA extensions, often a provided Docker image) — follow its README;
# the lines below are only the shape of the process.
git clone https://github.com/NVlabs/FoundationPose.git
cd FoundationPose
# The project recommends its Docker image or a conda env, then a build
# step for its custom CUDA modules. Check the current README for specifics.
```

**Minimal code to run it.** *(API names approximate — research repo, check
the README.)*

```python
# Goal: hand FoundationPose a CAD mesh + one RGB image + the matching
# depth image + a mask of the object, and get back the object's 6-DoF
# pose as a 4x4 transform matrix. This is "inference" — using the model,
# not training it.

import numpy as np                      # NumPy: arrays of numbers
import trimesh                          # loads 3D mesh (CAD) files
from estimater import FoundationPose    # the repo's estimator class
# (exact import path varies by version — see the repo's run scripts)

# 1. Load the object's CAD model (the .obj/.ply mesh). This is the
#    "model-based" route; for model-free you would instead supply a few
#    reference images of the object.
mesh = trimesh.load("mustard_bottle.obj")

# 2. Create the estimator, telling it about the object's geometry.
est = FoundationPose(
    model_pts=mesh.vertices,           # the mesh's 3D points
    model_normals=mesh.vertex_normals, # which way each surface faces
    mesh=mesh,
)

# 3. Load one frame of what the camera sees. "rgb" is the colour image,
#    "depth" is the per-pixel distance image (RGB-D), "mask" marks the
#    object's pixels (usually from a detection model run just before),
#    and "K" is the camera's calibration (its lens geometry).
rgb   = np.load("rgb.npy")             # H x W x 3 colour image
depth = np.load("depth.npy")           # H x W distances, in metres
mask  = np.load("mask.npy")            # H x W true/false: object pixels
K     = np.load("cam_K.npy")           # 3 x 3 camera intrinsics

# 4. register(...) does a fresh single-shot estimate and returns the pose
#    as a 4x4 transform matrix (object coordinates -> camera coordinates;
#    see 01-working.md). For video you would then call a track(...) method
#    each following frame, which is much faster.
pose = est.register(K=K, rgb=rgb, depth=depth, ob_mask=mask)

print("4x4 pose matrix:\n", pose)
```

**What you should see.** A 4x4 matrix of numbers — the object's pose. Its
top-left 3x3 block is the rotation, its right-hand column is the position
in metres, and its bottom row is `0 0 0 1` (the padding row from
[`01-working.md`](01-working.md)), e.g.:

```text
[[ 0.99 -0.02  0.10   0.12 ]
 [ 0.03  0.99 -0.05  -0.03 ]
 [-0.10  0.05  0.99   0.48 ]
 [ 0.00  0.00  0.00   1.00 ]]   # position ≈ (0.12, -0.03, 0.48) m
```

---

## 2. MegaPose

**What it is.** A model from Inria (the French research institute) for
the **6-DoF pose of *novel* objects** via **render-and-compare** (the
guess-render-compare-adjust loop from
[`01-working.md`](01-working.md)). "Novel" here means you do **not** have
to retrain the network for each object: you hand it the object's CAD mesh
at run time and it figures out the pose. It ships inside the **HappyPose**
toolkit, which packages several Inria pose methods behind one installable
library.

**Install.**

```bash
pip install happypose            # the toolkit that bundles MegaPose
# Pretrained weights download on first use, or via the toolkit's
# download command — see the HappyPose docs (commands drift).
```

**Minimal code to run it.** *(API names approximate — check HappyPose docs.)*

```python
# Goal: give MegaPose one RGB(-D) observation plus a detection box for an
# object whose CAD mesh we have, and get back its 6-DoF pose. Names follow
# the happypose package and may change between releases.

import numpy as np
from happypose.toolkit.inference import load_megapose, ObjectData, Observation
# (illustrative import path; the real one is in the HappyPose examples)

# 1. Load the pretrained MegaPose model and the set of object meshes it
#    should be able to handle (each entry points at a CAD file).
model = load_megapose("megapose-1.0-RGBD")
object_dataset = {"mustard_bottle": "meshes/mustard_bottle.ply"}

# 2. Build one observation: the colour image, optionally the depth image,
#    and the camera calibration. Depth is optional here but improves the
#    result (see "the role of depth" in 01-working.md).
observation = Observation(
    rgb=np.load("rgb.npy"),            # H x W x 3 colour image
    depth=np.load("depth.npy"),        # H x W distances (optional)
    camera_K=np.load("cam_K.npy"),     # 3 x 3 camera intrinsics
)

# 3. Tell it which object to find and roughly where (a detection box from
#    a perception model run just before — see 03-perception-vision-models).
detections = [ObjectData(label="mustard_bottle", bbox=[120, 80, 300, 360])]

# 4. Run inference. MegaPose renders the mesh at many candidate poses,
#    compares each against the image, and refines the best — returning the
#    pose as a 4x4 transform.
result = model.run_inference(observation, detections, object_dataset)
print("4x4 pose matrix:\n", result[0].pose)
```

**What you should see.** Again a 4x4 transform matrix per detected object
(rotation block + position column + `0 0 0 1` padding row), as shown for
FoundationPose above. Because MegaPose renders and compares many
candidate poses, a fresh estimate is on the slower side — fine for
picking a static object, less so for fast tracking.

---

## 3. DOPE (Deep Object Pose Estimation)

**What it is.** An older (2018) but famous and **lightweight** model from
NVIDIA. Its claim to fame: it estimates the 6-DoF pose of a *known*
household object from a **single ordinary RGB image — no depth camera
needed.** The catch is that each network is trained for a **specific set
of objects** (the original release covered some YCB household items — a
standard set of test objects like a mustard bottle, a soup can, a sugar
box). It cannot handle a novel object the way the two above can, but it is
small, fast, and easy to run, which is why it is still a common teaching
and baseline choice.

**Install.**

```bash
# Cloned from GitHub; it is a ROS-friendly research repo. The core network
# is small and runs without depth.
git clone https://github.com/NVlabs/Deep_Object_Pose.git
cd Deep_Object_Pose
pip install -r requirements.txt   # PyTorch and image libraries
# Download the pretrained per-object weight files as the README directs.
```

**Minimal code to run it.** *(API names approximate — research repo.)*

```python
# Goal: load DOPE's pretrained network for one known object and run it on
# a single RGB image to get that object's 6-DoF pose. No depth involved.

from PIL import Image                  # PIL = Python Imaging Library
from dope.inference import ObjectDetector  # the repo's detector wrapper
# (illustrative import; DOPE's real entry point is its inference scripts)

# 1. Load the pretrained network for ONE specific object. DOPE uses a
#    separate trained weight file per object it knows.
detector = ObjectDetector(
    weights="weights/mustard.pth",     # weights for the "mustard bottle"
    camera_K="cam_K.json",             # the camera's calibration
)

# 2. Load a single ordinary colour photo — that is the only sensor input.
image = Image.open("scene_rgb.jpg")

# 3. Run it. DOPE locates the object and infers its pose directly from the
#    RGB image. It returns the pose as a position plus an orientation
#    (here a quaternion + a position; convert to a 4x4 matrix if you need
#    one — see 01-working.md, all forms carry the same information).
results = detector.detect(image)
for obj in results:
    print("position (x, y, z) metres:", obj.location)
    print("orientation (quaternion):", obj.quaternion)
```

**What you should see.** For each found object, a **position** (three
numbers, the object's location in metres relative to the camera) and an
**orientation** as a **quaternion** (four numbers encoding the rotation —
see [`01-working.md`](01-working.md)). Together those are the full 6-DoF
pose; you can convert them into the same 4x4 transform matrix the other
two print. Because it is RGB-only and small, it runs comfortably on
modest hardware, even an embedded NVIDIA **Jetson** board.

---

## Choosing between them

- **Best overall, known *or* novel objects, plus tracking across video**
  → **FoundationPose** (state of the art, but heavier and wants RGB-D).
- **Novel objects you have a CAD mesh for, no per-object retraining**
  → **MegaPose** (clean render-and-compare; slower per estimate).
- **A fixed, small set of known objects, cheap hardware, RGB only**
  → **DOPE** (lightweight and proven, but tied to its trained objects).

For this repository's grocery-shelf framing — a *known* catalogue of
products with known shapes — the "keep it simple" path is to start with a
model-based estimator and a CAD model per product (DOPE if the catalogue
is small and fixed; FoundationPose when you want one model to cover the
whole range and follow items across frames), and reach for MegaPose's
novel-object flexibility only when you must handle items you have not
pre-scanned. See the model-based-first reasoning in
[`00-introduction.md`](00-introduction.md).

## See also

- What these are and when to use them:
  [`00-introduction.md`](00-introduction.md).
- The mechanics behind the code (render-and-compare, depth, tracking):
  [`01-working.md`](01-working.md).
- The step before this one (detection):
  [`../03-perception-vision-models/00-introduction.md`](../03-perception-vision-models/00-introduction.md).
- The step after a pose is known (grasping):
  [`../05-grasp-generation-models/00-introduction.md`](../05-grasp-generation-models/00-introduction.md).
- Hardware and tools for running models:
  [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).
- The wider perception field write-up:
  [`../../01-all-areas/02-perception-cv/README.md`](../../01-all-areas/02-perception-cv/README.md).
```