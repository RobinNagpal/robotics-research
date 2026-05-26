# Stack layer: Grasping

> **Job:** decide *where and how* to grab the product — the grasp pose
> the arm executes. Because v1 is a single rigid SKU with a known
> geometry and a preferred grasp, this layer can start almost trivially
> (analytical) and only needs the learned methods once the SKU set
> grows. The honest v1 answer is "don't over-engineer this."

## Comparison

| Method | Input | Grasp types | Novel-object generalization | Training / data needs | Speed | Bottom line |
|--------|-------|-------------|-----------------------------|-----------------------|-------|-------------|
| **Analytical / antipodal** (geometric) | Known model + pose | Parallel (and simple suction) | None (per-SKU) | None | Fast | Perfect for v1: one rigid SKU, known grasp points — no model to train |
| **Dex-Net 4 / GQ-CNN** | Depth image | Parallel **and suction** | Moderate | Pretrained (can fine-tune) | Fast | Mature, strong on bins; great if you need suction on flat-topped boxes |
| **Contact-GraspNet** | Point cloud (RGB-D) | Parallel | Strong | Pretrained | Moderate (GPU) | Robust 6-DoF grasps in clutter; widely used baseline |
| **AnyGrasp** | RGB-D | Parallel (+ stability) | **Strong** | Pretrained (license) | Moderate (GPU) | Best general-purpose generalization for mixed/unknown SKUs |
| **GIGA** | TSDF / depth | Parallel | Strong | Trained | Moderate | Good in clutter via implicit grasp/geometry; heavier to set up |
| **GraspNet-1B baseline** | Point cloud | Parallel | Moderate | Pretrained on GraspNet-1B | Moderate | Useful reference/benchmark model; AnyGrasp/CGN usually preferred in practice |

## Top choice

**Analytical / antipodal for v1; AnyGrasp (or Contact-GraspNet) for
generalization.**

The requirements pin v1 to a single rigid SKU with known dimensions and
a preferred grasp — so a hand-defined antipodal pinch (cans/bottles) or
a top-suction point (flat boxes) is the right amount of engineering, and
it composes directly with the **Dex-Net 4** suction model if the product
is best handled by vacuum. Reserve the learned generalizers —
**AnyGrasp** (strongest novel-object generalization; note its
license/availability) or **Contact-GraspNet** (open, robust) — for the
later milestone where the tray holds varied or unknown SKUs. Don't pay
the data/compute cost of a learned grasp model to solve a problem a
geometric grasp already solves.
