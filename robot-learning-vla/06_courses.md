# Courses for Robot Learning & Foundation Models (VLA)

A curated list of online courses that map directly to the skills you
need to ship a VLA project. Listed roughly in the order a junior web
developer should take them. All links go to the official course page;
many of them are free to audit or have free YouTube uploads.

A note on choosing: VLA work demands three skill stacks — (1) deep
learning fundamentals, (2) reinforcement and imitation learning, and
(3) robotics-specific topics. The list below covers all three. Pick at
least one from each stack.

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
  textbook). Knowing RL adds **+33% to robotics salary** per the
  2025 Robotics Salary Guide; this specialization is the lowest-
  friction way to put "RL" credibly on your resume.

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
