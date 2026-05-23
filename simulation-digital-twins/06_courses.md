# Courses for Simulation & Digital Twins

A curated list of online courses that map directly to the skills you
need to ship a simulation or digital-twin project. Listed roughly in
the order a junior web developer should take them. All links go to
the official course page; many are free to audit or have free YouTube
uploads.

A note on choosing: sim / digital-twin work spans three skill stacks
— (1) reinforcement learning (to train policies inside the sim), (2)
robotics fundamentals (kinematics, dynamics, ROS), and (3) the
NVIDIA Isaac / Omniverse stack specifically. At least one course from
each stack is recommended.

---

## Stack 1: Reinforcement learning (the main payload that lives inside sim)

### 1. Reinforcement Learning Specialization — University of Alberta on Coursera

- **Link:** https://www.coursera.org/specializations/reinforcement-learning
- **Length:** 4 courses, ~4 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Taught by Adam White and Martha
  White (co-authors with Sutton and Barto of *Reinforcement
  Learning: An Introduction*, the canonical RL textbook). Covers
  the algorithmic foundations — value iteration, policy gradients,
  function approximation, actor-critic — that you'll use to train
  policies inside Isaac Lab and MuJoCo. RL adds **+33% to robotics
  salary** per the 2025 Robotics Salary Guide.

### 2. CS285: Deep Reinforcement Learning — UC Berkeley (Sergey Levine)

- **Link:** https://rail.eecs.berkeley.edu/deeprlcourse/ (lecture
  videos free on YouTube).
- **Length:** ~25 lectures, full semester.
- **Cost:** Free.
- **Why this is 100% relevant.** The single most-referenced graduate
  RL course. Homework problems use MuJoCo — directly transferable to
  the simulators you'll be paid to work in. Levine's group at
  Berkeley produces a huge share of sim-to-real and robot-learning
  research (foundation of RT-X, OpenVLA), so the course material
  maps onto current industry practice precisely.

### 3. Hugging Face Deep RL Course

- **Link:** https://huggingface.co/learn/deep-rl-course
- **Length:** 8 units, ~30 hours.
- **Cost:** Free.
- **Why this is 100% relevant.** Free, hands-on, ships with
  Stable-Baselines3 + Unity ML-Agents integration. Covers PPO, SAC,
  DQN, multi-agent RL — PPO in particular is the workhorse of every
  Isaac Lab training run. Faster onramp than CS285 and a good
  prerequisite for it.

---

## Stack 2: Robotics fundamentals (so the sim isn't a black box)

### 4. Modern Robotics Specialization — Northwestern University (Kevin Lynch) on Coursera

- **Link:** https://www.coursera.org/specializations/modernrobotics
- **Length:** 6 courses, ~6 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Teaches the math under every
  simulated robot: rigid-body motion (SE(3), SO(3), screw theory),
  forward / inverse kinematics, dynamics, trajectory planning,
  motion planning, robot control. When your sim's robot doesn't
  move the way you expect, this is the knowledge base you debug
  with. Lynch's textbook is the standard undergraduate robotics
  reference.

### 5. Underactuated Robotics — MIT (Russ Tedrake) on edX / OCW

- **Link:** http://underactuated.mit.edu (free textbook + lectures
  on YouTube; offered periodically on edX as MIT 6.832x).
- **Length:** Full semester, ~24 lectures.
- **Cost:** Free.
- **Why this is 100% relevant.** Russ Tedrake leads Toyota Research
  Institute and built **Drake**, the simulator. His course covers
  contact dynamics, trajectory optimization, model-predictive
  control, and the differentiable-physics ideas that underlie MJX,
  Brax, and Genesis. If you want to work on the model-based /
  research side of simulation, this is essential.

### 6. Robotics Specialization — University of Pennsylvania on Coursera

- **Link:** https://www.coursera.org/specializations/robotics
- **Length:** 6 courses (Aerial Robotics, Mobility, Perception,
  Estimation, Computational Motion Planning, Capstone), ~7 months.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Penn's GRASP lab is one of the
  most respected robotics groups in the world. The Aerial Robotics
  course covers quadrotor dynamics and control (everything you'll
  put inside a drone simulator), and the Estimation course covers
  Kalman filtering and sensor fusion — fundamentals for sim-to-real
  state estimation.

---

## Stack 3: NVIDIA Isaac, Omniverse, and USD

### 7. NVIDIA Deep Learning Institute (DLI) — Isaac and Omniverse Learning Paths

- **Link:** https://www.nvidia.com/en-us/training/ (filter for
  "Robotics" / "Omniverse").
- **Length:** Per-course typically 4-8 hours; learning paths span
  several courses.
- **Cost:** Many free; paid courses ~$90 each.
- **Why this is 100% relevant.** NVIDIA's official training for
  the exact stack the industry pays for: Isaac Sim, Isaac Lab,
  Omniverse Kit, Replicator (synthetic data), and the new Cosmos
  world-foundation-models. As of 2025 NVIDIA has aggressive Isaac /
  Omniverse hiring; DLI certificates on your resume are a directly
  recognized signal to NVIDIA recruiters.

### 8. Pixar's OpenUSD Tutorials / NVIDIA "Learn OpenUSD" Path

- **Link:** https://openusd.org/release/tut_usd_tutorials.html and
  https://learn.nvidia.com/courses/course?course_id=course-v1:DLI+S-OV-15+V1
  (free NVIDIA "Learn OpenUSD" course).
- **Length:** A few hours for the basics; weeks for proficiency.
- **Cost:** Free.
- **Why this is 100% relevant.** USD (Universal Scene Description)
  is the file format every Isaac Sim asset and digital twin uses.
  It is non-optional knowledge for sim work in 2025-2026. Pixar's
  tutorials are the authoritative reference; NVIDIA's free "Learn
  OpenUSD" path is the most direct industrial onramp.

### 9. The Construct — ROS2 Basics / ROS Industrial Courses

- **Link:** https://app.theconstruct.ai (also see ROS Industrial
  training and Open Robotics' free tutorials at https://docs.ros.org).
- **Length:** ROS2 Basics in 5 Days (~25 hours).
- **Cost:** Free for basics; $20-30/mo for full library.
- **Why this is 100% relevant.** Most real-world digital twins
  integrate with **ROS2** via Gazebo or `isaac_ros`. The Construct
  is the most popular hands-on ROS2 / Gazebo training platform,
  with browser-based simulators you don't need to install. Customers
  buying digital twins will expect ROS2-fluent integration.

---

## Optional / supplementary

### 10. Self-Driving Cars Specialization — University of Toronto on Coursera

- **Link:** https://www.coursera.org/specializations/self-driving-cars
- **Length:** 4 courses, ~7 months at 7 hrs/week.
- **Cost:** Free to audit.
- **Why this is relevant.** The "Introduction to Self-Driving Cars"
  course uses **CARLA** simulator extensively — directly transferable
  if your sim work targets the AV market (Applied Intuition,
  Foretellix, Parallel Domain). Covers vehicle dynamics, sensor
  fusion, and the AV stack that lives on top of the sim.

### 11. CS287: Advanced Robotics — UC Berkeley (Pieter Abbeel)

- **Link:** http://www.cs.berkeley.edu/~pabbeel/cs287/ (lectures on
  YouTube).
- **Length:** Full semester.
- **Cost:** Free.
- **Why this is relevant.** Pieter Abbeel co-founded Covariant
  (acquired by Amazon 2024); his course covers MDPs, control,
  optimization, and sim-to-real. A natural successor to CS285 if
  you want to go deep on the research side.

### 12. Udacity Robotics Software Engineer Nanodegree

- **Link:** https://www.udacity.com/course/robotics-software-engineer--nd209
- **Length:** ~4 months.
- **Cost:** $399/month.
- **Why this is relevant.** Project-heavy curriculum centered on
  **Gazebo** and ROS — useful if you'd rather learn ROS2 + sim in a
  structured, reviewed format. Pricier than the free alternatives
  but the project portfolio at the end is hireable.
