# Stack layer: Perception

> **Job:** two distinct questions. (1) **Where is the product** to pick —
> its 6-DoF pose in the tray? (2) **Where is the target slot** on the
> shelf, and is it empty? These are different problems with different
> tools, so they get two comparison tables. The project's "simplest"
> framing lets you start almost geometry-only and add learned perception
> as you relax the "known tray layout" assumption.

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
