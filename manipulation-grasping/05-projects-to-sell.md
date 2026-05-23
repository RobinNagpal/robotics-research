# Four Projects You Can Build and Sell

## 1. Bin-picking-in-a-box service (~4 weeks)

For a contract-manufacturing customer with a single SKU mix: deliver a
trained Contact-GraspNet/AnyGrasp model + FoundationPose for known
parts + MoveIt 2 motion + a status dashboard. Sells as a turnkey
"singulation" cell.

- **Buyers:** small CMs, 3PLs that can't afford Covariant or Symbotic.
- **Pricing:** $25-75k integration + $1-3k/mo support.

## 2. Demo-amplification service (~3 weeks)

Customer ships 20-50 teleop demos; you return a synthetic 2-10k-episode
dataset via MimicGen-style trajectory replay + augmentation, plus a
trained Diffusion Policy or fine-tuned VLA.

- **Stack:** Robosuite/RoboCasa, MimicGen, LeRobot, Diffusion Policy.
- **Buyers:** robotics startups that can teleop but can't afford a
  collection army.
- **Pricing:** $5-25k per task; subscription credits.

## 3. Open-vocabulary grasping API (~3 weeks)

REST endpoint: send an RGB-D image and a text prompt ("grab the white
mug, not the cup"); returns a 6-DoF grasp pose. Wraps
Grounding-DINO + SAM 2 + AnyGrasp.

- **Buyers:** OEM arms (xArm, UR), educational robotics, prototype teams.
- **Pricing:** $0.01-0.10 per call; $200-2k/mo SaaS tier.

## 4. Tactile-grasp retrofit kit (~4 weeks)

Hardware + software bundle: 3D-printed GelSight-style tactile fingertip
(open hardware) + a slip-detection model + a force-aware Diffusion
Policy fine-tune. Sells to teams with cheap arms that need reliable
grasp on deformable / fragile objects.

- **Stack:** GelSight Mini or AnySkin design, PyTorch tactile model,
  LeRobot integration.
- **Buyers:** food, cosmetics, e-commerce returns processors.
- **Pricing:** $5-15k per arm + recurring sensor consumables.
