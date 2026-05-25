# Stack layer: Arm motion planning

> **Job:** plan collision-free arm trajectories for the pick (tray →
> grasp) and the place (grasp → slot), treating the shelf and already-
> placed neighbors as collision objects, and ending the place as a
> guarded/compliant set-down rather than a free-space drop. Knocking
> over a neighbor or clipping the shelf is a defined failure, so
> **collision checking** and a **clean ROS 2 integration** matter most.

## Comparison

| Framework | ROS 2 integration | Algorithm breadth (sampling / opt) | Collision checking | Speed (GPU?) | Trajectory optimization | Maturity / community | Bottom line |
|-----------|-------------------|------------------------------------|--------------------|--------------|-------------------------|----------------------|-------------|
| **MoveIt 2** | First-class (the standard) | Broad via OMPL + others | FCL / Bullet, scene-aware | CPU (seconds) | CHOMP/STOMP/Pilz plugins | Very high | The complete, ROS-native default; planning can be slow but it does everything this needs |
| **cuRobo** (NVIDIA cuMotion) | Yes (Isaac ROS / MoveIt plugin) | GPU collision-free trajopt | GPU, very fast | **GPU, ~milliseconds** | Core strength | Growing, NVIDIA-backed | Drop-in *accelerator* when planning latency dominates cycle time |
| **Drake** | Partial (not ROS-first) | Strong optimization + dynamics | Yes (excellent) | CPU | Best-in-class trajopt | High (research/control) | Superb for rigorous trajopt/control; heavier to wire into a ROS 2 app |
| **OMPL** (standalone) | Via MoveIt (it wraps OMPL) | Huge sampling-planner library | You supply it | CPU | No (planners only) | High | The planner core, not an application — use through MoveIt, not raw |
| **Tesseract** | Yes (ROS) | Sampling + trajopt (TrajOpt) | Continuous collision | CPU | Strong (TrajOpt) | Moderate (industrial) | Good for industrial cartesian/process paths; smaller community than MoveIt |
| **Pinocchio + custom** | DIY | Whatever you build | DIY (hpp-fcl) | CPU/fast kinematics | DIY | High (as a library) | Fast rigid-body math, but you assemble the whole planner yourself |

## Top choice

**MoveIt 2, with cuRobo as the acceleration path.**

MoveIt 2 is the only option that is ROS 2 native, ships scene-aware
collision checking (shelf + neighbors as collision objects), and offers
the full planner/IK/execution pipeline the pick-and-place loop needs out
of the box — including the cartesian approach/retreat moves a guarded
set-down requires. Start there. If per-unit cycle time later becomes
dominated by planning latency, add **cuRobo / cuMotion** as a MoveIt
planning plugin for millisecond GPU planning without leaving the
ecosystem. Use **Drake** only if you need rigorous contact-aware
trajectory optimization; reach for **OMPL** only *through* MoveIt.
