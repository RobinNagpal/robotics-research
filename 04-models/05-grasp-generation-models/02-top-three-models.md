# 02 — Top three grasp generation models (with code)

> **Goal of this page.** Name three of the best-known grasp generation
> models you can actually get hold of, compare them, and give a short,
> commented code sample for each. Builds on
> [`00-introduction.md`](00-introduction.md) and
> [`01-working.md`](01-working.md).
>
> **Read me first — all numbers and commands are approximate and drift
> fast.** These are research projects; their package names, file paths,
> and function names change often, and some need a paid licence key.
> Treat every code block as a *teaching sketch* that shows the *shape* of
> the interface, not a guaranteed-runnable script. Always check the
> project's current documentation. Running these comfortably wants a
> depth/RGB-D camera (Red-Green-Blue colour plus Depth) and an NVIDIA GPU
> (see
> [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md)).

## Why these three

All three target the common **parallel-jaw gripper** (the two-finger
"pincer" from [`00-introduction.md`](00-introduction.md)) and all work
from 3D geometry — a **point cloud** (a set of 3D dots sampled off
visible surfaces) or a **depth image** (a photo whose pixels store
distance, not colour). They cover the spectrum from "polished product"
to "academic reference":

| Model | Gripper type | Needs depth? | Output | Licence | Bottom line |
|---|---|---|---|---|---|
| **AnyGrasp** | Parallel-jaw | Yes (point cloud + colour) | Ranked set of 6-DoF grasps + scores | Commercial SDK (free key for academia) | Fastest, most robust off-the-shelf option — but a licensed black box |
| **Contact-GraspNet** | Parallel-jaw | Yes (depth → point cloud) | 6-DoF grasps + scores, whole scene | Open (research, non-commercial) | Strong open model that grasps a full cluttered scene from one depth frame |
| **GraspNet-baseline** | Parallel-jaw | Yes (point cloud) | `GraspGroup` (poses + widths + scores) | Open (research) | The academic reference and shared benchmark — best for learning |

"6-DoF" reads "six degrees of freedom": three numbers for position plus
three for orientation, which together pin the gripper down completely
(unpacked in [`01-working.md`](01-working.md)).

---

## 1. AnyGrasp

**What it is.** A fast, general grasp-detection system from the team
behind **GraspNet** (the group that built the GraspNet-1Billion dataset
and benchmark). You feed it a point cloud with colour and it returns a
**`GraspGroup`** — a ranked bundle of 6-DoF parallel-jaw grasps, each
with a grip width and a quality score — typically in a fraction of a
second, even in clutter. It is shipped as a **commercial SDK** (software
development kit) that needs a **licence key**; the makers grant free keys
for academic use. Because it is closed, you treat it as a reliable box:
points in, ranked grasps out.

**Install.**

```bash
# Distributed as a licensed SDK, not on the public package index.
# 1. Request a licence key from the AnyGrasp project page.
# 2. Download the SDK wheel they provide and install it:
pip install anygrasp_sdk-<version>.whl   # exact filename comes from them
pip install open3d numpy                  # Open3D: point-cloud handling
# Then place the licence-key file where the SDK expects it (see their docs).
```

**Minimal code to run it.** (API names follow the AnyGrasp SDK and may
change — check its README.)

```python
# Goal: hand AnyGrasp a point cloud (3D dots) plus the colour of each
# dot, and print the best few grasp poses it proposes. This is
# "inference" — using a trained model, not training one.

import numpy as np                       # NumPy: arrays of numbers
from gsnet import AnyGrasp               # the SDK's grasp detector class

# 1. Build and load the model. The config carries the licence path and
#    detection settings (e.g. how many grasps, the gripper's max width).
class Cfg:                               # a tiny stand-in for the SDK config
    checkpoint_path = "log/checkpoint_detection.tar"
    max_gripper_width = 0.08             # metres the jaws can open (~8 cm)
    gripper_height = 0.03                # jaw depth in metres
    top_down_grasp = False              # allow grasps from any angle
grasp_model = AnyGrasp(Cfg())
grasp_model.load_net()                  # loads weights onto the GPU

# 2. Provide the scene as two matching arrays: one 3D position per point,
#    and one colour per point. On a robot these come from a depth/RGB-D
#    camera; here we use blank stand-ins of N points.
N = 20000
points = np.zeros((N, 3), dtype=np.float32)   # x, y, z of each dot (metres)
colors = np.zeros((N, 3), dtype=np.float32)   # r, g, b of each dot (0..1)

# 3. Detect grasps. "lims" bounds the workspace box to search within.
#    The model returns a GraspGroup: many candidates, each with a pose,
#    a grip width, and a score.
lims = [-0.5, 0.5, -0.5, 0.5, 0.0, 1.0]       # x/y/z min,max of the box
grasp_group, _ = grasp_model.get_grasp(points, colors, lims=lims)

# 4. Sort best-first by score and look at the top few. Each grasp carries
#    a 4x4 transform (its 6-DoF pose), a width, and a score 0..1.
grasp_group = grasp_group.nms()         # drop near-duplicate grasps
grasp_group = grasp_group.sort_by_score()
for g in grasp_group[:3]:
    print("score:", g.score, " width:", g.width, " pose:\n", g.translation)
```

**What you should see.** A handful of printed grasps, each with a score
near 1 for confident grips, a finger-opening width in metres, and a 3D
position (and, in the full object, an orientation) for the gripper. On a
real robot you would pass the top reachable pose to a motion planner.

---

## 2. Contact-GraspNet

**What it is.** A grasp model from **NVIDIA** that predicts **6-DoF
parallel-jaw grasps directly for a whole scene** from a single depth
frame (or the point cloud computed from it). Its trick is to anchor each
grasp to an observed **contact point** on a surface, which keeps the
proposals physically grounded and makes it good at cluttered tabletops.
It is open source (research / non-commercial licence) and you get it by
**cloning its GitHub repository**.

**Install.**

```bash
# Cloned from source; the repo ships an environment file and weights.
git clone https://github.com/NVlabs/contact_graspnet.git
cd contact_graspnet
conda env create -f contact_graspnet_env.yml   # builds a matching env
conda activate contact_graspnet
# Then download the pretrained checkpoint per the repo's instructions.
```

**Minimal code to run it.** (Paths and helper names follow the repo and
may change — check its README.)

```python
# Goal: load a depth scene, run Contact-GraspNet once, and print the
# grasp poses and scores it predicts for the objects it sees.

import numpy as np
from contact_graspnet import config_utils
from contact_graspnet.contact_grasp_estimator import GraspEstimator

# 1. Load the model's configuration and build the estimator, then load
#    the pretrained weights (the trained network) onto the GPU.
cfg = config_utils.load_config(checkpoint_dir="checkpoints/scene_test")
estimator = GraspEstimator(cfg)
estimator.load_weights()                # restore the trained network

# 2. Provide the scene. The model can take a raw point cloud (an array of
#    3D dots) — here a blank stand-in. On a robot this comes from a
#    depth/RGB-D camera, optionally with a per-object mask so grasps are
#    grouped by object.
point_cloud = np.zeros((20000, 3), dtype=np.float32)   # x, y, z per dot

# 3. Run inference. It returns, for the scene, the predicted grasp poses
#    (each a 4x4 transform = a 6-DoF pose), a confidence score per grasp,
#    and the suggested grip opening width.
grasps, scores, widths, _ = estimator.predict_scene_grasps(point_cloud)

# 4. Look at the most confident grasps.
order = np.argsort(scores)[::-1]        # indices, highest score first
for i in order[:3]:
    print("score:", float(scores[i]), " width:", float(widths[i]))
    print("pose (4x4):\n", grasps[i])
```

**What you should see.** Arrays of grasp poses (4x4 transforms — the
6-DoF position-and-orientation of the gripper), one confidence score per
grasp, and a grip width per grasp. The repo also ships a viewer that
draws little gripper shapes onto the point cloud so you can *see* where
it wants to grab. Pass the top reachable pose to a motion planner.

---

## 3. GraspNet-baseline

**What it is.** The official **baseline** network released with
**GraspNet-1Billion** — the large benchmark (roughly a *billion* grasp
labels) that much of this field is measured against. It is the **academic
reference**: not the fastest or most robust, but the shared yardstick
everyone cites and the easiest to read and learn from. It takes a point
cloud and returns a **`GraspGroup`** (the same poses-plus-widths-plus-
scores bundle as AnyGrasp). You install the helper library
**`graspnetAPI`** and clone the baseline code.

**Install.**

```bash
pip install graspnetAPI                  # dataset + GraspGroup utilities
git clone https://github.com/graspnet/graspnet-baseline.git
cd graspnet-baseline
pip install -r requirements.txt          # PyTorch + point-cloud deps
# Some custom GPU operators must be compiled; follow the repo's steps.
# Then download the pretrained checkpoint per the repo's instructions.
```

**Minimal code to run it.** (Module and function names follow the repo
and may change — check its README.)

```python
# Goal: load the GraspNet-baseline network, run it on one point cloud,
# and print the top grasps from the GraspGroup it returns.

import numpy as np
import torch                             # PyTorch: runs the neural network
from graspnet import GraspNet            # the baseline network class
from graspnetAPI import GraspGroup       # wrapper around the output grasps

# 1. Build the network and load the pretrained weights onto the GPU.
net = GraspNet(input_feature_dim=0, num_view=300)   # config from the repo
net.load_state_dict(torch.load("checkpoint.tar")["model_state_dict"])
net.eval().to("cuda")                    # "use it", not "train it", mode

# 2. Provide the scene as a point cloud (3D dots). Real input comes from a
#    depth/RGB-D camera; here a blank stand-in of N points, shaped as the
#    network expects (a batch of 1).
N = 20000
points = torch.zeros(1, N, 3, dtype=torch.float32).to("cuda")

# 3. Run inference and wrap the raw output in a GraspGroup, which knows
#    how to sort and de-duplicate grasps for you.
with torch.no_grad():                    # we are not training
    pred = net({"point_clouds": points})
gg = GraspGroup(pred[0].detach().cpu().numpy())

# 4. Clean up and rank, then read off the best grasps. Each grasp carries
#    a score, a grip width, and a 6-DoF pose.
gg.nms()                                 # drop near-duplicate grasps
gg.sort_by_score()                       # best first
for g in gg[:3]:
    print("score:", g.score, " width:", g.width)
    print("translation:", g.translation, " rotation:\n", g.rotation_matrix)
```

**What you should see.** A `GraspGroup` of ranked candidates; printing
the top few gives a score, a finger-opening width, and a 6-DoF pose
(position plus a 3x3 rotation describing the gripper's orientation). The
repo includes an Open3D viewer that overlays the grasps on the cloud.

---

## Choosing between them

- **Best plug-and-play robustness, and you can accept a licence** →
  **AnyGrasp** (fast, well-tuned, but a closed box).
- **Open, grasps a whole cluttered scene from one depth frame** →
  **Contact-GraspNet**.
- **Learning how grasp models work, or benchmarking your own** →
  **GraspNet-baseline** (readable reference on a shared yardstick).

Remember the staging this repo prefers
([`00-introduction.md`](00-introduction.md)): for a few **known, rigid**
objects in a tidy scene, a **hand-computed geometric grip** beats all
three — no model, no GPU, fully explainable. Reach for these learned
models only when you face **many unknown objects in clutter**.

## See also

- What this model type is and when to use it:
  [`00-introduction.md`](00-introduction.md).
- The mechanics behind the code: [`01-working.md`](01-working.md).
- The hand-computed grip this repo starts from:
  [`../../03-hplc-autosampler/04-hello-worlds/05-grab-the-vial.md`](../../03-hplc-autosampler/04-hello-worlds/05-grab-the-vial.md).
- The manipulation field write-up:
  [`../../01-all-areas/05-manipulation/README.md`](../../01-all-areas/05-manipulation/README.md).
