# Important Things to Learn

## Foundations

- Rigid-body kinematics / dynamics for serial manipulators.
- Contact mechanics: friction cones, wrench-closure, force closure.
- Grasp metrics: epsilon-quality, Ferrari-Canny.
- Trajectory optimization with contacts.

## Perception for manipulation

- 6-DoF pose estimation (FoundationPose, MegaPose).
- Open-vocabulary detection (YOLO-World, Grounding DINO).
- Segmentation (SAM 2).
- Depth from stereo / structured light / ToF.
- Tactile sensing: GelSight, DIGIT, Reskin, AnySkin.

## Grasping algorithms

- Analytical: antipodal, force-closure, sampling-based.
- Data-driven: Dex-Net, Contact-GraspNet, AnyGrasp, GraspNet-1Billion
  models.
- Suction grasp planning (Dex-Net 4, AnyGrasp suction).

## Manipulation learning

- Imitation: ACT, Diffusion Policy, 3D Diffusion Policy, RDT.
- Sim-to-real RL with domain randomization (DextrAH, ANYmal-style for
  arms).
- VLA fine-tuning (OpenVLA, pi0).
- Demo amplification: MimicGen (NVIDIA) for synthetic demo generation.

## Bimanual and dexterous

- Coordination strategies, leader-follower teleop (Aloha).
- Five-fingered hands (Shadow, Allegro, LEAP, Inspire).
- Whole-body manipulation: mobile base + arm coordination.

## Tools

- **Sim:** Robosuite, RoboCasa, ManiSkill 3, Isaac Lab, MuJoCo MPC,
  Genesis.
- **Hardware:** Franka, UR5e, xArm 7, Aloha, SO-100, Shadow Hand,
  Allegro.
- **Software:** LeRobot, MoveIt 2, GraspIt!, AnyGrasp.

## Must-read papers

Dex-Net 1-4, Contact-GraspNet, ACT, Diffusion Policy, 3D Diffusion
Policy, MimicGen, OpenVLA, pi0, DextrAH-Hand, Mobile Aloha.
