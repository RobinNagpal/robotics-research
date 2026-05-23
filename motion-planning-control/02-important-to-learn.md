# Important Things to Learn

## Math and control theory

- Linear algebra and matrix calculus.
- Classical control: PID, root locus, frequency-domain.
- State-space control: LQR, observers, Kalman filters.
- Nonlinear control: feedback linearization, sliding mode, Lyapunov
  methods.
- Optimization: convex (CVX, MOSEK), QP solvers (OSQP, qpOASES, HPIPM),
  nonlinear (IPOPT, SNOPT, CasADi).
- MPC: linear MPC, NMPC, real-time iteration scheme.
- Optimal control: DDP, iLQR, sequential quadratic programming.

## Rigid-body dynamics

- Forward / inverse kinematics, manipulator Jacobians.
- Recursive Newton-Euler, articulated-body algorithm (Pinocchio).
- Contact dynamics, complementarity, soft contact models (MuJoCo,
  RaiSim).

## Motion planning

- Sampling: PRM, RRT, RRT*, RRT-Connect, BIT*, AIT*.
- Search: A*, Hybrid A*, lattice planners.
- Trajectory optimization: CHOMP, TrajOpt, GPMP, GuSTO.
- Constrained planning: TAMP (task-and-motion planning), PDDLStream.

## Learning-based control

- RL: PPO, SAC, TD3, model-based RL (DreamerV3, TD-MPC2).
- Imitation: BC, DAgger, Diffusion Policy, ACT.
- Sim-to-real: domain randomization, RMA, system identification.
- Differentiable physics: Brax, MJX, Warp, Genesis.

## Safety

- Control Barrier Functions (CBFs).
- Reachability analysis (HJ reachability, Levelset toolbox).
- Robust MPC (tube MPC, scenario MPC).

## Tools

DRAKE, MoveIt 2, OMPL, Pinocchio, Crocoddyl, ACADOS, CasADi, MuJoCo /
MJX, Isaac Lab, Brax.

## Must-read papers / books

Tedrake "Underactuated Robotics" (free book + edX), Tedrake "Robotic
Manipulation" (free book), LaValle "Planning Algorithms" (free book),
Hwangbo "Learning Agile and Dynamic Motor Skills", Margolis "Walk These
Ways", Di Carlo "Dynamic Locomotion in the MIT Cheetah 3".
