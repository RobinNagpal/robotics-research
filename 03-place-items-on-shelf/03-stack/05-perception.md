# Stack layer: Perception

> **Job:** two distinct questions. (1) **Where is the product** to pick —
> its 6-DoF pose in the tray? (2) **Where is the target slot** on the
> shelf, and is it empty? These are different problems with different
> tools, so they get two comparison tables. The project's "simplest"
> framing lets you start almost geometry-only and add learned perception
> as you relax the "known tray layout" assumption.

## How this layer fits into the architecture

Perception is the robot's **eyes, plus the part of the brain that
interprets what the eyes see**. Everything the robot does physically
depends on first knowing two facts, and producing those two answers is
perception's entire job in the architecture:

1. **Where exactly is the next product** in the tray (its 6-DoF pose) —
   so the arm can pick it.
2. **Where on the shelf is the empty slot, and is it actually empty** —
   so the arm knows where to place.

In one cycle, perception runs twice (sometimes three times). First,
before the pick: the orchestration layer (`07-orchestration.md`) asks
"where's the product?"; perception reads the wrist RGB-D camera and
returns a pose, which feeds the grasping layer (`06-grasping.md`).
Second, before the place: "where's the slot?"; perception segments the
shelf and returns the target location to the arm-motion layer
(`04-arm-motion-planning.md`). After the place it can run once more to
**verify** the product landed upright.

It produces *information, not motion* — it never drives a motor. It
consumes camera images (from the real camera, or in development from the
simulator, `01-simulator.md`) and publishes poses and detections over
ROS 2 (`02-middleware.md`) for the grasping and arm-motion layers to act
on. This is the layer most directly tied to the perception-cv area of
the wider repo.

## A. Product 6-DoF pose estimation (the pick)

| Method | Needs CAD/mesh? | Novel-object generalization | Accuracy | Speed | Training data needed | Bottom line |
|--------|-----------------|-----------------------------|----------|-------|----------------------|-------------|
| **Geometric** (Open3D ICP / registration + planar fit) | Yes (model) | Low | High *when init is good* | Fast | None | Ideal for v1 known SKU from a roughly-known tray pose; brittle without a good initial guess |
| **FoundationPose** | Yes (or a few refs) | Strong (model-based, zero-shot) | High | Moderate (GPU) | None (uses the model) | Best step up from geometric for a *known rigid SKU*; robust 6-DoF from RGB-D |
| **MegaPose** | Yes (CAD) | Strong (novel objects) | High | Moderate–slow (GPU) | None | Comparable model-based pose; FoundationPose generally more current/robust |
| **Learned detector + PnP** | Keypoints/model | Moderate | Moderate | Fast | Yes (label keypoints) | Lightweight if you already detect the product; weaker on textureless/symmetric items |

## B. Detection & segmentation (find the product / the empty slot)

| Model | Open-vocabulary | Output | Zero-shot use | Speed | Fine-tune ease | Bottom line |
|-------|-----------------|--------|---------------|-------|----------------|-------------|
| **YOLO (v8 / v11)** | No | Boxes (+ seg) | No (train it) | **Real-time** | Easy (Roboflow) | Fastest, simplest once you have ~hundreds of labels of your SKU/shelf |
| **YOLO-World** | Yes | Boxes | Yes (text prompt) | Real-time | Easy | Open-vocab speed; great for "find the cans" without per-SKU training |
| **Grounding DINO** | Yes | Boxes | Yes (text prompt) | Slower | Moderate | Strongest open-vocab grounding; pair with SAM 2 for masks |
| **SAM 2** | Promptable | **Masks** (precise) | Yes | Moderate (GPU) | N/A (promptable) | Best for pixel-accurate slot/empty-space segmentation; needs a prompt/box |
| **Mask R-CNN** | No | Masks | No (train it) | Moderate | Moderate | Classic instance seg; superseded by the above for most new work |

## Top choice

- **Pick (pose):** start **geometric (Open3D)** for the v1 known SKU
  from a known tray pose — minimal moving parts. Graduate to
  **FoundationPose** the moment tray position becomes uncertain; it
  gives robust 6-DoF from RGB-D using just the product mesh, no
  per-object training.
- **Slot/product detection:** **YOLO-World** (or Grounding DINO) +
  **SAM 2**. Open-vocab detection finds the product and the shelf region
  without per-SKU labeling, and SAM 2 turns a box into a precise mask so
  you can measure the empty slot. Once a SKU is fixed and high-volume,
  fine-tune a plain **YOLO** for speed.

Validate all of it against **Isaac Sim Replicator** domain randomization
so it survives the sim-to-real gap (see `03-stack/01-simulator.md`).
