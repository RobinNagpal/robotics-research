# Courses for Perception & Computer Vision

A curated list of online courses that map to the skills needed to ship a perception project. Listed roughly in the order a junior web developer should take them. All links go to the official course page; many are free to audit or have free YouTube uploads.

Perception work spans six skill stacks: (0) absolute basics if you're brand new, (1) classical CV and multi-view geometry, (2) deep learning for vision, (3) robotics-specific perception (SLAM, 3D, sensor fusion), (4) project-driven courses where the team builds shippable artifacts, and (5) reference books. Pick at least one from each stack you don't already know.

A note on auditing vs. building: treat every course as a scaffold. If you don't have a small repo (even a few notebooks) per course on your GitHub by the end, you didn't really take the course. Watching ten hours of tutorial videos won't build the muscle — only typing along while pausing every two minutes will.

---

## Fast track for the shelf-stocking project

Building `05-projects/01-place-items-on-shelf` (a mobile base + arm that stocks a grocery shelf)? These are the courses from the full list below that map most directly to that project's **perception** half. Take them in this order, then return for the rest.

1. **ROS2 in 5 Days - The Construct** (Stack 3, #9b). The middleware everything else plugs into; the perception sub-track (camera drivers, point-cloud nodes, tf2) is exactly the glue between your CV model and the robot.
2. **Robotics: Perception - UPenn** (Stack 1, #3). Camera model, calibration, and PnP/pose estimation in robotics framing (body/world frames) — the foundation for localizing the product and the shelf slot.
3. **CS231A - Stanford** (Stack 1, #2). The geometry under 6-DoF pose: pinhole model, triangulation, PnP. This is what makes FoundationPose-style product-pose estimation intelligible rather than magic.
4. **Visual SLAM for Robotics - Stachniss** (Stack 3, #8). Mapping and localization for the mobile-base half (what Nav2 does under the hood) — how the robot knows where it is relative to the shelf.
5. **CS231n + Roboflow Notebooks** (Stack 2, #4 and Stack 4, #13). Detection/segmentation and hands-on fine-tuning for shelf-slot and product detection (SAM 2, YOLO-World, Grounding DINO) once you relax the "known tray layout" assumption.
6. **NVIDIA DLI CV learning paths** (Stack 3, #9). RGB-D pipelines and ONNX/TensorRT deployment for running perception on the robot's onboard compute at frame rate.

Book to keep on the desk: **Peter Corke, *Robotics, Vision and Control*** (Stack 5) — the one reference that covers manipulator kinematics *and* vision together, which is precisely the arm-plus-camera combination this project needs.

**What this perception list deliberately does not cover.** The shelf robot also needs **arm motion planning (MoveIt 2)**, **grasp synthesis (AnyGrasp / Contact-GraspNet, Dex-Net)**, and the **simulators (Isaac Sim / Isaac Lab, Gazebo, MuJoCo)** described in `05-projects/01-place-items-on-shelf/02-high-level-tech.md`. Those are manipulation and simulation skills, not perception — find their learning resources in the manipulation area (`../05-manipulation/02-learn.md`) rather than duplicated here.

---

## Stack 0 - Foundational basics

Prereqs every later course assumes. If you're a working web dev, you already have the Python side; you may still want the math refreshers.

### A. Python for Everybody Specialization - University of Michigan (Charles Severance) on Coursera

- **Link:** https://www.coursera.org/specializations/python
- **Length:** 5 courses, ~8 months at 3 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why relevant.** Every CV course assumes Python fluency and NumPy comfort, which the Capstone builds. Skip if you already use Python daily.

### B. Mathematics for Machine Learning Specialization - Imperial College London on Coursera

- **Link:** https://www.coursera.org/specializations/mathematics-machine-learning
- **Length:** 3 courses (Linear Algebra, Multivariate Calculus, PCA), ~4 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why relevant.** Linear algebra (SVD, eigenvectors, projections) is the language of multi-view geometry and 3D reconstruction. The most direct math prep for CS231A. The team learns to derive the 8-point algorithm and explain why SVD recovers rotation, because every multi-view client project hinges on those two operations.

### C. Essence of Linear Algebra - 3Blue1Brown (YouTube)

- **Link:** https://www.3blue1brown.com/topics/linear-algebra
- **Length:** ~3 hours.
- **Cost:** Free.
- **Why relevant.** Visual intuition for matrices as transforms. The change-of-basis video makes camera intrinsics and extrinsics click in 10 minutes instead of two days. Geometric grounding for what a 4x4 transform does to a point cloud.

### D. Khan Academy - Linear Algebra + Multivariable Calculus

- **Link:** https://www.khanacademy.org/math/linear-algebra and https://www.khanacademy.org/math/multivariable-calculus
- **Length:** Self-paced; ~40 hours each.
- **Cost:** Free.
- **Why relevant.** Drill-heavy refresher. If the Imperial College specialization assumes too much, Khan Academy fills the floor below it. Mechanical fluency in dot products, matrix-vector multiplies, partial derivatives, and chain rule — the arithmetic you'll need to debug a Jacobian by hand when your optimizer diverges.

### E. CS50's Introduction to Programming with Python - Harvard on edX

- **Link:** https://www.edx.org/learn/python/harvard-university-cs50-s-introduction-to-programming-with-python
- **Length:** 10 weeks at ~10 hrs/week.
- **Cost:** Free to audit; $200 for certificate.
- **Why relevant.** Every week ends with a coded project. Builds the "wire library X into a Python program" reflex you'll need before stacking OpenCV, PyTorch, and Open3D together. Real perception scripts always import five libraries that weren't written to talk to each other.

---

## Stack 1 - Classical computer vision and multi-view geometry

### 1. First Principles of Computer Vision - Columbia University (Shree Nayar) on Coursera

- **Link:** https://www.coursera.org/specializations/firstprinciplesofcomputervision
- **Length:** 6-course specialization, ~6 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why relevant.** Nayar (Columbia CV professor for ~30 years) covers the entire classical CV stack: camera optics, image formation, features, stereo, 3D reconstruction, color, texture. The foundation neural nets sit on top of. Parallel free YouTube lectures at firstprinciplesofcomputervision.com are the same material without the certificate. After ~3 modules you'll have a camera-calibration script (checkerboard in, intrinsics out) in GitHub.

### 2. CS231A: Computer Vision, From 3D Reconstruction to Recognition - Stanford

- **Link:** https://web.stanford.edu/class/cs231a/ (notes + slides free).
- **Length:** ~20 lectures, full semester.
- **Cost:** Free.
- **Why relevant.** The most-recommended single course for robotics perception. Covers the pinhole camera model, epipolar geometry, triangulation, PnP, bundle adjustment, structure from motion — the math powering ORB-SLAM3, COLMAP, and every 3D-from-photos pipeline. The bundle-adjustment problem set is exactly the kind of Python wrapper the team writes around client camera rigs. If you pick one course from this stack, pick this one. Assignment 2 produces a two-view structure-from-motion notebook the team can adapt into a client demo.

### 3. Robotics: Perception - University of Pennsylvania (Kostas Daniilidis) on Coursera

- **Link:** https://www.coursera.org/learn/robotics-perception
- **Length:** ~4 weeks at 4 hrs/week (part of the UPenn Robotics Specialization).
- **Cost:** Free to audit.
- **Why relevant.** Robotics-specific framing from Daniilidis's GRASP lab. Projective geometry, vanishing points, calibration, SfM, and pose estimation in the robotics context — with the naming conventions (body frame, world frame, ego motion) academic CV courses skip. Produces a working monocular visual-odometry notebook by week 3.

### 3b. CS280: Computer Vision - UC Berkeley (Jitendra Malik, Alyosha Efros, and rotating co-instructors)

- **Link:** Search "Berkeley CS280" on the EECS course site (slides are linked from the current instructor's home page).
- **Length:** Full semester; ~24 lectures.
- **Cost:** Free.
- **Why relevant.** Berkeley's flagship grad CV course — Malik (perceptual grouping, segmentation) and Efros (texture synthesis, image-to-image translation). Skews toward the history and philosophy of vision, which makes it the better course if the team wants to evaluate research-flavored client briefs. After Malik's lectures the team instinctively knows whether a "novel" arXiv paper is a 2003 idea with a transformer attached.

### 3c. 16-385: Computer Vision - Carnegie Mellon University

- **Link:** Search "CMU 16-385" — Kris Kitani's and Ioannis Gkioulekas's offerings have full slides + assignments online.
- **Length:** Full semester; ~26 lectures.
- **Cost:** Free.
- **Why relevant.** Undergraduate-level CMU CV course. Heavy on classical assignments (Lucas-Kanade tracking, Harris corners, panorama stitching, structured light) and a gentler pace than CS231A. 16-720 is the grad version if you want more depth. Produces a panorama stitcher (5 phone photos in, 1 stitched image out) by ~week 4.

### 3d. EECS 442 / 504: Computer Vision - University of Michigan (David Fouhey, and others)

- **Link:** Search "UMich EECS 442" or "EECS 504" — Fouhey's course pages are usually the top hit.
- **Length:** Full semester; ~28 lectures.
- **Cost:** Free.
- **Why relevant.** Famously clear lectures. EECS 442 is undergrad-friendly, EECS 504 the grad follow-on. Together they cover roughly CS231A + CS231n with more practical, less theoretical assignments. Fouhey's homeworks force you to debug your own implementation — the same muscle the team uses when a model fine-tune plateaus on a customer's data.

### 3e. 3D Vision - ETH Zurich (Marc Pollefeys)

- **Link:** Search "ETH 3D Vision Pollefeys" — slides and recordings on the CVG group's site.
- **Length:** Full semester; ~14 lectures plus project.
- **Cost:** Free.
- **Why relevant.** Pollefeys leads the Microsoft HoloLens spatial-mapping group on top of his ETH professorship; this is the graduate-level treatment of SfM, multi-view stereo, and dense reconstruction. Highly relevant for AR / XR / spatial-mapping client work. Produces a multi-view stereo reconstruction from 20 phone photos — excellent demo material for prospective customers.

---

## Stack 2 - Deep learning for vision

### 4. CS231n: Deep Learning for Computer Vision - Stanford

- **Link:** http://cs231n.stanford.edu (lecture videos free on YouTube).
- **Length:** ~20 lectures.
- **Cost:** Free.
- **Why relevant.** The deep-CV course. CNNs, vision transformers, detection, segmentation, generative models, and self-supervised representation learning. Every model on your must-know list (YOLO, DETR, Mask2Former, DINOv2, SAM) is built on or directly discussed here. Hand-deriving backprop through a conv layer (assignment 2) is the single best way to internalize what the optimizer is actually doing. The assignments are the course; skipping them is reading the React docs on the toilet.

### 5. Deep Learning Specialization (Course 4: Convolutional Neural Networks) - DeepLearning.AI on Coursera

- **Link:** https://www.coursera.org/specializations/deep-learning
- **Length:** Course 4 is ~4 weeks at 5 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why relevant.** The most beginner-friendly treatment of detection (YOLO), segmentation (U-Net), face recognition, and neural style transfer. Pairs well with CS231n if CS231n's pace feels too aggressive. Builds the mental model of detection vs. segmentation vs. classification — the three task framings every client conversation snaps into. Ends with a YOLO fine-tune on a ~200-image custom dataset.

### 6. Hugging Face Computer Vision Course

- **Link:** https://huggingface.co/learn/computer-vision-course
- **Length:** ~10 units.
- **Cost:** Free.
- **Why relevant.** Hands-on, uses the same Hugging Face APIs you'll use in production. Covers vision transformers, multimodal models (CLIP), and the foundation-model toolkit in modern robotics perception. The "load a pretrained model in 3 lines" approach matches the daily workflow. Produces a semantic image search demo (text query in, top-k images out) using CLIP by the end of unit 4.

### 6b. Hugging Face Diffusion Models Class

- **Link:** https://huggingface.co/learn/diffusion-course
- **Length:** ~4 units, self-paced (~20 hours total).
- **Cost:** Free.
- **Why relevant.** Diffusion has crept into perception, not just art generation — depth diffusion (Marigold), monocular reconstruction (Wonder3D), and novel-view synthesis all build on the denoising framework. Useful for recognizing when a paper is genuinely novel vs. "diffusion applied to task X."

### 6c. fast.ai - Practical Deep Learning for Coders (Part 1) - Jeremy Howard

- **Link:** https://course.fast.ai
- **Length:** 9 lessons, ~60 hours of work.
- **Cost:** Free.
- **Why relevant.** Top-down pedagogy: ship a working image classifier in lesson 1, then peel back the layers. The opposite philosophy of CS231n and the better fit for working developers who want results before theory. Drills the pragmatic instincts that work in real perception teams: pick a baseline, train, look at the data, iterate. Lesson 2 ends with a custom image classifier deployed to Hugging Face Spaces.

---

## Stack 3 - Robotics-specific perception (SLAM, 3D, AV)

### 7. Self-Driving Cars Specialization - University of Toronto on Coursera

- **Link:** https://www.coursera.org/specializations/self-driving-cars
- **Length:** 4 courses, ~7 months at 7 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why relevant.** "Visual Perception for Self-Driving Cars" (Course 3) is the most comprehensive online treatment of multi-sensor perception. Depth estimation, feature matching, ego-motion, semantic segmentation for driving, 3D object detection. Covers the full sensor stack the team encounters when AV-adjacent clients (fleet operators, yard automation, mining) come in. Builds multi-sensor reasoning: when to trust camera vs. lidar vs. radar, how to fuse them, how latency compounds. Course 3 ends with a lane-detection + vehicle-detection pipeline on a KITTI sequence.

### 8. Visual SLAM for Robotics - Cyrill Stachniss / University of Bonn (YouTube + photogrammetry course)

- **Link:** https://www.ipb.uni-bonn.de/teaching/ (lectures on Cyrill Stachniss's YouTube channel — search "Cyrill Stachniss SLAM").
- **Length:** Two playlists: "Mobile Sensing and Robotics 2" and "Photogrammetry I & II" — ~60+ hours.
- **Cost:** Free.
- **Why relevant.** Stachniss is the most approachable lecturer in SLAM. Covers Kalman filtering, EKF / particle filter SLAM, graph SLAM, and bundle adjustment — the math behind ORB-SLAM3 and the production-grade SLAM stacks the team integrates for client projects. Once you can hand-derive the EKF update, the giant Eigen expressions in any C++ SLAM library stop looking like noise. Produces a 2D EKF-SLAM notebook by ~lecture 12 and an ORB-SLAM3 demo on phone video by month 3.

### 8b. Photogrammetry I & II - Cyrill Stachniss (separate from the SLAM playlist)

- **Link:** YouTube "Cyrill Stachniss Photogrammetry" — two full playlists.
- **Length:** ~50 hours combined.
- **Cost:** Free.
- **Why relevant.** Where the SLAM lectures assume image formation and camera models, the Photogrammetry lectures teach them — pinhole geometry, homogeneous coordinates, distortion models, calibration, bundle adjustment from first principles. Watch these before the SLAM ones if you're new to multi-view. Maps directly to debugging COLMAP failures.

### 9. NVIDIA Deep Learning Institute - Computer Vision Learning Paths

- **Link:** https://www.nvidia.com/en-us/training/
- **Cost:** Many free; paid courses ~$90.
- **Why relevant.** CUDA-accelerated perception, TensorRT inference, DeepStream pipelines, and Jetson deployment — the production stack the team ships on for most edge-deployed client work. After CS231n and CS231A teach the algorithms, NVIDIA DLI teaches the team to ship them at 30+ Hz on edge hardware. Turning a research-grade PyTorch model into an ONNX + TensorRT engine is the single biggest delivery bottleneck the team needs to remove.

### 9b. ROS2 in 5 Days - The Construct (perception sub-track)

- **Link:** https://www.theconstruct.ai/robotigniteacademy_learnros/ros-courses-library/
- **Length:** ~5 days of paced lessons; doable in 2-3 weekends.
- **Cost:** Free trial; subscription thereafter.
- **Why relevant.** ROS2 is the lingua franca of robotics middleware. The perception sub-track covers camera drivers, image_transport, point-cloud processing nodes, tf2 transforms, and OpenCV integration — the glue code that turns a CV model into a node a robot can use. Produces a ROS2 node that subscribes to a camera topic, runs a detector, and publishes bounding boxes.

---

## Stack 4 - Project-driven / hands-on courses

The courses above teach the what and why of perception. These push the team through building real systems end-to-end — the kind of shippable artifacts that become client deliverables or internal reference builds.

### 10. PyImageSearch University - Adrian Rosebrock

- **Link:** https://pyimagesearch.com/pyimagesearch-university/
- **Length:** Self-paced library of 60+ courses; pick lessons by project.
- **Cost:** $497/year (often discounted; trials available).
- **Why relevant.** The most project-driven CV resource on the internet. Every lesson ends with code the team can drop into a client service: license-plate readers, document scanners, face-recognition systems, OCR pipelines, custom-data detector trainings. If the team learns by building, the highest-ROI paid course in CV. Within 30 days the team has a working OCR app, a face-recognition door cam, and a custom detector — all three adaptable for client demos.

### 11. LearnOpenCV Courses - OpenCV University (Satya Mallick)

- **Link:** https://opencv.org/university/
- **Length:** Course-by-course; 4-12 weeks each.
- **Cost:** $500-1500 depending on bundle (frequent sales).
- **Why relevant.** Run by the OpenCV maintainers themselves. "Computer Vision I: Introduction" and "Deep Learning with PyTorch" tracks both end in deployable projects. The instructors maintain the library the team uses every day. The OpenCV API is huge and inconsistent; this is the closest thing to a guided tour.

### 12. Udacity Self-Driving Car Engineer Nanodegree

- **Link:** https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
- **Length:** ~6 months.
- **Cost:** $399/month (often discounted).
- **Why relevant.** The most project-driven program for AV perception specifically. Projects: lane detection, traffic-sign classifier, behavioral cloning, advanced lane finding, sensor fusion (Kalman filter), localization, path planning, and a system-integration capstone on a real Lincoln MKZ via Carla. If the team plans to take on AV-adjacent client work, the most direct paid path. Reviewers grade the code; the projects become adaptable internal reference builds the team can show prospective customers.

### 13. Roboflow Notebooks and YouTube Series

- **Link:** https://github.com/roboflow/notebooks (notebooks), https://www.youtube.com/@Roboflow (videos)
- **Length:** Per-tutorial 30 min - 3 hours.
- **Cost:** Free.
- **Why relevant.** Ready-to-run Colab notebooks for every major perception model (YOLO v8/v11, RT-DETR, SAM 2, Florence-2, PaliGemma). Each is end-to-end: load data, fine-tune, evaluate, export to ONNX. Pair with Roboflow Universe (free datasets) and the team can ship a new detector or segmenter every weekend. The difference between a teammate who needs three days to fine-tune a model on a client dataset and one who does it in three hours is usually just Roboflow notebook familiarity.

### 14. Zero to Mastery - PyTorch for Deep Learning

- **Link:** https://zerotomastery.io/courses/learn-pytorch/
- **Length:** ~30 hours.
- **Cost:** ZTM subscription (~$39/mo).
- **Why relevant.** Daniel Bourke's PyTorch course is one of the most beginner-friendly project-driven options. Capstone is a custom image classifier (FoodVision); covers transfer learning and deployment to Gradio / Hugging Face Spaces. Builds PyTorch fluency at the level you can write a custom Dataset, DataLoader, training loop, and eval script from a blank file.

### 15. Kaggle Learn - Computer Vision (free micro-courses + competitions)

- **Link:** https://www.kaggle.com/learn/computer-vision
- **Length:** ~6 hours micro-course; competitions extend indefinitely.
- **Cost:** Free.
- **Why relevant.** The course is intentionally small; the real value is entering Kaggle's vision competitions (classification, segmentation, detection) and reading the winning notebooks. Builds the muscle of reading and ruthlessly adapting other people's high-performance code — the actual daily activity for the team when a client dataset lands. A few Expert-tier finishes give the team concrete proof points to cite in pitches.

### 16. NVIDIA DLI - "Getting Started with DeepStream for Video Analytics"

- **Link:** https://www.nvidia.com/en-us/training/ (filter "DeepStream").
- **Length:** ~8 hours.
- **Cost:** Free.
- **Why relevant.** Hands-on lab that builds an end-to-end real-time video analytics pipeline on Jetson — the exact deployment target for robotics perception. Builds stream-graph thinking: arranging GStreamer-style elements (source -> decode -> infer -> overlay -> sink) into a working pipeline. Ends with real-time person detection on a webcam.

---

## Optional / supplementary

### Computer Vision Nanodegree - Udacity

- **Link:** https://www.udacity.com/course/computer-vision-nanodegree--nd891
- **Length:** ~3 months.
- **Cost:** $399/month (often discounted).
- **Why relevant.** Structured program with reviewed projects. Capstones (landmark detection, image captioning, facial-keypoint detection) are reasonable internal reference builds the team can adapt for client demos. Worth the cost only if structured curriculum and mentor reviews matter to the team.

### LinkedIn Learning: "Building Computer Vision Applications with Python" - Eduardo Corpeño

- **Link:** https://www.linkedin.com/learning/building-computer-vision-applications-with-python
- **Length:** ~3 hours.
- **Cost:** LinkedIn Learning subscription (~$30/mo; often free via employer or library card).
- **Why relevant.** Short, OpenCV-heavy hands-on intro. Useful for filling OpenCV gaps if you came from a pure-ML background and never used it.

---

## Stack 5 - Books worth owning

The internet ages out fast; well-edited books don't. Keep these on your desk and read whichever chapter maps to whatever you're stuck on this week.

- **Multiple View Geometry in Computer Vision** - Richard Hartley & Andrew Zisserman. 2nd ed., 2004. The single reference for projective geometry, the fundamental matrix, triangulation, and bundle adjustment. Reference manual, not cover-to-cover.
- **Computer Vision: Algorithms and Applications** - Richard Szeliski. 2nd ed., 2022. Free PDF at szeliski.org. Broadest single-volume CV reference; use as a Wikipedia for CV before diving into papers.
- **Probabilistic Robotics** - Sebastian Thrun, Wolfram Burgard, Dieter Fox. 1st ed., 2005. Codified EKF, particle filter, and graph-based SLAM. Every modern SLAM paper assumes you've read it.
- **Computer Vision: Models, Learning, and Inference** - Simon Prince. 1st ed., 2012. Free PDF on author's site. Bridges classical statistical CV with probabilistic graphical models. Second-opinion book when Szeliski doesn't click.
- **Deep Learning for Vision Systems** - Mohamed Elgendy. 1st ed., 2020 (Manning). Practitioner-flavored CNN / detection / GAN intro. Good alternative if CS231n feels too dense.
- **Robotics, Vision and Control** - Peter Corke. 3rd ed., 2023 (with MATLAB/Python toolboxes). The one book that covers manipulator kinematics, vision, and control coherently. Indispensable if your robot has an arm.
- **An Invitation to 3-D Vision** - Yi Ma, Stefano Soatto, Jana Kosecka, Shankar Sastry. 1st ed., 2003. A gentler ramp into multi-view geometry than Hartley & Zisserman, with cleaner notation.

---

## Recommended sequence

Three 6-month paths. Pick the one closest to your intended outcome.

**Path (a) - perception job at an AV company.** Months 1-2: CS231A (Stanford). Months 2-4: CS231n (Stanford), all three assignments. Months 4-5: U Toronto Self-Driving Cars Specialization (focus Course 3). Months 5-6: Stachniss SLAM playlist + ORB-SLAM3 demo on your own video with writeup. Throughout: one CVPR best-paper per week from the AV / 3D track.

**Path (b) - start a perception-services agency.** Month 1: Hugging Face Computer Vision Course (front-to-back). Month 2: Roboflow Notebooks, one custom detector per week. Months 3-4: PyImageSearch University, 8-10 project lessons mapped to real client asks (OCR, license plates, anomaly detection, face matching). Month 5: NVIDIA DLI DeepStream for 30+ fps Jetson deploys. Month 6: three demo verticals (retail shoplifting, factory defect, warehouse counting) shipped to public URLs.

**Path (c) - research someday.** Months 1-2: CS231A (Stanford) with assignments. Months 3-4: CS231n (Stanford) with assignments. Months 4-5: CS280 (Berkeley), all lectures + recommended papers. Month 6: reimplement one CVPR 2024 / 2025 paper end-to-end and publish the code with a writeup — the highest-signal application material for a PhD or research-engineer role.

---

## Free YouTube playlists to bookmark NOW

Background tabs of a perception career. Watch on the train, on a run, while washing dishes.

1. **Andrej Karpathy - "Neural Networks: Zero to Hero."** Hand-builds a GPT and a CNN from scratch in pure Python. The single best video series on what's inside a neural net.
2. **Yannic Kilcher - paper reviews.** One major paper per video at the pace of a senior reviewer thinking aloud. Best way to learn how to read a paper.
3. **Two Minute Papers - Károly Zsolnai-Fehér.** 5-minute summaries of new CV / graphics / ML papers. Keeps wide-but-shallow awareness of the field.
4. **Cyrill Stachniss - SLAM and Photogrammetry.** Listed as a course above; the YouTube playlists are the actual material.
5. **First Principles of Computer Vision - Shree Nayar.** Full free lecture series at firstprinciplesofcomputervision.com. Same content as the Coursera specialization, no paywall.
6. **Jeremy Howard - fast.ai videos.** Companion videos to Practical Deep Learning. Worth watching for the philosophy alone.
7. **3Blue1Brown - Essence of Linear Algebra and Essence of Calculus.** Visual-intuition gold standard. Re-watch change-of-basis at least twice a year.
8. **Welch Labs - "Imaginary Numbers Are Real" and "Neural Networks Demystified."** Short, beautifully produced explainers. The neural-net series is the cleanest "what is a hidden layer doing" video anywhere.
9. **DeepLearning.AI YouTube channel.** Andrew Ng's team uploads "The Batch" interviews, short courses, and summary talks. Tracks industry sentiment.
10. **LeRobot - Hugging Face robotics tutorials.** Imitation learning, behavior cloning, and the SO-100 arm. Increasingly the on-ramp for perception engineers crossing into robot learning.

---

## Conferences (watch the talks free)

Most major CV / robotics conferences post talks free within weeks. You don't need to attend.

- **CVPR (Computer Vision and Pattern Recognition) - June.** Open-access proceedings at openaccess.thecvf.com; talks on YouTube. The single most important CV venue.
- **ICCV (International Conference on Computer Vision) - October, odd years.** Open-access via CVF.
- **ECCV (European Conference on Computer Vision) - October, even years.** Proceedings via ECVA; YouTube talks appear within a month.
- **CoRL (Conference on Robot Learning) - November.** CoRL YouTube channel. Flagship venue for learning-based robotics, including perception.
- **ICRA (International Conference on Robotics and Automation) - May.** IEEE-published; key talks mirrored on YouTube. Heavier on systems and control than CoRL.
- **IROS (Intelligent Robots and Systems) - October.** Sister conference to ICRA, slightly more applied / sensors-heavy.

**How to skim a conference in a weekend.** Friday: read the best-paper-award winners. Saturday: skim workshop abstracts in your sub-area — workshop papers are usually more forward-looking than main-track. Sunday: pick three papers that caught your eye and read them properly. ~6 hours total for a better-than-average grip on the field's direction.

---

## 24-month learning budget

A realistic timeline if you're a working web dev keeping your day job. Total budget: ~1000 hours over two years — about 1 hour every weekday plus a long Saturday session.

- **Months 1-3 - Stack 0 basics.** ~6 hrs/week. Math refreshers, Python / NumPy, 3Blue1Brown. ~75 hours.
- **Months 4-9 - Stacks 1 + 2 (classical and deep CV).** ~8 hrs/week. CS231A + CS231n in parallel (or sequence), with one Roboflow / Hugging Face notebook per fortnight. ~200 hours.
- **Months 10-15 - Stacks 3 + 4 (robotics-specific and project-driven).** ~10 hrs/week. U Toronto SDC, Stachniss SLAM, NVIDIA DLI, ROS2 in 5 Days, and one PyImageSearch / Roboflow project per month. ~260 hours.
- **Months 16-24 - team capability rollout.** ~10 hrs/week. Ship one publicly-deployed reference project that takes 2-3 months (visual SLAM on phone video packaged as a web app; or a Jetson-deployed detector for a real customer-shaped problem). Remainder: open-source contributions and writing case studies for the sales pipeline. ~360 hours.

Total ~895 hours over 24 months, leaving ~100 hours of slack. The team can compress to 12-15 months if aggressive, but quality of the reference builds matters more than speed of arrival.
