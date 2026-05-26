# Stack layer: Grasping

> **Job:** decide *where and how* to grab the product — the grasp pose
> the arm executes. Because v1 is a single rigid SKU with a known
> geometry and a preferred grasp, this layer can start almost trivially
> (analytical) and only needs the learned methods once the SKU set
> grows. The honest v1 answer is "don't over-engineer this."

## How this layer fits into the architecture

Grasping is a small but pivotal **decision** layer. Given that the
perception layer has already found the product, grasping decides exactly
*how the gripper should grab it* — the precise position and orientation
to approach from, and (for a parallel gripper) how wide to open, or which
suction point to use on a flat-topped box.

It sits **between perception and arm motion**, and because those three
are easy to confuse, the boundary is worth stating plainly:

- Perception (`05-perception.md`) says **where the object is**.
- Grasping says **where to put the gripper to hold it**.
- Arm motion (`04-arm-motion-planning.md`) says **how to move the arm to
  get the gripper there**.

In the cycle: the orchestration layer, holding the product pose from
perception, asks the grasping layer for a grasp. Grasping returns a
single target gripper pose (plus a width or suction choice). That pose
becomes the goal the arm-motion layer plans toward; after the move, the
gripper closes and a grasp check confirms it worked.

For v1 with one known rigid SKU this layer is deliberately tiny — a
fixed, hand-defined grasp. Keeping it as its own clean box is what lets
you later swap in a learned grasp model (AnyGrasp / Contact-GraspNet)
when SKUs vary, **without touching any other layer**. Its inputs and
outputs travel over ROS 2 (`02-middleware.md`) like everything else.

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

## Cost, hardware & where it runs

| Tier | Pick | Where it runs | Machine requirements | Cost |
|------|------|---------------|----------------------|------|
| **Best in class** | AnyGrasp (strongest novel-object generalization) | Onboard / edge GPU computer | RTX GPU or Jetson Orin, CUDA | Free for research/eval but a **commercial license fee** to ship; plus GPU cost |
| **Good enough & cheapest** | Analytical / antipodal (geometric) | Onboard CPU | Any CPU — it's pure geometry | **Free** — no model, no GPU, no training data |
| **Best cost-for-performance** | Analytical for v1's known SKU; Contact-GraspNet (open) when SKUs vary | CPU now; add a GPU only at the generalization milestone | CPU-only for v1; GPU later | Free now; Contact-GraspNet is open (no license fee), so the only later cost is the GPU |

This is the cheapest layer in the stack for v1: a known rigid SKU with a
preferred grasp needs zero hardware beyond the CPU already running ROS 2.
Spend nothing here until the tray genuinely holds varied SKUs — and even
then, open Contact-GraspNet avoids AnyGrasp's license fee.
