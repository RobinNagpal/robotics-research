# Learn: the stack, framework by framework

> Hands-on learning notes for the **recommended framework of each
> stack layer** in the shelf-stocking project. The deep-dive files in
> `../` (the `03-stack/` folder) explain *which* framework was chosen
> and *why*; the files here teach *how to actually use* that framework,
> written for someone who can program but has never touched robotics —
> a junior web developer, say. New to a term? Every layer also points
> at the plain-language `../../02-glossary.md`.

Each document follows the same five-part shape:

1. **Introduction and basic concepts** — what the tool is and the
   problem it solves.
2. **Important concepts that are used most often** — the handful of
   ideas you meet on day one.
3. **Hello world example with code** — the smallest thing that runs.
4. **A bit advanced example with code** — one realistic step up.
5. **Explanation of place-on-shelf code** — that framework's slice of
   *this* project (the grocery shelf-stocking robot), walked through
   line by line.

Read them in order — later files assume you have met ROS 2 (the common
language the other tools talk through).

| # | Document | Layer | Framework taught |
|---|----------|-------|------------------|
| 01 | [`01-gazebo-harmonic.md`](01-gazebo-harmonic.md) | Simulator | **Gazebo (Harmonic)** |
| 02 | [`02-ros2.md`](02-ros2.md) | Middleware | **ROS 2** |
| 03 | [`03-nav2.md`](03-nav2.md) | Mobile-base navigation | **Nav2** (+ slam_toolbox / AMCL) |
| 04 | [`04-moveit2.md`](04-moveit2.md) | Arm motion planning | **MoveIt 2** |
| 05 | [`05-perception.md`](05-perception.md) | Perception | **Open3D** geometric + **FoundationPose** |
| 06 | [`06-grasping.md`](06-grasping.md) | Grasping | **Analytical antipodal** + **AnyGrasp** |
| 07 | [`07-behavior-trees.md`](07-behavior-trees.md) | Orchestration | **BehaviorTree.CPP** (+ Groot2) |

All seven share one consistent vocabulary so the code lines up across
files: the same ROS 2 action names (`navigate_to_shelf`, `pick_product`,
`locate_slot`, `place_product`, `verify_placement`), the same topics
(`/wrist_camera/depth/points`, `/scan`, `/cmd_vel`, …), the same `tf2`
frame chain (`map` → `odom` → `base_link` → … → `wrist_camera_link`,
`tool0`), and the same example product (`soup_can_400g`).
