# Courses for Perception & Computer Vision

A curated list of online courses that map directly to the skills you
need to ship a perception project. Listed roughly in the order a
junior web developer should take them. All links go to the official
course page; many are free to audit or have free YouTube uploads.

A note on choosing: perception work spans six skill stacks — (0)
absolute basics if you're brand new, (1) classical CV and multi-view
geometry, (2) deep learning for vision, (3) robotics-specific
perception (SLAM, 3D, sensor fusion), (4) project-driven courses
where you build something you can show off, and (5) reference books
worth owning. Pick at least one from each stack you don't already
know.

A second note on auditing vs. building. Coursera's auditing
experience is roughly equivalent to skimming an O'Reilly book on
the train — fast, surface-level, and you'll forget half by next
month unless you build alongside. Treat every course as a scaffold:
if you don't have a small repo (even just a few notebooks) per
course on your GitHub by the end, you didn't really take the course.
This is the same lesson web devs learn the hard way with React
tutorials — watching ten hours of Wes Bos won't build a Next.js
app, only typing along while pausing every two minutes will.

---

## Stack 0: Foundational basics — the npm-install and "Hello World" layer of perception. You wouldn't try to learn React without knowing JavaScript; you can't learn CS231A without knowing what a matrix multiply does to a vector.

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
- **Skill it builds for the job.** Comfort reading "Pythonic" code:
  list comprehensions, generators, context managers, decorators.
  When you open a perception team's repo on day one and see
  `@torch.no_grad()` over a function returning a generator of
  tensors, you should not pause.
- **Web-dev analogy.** Roughly equivalent to "JavaScript for
  beginners" on Udemy — necessary if you've never typed `def`, a
  waste of money if you ship Node services for a living.
- **Time to first portfolio artifact.** Realistically you'll have
  a small CLI-style data-munging script in your GitHub after week
  4. Nothing CV-shaped yet — this is pure scaffolding.

### B. Mathematics for Machine Learning Specialization — Imperial College London on Coursera

- **Link:** https://www.coursera.org/specializations/mathematics-machine-learning
- **Length:** 3 courses (Linear Algebra, Multivariate Calculus,
  PCA), ~4 months at 4 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Linear algebra (SVD, eigenvectors,
  projections) is the entire language of multi-view geometry and
  3D reconstruction. PCA shows up in feature matching. This
  specialization is the most direct math prep for CS231A.
- **Skill it builds for the job.** Reading a SLAM paper without
  glazing over at the equations. When the senior engineer says
  "we factorize the information matrix with Cholesky" you should
  recognize each word. Most perception interviews include at
  least one whiteboard linear-algebra question (typical: derive
  the 8-point algorithm, or explain why SVD recovers rotation).
- **Web-dev analogy.** Like learning the underlying TCP/IP stack
  when you've only ever called `fetch()`. You can hand-wave it
  for a while, but the moment something breaks at a low level
  you'll be helpless without it.
- **Time to first portfolio artifact.** Nothing portfolio-shaped
  from this course directly — but week 6 of CS231A (which this
  course unblocks) is where you ship a working two-view
  triangulation Jupyter notebook.

### C. Essence of Linear Algebra — 3Blue1Brown (YouTube)

- **Link:** https://www.3blue1brown.com/topics/linear-algebra
- **Length:** ~3 hours.
- **Cost:** Free.
- **Why this is 100% relevant.** Visual intuition for matrices as
  transforms. Watching the "change of basis" video makes camera
  intrinsics / extrinsics click in 10 minutes instead of two days.
- **Skill it builds for the job.** Geometric intuition for what
  a 4x4 transform matrix is doing to a point cloud. When the
  ROS tf tree throws a "frame X is not connected to frame Y"
  error, you'll know in your gut what a frame even is.
- **Web-dev analogy.** Like watching Wes Bos's "JavaScript 30"
  on a weekend — three hours of pure intuition that pays back
  for months. Free, no excuse not to watch.
- **Time to first portfolio artifact.** None — this is pure
  intuition fuel. But the next time you write a manual rotation
  matrix in NumPy, it'll take 5 minutes not 5 hours.

### D. Khan Academy — Linear Algebra + Multivariable Calculus

- **Link:** https://www.khanacademy.org/math/linear-algebra and
  https://www.khanacademy.org/math/multivariable-calculus
- **Length:** Self-paced; ~40 hours each.
- **Cost:** Free.
- **Why this is 100% relevant.** Drill-heavy refresher. If the
  Imperial College specialization assumes too much, Khan Academy
  fills the floor below it.
- **Skill it builds for the job.** Mechanical fluency: dot
  products, matrix-vector multiplies, partial derivatives, chain
  rule. The arithmetic you'll need to debug a Jacobian by hand
  at 2am when your optimizer diverges.
- **Web-dev analogy.** Like FreeCodeCamp's algorithm-and-data-
  structures curriculum — repetitive, sometimes boring, but the
  only way to build muscle memory.
- **Time to first portfolio artifact.** Zero direct artifact;
  this is gym work, not building.

### E. CS50's Introduction to Programming with Python — Harvard on edX

- **Link:** https://www.edx.org/learn/python/harvard-university-cs50-s-introduction-to-programming-with-python
- **Length:** 10 weeks at ~10 hrs/week.
- **Cost:** Free to audit; $200 for certificate.
- **Why this is 100% relevant.** Every week ends with a coded
  project. CS50P builds the "I can wire library X into a Python
  program" reflex you'll need before stacking OpenCV / PyTorch /
  Open3D together in week 1 of any real perception project.
- **Skill it builds for the job.** Library-juggling. Real
  perception scripts always import five libraries that weren't
  written to talk to each other; CS50P trains the calm
  patience for reading docs and gluing them.
- **Web-dev analogy.** Feels like the Odin Project's Node
  curriculum — structured, project-per-week, lots of "type
  this in your terminal and screenshot the result."
- **Time to first portfolio artifact.** A handful of small
  Python CLI tools by week 6 (file de-duplicator, scraper,
  etc.). Not perception, but real shippable code.

---

## Stack 1: Classical computer vision and multi-view geometry — the vanilla-DOM and CSS-grid layer of perception. Boring? Maybe. But every modern framework still compiles down to it, and the senior engineer reviewing your PR will absolutely ask why you didn't just use a homography.

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
- **Skill it builds for the job.** Reasoning about *what the
  pixels actually are* before you reach for a neural net.
  When a senior engineer asks "is that artifact from your sensor
  rolling shutter or from your CNN?" you should be able to answer
  in 30 seconds.
- **Web-dev analogy.** Watching Nayar's lectures is like reading
  the HTML5 spec end-to-end — exhaustive, occasionally dry, but
  it leaves you with a model of the platform that nothing else
  gives you. Free version on his website is the same content as
  Coursera's paid track.
- **Time to first portfolio artifact.** After ~3 modules you'll
  have your own camera-calibration script (checkerboard images
  in, intrinsics matrix out) checked into GitHub — already a
  legitimate resume bullet.

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
- **Skill it builds for the job.** The bundle-adjustment problem
  set in this course is exactly what you'll write a Python wrapper
  around at any SLAM-heavy startup — Skydio, Wayve, Nuro, Cobalt
  Robotics, all of them. Same for the PnP assignment, which maps
  directly to the function you'll call inside any visual-relocalization
  pipeline.
- **Web-dev analogy.** CS231A feels like reading the V8 source.
  Most days you don't need to know it; the day you do, nothing
  else helps. Going through the assignments instead of just
  reading the notes is the difference between knowing JavaScript
  and knowing how the event loop actually runs.
- **Time to first portfolio artifact.** Finish assignment 2 and
  you have a two-view structure-from-motion notebook (two photos
  of a building in, a 3D point cloud out) — already a portfolio-
  grade artifact, and very visual.

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
- **Skill it builds for the job.** Speaking robotics' dialect of
  CV. The naming conventions ("body frame," "world frame," "ego
  motion") that academic CV courses skip are baked into every
  week here.
- **Web-dev analogy.** Roughly equivalent to a focused
  Frontend-Masters workshop after you've already done the broader
  Stanford track: same material, narrower lens, half the time.
- **Time to first portfolio artifact.** A working monocular
  visual-odometry notebook by week 3 — feed it a video, it
  draws the camera trajectory.

### 3b. CS280: Computer Vision — UC Berkeley (Jitendra Malik, Alyosha Efros, and rotating co-instructors)

- **Link:** Search "Berkeley CS280" on the EECS course site
  (page moves each semester; the current offering's slides are
  always linked from the instructor's home page).
- **Length:** Full semester; ~24 lectures.
- **Cost:** Free (course materials publicly available).
- **Why this is 100% relevant.** Berkeley's flagship grad CV
  course — taught by Jitendra Malik (perceptual grouping,
  segmentation pioneer) and Alyosha Efros (texture synthesis,
  image-to-image translation pioneer). Skews more toward the
  *history and philosophy* of vision than Stanford's CS231A,
  which makes it the better course for anyone who wants to do
  research someday.
- **Skill it builds for the job.** Pattern recognition for what
  has and hasn't worked in CV. After watching Malik's lectures
  you'll instinctively know whether a "novel" arXiv paper is
  actually a 2003 idea with a transformer slapped on.
- **Web-dev analogy.** Reading the React core team's blog
  posts from 2014-2016 — not the most efficient way to learn
  hooks today, but it teaches you *why* the API looks like it
  does.
- **Time to first portfolio artifact.** None directly — this
  is more of a "raise your taste" course. Watch it while you
  build artifacts from CS231A / CS231n.

### 3c. 16-385: Computer Vision — Carnegie Mellon University

- **Link:** Search "CMU 16-385" — Kris Kitani's and Ioannis
  Gkioulekas's offerings have full slides + assignments online.
- **Length:** Full semester; ~26 lectures.
- **Cost:** Free.
- **Why this is 100% relevant.** Undergraduate-level CMU CV
  course. Heavy on classical-CV assignments (Lucas-Kanade
  tracking, Harris corners, panorama stitching, structured
  light) and a great pace if CS231A's grad-level math feels
  punishing. CMU also has 16-720 (graduate version) if you
  want the more advanced track.
- **Skill it builds for the job.** Implementing a perception
  primitive from scratch and recognizing it later in someone
  else's codebase. Once you've written your own Lucas-Kanade
  tracker you'll never again be intimidated by the OpenCV
  source.
- **Web-dev analogy.** Like working through "You Don't Know
  JS" cover to cover after already shipping React apps for a
  year — pieces you thought you understood suddenly snap into
  focus.
- **Time to first portfolio artifact.** A panorama stitcher
  (5 phone photos in, 1 stitched image out) by roughly week 4.

### 3d. EECS 442 / 504: Computer Vision — University of Michigan (David Fouhey, and others)

- **Link:** Search "UMich EECS 442" or "EECS 504" — Fouhey's
  course pages are usually the top hit.
- **Length:** Full semester; ~28 lectures.
- **Cost:** Free.
- **Why this is 100% relevant.** Famously clear lectures.
  EECS 442 is undergrad-friendly, EECS 504 is the grad-level
  follow-on. Together they cover roughly the same ground as
  CS231A + CS231n combined but with assignments that lean
  more practical and less theoretical.
- **Skill it builds for the job.** Fouhey's homeworks force
  you to debug your own implementation — exactly the muscle
  you use when a YOLO fine-tune mysteriously plateaus on a
  customer's data.
- **Web-dev analogy.** Roughly the Kent C. Dodds of CV
  pedagogy — meaning extremely good at making the obvious
  feel inevitable.
- **Time to first portfolio artifact.** A working image
  classifier with hand-derived backprop by ~week 5.

### 3e. 3D Vision — ETH Zurich (Marc Pollefeys)

- **Link:** Search "ETH 3D Vision Pollefeys" — slides and
  lecture recordings on the CVG group's site.
- **Length:** Full semester; ~14 lectures plus project.
- **Cost:** Free.
- **Why this is 100% relevant.** Marc Pollefeys leads the
  Microsoft HoloLens spatial-mapping group on top of his ETH
  professorship; this course is *the* graduate-level treatment
  of SfM, multi-view stereo, and dense reconstruction. Hugely
  relevant for anyone targeting AR / XR / spatial-mapping
  roles (Niantic, Meta Reality Labs, Apple Vision Pro team).
- **Skill it builds for the job.** Reading a COLMAP or
  OpenMVS paper and recognizing every block in the pipeline.
- **Web-dev analogy.** A focused workshop with the maintainer
  of a framework you actually use — like a one-week deep
  dive with the Next.js team after you've already shipped
  Next apps.
- **Time to first portfolio artifact.** A multi-view stereo
  reconstruction of a small object from 20 phone photos —
  excellent demo material.

---

## Stack 2: Deep learning for vision — the React + Next.js layer of perception. The classical stuff (Stack 1) is the underlying browser API; this is the framework that ships features fast, with all the same risks of overuse.

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
- **Skill it builds for the job.** Hand-deriving backprop through
  a conv layer (assignment 2) is the single best way to internalize
  what the optimizer is actually doing. You'll never again "guess
  and hit run" when a model isn't training.
- **Web-dev analogy.** Skipping the assignments and only watching
  the videos is roughly equivalent to reading the React docs on
  the toilet — you'll feel productive and learn nothing. The
  assignments are the actual course.
- **Time to first portfolio artifact.** A Jupyter notebook with
  your from-scratch CNN training on CIFAR-10 by ~week 4, and a
  fine-tuned vision transformer on a custom dataset by ~week 8.

### 5. Deep Learning Specialization (Course 4: Convolutional Neural Networks) — DeepLearning.AI on Coursera

- **Link:** https://www.coursera.org/specializations/deep-learning
- **Length:** Course 4 is ~4 weeks at 5 hrs/week.
- **Cost:** Free to audit; $49/mo for certificates.
- **Why this is 100% relevant.** Andrew Ng's CNN course inside the
  Deep Learning Specialization is the most beginner-friendly
  treatment of detection (YOLO), segmentation (U-Net), face
  recognition, and neural style transfer. Pairs well with CS231n if
  CS231n's pace feels too aggressive.
- **Skill it builds for the job.** A working mental model of
  detection vs. segmentation vs. classification — the three
  most common interview filter questions for junior CV roles.
- **Web-dev analogy.** Like the "Net Ninja" YouTube tutorials —
  hand-held, low-anxiety, you'll be writing Hello World code
  within an hour. Don't mistake that for understanding.
- **Time to first portfolio artifact.** A YOLO fine-tune on your
  own ~200-image dataset by end of week 3.

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
- **Skill it builds for the job.** Loading a CLIP / DINOv2 /
  SAM checkpoint and getting useful features out the same
  afternoon. This is exactly what perception team leads will
  ask you to do in a take-home.
- **Web-dev analogy.** Feels like the official Vercel /
  Next.js tutorials — modern, opinionated, and the code you
  write here matches what you'd actually ship.
- **Time to first portfolio artifact.** A semantic image
  search demo (text query in, top-k images out) using CLIP
  by the end of unit 4 — about week 2 if you're moving fast.

### 6b. Hugging Face Diffusion Models Class

- **Link:** https://huggingface.co/learn/diffusion-course
- **Length:** ~4 units, self-paced (~20 hours total).
- **Cost:** Free.
- **Why this is 100% relevant.** Diffusion has crept into
  *perception*, not just art generation — depth diffusion
  (Marigold), monocular reconstruction (Wonder3D), and
  novel-view synthesis all build on the same denoising
  framework. Useful for staying current on what's coming.
- **Skill it builds for the job.** Recognizing when a paper
  is genuinely novel vs. "diffusion applied to task X." Saves
  you from chasing hype.
- **Web-dev analogy.** Like a workshop on the latest CSS
  feature — not strictly required, but the people who pick
  it up early get asked to lead the team's adoption of it.
- **Time to first portfolio artifact.** A small text-to-image
  fine-tune (on a custom concept, say "my dog") in a Gradio
  Space by week 2.

### 6c. fast.ai — Practical Deep Learning for Coders (Part 1) — Jeremy Howard

- **Link:** https://course.fast.ai
- **Length:** 9 lessons, ~60 hours of work.
- **Cost:** Free.
- **Why this is 100% relevant.** Top-down pedagogy: ship a
  working image classifier in lesson 1, then peel back the
  layers. The opposite philosophy of CS231n and the better
  fit for working developers who want results before theory.
- **Skill it builds for the job.** Pragmatic instincts —
  pick a baseline, train, look at the data, iterate. The
  habits Jeremy drills are exactly what works in real
  perception teams.
- **Web-dev analogy.** The fast.ai equivalent in web is
  "Build X with Y in 7 days" boot camps — opinionated,
  results-first, you'll be productive within a week.
- **Time to first portfolio artifact.** A custom image
  classifier deployed to Hugging Face Spaces by the end of
  lesson 2. Genuinely 48 hours from zero to demo-able.

---

## Stack 3: Robotics-specific perception (SLAM, 3D, AV) — the deployment + infra layer of perception. Pure CV courses teach you to recognize a cat in a photo; this stack teaches you to localize a robot among ten thousand cats at 30 Hz while the GPU runs at 90°C.

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
- **Skill it builds for the job.** Multi-sensor reasoning —
  when to trust camera vs. lidar vs. radar, how to fuse them,
  how latency compounds across a stack. This is the framework
  an AV perception interviewer will probe in 20 different ways.
- **Web-dev analogy.** Roughly equivalent to a "full stack
  Next.js + Postgres + auth + deploy" bootcamp — long, broad,
  and the only one that covers the whole pipeline end-to-end.
- **Time to first portfolio artifact.** A lane-detection +
  vehicle-detection pipeline working on a KITTI sequence by
  the end of Course 3.

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
- **Skill it builds for the job.** Reading a SLAM codebase
  without flinching. Once you can hand-derive the EKF update,
  the giant Eigen expressions in any C++ SLAM library stop
  looking like noise.
- **Web-dev analogy.** Stachniss's pace is roughly that of a
  patient pair-programming session with a staff engineer who
  explains every line. Watch at 1.5x speed; he plans for that.
- **Time to first portfolio artifact.** A working 2D EKF-SLAM
  notebook on a simulated robot by ~lecture 12, and an
  ORB-SLAM3 demo on your phone video by month 3.

### 8b. Photogrammetry I & II — Cyrill Stachniss (separate from the SLAM playlist)

- **Link:** YouTube "Cyrill Stachniss Photogrammetry" — two
  full playlists, separate from the SLAM lectures.
- **Length:** ~50 hours combined.
- **Cost:** Free.
- **Why this is 100% relevant.** Where the SLAM lectures
  assume you know image formation and camera models, the
  Photogrammetry lectures *teach* them — pinhole geometry,
  homogeneous coordinates, distortion models, calibration,
  bundle adjustment from first principles. Watch these
  *before* the SLAM ones if you're new to multi-view.
- **Skill it builds for the job.** Cleaner intuition for
  what bundle adjustment is actually optimizing. Maps
  directly to debugging COLMAP failures.
- **Web-dev analogy.** Like reading the HTTP/2 spec before
  the gRPC docs. You can absolutely skip it, and you'll
  regret it the first time something goes weird in
  production.
- **Time to first portfolio artifact.** A from-scratch
  calibration + undistortion pipeline by ~lecture 8.

### 9. NVIDIA Deep Learning Institute — Computer Vision Learning Paths

- **Link:** https://www.nvidia.com/en-us/training/
- **Cost:** Many free; paid courses ~$90.
- **Why this is 100% relevant.** NVIDIA's training paths cover
  CUDA-accelerated perception, TensorRT inference, DeepStream
  pipelines, and Jetson deployment — the deployment stack used by
  most production robotics teams. After CS231n and CS231A teach you
  the algorithms, NVIDIA DLI teaches you how to ship them at 30+
  Hz on edge hardware.
- **Skill it builds for the job.** Turning a research-grade
  PyTorch model into an ONNX + TensorRT engine that runs at
  the latency budget the robot allows. This is the most-asked,
  least-taught skill in robotics perception.
- **Web-dev analogy.** Like learning Cloudflare Workers /
  Vercel Edge after you already know React — same code, very
  different deployment shape, big consequences.
- **Time to first portfolio artifact.** A YOLO model running
  on a Jetson Nano (or in Jetson emulator) at 30 fps inside
  a DeepStream pipeline by end of the 8-hour lab.

### 9b. ROS2 in 5 Days — The Construct (perception sub-track)

- **Link:** https://www.theconstruct.ai/robotigniteacademy_learnros/ros-courses-library/
- **Length:** ~5 days of paced lessons; can be done in 2-3
  weekends.
- **Cost:** Free trial; subscription thereafter.
- **Why this is 100% relevant.** ROS2 is the lingua franca of
  robotics middleware; you'll encounter it at any robotics
  company with hardware. The Construct's perception sub-track
  covers camera drivers, image_transport, point-cloud
  processing nodes, tf2 transforms, and integration with OpenCV
  — exactly the glue code that turns a CV model into a node a
  robot can actually use.
- **Skill it builds for the job.** Wiring a perception model
  into a real robot's nervous system. The day-one task at any
  robotics startup.
- **Web-dev analogy.** Like learning Kubernetes after you've
  only deployed to Heroku. ROS2 is the cluster-orchestrator
  layer of robotics, with the same steep but bounded ramp.
- **Time to first portfolio artifact.** A ROS2 node that
  subscribes to a camera topic, runs a detector, and publishes
  bounding boxes — by end of the perception sub-track.

---

## Stack 4: Project-driven / hands-on courses — the "ship it on Friday" layer. Everything above teaches you why a thing works; these teach you how to package it into a repo a hiring manager will actually clone.

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
- **Skill it builds for the job.** "Yes, I can build that by
  Friday" — the most valuable mindset on any CV team. Rosebrock
  drills the build-first habit until it's reflex.
- **Web-dev analogy.** Like Wes Bos's paid courses — opinionated,
  shippable, the projects look good in a portfolio without
  needing extra polish.
- **Time to first portfolio artifact.** A working OCR app, a
  face-recognition door cam, *and* a YOLO custom detector — all
  three within the first 30 days if you pace yourself.

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
- **Skill it builds for the job.** Deep OpenCV literacy. The
  API is huge and weirdly inconsistent; this course is the
  closest thing to a guided tour.
- **Web-dev analogy.** Like a paid course taught by an
  Express.js core maintainer — you'll learn which APIs are
  blessed, which are legacy, and which to avoid.
- **Time to first portfolio artifact.** Each track ends with
  a deployable project — typically a real-time webcam app or
  a small classifier API.

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
- **Skill it builds for the job.** A portfolio that maps 1:1
  to AV job descriptions. Reviewers grade your code; you can
  literally cite the projects in your resume.
- **Web-dev analogy.** Like a Lambda School / Bloom Institute
  bootcamp aimed at one specific industry — opinionated, paced,
  expensive, and only worth it if you're committed to the
  outcome.
- **Time to first portfolio artifact.** Lane-detection project
  by week 4; full sensor-fusion Kalman filter by ~month 3.

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
- **Skill it builds for the job.** Speed of iteration. The
  difference between a junior who needs three days to fine-tune
  a model and one who does it in three hours is usually just
  Roboflow notebook familiarity.
- **Web-dev analogy.** Like the create-next-app starter
  templates — opinionated scaffolds that get you to "running
  app" before you've poured coffee.
- **Time to first portfolio artifact.** A custom-trained YOLO
  detector deployed to a free Roboflow inference URL — about
  one weekend.

### 14. Zero to Mastery — PyTorch for Deep Learning

- **Link:** https://zerotomastery.io/courses/learn-pytorch/
- **Length:** ~30 hours.
- **Cost:** ZTM subscription (~$39/mo).
- **Why this is 100% relevant.** Daniel Bourke's PyTorch course is
  one of the most beginner-friendly project-driven options. The
  capstone is a custom image classifier (FoodVision), and the
  course covers transfer learning, deployment to Gradio / Hugging
  Face Spaces. Good fit if Coursera's auditing feels too passive.
- **Skill it builds for the job.** PyTorch fluency at the
  level you can write a custom Dataset, DataLoader, training
  loop, and eval script from a blank file.
- **Web-dev analogy.** Like Bourke's broader brand — the
  PyTorch equivalent of a long-form YouTube series on
  building a SaaS in public. Approachable, sometimes slow,
  good for sticky habit formation.
- **Time to first portfolio artifact.** A deployed FoodVision
  classifier on a Gradio Space by the capstone — looks great
  in a portfolio link.

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
- **Skill it builds for the job.** Reading and ruthlessly
  adapting *other people's* high-performance code. The actual
  daily activity of most CV engineers.
- **Web-dev analogy.** Like grinding LeetCode, except the
  problems matter. A few Expert-tier finishes punch above a
  CS degree on a junior CV resume.
- **Time to first portfolio artifact.** A bronze-medal Kaggle
  finish in a vision comp is realistic within 3-4 months of
  focused effort and becomes a resume bullet immediately.

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
- **Skill it builds for the job.** Stream-graph thinking —
  arranging GStreamer-style elements (source -> decode ->
  infer -> overlay -> sink) into a working pipeline. The
  same mental model used by most edge-video systems.
- **Web-dev analogy.** Like learning a streaming-data
  framework after only knowing REST — the new question is
  "what gets dropped under back-pressure?" not "is the JSON
  valid?"
- **Time to first portfolio artifact.** A working DeepStream
  pipeline doing real-time person detection on a webcam by
  the end of the 8-hour lab.

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
- **Web-dev analogy.** Like a Codecademy Pro track for
  fundamentals you already know — useful for the deadline
  pressure, less useful for the information density.
- **Time to first portfolio artifact.** Facial-keypoint
  detector by ~month 2.

### 11. LinkedIn Learning: "Building Computer Vision Applications with Python" — Eduardo Corpeño

- **Link:** https://www.linkedin.com/learning/building-computer-vision-applications-with-python
- **Length:** ~3 hours.
- **Cost:** LinkedIn Learning subscription (~$30/mo; often free via
  employer or library card).
- **Why this is relevant.** Short, OpenCV-heavy hands-on intro.
  Useful for filling in OpenCV gaps if you came from a pure-ML
  background and never used it.
- **Web-dev analogy.** A LinkedIn-Learning-style snack-sized
  tutorial — fine for a Sunday afternoon, nothing more.
- **Time to first portfolio artifact.** A small webcam OpenCV
  demo by the end of the 3 hours.

---

## Stack 5: Books worth owning

The internet ages out fast; well-edited books don't. Each of these
is worth a desk slot. Use them like O'Reilly books — keep them on
your desk, dog-ear three pages a week, and read whichever chapter
maps to whatever you're stuck on this Tuesday. Years given are the
last edition I'm reasonably confident about; check the publisher
page for newer printings.

### Multiple View Geometry in Computer Vision — Richard Hartley & Andrew Zisserman

- **Edition / year.** 2nd edition, 2004 (still authoritative;
  no newer edition as of 2026).
- **Why own it.** The single reference for projective geometry,
  the fundamental matrix, triangulation, and bundle adjustment.
  If you ever do real SfM / SLAM work, you will open this
  book at least twice a month.
- **Use it like.** A reference manual. Don't read cover to
  cover; jump to the chapter that maps to your current bug.

### Computer Vision: Algorithms and Applications — Richard Szeliski

- **Edition / year.** 2nd edition, 2022. Author releases a
  free PDF at szeliski.org.
- **Why own it.** The broadest single-volume CV reference.
  Covers everything from image processing to deep learning,
  with citations for further reading on each topic.
- **Use it like.** A Wikipedia for CV — start every new topic
  by reading Szeliski's 5-page summary before diving into
  papers.

### Probabilistic Robotics — Sebastian Thrun, Wolfram Burgard, Dieter Fox

- **Edition / year.** 1st edition, 2005 (still standard).
- **Why own it.** The book that codified EKF, particle filter,
  and graph-based SLAM. Every modern SLAM paper assumes you've
  read it.
- **Use it like.** A graduate seminar in book form. Read with
  pen in hand; the derivations are worth typing into your own
  notes.

### Computer Vision: Models, Learning, and Inference — Simon Prince

- **Edition / year.** 1st edition, 2012. Free PDF on the
  author's website.
- **Why own it.** Bridges classical statistical CV with the
  probabilistic-graphical-models view. Excellent for
  intuition-building if you find Szeliski too encyclopedic.
- **Use it like.** A second-opinion book — when one chapter
  in Szeliski doesn't click, read Prince's version.

### Deep Learning for Vision Systems — Mohamed Elgendy

- **Edition / year.** 1st edition, 2020 (Manning).
- **Why own it.** Practitioner-flavored intro to CNNs,
  detection, GANs. Code-heavy and approachable.
- **Use it like.** A second computer-vision book if CS231n
  feels too dense; Elgendy explains the same ideas with
  more pictures.

### Robotics, Vision and Control — Peter Corke

- **Edition / year.** 3rd edition, 2023 (with MATLAB/Python
  toolboxes).
- **Why own it.** The one book that covers manipulator
  kinematics, vision, and control in a single coherent
  framework. Indispensable if your robot has an arm.
- **Use it like.** A bench reference — work through the
  Python notebooks Corke maintains alongside the book.

### An Invitation to 3-D Vision — Yi Ma, Stefano Soatto, Jana Kosecka, Shankar Sastry

- **Edition / year.** 1st edition, 2003 (still cited in
  modern 3D-vision papers).
- **Why own it.** A gentler ramp into multi-view geometry
  than Hartley & Zisserman, with cleaner notation. Worth
  having if you find H&Z impenetrable on first read.
- **Use it like.** A "for-beginners" companion to Hartley &
  Zisserman — read the same topic in both, pick the
  notation that sticks.

---

## Recommended sequence

Three sample 6-month paths. Pick the one closest to your
intended outcome; don't try to do all three at once.

### Path (a): "I want a perception job at an AV company"

1. **Month 1-2.** CS231A — Stanford. Notes + assignments
   first; lectures only if you get stuck.
2. **Month 2-4.** CS231n — Stanford. Aim to finish all three
   assignments end-to-end.
3. **Month 4-5.** U Toronto Self-Driving Cars Specialization
   (focus on Course 3: Visual Perception).
4. **Month 5-6.** Cyrill Stachniss SLAM playlist + run
   ORB-SLAM3 on your own video; publish the demo with a
   short writeup.
5. **Throughout.** Read one CVPR-best-paper per week from
   the AV / 3D track.

### Path (b): "I want to start a perception-services agency"

1. **Month 1.** Hugging Face Computer Vision Course
   (front-to-back, ship the notebooks).
2. **Month 2.** Roboflow Notebooks — train and deploy one
   custom detector per week.
3. **Month 3-4.** PyImageSearch University — pick 8-10
   project lessons that map to real client asks (OCR,
   license plates, anomaly detection, face matching).
4. **Month 5.** NVIDIA DLI DeepStream — learn to ship at
   30+ fps on Jetson; this is the "we'll deploy it on your
   hardware" pitch agencies use.
5. **Month 6.** Pick three demo verticals (retail
   shoplifting, factory defect, warehouse counting); ship
   a polished demo for each on a public URL.

### Path (c): "I want to do research someday"

1. **Month 1-2.** CS231A — Stanford. Do the assignments.
2. **Month 3-4.** CS231n — Stanford. Same.
3. **Month 4-5.** CS280 — Berkeley. Watch all lectures;
   skip the assignments if time-constrained but read the
   recommended papers.
4. **Month 6.** Pick one CVPR 2024 / 2025 paper in an area
   you find interesting and *reimplement it* end-to-end.
   Publish the code with a writeup; this is the single
   highest-signal application material for a PhD or
   research-engineer role.

---

## Free YouTube playlists to bookmark NOW

These are not full courses — they're the "background tabs"
of a perception career. Watch on the train, on a run, while
washing dishes. Speeds up your taste calibration enormously.

1. **Andrej Karpathy — "Neural Networks: Zero to Hero."**
   Hand-builds GPT and a CNN from scratch in pure Python.
   The single best video series on what's *inside* a neural
   net. Search YouTube for the playlist name.

2. **Yannic Kilcher — paper reviews.** Goes through one
   major paper per video at the pace of a senior reviewer
   thinking aloud. Best way to learn how to read a paper.

3. **Two Minute Papers — Károly Zsolnai-Fehér.** 5-minute
   summaries of new CV / graphics / ML papers. Great for
   keeping a wide-but-shallow awareness of the field.

4. **Cyrill Stachniss — SLAM and Photogrammetry.** Already
   listed as a course above. The YouTube playlists are
   the actual course material; bookmark them.

5. **First Principles of Computer Vision — Shree Nayar.**
   The full free lecture series on
   firstprinciplesofcomputervision.com (and a YouTube
   mirror). Same content as the Coursera specialization,
   no paywall.

6. **Jeremy Howard — fast.ai videos.** Companion videos to
   the Practical Deep Learning course. Worth watching for
   the philosophy even if you don't do the homework.

7. **3Blue1Brown — Essence of Linear Algebra and Essence
   of Calculus.** The visual-intuition gold standard.
   Re-watch the change-of-basis video at least twice a
   year.

8. **Welch Labs — "Imaginary Numbers Are Real" and
   "Neural Networks Demystified."** Short, beautifully
   produced explainer series. The neural-net series is
   the cleanest "what is a hidden layer doing" video
   anywhere.

9. **DeepLearning.AI YouTube channel.** Andrew Ng's team
   uploads "The Batch" interviews, short courses, and
   summary talks. Good for tracking industry sentiment.

10. **LeRobot — Hugging Face robotics tutorials.** The
    HF LeRobot team's YouTube series on imitation
    learning, behavior cloning, and the SO-100 arm.
    Increasingly the on-ramp for perception engineers
    who want to cross into robot learning.

---

## Conferences (you can watch the talks free)

You don't need to attend. Most major CV / robotics
conferences post talks free within weeks.

- **CVPR (Computer Vision and Pattern Recognition) — June.**
  Open-access proceedings at openaccess.thecvf.com; talks
  and oral sessions are on YouTube (search "CVPR <year>").
  The single most important CV venue.
- **ICCV (International Conference on Computer Vision) —
  October, odd years.** Open-access via the same CVF site.
  Alternates with ECCV; together they're the "top two CV
  conferences" outside CVPR.
- **ECCV (European Conference on Computer Vision) —
  October, even years.** Proceedings via the ECVA site;
  YouTube talks usually appear within a month.
- **CoRL (Conference on Robot Learning) — November.**
  Talks live on the CoRL YouTube channel. The flagship
  venue for learning-based robotics, including perception.
- **ICRA (International Conference on Robotics and
  Automation) — May.** IEEE-published, but the most
  important talks are usually mirrored on YouTube.
  Heavier on systems and control than CoRL, but plenty
  of perception.
- **IROS (Intelligent Robots and Systems) — October.**
  IEEE again. Sister conference to ICRA, slightly more
  applied / sensors-heavy.

**How to skim a conference in a weekend.** Friday night:
read the best-paper-award winners (always announced in
the closing ceremony; one quick web search finds them).
Saturday: skim the abstracts of the workshops in your
sub-area — workshop papers are usually more forward-
looking than main-track. Sunday: pick three papers that
caught your eye and read them properly; bookmark the
rest for later. Total time: ~6 hours; you'll have a
better-than-average grip on the field's current
direction.

---

## Web-dev to perception engineer — the 24-month learning budget

A realistic timeline if you're a working web dev keeping
your day job. Total budget: ~1000 hours over two years —
that's about 1 hour every weekday plus a long Saturday
session, sustainably.

- **Months 1-3 — Stack 0 basics.** ~6 hrs/week. Math
  refreshers, Python / NumPy, 3Blue1Brown. ~75 hours total.
- **Months 4-9 — Stacks 1 + 2 (deep CV and multi-view
  geometry).** ~8 hrs/week. CS231A + CS231n in parallel
  (or sequence if that's too much), with one Roboflow /
  Hugging Face notebook per fortnight on the side.
  ~200 hours total.
- **Months 10-15 — Stacks 3 + 4 (robotics-specific and
  project-driven).** ~10 hrs/week. U Toronto SDC,
  Stachniss SLAM, NVIDIA DLI, ROS2 in 5 Days, and one
  PyImageSearch / Roboflow project per month.
  ~260 hours total.
- **Months 16-24 — Build a portfolio project AND apply
  to jobs in parallel.** ~10 hrs/week. One real,
  publicly-deployed project that takes 2-3 months
  (something like: visual SLAM on your phone video,
  packaged as a web app; or a Jetson-deployed
  detector for a real customer-shaped problem). The
  remainder goes into interview prep, networking,
  open-source contributions to a perception library.
  ~360 hours total.

Total: ~895 hours over 24 months, leaving ~100 hours of
slack for life. If you're more aggressive, you can
compress this to 12-15 months — but quality of
portfolio matters more than speed of arrival, and
hiring managers can tell the difference between a
rushed and a deliberate ramp.
