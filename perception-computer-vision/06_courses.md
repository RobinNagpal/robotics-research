# Courses for Perception & Computer Vision

A curated list of online courses that map directly to the skills you
need to ship a perception project. Listed roughly in the order a
junior web developer should take them. All links go to the official
course page; many are free to audit or have free YouTube uploads.

A note on choosing: perception work spans five skill stacks — (0)
absolute basics if you're brand new, (1) classical CV and multi-view
geometry, (2) deep learning for vision, (3) robotics-specific
perception (SLAM, 3D, sensor fusion), and (4) project-driven courses
where you build something you can show off. Pick at least one from
each stack you don't already know.

---

## Stack 0: Foundational basics (skip if you already have a CS degree)

These are the prereqs every later course assumes. If you're a working
web dev, you already have the Python side; you may still want the
math refreshers.

### A. Python for Everybody Specialization — University of Michigan (Charles Severance) on Coursera

- **Link:** https://www.coursera.org/specializations/python
- **Length:** 5 courses, ~8 months at 3 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Every CV course assumes Python
  fluency. Most also assume NumPy comfort, which the final course
  in this specialization (Capstone) builds. Skip if you already
  use Python daily.

### B. Mathematics for Machine Learning Specialization — Imperial College London on Coursera

- **Link:** https://www.coursera.org/specializations/mathematics-machine-learning
- **Length:** 3 courses (Linear Algebra, Multivariate Calculus,
  PCA), ~4 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Linear algebra (SVD, eigenvectors,
  projections) is the entire language of multi-view geometry and
  3D reconstruction. PCA shows up in feature matching. This
  specialization is the most direct math prep for CS231A.

### C. Essence of Linear Algebra — 3Blue1Brown (YouTube)

- **Link:** https://www.3blue1brown.com/topics/linear-algebra
- **Length:** ~3 hours.
- **Cost:** Free.
- **Why this is 100% relevant.** Visual intuition for matrices as
  transforms. Watching the "change of basis" video makes camera
  intrinsics / extrinsics click in 10 minutes instead of two days.

### D. Khan Academy — Linear Algebra + Multivariable Calculus

- **Link:** https://www.khanacademy.org/math/linear-algebra and
  https://www.khanacademy.org/math/multivariable-calculus
- **Length:** Self-paced; ~40 hours each.
- **Cost:** Free.
- **Why this is 100% relevant.** Drill-heavy refresher. If the
  Imperial College specialization assumes too much, Khan Academy
  fills the floor below it.

### E. CS50's Introduction to Programming with Python — Harvard on edX

- **Link:** https://www.edx.org/learn/python/harvard-university-cs50-s-introduction-to-programming-with-python
- **Length:** 10 weeks at ~10 hrs/week.
- **Cost:** Free to audit; $200 for certificate.
- **Why this is 100% relevant.** Every week ends with a coded
  project. CS50P builds the "I can wire library X into a Python
  program" reflex you'll need before stacking OpenCV / PyTorch /
  Open3D together in week 1 of any real perception project.

---

## Stack 1: Classical computer vision and multi-view geometry

### 1. First Principles of Computer Vision — Columbia University (Shree Nayar) on Coursera

- **Link:** https://www.coursera.org/specializations/firstprinciplesofcomputervision
- **Length:** 6-course specialization, ~6 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Shree Nayar (Columbia CV professor
  for ~30 years) covers the entire classical CV stack: camera optics,
  image formation, features, stereo, 3D reconstruction, color, and
  texture. Every modern perception engineer needs this foundation —
  it's the layer the neural nets sit on top of. Nayar's parallel
  free YouTube lectures (`firstprinciplesofcomputervision.com`) are
  the same material if you don't want the Coursera certificate.

### 2. CS231A: Computer Vision, From 3D Reconstruction to Recognition — Stanford

- **Link:** https://web.stanford.edu/class/cs231a/ (notes + slides
  free).
- **Length:** ~20 lectures, full semester.
- **Cost:** Free.
- **Why this is 100% relevant.** The most-recommended single course
  for robotics perception. Covers the pinhole camera model, epipolar
  geometry, triangulation, PnP, bundle adjustment, structure from
  motion — exactly the math that powers ORB-SLAM3, COLMAP, and every
  3D-from-photos pipeline you'll touch. If you're picking one course
  from this stack, pick this one.

### 3. Robotics: Perception — University of Pennsylvania (Kostas Daniilidis) on Coursera

- **Link:** https://www.coursera.org/learn/robotics-perception
- **Length:** ~4 weeks at 4 hrs/week (part of the UPenn Robotics
  Specialization).
- **Cost:** Free to audit.
- **Why this is 100% relevant.** Robotics-specific perception
  course, by one of the leading academic groups in the field
  (Daniilidis runs the GRASP lab). Covers projective geometry,
  vanishing points, calibration, SfM, and pose estimation in the
  robotics context — the exact framing perception engineers see
  on the job.

---

## Stack 2: Deep learning for vision

### 4. CS231n: Deep Learning for Computer Vision — Stanford

- **Link:** http://cs231n.stanford.edu (lecture videos free on
  YouTube).
- **Length:** ~20 lectures.
- **Cost:** Free.
- **Why this is 100% relevant.** *The* deep-CV course. Covers CNNs,
  vision transformers, detection, segmentation, generative models,
  and self-supervised representation learning. Every model on your
  must-know list (YOLO, DETR, Mask2Former, DINOv2, SAM) is either
  built on or directly discussed in CS231n.

### 5. Deep Learning Specialization (Course 4: Convolutional Neural Networks) — DeepLearning.AI on Coursera

- **Link:** https://www.coursera.org/specializations/deep-learning
- **Length:** Course 4 is ~4 weeks at 5 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Andrew Ng's CNN course inside the
  Deep Learning Specialization is the most beginner-friendly
  treatment of detection (YOLO), segmentation (U-Net), face
  recognition, and neural style transfer. Pairs well with CS231n if
  CS231n's pace feels too aggressive.

### 6. Hugging Face Computer Vision Course

- **Link:** https://huggingface.co/learn/computer-vision-course
- **Length:** ~10 units.
- **Cost:** Free.
- **Why this is 100% relevant.** Free, hands-on, uses the same
  Hugging Face APIs you'll use in production. Covers vision
  transformers, multimodal models (CLIP), SAM, DINOv2, and
  Depth-Anything — exactly the foundation models in modern
  robotics perception. The course's "load a pretrained model in
  3 lines" approach matches the daily workflow of perception
  engineers in 2025.

---

## Stack 3: Robotics-specific perception (SLAM, 3D, AV)

### 7. Self-Driving Cars Specialization — University of Toronto on Coursera

- **Link:** https://www.coursera.org/specializations/self-driving-cars
- **Length:** 4 courses, ~7 months at 7 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** "Visual Perception for Self-Driving
  Cars" (Course 3) is the most comprehensive online treatment of
  multi-sensor perception you can take. Covers depth estimation,
  feature matching, ego-motion, semantic segmentation for driving,
  and 3D object detection. The Waymo / Zoox / Tesla / Cruise
  perception job descriptions read like this course's syllabus.

### 8. Visual SLAM for Robotics — Cyrill Stachniss / University of Bonn (YouTube + photogrammetry course)

- **Link:** https://www.ipb.uni-bonn.de/teaching/ (lectures on
  Cyrill Stachniss's YouTube channel — search "Cyrill Stachniss
  SLAM").
- **Length:** Two playlists: "Mobile Sensing and Robotics 2" and
  "Photogrammetry I & II" — together ~60+ hours.
- **Cost:** Free.
- **Why this is 100% relevant.** Cyrill Stachniss is the most
  approachable lecturer in SLAM. His ~60 hours of free lectures
  cover photogrammetry, Kalman filtering, EKF / particle filter
  SLAM, graph SLAM, and bundle adjustment — all the math behind
  ORB-SLAM3 and the production SLAM stacks you'll encounter at
  Skydio / Boston Dynamics / Wayve.

### 9. NVIDIA Deep Learning Institute — Computer Vision Learning Paths

- **Link:** https://www.nvidia.com/en-us/training/
- **Cost:** Many free; paid courses ~$90.
- **Why this is 100% relevant.** NVIDIA's training paths cover
  CUDA-accelerated perception, TensorRT inference, DeepStream
  pipelines, and Jetson deployment — the deployment stack used by
  most production robotics teams. After CS231n and CS231A teach you
  the algorithms, NVIDIA DLI teaches you how to ship them at 30+
  Hz on edge hardware.

---

## Stack 4: Project-driven / hands-on courses (where you actually ship something)

The courses above teach you the *what* and *why* of perception. The
courses below push you through building real systems end-to-end —
the kind of artifacts that become portfolio pieces or paid projects.

### 10. PyImageSearch University — Adrian Rosebrock

- **Link:** https://pyimagesearch.com/pyimagesearch-university/
- **Length:** Self-paced library of 60+ courses; pick lessons by
  project.
- **Cost:** $497/year (often discounted; trials available).
- **Why this is 100% relevant.** PyImageSearch is the most
  project-driven CV resource on the internet. Every lesson ends
  with code you can drop into a service: license-plate readers,
  document scanners, face-recognition systems, OCR pipelines,
  YOLO trainings on your own data. If you learn by building,
  this is the highest-ROI paid course in CV.

### 11. LearnOpenCV Courses — OpenCV University (Satya Mallick)

- **Link:** https://opencv.org/university/
- **Length:** Course-by-course; 4-12 weeks each.
- **Cost:** $500-1500 depending on bundle (frequent sales).
- **Why this is 100% relevant.** Run by the OpenCV maintainers
  themselves. The "Computer Vision I: Introduction" and "Deep
  Learning with PyTorch" tracks both end in deployable projects.
  The instructors are the people who maintain the library you'll
  use every day. The OpenCV-backed certificate carries weight
  with hiring managers.

### 12. Udacity Self-Driving Car Engineer Nanodegree

- **Link:** https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
- **Length:** ~6 months.
- **Cost:** $399/month (often discounted).
- **Why this is 100% relevant.** The most project-driven program
  for AV perception specifically. Projects include lane detection,
  traffic-sign classifier, behavioral cloning, advanced lane
  finding, sensor fusion (Kalman filter), localization, path
  planning, and a system integration capstone on a real Lincoln
  MKZ via Carla. If your goal is Waymo / Cruise / Zoox, this is
  the most direct paid path.

### 13. Roboflow Notebooks and YouTube Series

- **Link:** https://github.com/roboflow/notebooks (notebooks),
  https://www.youtube.com/@Roboflow (videos)
- **Length:** Per-tutorial 30 min - 3 hours.
- **Cost:** Free.
- **Why this is 100% relevant.** Roboflow ships ready-to-run
  Colab notebooks for *every* major perception model (YOLO v8/v11,
  RT-DETR, SAM 2, Florence-2, PaliGemma). Each notebook is
  end-to-end: load your data, fine-tune, evaluate, export to
  ONNX. Pair with Roboflow Universe (free datasets) and you can
  ship a new detector / segmenter every weekend.

### 14. Zero to Mastery — PyTorch for Deep Learning

- **Link:** https://zerotomastery.io/courses/learn-pytorch/
- **Length:** ~30 hours.
- **Cost:** ZTM subscription (~$39/mo).
- **Why this is 100% relevant.** Daniel Bourke's PyTorch course is
  one of the most beginner-friendly project-driven options. The
  capstone is a custom image classifier (FoodVision), and the
  course covers transfer learning, deployment to Gradio / Hugging
  Face Spaces. Good fit if Coursera's auditing feels too passive.

### 15. Kaggle Learn — Computer Vision (free micro-courses + competitions)

- **Link:** https://www.kaggle.com/learn/computer-vision
- **Length:** ~6 hours micro-course; competitions extend
  indefinitely.
- **Cost:** Free.
- **Why this is 100% relevant.** The "course" is intentionally
  small; the real value is entering Kaggle's vision competitions
  (classification, segmentation, detection) and reading the winning
  notebooks. Top kaggler is a credible resume signal for CV roles
  at perception-heavy companies.

### 16. NVIDIA DLI — "Getting Started with DeepStream for Video Analytics"

- **Link:** https://www.nvidia.com/en-us/training/ (filter
  "DeepStream").
- **Length:** ~8 hours.
- **Cost:** Free.
- **Why this is 100% relevant.** Hands-on lab that builds an
  end-to-end real-time video analytics pipeline on Jetson — the
  exact deployment target for robotics perception. After CS231n
  teaches you the model, DeepStream teaches you to ship it at
  30+ fps.

---

## Optional / supplementary

### 10. Computer Vision Nanodegree — Udacity

- **Link:** https://www.udacity.com/course/computer-vision-nanodegree--nd891
- **Length:** ~3 months.
- **Cost:** $399/month (often discounted).
- **Why this is relevant.** Hand-holdy structured program with
  reviewed projects. The capstones (landmark detection, image
  captioning, facial-keypoint detection) are reasonable resume
  artifacts if you don't have an academic background to show.
  Worth the cost only if structured curriculum + mentor reviews
  matter to you.

### 11. LinkedIn Learning: "Building Computer Vision Applications with Python" — Eduardo Corpeño

- **Link:** https://www.linkedin.com/learning/building-computer-vision-applications-with-python
- **Length:** ~3 hours.
- **Cost:** LinkedIn Learning subscription (~$30/mo; often free via
  employer or library card).
- **Why this is relevant.** Short, OpenCV-heavy hands-on intro.
  Useful for filling in OpenCV gaps if you came from a pure-ML
  background and never used it.
