# Courses for Robot Learning & Foundation Models (VLA)

A curated list of online courses that map directly to the skills
the team needs to deliver VLA client work. Listed roughly in the
order someone ramping from a web / generalist eng background should
take them. All links go to the official course page; many are free
to audit or have free YouTube uploads.

A note on choosing: VLA delivery demands five skill stacks — (0)
absolute basics for team members who are brand new, (1) deep
learning fundamentals, (2) reinforcement and imitation learning,
(3) robotics-specific topics, and (4) project-driven courses where
the team actually builds and ships internal reference systems. The
team picks at least one from each stack they don't already know.

---

## Stack 0: Foundational basics (skip if you already have a CS degree)

These are the prereqs every later course assumes. If you're a working
web dev, you already have the Python side; you may still want the
math refreshers.

### A. Python for Everybody Specialization — University of Michigan (Charles Severance) on Coursera

- **Link:** https://www.coursera.org/specializations/python
- **Length:** 5 courses, ~8 months at 3 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** The cleanest intro to Python for
  non-programmers. Every other course on this list assumes Python
  fluency. If you've never written a `for` loop, start here. If you
  have, skip it.

### B. Mathematics for Machine Learning Specialization — Imperial College London on Coursera

- **Link:** https://www.coursera.org/specializations/mathematics-machine-learning
- **Length:** 3 courses (Linear Algebra, Multivariate Calculus,
  PCA), ~4 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** The exact math you need for VLA
  papers: matrices, eigendecomposition, gradients, chain rule, KL
  divergence. Stops short of probability/optimization, but pairs
  perfectly with the next course. Taught at the level a working
  engineer can finish without a math degree.

### C. Essence of Linear Algebra + Essence of Calculus — 3Blue1Brown (YouTube)

- **Link:** https://www.3blue1brown.com/topics/linear-algebra and
  https://www.3blue1brown.com/topics/calculus
- **Length:** ~6 hours total.
- **Cost:** Free.
- **Why this is 100% relevant.** Visualization-first math
  refreshers. Eigenvectors and gradients stop being scary after
  these. Watch before any of the Coursera math content if you want
  intuition first, formulas later.

### D. Machine Learning Specialization — DeepLearning.AI + Stanford on Coursera

- **Link:** https://www.coursera.org/specializations/machine-learning-introduction
- **Length:** 3 courses, ~2 months at 9 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** The 2022 rebuild of Andrew Ng's
  legendary original ML course. Covers linear/logistic regression,
  neural nets, decision trees, and unsupervised learning — the
  vocabulary that every VLA paper assumes you have.

### E. CS50's Introduction to Artificial Intelligence with Python — Harvard on edX

- **Link:** https://www.edx.org/learn/artificial-intelligence/harvard-university-cs50-s-introduction-to-artificial-intelligence-with-python
- **Length:** 7 weeks at ~12 hrs/week.
- **Cost:** Free to audit; $200 for certificate.
- **Why this is 100% relevant.** Each week ends with a real Python
  project (minimax for tic-tac-toe, Bayesian network, neural net
  for traffic-sign recognition). Builds the "I can wire AI into a
  Python program" reflex you'll need before fine-tuning a VLA.

---

## Stack 1: Deep learning fundamentals (start here)

### 1. Deep Learning Specialization — DeepLearning.AI (Andrew Ng) on Coursera

- **Link:** https://www.coursera.org/specializations/deep-learning
- **Length:** ~3 months at 10 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Every VLA — RT-2, OpenVLA, pi0,
  Helix — is built on the deep learning building blocks taught here:
  backprop, CNNs, sequence models, optimization, regularization. You
  cannot read the OpenVLA paper without this material. Andrew Ng's
  course is the canonical entry point and the one most VLA engineers
  did first.

### 2. Practical Deep Learning for Coders — fast.ai

- **Link:** https://course.fast.ai
- **Length:** 7 lessons, ~50 hrs total.
- **Cost:** Free.
- **Why this is 100% relevant.** fast.ai's "code first, math later"
  approach is exactly how a web dev should ramp into PyTorch. You'll
  fine-tune real models in the first lesson, which is the same daily
  workflow as VLA fine-tuning. The course explicitly covers transfer
  learning and fine-tuning — the two operations you'll do 99% of the
  time with a pretrained VLA.

### 3. Neural Networks: Zero to Hero — Andrej Karpathy (YouTube)

- **Link:** https://karpathy.ai/zero-to-hero.html
- **Length:** 10 videos, ~25 hours.
- **Cost:** Free.
- **Why this is 100% relevant.** The "build nanoGPT from scratch"
  lecture is the fastest way to understand the transformer
  architecture that underlies every modern VLA (OpenVLA wraps a
  Llama 7B; pi0 wraps a PaliGemma). After this you can read VLA
  papers and know exactly which parts are "standard transformer"
  vs. "novel head." Karpathy's micrograd lecture also rebuilds
  autograd in 100 lines — invaluable mental model.

---

## Stack 2: Reinforcement learning and imitation learning

### 4. CS285: Deep Reinforcement Learning — UC Berkeley (Sergey Levine)

- **Link:** https://rail.eecs.berkeley.edu/deeprlcourse/ (lectures
  free on YouTube).
- **Length:** ~25 lectures, full semester.
- **Cost:** Free.
- **Why this is 100% relevant.** Sergey Levine is one of the most
  prolific researchers in VLA / robot learning. The course covers
  policy gradients, actor-critic, model-based RL, offline RL,
  imitation learning, and several robotics-specific lectures. This
  is the single most-referenced course by VLA engineers. CS285's
  homework also uses MuJoCo, which carries over to LeRobot work.

### 5. Reinforcement Learning Specialization — University of Alberta on Coursera

- **Link:** https://www.coursera.org/specializations/reinforcement-learning
- **Length:** 4 courses, ~4 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** A gentler on-ramp than CS285,
  taught by Adam White and Martha White (authors of *Reinforcement
  Learning: An Introduction* with Sutton and Barto — the canonical
  textbook). RL skills carry a **+33% premium** in the 2025
  Robotics Salary Guide, which tracks with the higher rates VLA
  client work commands; this specialization is the lowest-friction
  credible path for the team to learn RL fundamentals.

### 6. Hugging Face Deep RL Course

- **Link:** https://huggingface.co/learn/deep-rl-course
- **Length:** 8 units, ~30 hours.
- **Cost:** Free.
- **Why this is 100% relevant.** Free, hands-on, and uses the exact
  Hugging Face stack you'll use for VLA work. Covers PPO, SAC, DQN,
  and includes Unity ML-Agents integration. Hugging Face's LeRobot
  library — the one you'll fine-tune VLAs with — was built by the
  same team. The shared mental model makes onboarding to LeRobot
  trivial after this course.

---

## Stack 3: Robotics and embodied AI

### 7. Modern Robotics Specialization — Northwestern University (Kevin Lynch) on Coursera

- **Link:** https://www.coursera.org/specializations/modernrobotics
- **Length:** 6 courses, ~6 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Teaches the classical robotics
  layer underneath every VLA: forward / inverse kinematics, screw
  theory, trajectory planning, dynamics. When you fine-tune a VLA
  to output joint angles, *what* those joint angles mean and how
  they map to end-effector pose is exactly what this course teaches.
  Kevin Lynch's textbook is the de-facto undergrad robotics book.

### 8. CS231n: Deep Learning for Computer Vision — Stanford

- **Link:** http://cs231n.stanford.edu (lecture videos free on
  YouTube).
- **Length:** ~20 lectures.
- **Cost:** Free.
- **Why this is 100% relevant.** A VLA is a **V**ision-Language-
  Action model — the "V" is what you learn here. CNNs, vision
  transformers, attention, training-from-scratch vs. fine-tuning,
  visualization, generative models. Every VLA's image encoder
  (DINOv2, SigLIP, CLIP) is covered or directly extended in CS231n.

### 9. CS25: Transformers United — Stanford

- **Link:** https://web.stanford.edu/class/cs25/ (lectures on
  YouTube).
- **Length:** ~15 guest lectures per semester.
- **Cost:** Free.
- **Why this is 100% relevant.** The transformer is the core
  architecture of every modern VLA. CS25 brings in researchers from
  Anthropic, OpenAI, Google, and academic labs to talk about
  transformer variants, scaling, multimodality, and robotics
  applications. Several lectures are explicitly on VLAs and robot
  foundation models.

---

## Stack 4: Project-driven / hands-on courses (where you actually ship something)

The courses above teach the *what* and *why*. The courses below
push the team through building real systems end-to-end — the kind
of work that becomes an internal reference build, a credibility-
anchor demo for client pitches, or the scaffolding for a paid
engagement.

### 12. Hugging Face LeRobot Tutorials and Community Course

- **Link:** https://huggingface.co/docs/lerobot and https://github.com/huggingface/lerobot (notebooks)
- **Length:** Self-paced; ~3-4 weekends to work through.
- **Cost:** Free (you need a cloud GPU or a $100-200 SO-100 arm if
  you want the full real-robot experience).
- **Why this is 100% relevant.** This is *the* hands-on course for
  VLA work specifically. You'll record your own teleoperation data
  on an SO-100 arm (or load BridgeData/DROID), fine-tune Diffusion
  Policy / ACT / OpenVLA on it, and deploy. By the end the team has
  a real working policy, a Hugging Face model card, and a video.
  This exact artifact is the credibility-anchor demo we show in
  client pitches to prove the shop can deliver an end-to-end VLA
  fine-tune.

### 13. Hugging Face Agents Course

- **Link:** https://huggingface.co/learn/agents-course
- **Length:** ~6 weeks self-paced.
- **Cost:** Free.
- **Why this is 100% relevant.** Builds AI agents end-to-end with
  function calling, tool use, and multi-step reasoning — exactly
  the "high-level controller" pattern many production VLA stacks
  use (a VLM-based planner that calls a low-level VLA). Ships a
  capstone agent you can demo.

### 14. Full Stack Deep Learning (FSDL)

- **Link:** https://fullstackdeeplearning.com/course/
- **Length:** ~9 lectures + a multi-week capstone project.
- **Cost:** Free.
- **Why this is 100% relevant.** Taught by Pieter Abbeel's
  ex-students; the only course that covers *shipping* an ML model
  end-to-end — data labeling, training infra, deployment, monitoring,
  testing. The exact skills that turn a fine-tuned VLA into a
  client deliverable the shop can stand behind. The capstone
  project becomes another internal reference build.

### 15. Made With ML — Goku Mohandas

- **Link:** https://madewithml.com
- **Length:** ~30 lessons, self-paced.
- **Cost:** Free.
- **Why this is 100% relevant.** End-to-end MLOps course built
  around a single ongoing project. You'll write tests, set up CI,
  containerize, deploy, monitor — the production muscle the team
  needs to ship VLA work as a real customer deliverable rather
  than a research artifact. Pairs perfectly with the team's
  existing web / generalist eng background.

### 16. fast.ai Practical Deep Learning for Coders (Part 2: From Deep Learning Foundations to Stable Diffusion)

- **Link:** https://course.fast.ai/Lessons/part2.html
- **Length:** ~30 hours.
- **Cost:** Free.
- **Why this is 100% relevant.** Part 2 of the fast.ai sequence
  rebuilds Stable Diffusion from scratch — and **diffusion is the
  exact math that pi0 uses for action generation**. Building a
  diffusion sampler in this course gives you direct, hands-on
  understanding of how pi0 / Diffusion Policy / RDT-1B actually
  work under the hood.

### 17. Udacity Deep Reinforcement Learning Nanodegree

- **Link:** https://www.udacity.com/course/deep-reinforcement-learning-nanodegree--nd893
- **Length:** ~4 months.
- **Cost:** $399/month (often discounted).
- **Why this is 100% relevant.** Three full projects: train an
  agent to navigate a banana-collection environment (DQN), train
  a continuous-control robotic arm (DDPG), and train multi-agent
  tennis players (MADDPG). Reviewed projects + mentor feedback.
  The price is steep but the deliverables are demo-grade — usable
  as internal reference builds and as material for client-facing
  case studies.

### 18. NVIDIA DLI — "Getting Started with AI on Jetson Nano" / Jetson hands-on labs

- **Link:** https://www.nvidia.com/en-us/training/ (filter
  "Jetson").
- **Length:** ~8 hours.
- **Cost:** Free (some paid extensions).
- **Why this is 100% relevant.** Hands-on labs that take you from
  zero to running real-time inference on Jetson hardware — the
  exact edge GPU most production robots use. After fine-tuning a
  VLA on a cloud GPU, this is the course that teaches you to
  deploy it on the actual robot's onboard computer.

---

## Optional / supplementary

### 10. CS224R: Deep Reinforcement Learning — Stanford (Chelsea Finn)

- **Link:** https://cs224r.stanford.edu
- **Cost:** Free (recordings + slides).
- **Why this is relevant.** Chelsea Finn is one of the architects
  of modern imitation learning and robot foundation models (RT-1,
  RT-2 lineage). The course leans into meta-learning, imitation,
  and offline RL — the exact topics inside pi0 and OpenVLA.

### 11. NVIDIA Deep Learning Institute — "Building AI-Based Robotics Applications"

- **Link:** https://www.nvidia.com/en-us/training/
- **Cost:** Some free, some paid ($90 typical).
- **Why this is relevant.** NVIDIA's own training paths for Isaac
  Lab, Jetson deployment, and TensorRT inference. After fine-tuning
  a VLA you'll need to deploy it on a real robot's edge GPU; the
  DLI courses are the most direct path to that skill set.
