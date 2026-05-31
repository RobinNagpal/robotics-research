# Top-down value chain — who builds this robot

This document maps the **value chain** behind our project robot — a
**mobile manipulator that stocks a grocery shelf** (a wheeled base + a
6/7-DoF arm + a parallel-jaw gripper + an RGB-D camera, running on
ROS 2). A "value chain" just means the stack of companies whose work
adds up to the finished machine. We start at the **top** — the complete
robot a customer buys — and work **down** to the chips, magnets, and raw
materials inside it.

New to a term? See `02-glossary.md`.

> _Compiled by cross-checking several independent research passes and
> reconciling the company lists, classifications, and tickers. It is
> still a point-in-time snapshot — see the disclaimer below._

> **Disclaimer (read first).** Company status, ownership, tickers, and
> valuations drift constantly. Startups IPO, get acquired, or fold;
> tickers and exchanges change. Every figure below is approximate (`~`)
> and reflects roughly **early 2026**. Re-verify any ticker, valuation,
> or "private vs. public" label before you quote it or act on it.

A note on how to read this: each layer feeds the one **above** it. The
foundries make chips; the chips go into compute modules; the compute
goes into the robot; the system integrator bolts it all together and
sells the finished machine. A single company can appear in several
layers (NVIDIA shows up in compute *and* software, for example) — we
flag those overlaps.

---

## 1. System integrators / full-robot OEMs

This is the **top** of the chain: the company that designs the complete
mobile manipulator, integrates every part below, writes (or licenses)
the behavior, and sells or leases the finished robot to the grocery
customer. They are the "general contractor" of the whole stack.

### Public

- **ABB Ltd (SIX: ABBN; also NYSE: ABB)** — A Swiss-Swedish industrial
  giant and one of the "big four" robot makers. Its Robotics division
  builds full industrial and collaborative robot systems and does
  large-scale integration. For our project they are a **deep, pure-play
  leader** in full-robot integration, though robotics is only one slice
  of a much larger electrification-and-automation conglomerate.

- **FANUC (TSE: 6954)** — A Japanese pure-play robotics and factory-
  automation company, famous for its yellow arms and for making most of
  its own motors and controllers in-house. It is **about as deep as
  integration gets** — it builds the arm, the drive, and the controller
  itself, so it sits in several layers below this one too.

- **Yaskawa Electric (TSE: 6506)** — Japanese maker of Motoman robots
  and a top-tier servo-motor and drive supplier. **Highly vertically
  integrated**: like FANUC it makes its own motors, so it appears again
  in the actuators layer. A serious candidate to build a full mobile
  manipulator.

- **KUKA (private — verify status)** — German robot-arm maker, owned by
  China's Midea Group since 2016 and taken private. A classic full-robot
  OEM and integrator. **Deep involvement**, but now a subsidiary rather
  than a standalone listing, so treat it as effectively private as of
  early 2026.

- **Zebra Technologies (NASDAQ: ZBRA)** — Acquired Fetch Robotics, a
  pioneer of warehouse mobile manipulators. Zebra is mostly a
  barcode/scanning/enterprise-mobility company, so robotics is a
  **smaller part of a larger whole** — but the Fetch heritage is
  directly relevant to a shelf-stocking robot.

### Private (not yet public)

- **Boston Dynamics (private)** — Owned by Hyundai Motor Group. Builds
  Stretch (a box-moving mobile manipulator) and the Atlas humanoid.
  **Deep full-robot OEM** expertise; a likely builder of a machine like
  ours, but it sits inside Hyundai rather than trading on its own.

- **Agility Robotics (private)** — Makes the Digit humanoid that picks
  and moves totes in warehouses (deployed with Amazon and others). A
  **pure-play full-robot OEM** for mobile manipulation. Heavily funded
  and frequently rumored as an IPO candidate; still private as of early
  2026.

- **Fizyr / Dexterity Inc. (private)** — Dexterity builds full
  pick-and-pack robotic systems (arm + perception + software) for
  logistics. A **pure-play integrator** of exactly the arm-plus-vision
  pattern our project uses.

- **Berkshire Grey (private — verify status)** — Warehouse robotic
  picking systems integrator; was public, then taken private by SoftBank
  around 2023. Treat as private as of early 2026. **Deep integration**
  of pick-and-place cells.

- **RightHand Robotics (private)** — Builds complete piece-picking
  robotic stations (arm + gripper + vision + software). A **focused
  pure-play integrator** for the exact grasp-and-place task we care
  about.

- **Nimble Robotics (private)** — Autonomous pick-and-pack fulfillment
  systems combining arms, grippers, and learned grasping. **Pure-play
  integrator/OEM** in the same niche as our robot.

- **Mujin (private)** — Japan-based maker of "intelligent" robot
  controllers and full piece-picking/depalletizing cells. **Deep
  integrator**, and notably it also supplies the control "brain" that
  other integrators use, so it straddles the software layer too.

---

## 2. Mobile base / AMR platforms

The **mobile base** is the wheeled, self-driving cart the arm rides on.
"AMR" means Autonomous Mobile Robot — a base that maps a space and
navigates it on its own (this is what Nav2 drives in our stack). The
base feeds the integrator above as the robot's "legs."

### Public

- **Teradyne (NYSE: TER)** — Owns **Mobile Industrial Robots (MiR)**, a
  leading AMR maker, alongside Universal Robots. AMRs are **one focused
  division** of a company whose core business is semiconductor test
  equipment, so it is a strong but non-pure-play supplier here. (Teradyne
  reappears in the arms layer via Universal Robots.)

- **Symbotic (NASDAQ: SYM)** — Builds warehouse automation systems
  including autonomous mobile robots that move goods through a structured
  facility. **Deep** in mobile automation, though its design is a
  whole-warehouse system rather than a single free-roaming base.

- **KION Group (XETRA: KGX)** — Owner of Dematic and a major forklift /
  intralogistics player; supplies AGVs and AMRs at scale. AMRs are **one
  product line** within a large material-handling conglomerate.

- **Jungheinrich (XETRA: JUN3)** — German intralogistics and
  warehouse-vehicle maker with a growing AGV/AMR portfolio. **Tier-1
  supplier** of mobile platforms, again as part of a broader
  forklift/logistics business.

- **Honeywell (NASDAQ: HON)** — Through Honeywell Intelligrated, supplies
  warehouse automation and mobile robotics. A **small slice** of a vast
  industrial conglomerate, but a credible base supplier.

### Private (not yet public)

- **Locus Robotics (private)** — A leading warehouse AMR pure-play; its
  robots guide workers and move goods through fulfillment centers.
  **Deep pure-play AMR leader**; frequently cited as an IPO candidate but
  still private as of early 2026.

- **Fetch Robotics (now part of Zebra)** — Originated the research-grade
  mobile-manipulator base widely used in academia. Now inside Zebra
  (public), but the platform itself is a **direct ancestor** of our
  robot's base.

- **OTTO Motors (private)** — A division of Rockwell Automation
  (Rockwell is NYSE: ROK); makes heavy-duty industrial AMRs. **Deep AMR
  pure-play** by heritage, now owned by a public parent.

- **Geek+ (private — verify status)** — Chinese warehouse AMR maker, one
  of the global volume leaders; has pursued a Hong Kong listing, so check
  current status. **Deep pure-play** AMR supplier.

- **Quicktron (private)** — Chinese AMR maker for warehouses and
  logistics. **Pure-play** mobile-base supplier at high volume.

- **Clearpath Robotics (now part of Rockwell)** — Makes the Husky and
  Jackal research robots that are staples of ROS-based mobile-robot
  development. **Directly relevant** to a ROS 2 project like ours;
  acquired into Rockwell Automation.

- **Vecna Robotics (private)** — Material-handling AMRs and
  pallet-moving robots for warehouses. **Pure-play** mobile-automation
  supplier.

---

## 3. Robotic arms / manipulators (cobots)

The **arm** is the 6/7-DoF (degrees-of-freedom — the number of
independent joints) limb that reaches for and places items. A "cobot"
is a *collaborative* robot designed to work safely near people. The arm
feeds the integrator and is what MoveIt 2 plans motions for in our
stack.

### Public

- **Universal Robots (owned by Teradyne, NYSE: TER)** — The market-
  defining cobot maker (UR3/UR5/UR10/UR20). Commands a very large share
  of the global cobot market. **Deep pure-play cobot leader**, now a
  Teradyne subsidiary. A top candidate for the arm in our robot.

- **FANUC (TSE: 6954)** — Also makes cobots (CRX series) and a huge range
  of industrial arms. **Deep, fully integrated** arm maker (see layer 1).

- **Yaskawa Electric (TSE: 6506)** — Motoman arms plus the HC series of
  cobots. **Deep, vertically integrated** arm maker.

- **ABB (SIX: ABBN)** — Makes the GoFa and YuMi cobots plus a full
  industrial line. **Deep** arm supplier within the broader ABB
  automation business.

- **Kawasaki Heavy Industries (TSE: 7012)** — Long-standing industrial
  arm maker with the duAro cobot line. Arms are **one division** of a
  heavy-industry conglomerate (ships, trains, engines).

- **Estun Automation (SHE: 002747)** — Chinese arm and motion-control
  maker, growing fast in cobots and industrial robots. **Increasingly
  pure-play** robotics, with strong in-house motion-control.

### Private (not yet public)

- **Doosan Robotics (KOSPI: 454910)** — South Korean cobot maker; note
  it **IPO'd in late 2023**, so it is now public — included here because
  it is still sometimes listed as a newcomer. **Pure-play cobot leader**
  in Korea.

- **Franka Robotics (formerly Franka Emika) (private)** — German maker of
  the torque-sensitive Panda/FR3 research arm, a favorite in robot-
  learning labs and tightly integrated with ROS. **Deep, research-
  grade** arm supplier directly relevant to our project.

- **Techman Robot (private — verify status)** — Taiwanese cobot maker
  (backed by Quanta) with built-in vision. **Deep pure-play** cobot
  supplier; may be carved out or listed — verify.

- **Standard Bots (private)** — US cobot startup (the RO1 arm) targeting
  affordable, software-defined automation. **Pure-play** cobot maker,
  well-funded as of early 2026.

- **Kassow Robots (private — verify status)** — Danish 7-axis cobot
  maker; partly owned by Bosch. **Pure-play** cobot specialist, now under
  a larger parent.

- **Mecademic (private)** — Maker of ultra-compact precision arms for
  benchtop tasks. **Niche pure-play** arm supplier.

- **AUBO Robotics (private)** — Chinese cobot maker with an open,
  ROS-friendly controller. **Pure-play** cobot supplier relevant to a
  ROS 2 build.

---

## 4. End-effectors / grippers

The **end-effector** is the "hand" — here a **parallel-jaw gripper**
(two fingers that close like a clamp) plus, optionally, suction. This is
the part that actually touches the grocery item; it feeds the arm and is
what our grasping layer (analytical → AnyGrasp) commands.

### Public

- **SMC Corporation (TSE: 6273)** — Global leader in pneumatic
  components, including grippers and actuators. Grippers are **one
  product family** in a vast pneumatics catalog; a major tier-1 supplier.

- **Zimmer Group (private)** — see private list; many gripper leaders are
  private, so the public roster here is thinner.

- **Festo (private)** — see private list (Festo is a private German
  company).

- **Schunk (private)** — see private list (also private).

- **Parker Hannifin (NYSE: PH)** — Motion-and-control conglomerate that
  supplies pneumatic and electric actuation components used in grippers.
  Grippers are a **small slice** of a huge fluid-power business.

- **Emerson Electric (NYSE: EMR)** — Via its automation businesses,
  supplies pneumatic and actuation components feeding gripper makers. A
  **minor, indirect** participant in this layer.

### Private (not yet public)

- **Schunk (private)** — German market leader in robotic grippers and
  clamping technology. **Deep pure-play leader** in end-effectors;
  arguably the reference supplier for a parallel-jaw gripper.

- **Zimmer Group (private)** — German maker of a broad range of robotic
  grippers (electric and pneumatic). **Deep pure-play** gripper
  specialist.

- **OnRobot (private)** — Danish company built specifically to make
  plug-and-play end-effectors (grippers, vacuum, force sensors) for
  cobots. **Pure-play** end-effector supplier, perfectly matched to a
  UR-style arm.

- **Robotiq (private)** — Canadian maker of the widely used 2F-85
  parallel-jaw gripper and force-torque sensors, deeply integrated with
  Universal Robots and ROS. **Deep pure-play** and **highly relevant** to
  our exact gripper choice.

- **Festo (private)** — German automation house with extensive grippers
  and pneumatic hands, plus research into adaptive/soft grippers.
  **Broad pure-play** in actuation and gripping.

- **Soft Robotics Inc. (private — verify status)** — Pioneer of
  food-safe soft (compliant) grippers for handling delicate, varied
  items — very relevant to groceries. **Niche pure-play**; verify
  current status as it has restructured.

- **Wonik Robotics / Allegro Hand (private)** — Korean maker of
  multi-fingered dexterous hands used in research. **Niche pure-play**
  for advanced grasping (a later-milestone option, not v1).

- **Sake Robotics / SAKE (private)** — Maker of the EZGripper used widely
  in ROS research. **Small niche** supplier relevant to a v1 prototype.

---

## 5. Actuators, servo motors, harmonic drives & gearboxes

This is what makes joints **move and hold position precisely**. A
**servo motor** is a motor with feedback so it can hit an exact angle; a
**harmonic drive** is a compact, near-zero-backlash gearbox that is the
heart of most robot joints. These parts feed the arm, the gripper, and
the wheels above.

### Public

- **Harmonic Drive Systems (TSE: 6324)** — The company that
  commercialized the harmonic (strain-wave) gear; the dominant name in
  high-precision robot-joint gearboxes. **Deep pure-play leader** —
  arguably the single most important supplier in this layer.

- **Nabtesco (TSE: 6268)** — Leading maker of RV cycloidal gears used in
  the large joints of industrial robots. **Deep pure-play leader** in
  precision reduction gears, complementary to Harmonic Drive.

- **Nidec (TSE: 6594; ADR: NJDCY)** — The world's largest maker of
  precision motors, including servo and reduction-gear products. **Deep,
  broad** motor supplier; motors are its core business.

- **Yaskawa Electric (TSE: 6506)** — A top global servo-motor and drive
  maker (it also makes the arms above). **Deep, vertically integrated**
  in servo drives.

- **Mitsubishi Electric (TSE: 6503)** — Major servo-motor, drive, and
  factory-automation supplier. Servos are **one large division** of a
  diversified electronics conglomerate.

- **Sumitomo Heavy Industries (TSE: 6302)** — Maker of precision
  cycloidal gearboxes (Cyclo drives). Precision gearing is **one
  business line** within a heavy-industry group.

### Private (not yet public)

- **maxon (private)** — Swiss maker of high-precision brushless DC motors
  and drives (its motors famously ran on Mars rovers). **Deep pure-play**
  precision-motor supplier, common in research arms and grippers.

- **Faulhaber (private)** — German maker of miniature precision motors
  and micro-drives. **Pure-play** small-motor specialist, used in
  grippers and small joints.

- **Leaderdrive / Leadereo (private)** — Chinese maker of harmonic
  (strain-wave) gears, a fast-growing challenger to Harmonic Drive
  Systems. **Pure-play** precision-gear supplier; verify exact corporate
  name/listing status.

- **Tianjin LISN / Laifual (private)** — Chinese harmonic-gear makers
  scaling for the robotics boom. **Pure-play** gear suppliers; status and
  naming vary, so verify.

- **Kollmorgen (part of Regal Rexnord, NYSE: RRX)** — Maker of servo
  motors and frameless "direct-drive" motors used in robot joints.
  **Deep** servo specialist, now inside a public parent.

- **Sensata / Dynapar and similar encoder makers (mixed)** — Encoders
  (the position sensors inside servos) are supplied by firms like Heidenhain
  (private) and Renishaw (LSE: RSW). **Tier-2 component** suppliers feeding
  the motor makers above.

- **Genesis Robotics / Quasi-Direct-Drive startups (private)** — Several
  startups build integrated "actuator modules" (motor + gearbox +
  encoder + driver in one unit) aimed at humanoids and cobots.
  **Emerging pure-plays** worth watching; verify individual status.

---

## 6. Depth cameras & vision sensors (RGB-D)

An **RGB-D camera** captures a normal color image plus a per-pixel
**depth** map (how far away each point is) — this is how the robot sees
the 3-D shape of a grocery item. It feeds the perception layer
(FoundationPose / geometric) in our stack.

### Public

- **Intel (NASDAQ: INTC)** — Makes the **RealSense** depth cameras (e.g.
  D435/D455) that are the default RGB-D sensor in countless ROS
  projects. Note Intel has spun RealSense toward an independent entity;
  the cameras are **directly relevant** to our build, but a tiny part of
  Intel's chip business.

- **Microsoft (NASDAQ: MSFT)** — Made the original Kinect and the Azure
  Kinect DK depth camera (now wound down). A **historically pivotal** but
  no-longer-core depth-camera player.

- **Sony (TSE: 6758; NYSE: SONY)** — Dominant maker of the **image
  sensors** inside most cameras (including depth cameras) and of
  time-of-flight depth chips. **Deep, foundational** sensor supplier —
  it sits *below* most camera brands.

- **OMRON (TSE: 6645)** — Makes industrial 3-D vision and sensing
  systems for automation. **One division** of a broad automation company.

- **Cognex (NASDAQ: CGNX)** — Machine-vision leader (2-D and 3-D) for
  industrial inspection and guidance. **Deep pure-play** in industrial
  vision, adjacent to depth sensing.

- **Teledyne (NYSE: TDY)** — Owns FLIR and a broad imaging portfolio,
  including 3-D and machine-vision cameras. Vision is **one large
  segment** of a diversified instruments company.

### Private (not yet public)

- **Orbbec (private — verify status)** — Chinese maker of low-cost RGB-D
  cameras (Astra, Femto) widely used in robotics; partners with the
  RealSense ecosystem. **Deep pure-play** depth-camera supplier; may have
  listed, so verify.

- **Stereolabs (private)** — Maker of the **ZED** stereo depth cameras
  popular in outdoor/mobile robotics and tightly integrated with NVIDIA
  Jetson. **Pure-play** depth-camera supplier, very relevant to our base.

- **Zivid (private)** — Norwegian maker of high-accuracy industrial 3-D
  color cameras built for bin-picking and precise grasping. **Pure-play**
  and **highly relevant** to accurate grocery-item pose estimation.

- **Photoneo (private — verify status)** — Slovak maker of high-end
  structured-light 3-D scanners for robotic picking. **Deep pure-play**
  in industrial 3-D vision; may have been acquired (verify).

- **Mech-Mind Robotics (private)** — Chinese maker of 3-D cameras *plus*
  the perception software for bin-picking. **Deep pure-play** that
  straddles this layer and the perception-software layer.

- **Roboception (private)** — German maker of stereo 3-D sensors with
  on-board pose estimation, designed for ROS. **Niche pure-play**
  directly aligned with our perception stack.

- **Framos (private)** — Supplier and integrator of imaging components
  and depth modules (including RealSense distribution). **Tier-2**
  enabler that connects sensor chips to camera builders.

---

## 7. Lidar & range sensors

**Lidar** ("light radar") spins a laser to measure distances all around
the robot, building a 2-D or 3-D map for safe navigation. Our base uses
lidar (or similar range sensors) so Nav2 can avoid people and obstacles
in store aisles.

### Public

- **Hesai Group (NASDAQ: HSAI; HKEX: 2525)** — The global volume leader
  in lidar, strong in both automotive and robotics. **Deep pure-play
  lidar leader**; dual-listed.

- **Ouster (NASDAQ: OUST)** — US maker of digital spinning lidar widely
  used in robotics, AMRs, and industrial sensing (merged with Velodyne).
  **Deep pure-play** lidar supplier, very relevant to mobile robots.

- **RoboSense / LDROBOT (HKEX: 01236)** — Chinese lidar maker that
  **IPO'd in 2026** on the Hong Kong main board; strong in both auto and
  robotics lidar. **Deep pure-play** lidar leader.

- **Innoviz Technologies (NASDAQ: INVZ)** — Israeli automotive-grade
  lidar maker. **Pure-play** lidar, more auto-focused but technically
  relevant.

- **Aeva Technologies (NASDAQ: AEVA)** — Maker of FMCW lidar that also
  measures velocity per point. **Pure-play** lidar with a differentiated
  approach.

- **SICK AG (XETRA: SICK)** — German industrial-sensor giant; its 2-D
  safety laser scanners are the **workhorse** for indoor AMR navigation
  and safety. **Deep, directly relevant** — a 2-D SICK scanner is a very
  likely choice for our base.

### Private (not yet public)

- **Hokuyo (private)** — Japanese maker of compact 2-D laser scanners
  (URG/UST series) that are a **staple of ROS mobile robots**. **Deep
  pure-play** and extremely relevant to a low-cost shelf-stocking base.

- **Slamtec (private — verify status)** — Chinese maker of low-cost
  RPLIDAR spinning sensors ubiquitous in hobby/educational and
  light-industrial ROS robots. **Pure-play**, perfect for a v1
  prototype; verify listing status.

- **Livox (private)** — Lidar arm associated with DJI, known for
  low-cost solid-state-style lidar. **Pure-play** lidar supplier under a
  larger drone parent.

- **Quanergy (private — verify status)** — Solid-state lidar maker; went
  public then bankrupt then restructured, so its status is uncertain —
  verify. Historically a **pure-play** lidar firm.

- **Cepton (private — verify status)** — Lidar maker; was public, with
  Koito (a Japanese auto-lighting firm) taking a majority/buyout stake,
  so it may now be effectively private — verify. **Pure-play** lidar.

- **Pepperl+Fuchs (private)** — German industrial-sensor maker with laser
  scanners and proximity sensors for factory automation. **Broad
  pure-play** in industrial sensing.

- **Leddartech / Opsys / other solid-state startups (mixed)** — A cluster
  of startups chasing cheaper solid-state lidar. **Emerging pure-plays**;
  verify each one's status individually.

---

## 8. Onboard compute / edge-AI modules & GPUs

This is the robot's **brain**: the computer that runs ROS 2, the
perception models, and the planning. "Edge AI" means running AI on the
robot itself rather than in the cloud. A **GPU** is a chip that runs many
calculations in parallel, which is what neural-net perception needs. This
layer feeds everything that thinks.

### Public

- **NVIDIA (NASDAQ: NVDA)** — Makes the **Jetson** edge modules (Orin,
  and newer Thor) that are the default robot brain, plus the GPUs used to
  *train* the models and run Isaac Sim. **Deep, dominant** in this layer
  — and it reappears in the software/simulation layer below, so note the
  overlap.

- **Qualcomm (NASDAQ: QCOM)** — Makes robotics/edge SoCs (the RB-series
  platforms) combining CPU, GPU, and AI accelerators. **Deep** edge-
  compute supplier; a credible alternative brain for a mobile robot.

- **Intel (NASDAQ: INTC)** — CPUs, plus Movidius/edge-AI accelerators
  and the GPU line. **Broad** compute supplier (and the RealSense
  heritage above), though it trails NVIDIA in robot edge AI.

- **Advanced Micro Devices (NASDAQ: AMD)** — CPUs, GPUs, and (via Xilinx)
  the FPGAs/adaptive SoCs used in real-time robot control. **Deep, broad**
  compute supplier; the Xilinx parts are common in motor-control boards.

- **Texas Instruments (NASDAQ: TXN)** — Makes the real-time
  microcontrollers and processors that handle low-level motor and sensor
  control beneath the main GPU. **Deep, foundational** in the embedded
  control sub-layer.

- **NXP Semiconductors (NASDAQ: NXPI)** — Microcontrollers and processors
  for real-time and safety-rated robot control. **Deep** embedded-control
  supplier.

### Private (not yet public)

- **Hailo (private)** — Israeli maker of efficient edge-AI accelerator
  chips for running neural nets at low power. **Pure-play** edge-AI
  silicon, a possible perception accelerator for our robot.

- **SiMa.ai (private)** — Maker of low-power "MLSoC" chips for embedded
  AI at the edge. **Pure-play** edge-AI silicon startup.

- **Axelera AI (private)** — European edge-AI inference chip startup.
  **Pure-play** edge accelerator.

- **Advantech (TWSE: 2395)** — Note this is actually **public** in
  Taiwan; it makes rugged industrial PCs and edge boxes used as robot
  controllers. **Deep** industrial-compute supplier (listed — included
  here for completeness).

- **AAEON (private — part of Asus group)** — Maker of rugged single-board
  computers and edge-AI carriers (often pairing NVIDIA Jetson). **Tier-2
  integrator** that turns chips into robot-ready boards.

- **Connect Tech (private)** — Canadian maker of Jetson carrier boards
  and rugged enclosures for robots. **Niche pure-play** that packages
  NVIDIA modules for real robots — directly relevant.

- **Tenstorrent (private)** — AI-compute startup building processors and
  IP for training and inference. **Emerging pure-play** in AI silicon.

---

## 9. Semiconductors / foundries / core ICs

Below the compute modules sit the companies that actually **fabricate
the chips** and supply the core building blocks. A **foundry** is a
factory that manufactures chips designed by others. This is the deepest
"silicon" layer — everything above ultimately depends on it.

### Public

- **TSMC (TWSE: 2330; NYSE: TSM)** — The world's largest contract chip
  foundry; it physically makes the leading-edge chips that NVIDIA,
  Qualcomm, AMD, and others design. **Deep, foundational, near-
  irreplaceable** — almost every smart part in the robot traces back
  here.

- **ASML (Euronext: ASML; NASDAQ: ASML)** — Dutch maker of the EUV
  lithography machines that foundries *must* have to print advanced
  chips. **A monopoly-like keystone** one layer below even TSMC.

- **Samsung Electronics (KRX: 005930)** — A foundry and a top maker of
  memory (DRAM/flash) and image sensors. **Deep, broad** — competes with
  TSMC in fabrication and supplies memory to the robot's compute.

- **STMicroelectronics (NYSE: STM; Euronext: STMPA)** — Maker of
  microcontrollers, motor drivers, MEMS sensors (IMUs), and power chips
  used throughout a robot. **Deep, broad** supplier of the "glue"
  silicon.

- **Infineon Technologies (XETRA: IFX)** — Leader in power semiconductors
  and motor-drive ICs — the chips that actually switch current to the
  motors. **Deep** in the power/motor-control sub-layer.

- **Analog Devices (NASDAQ: ADI)** — Maker of high-precision analog,
  data-converter, and sensor-interface chips (e.g., for encoders and
  IMUs). **Deep** in the signal-chain sub-layer.

- **Arm Holdings (NASDAQ: ARM)** — Licenses the CPU architecture inside
  nearly every robot SoC (Jetson, Qualcomm). Not a chipmaker itself — a
  **deep, foundational IP** layer beneath the chips. (Public since 2023.)

- **GlobalFoundries (NASDAQ: GFS)** — A major foundry for mature-node
  chips (power, analog, microcontrollers) that a robot uses by the
  dozen. **Deep** foundry.

- **SMIC (HKEX: 0981; SSE: 688981)** — China's largest foundry; relevant
  to the China-based supply chains feeding many robot parts.

- **Tower Semiconductor (NASDAQ: TSEM)** — Specialty foundry for the
  analog and sensor chips that fill out a robot's electronics. **Niche
  foundry.**

- **ASE (NYSE: ASX) and Amkor (NASDAQ: AMKR)** — The big "OSAT"
  assembly-and-test houses that package and test finished chips — the
  **tier-2 back-end** between the foundry and the board.

### Private (not yet public)

- **SiFive (private)** — Designs **RISC-V** CPU cores, an open-standard
  alternative to Arm increasingly used in embedded controllers. A
  genuinely private core-IP **pure-play.**

- **Imagination Technologies (private)** — UK GPU/AI-IP designer, taken
  private; its cores appear in some edge chips. **Tier-2 IP** supplier.

- **Tenstorrent (private)** — AI-chip startup (RISC-V + AI accelerators,
  led by chip architect Jim Keller) aimed at training and edge
  inference. **Pure-play** AI-silicon challenger.

- **Groq (private)** — AI-inference-chip startup; mostly data-center
  today but relevant as inference silicon matures toward the edge.
  **Pure-play** AI silicon.

- **d-Matrix / Untether AI (private)** — Energy-efficient AI-inference
  silicon startups; upstream **pure-plays** that could feed future robot
  compute.

- **Black Semiconductor (private)** — German graphene chip-interconnect
  startup; a frontier **pure-play**, far upstream.

---

## 10. Batteries & power systems

A mobile robot needs to carry its own energy. This layer makes the
**battery cells**, the **battery-management system** (the electronics
that keep cells safe and balanced), and the power conversion that feeds
the motors and compute. It feeds the mobile base above.

### Public

- **Panasonic (TSE: 6752)** — Major lithium-ion cell maker (notably for
  Tesla) and broad electronics supplier. **Deep** cell supplier, though
  batteries are one part of a huge conglomerate.

- **Samsung SDI (KRX: 006400)** — Top-tier lithium-ion cell maker for
  EVs, tools, and industrial robots. **Deep pure-play-ish** battery
  maker within the Samsung group.

- **LG Energy Solution (KRX: 373220)** — One of the largest battery cell
  makers globally. **Deep pure-play** battery manufacturer.

- **CATL (SZSE: 300750)** — The world's largest lithium-ion battery
  maker; also a leader in LFP chemistry well-suited to robots/AMRs.
  **Deep pure-play global leader**.

- **BYD (HKEX: 1211; SZSE: 002594)** — Major battery and EV maker; its
  Blade LFP cells are used well beyond cars. **Deep** battery maker
  within a broader auto/electronics group.

- **Amprius Technologies (NYSE: AMPX)** — Maker of high-energy
  silicon-anode cells for lighter, denser packs. A **pure-play**
  advanced-cell company. (Public.)

- **Vicor (NASDAQ: VICR)** — Maker of high-density power-conversion
  modules (DC-DC) that turn battery voltage into what the motors and
  compute actually need. **Deep** power-electronics supplier. (Public.)

### Private (not yet public)

- **Inventus Power (private)** — US maker of complete battery packs and
  battery-management systems for industrial/mobile robots. **Deep
  pure-play** at the *pack* level — which is what a robot actually buys.

- **RRC Power Solutions (private)** — Maker of smart battery packs and
  chargers for professional mobile equipment, including robots. **Pure-
  play** pack supplier.

- **Northvolt (private — verify status)** — European battery-cell maker
  that hit severe financial distress and restructuring, so its status is
  uncertain as of early 2026 — verify. A cautionary tale for how volatile
  this layer is.

- **Our Next Energy / ONE (private)** — US battery-pack and cell startup.
  **Pure-play** energy-storage challenger.

- **Forge Nano / Sila Nanotechnologies (private)** — Advanced battery-
  materials and silicon-anode startups feeding the cell makers above.
  **Tier-2 materials** pure-plays.

- **Bren-Tronics (private)** — US maker of rugged rechargeable battery
  packs and chargers for demanding mobile-power needs. **Pure-play** in
  mobile power.

---

## 11. Robotics software, middleware, simulation & AI models

This is the **non-physical** layer: the operating framework (ROS 2),
the simulator (Gazebo/Isaac Sim), the navigation/motion/perception
libraries, and the AI "policies" that decide how to grasp. It is the
layer our whole project lives in. It feeds the integrator at the top by
turning hardware into behavior.

### Public

- **NVIDIA (NASDAQ: NVDA)** — Makes **Isaac Sim** and the Isaac robotics
  stack (and the GPUs that run them) — our recommended simulator at
  scale. **Deep, dominant** in robotics simulation and AI tooling
  (overlaps with the compute layer above).

- **Microsoft (NASDAQ: MSFT)** — Cloud, dev tools, and (historically) a
  robotics simulator (AirSim). Also a major investor in AI-model labs.
  **Broad** enabler rather than a pure-play robotics-software firm.

- **Alphabet / Google (NASDAQ: GOOGL)** — Through **Intrinsic** (its
  robotics-software subsidiary) and **DeepMind** (robotics foundation
  models / VLAs). **Deep** in robotics software and AI policy, but inside
  a giant — note the overlap with cloud below.

- **PTC (NASDAQ: PTC)** — CAD/PLM and IoT software; relevant to
  digital-twin and design workflows around robots. **Adjacent** software
  supplier.

- **Siemens (XETRA: SIE)** — Owns the **Tecnomatix/Process Simulate** and
  broader digital-factory software, plus PLC automation. **Deep** in
  industrial simulation and control software (overlaps cloud/twin below).

### Private (not yet public)

- **Open Source Robotics Foundation / Open Robotics (non-profit)** —
  Stewards **ROS 2** and **Gazebo**, the open middleware and simulator at
  the center of our stack. **The foundational steward**, not a for-profit
  vendor — but the single most important name in this layer.

- **Intrinsic (private — Alphabet subsidiary)** — Builds developer tools
  and foundation-model-driven manipulation software for robot arms
  (partnered with NVIDIA on Isaac Manipulator). **Deep pure-play**
  robotics software, inside Alphabet.

- **Physical Intelligence (private)** — Builds general-purpose
  vision-language-action (VLA) "robot brain" models (π0 / π0.5). **Deep
  pure-play** in robot foundation models; reportedly raising at an
  ~$11B+ valuation as of early 2026.

- **Skild AI (private)** — Building an "omni-bodied" foundation model to
  control many robot bodies; raised ~$1.4B in early 2026. **Deep
  pure-play** robot-AI model lab.

- **Figure AI (private)** — Humanoid OEM that also builds its own
  end-to-end manipulation AI (Helix). **Deep** in robot AI; ~$39B
  valuation as of late 2025 — a possible IPO candidate, still private.

- **Foxglove (private)** — Maker of the leading data/observability
  platform for robotics (visualizing and curating robot data). **Pure-
  play** robot-software-infrastructure startup; raised a ~$40M Series B.

- **Wandelbots (private)** — German robotics-software firm for
  simulating, programming, and operating arms (now software-only after
  exiting hardware). **Pure-play** robot software.

- **PickNik Robotics (private)** — The commercial maintainer of
  **MoveIt 2**, the arm-motion-planning framework in our stack. **Deep,
  directly relevant pure-play** — they support the exact library our arm
  uses.

---

## 12. Cloud / fleet-management / digital-twin platforms

Once robots are deployed, this layer **runs the fleet**: it monitors
many robots, pushes software updates, and keeps a **digital twin** (a
live virtual copy) of the operation. It feeds the integrator's product
as the "operations" backend and connects back to the simulation layer.

### Public

- **Amazon / AWS (NASDAQ: AMZN)** — Cloud robotics services and fleet
  tooling, plus huge internal robotics deployments. **Deep, broad**
  cloud backbone; robotics is one workload among many.

- **Microsoft / Azure (NASDAQ: MSFT)** — Cloud, IoT Hub, and digital-twin
  services used to manage robot fleets. **Deep, broad** cloud platform.

- **Alphabet / Google Cloud (NASDAQ: GOOGL)** — Cloud and AI services for
  fleet data and model serving. **Deep, broad** cloud platform (overlaps
  the software layer).

- **Siemens (XETRA: SIE)** — Its Xcelerator/Insights and digital-twin
  software manage industrial assets including robots. **Deep** in
  industrial digital twins.

- **Dassault Systèmes (Euronext: DSY)** — Maker of the 3DEXPERIENCE /
  DELMIA platform for simulating and operating factory and robot
  systems. **Deep pure-play** in industrial twin/simulation software.

### Private (not yet public)

- **Formant (private)** — Cloud platform purpose-built for observing and
  operating robot fleets. **Pure-play** fleet-ops software, directly
  relevant to deploying our robot at many stores.

- **InOrbit (private)** — Cloud robot-operations and fleet-management
  platform (RobOps). **Pure-play** fleet-management startup.

- **Freedom Robotics (private — verify status)** — Robot monitoring and
  fleet-management software; verify current status (acquisition rumored).
  **Pure-play** fleet ops.

- **Rocos (private — acquired)** — Robot fleet-operations platform,
  acquired by Boston Dynamics. **Pure-play** heritage, now inside an OEM.

- **Foxglove (private)** — Also fits here for its fleet-data platform
  (see software layer). **Pure-play** robot-data infrastructure.

- **Viam (private)** — Platform that unifies robot configuration, data,
  and fleet management across hardware. **Pure-play** robot-platform
  startup.

- **Cogniteam / others (private)** — Cloud robot management and
  orchestration startups. **Niche pure-plays**; verify each.

---

## 13. Mechanical components (bearings, structural, connectors, PCBs)

The "boring but essential" hardware: **bearings** (let joints spin
smoothly), structural frames and aluminum extrusion, **connectors** and
cabling, and the **PCBs** (printed circuit boards) that hold the
electronics. These tier-2 parts feed every physical layer above.

### Public

- **SKF (OMX: SKF B)** — Swedish global leader in bearings. **Deep
  pure-play** in a component every robot joint and wheel needs.

- **Schaeffler (XETRA: SHA)** — German bearings and precision-mechanical
  components (INA/FAG brands). **Deep pure-play** bearings/mechatronics
  supplier.

- **NSK (TSE: 6471)** — Major Japanese bearing and linear-motion maker.
  **Deep pure-play** in bearings and ball screws used in arms.

- **TE Connectivity (NYSE: TEL)** — Global leader in connectors and
  sensors — the plugs and harnesses tying a robot together. **Deep
  pure-play** in interconnect.

- **Amphenol (NYSE: APH)** — Major connector and interconnect maker.
  **Deep pure-play** in connectors/cabling.

- **THK (TSE: 6481)** — Maker of linear guides and ball screws central to
  precise linear motion. **Deep pure-play** in linear-motion components.

- **Hiwin (TWSE: 2049)** — Maker of linear guides, ball screws, and even
  complete robots. **Deep pure-play** motion-component supplier. (Public
  in Taiwan.)

- **Misumi Group (TSE: 9962)** — Vast catalog supplier of configurable
  mechanical parts and aluminum framing used to build and prototype robot
  structures. **Deep** configurable-parts supplier. (Public.)

- **TTM Technologies (NASDAQ: TTMI)** — Maker of the bare **PCBs** that
  all robot electronics are built on. **Deep pure-play** board maker.
  (Public.)

### Private (not yet public)

- **igus (private; family-owned)** — German maker of polymer bearings,
  cable carriers ("energy chains"), and low-cost robot components —
  directly relevant for affordable builds. **Deep pure-play**
  motion-plastics specialist.

- **Bosch Rexroth (private; part of Bosch)** — Linear motion, aluminum
  framing, and drive technology; a large, privately/foundation-held
  motion supplier.

- **Harting (private; family-owned)** — German maker of heavy-duty
  industrial connectors. **Deep pure-play** interconnect.

- **Phoenix Contact (private; family-owned)** — German maker of terminal
  blocks, connectors, and control components for robot cabinets. **Deep
  pure-play** electrical-connection specialist.

- **80/20 Inc. (private)** — US maker of T-slot aluminum extrusion used
  to build robot frames and fixtures. **Niche pure-play** structural
  supplier, common in prototypes.

- **Bishop-Wisecarver (private)** — US maker of guide-wheel and
  linear-motion systems. **Niche pure-play** motion components.

- **Würth Group (private; family-owned)** — Giant German distributor of
  fasteners, connectors, and assembly materials — the bolts-and-screws
  backbone. **Broad** mechanical supplier.

---

## 14. Foundational raw materials & contract manufacturing (EMS)

The **bottom** of the chain: the raw inputs (especially **rare-earth
magnets** for motors, plus copper, aluminum, lithium, silicon) and the
**EMS** (Electronics Manufacturing Services) firms that assemble
finished boards and products at volume for everyone above.

### Public — raw materials

- **MP Materials (NYSE: MP)** — US rare-earth miner and (increasingly)
  magnet maker. **Deep pure-play** in the rare-earth magnets that every
  servo motor depends on; strategically important for non-China supply.

- **Lynas Rare Earths (ASX: LYC)** — Australian rare-earth miner and
  processor, the largest outside China. **Deep pure-play** rare-earth
  supplier.

- **Albemarle (NYSE: ALB)** — Major lithium producer feeding the battery
  layer. **Deep pure-play** in lithium chemicals.

- **Freeport-McMoRan (NYSE: FCX)** — Major copper miner; copper is in
  every motor winding and wire. **Deep pure-play** copper supplier.

- **Shin-Etsu Chemical (TSE: 4063)** — World's largest maker of
  silicon wafers (the base of every chip) and a major rare-earth-magnet
  maker. **Deep, foundational** at the very bottom of the silicon and
  magnet chains.

### Public — contract manufacturing (EMS)

- **Foxconn / Hon Hai Precision (TWSE: 2317)** — The world's largest EMS;
  assembles electronics and is pushing into robot manufacturing itself.
  **Deep, dominant** contract manufacturer — it could physically build
  robots like ours at scale.

- **Jabil (NYSE: JBL)** — Global EMS provider that assembles complex
  electromechanical products, including robots. **Deep pure-play** EMS.

- **Flex Ltd (NASDAQ: FLEX)** — Major EMS and design-manufacturing
  partner. **Deep pure-play** EMS that often co-designs and builds
  hardware products.

- **Benchmark Electronics (NYSE: BHE)** — EMS provider for complex and
  regulated hardware. **Pure-play** contract manufacturer.

- **Kimball Electronics (NASDAQ: KE)** — EMS for industrial and medical
  electronics. **Pure-play** contract manufacturer.

### Private (not yet public)

- **Proterial (formerly Hitachi Metals) (private — verify status)** —
  Leading maker of high-performance neodymium magnets; taken private in a
  Bain-led buyout, so verify. **Deep** magnet supplier feeding the motor
  layer.

- **Vacuumschmelze / VAC (private)** — German maker of advanced magnetic
  materials and finished magnets for motors. **Deep pure-play**
  magnet-materials supplier — directly upstream of every servo motor.

- **Arnold Magnetic Technologies (private)** — US specialist maker of
  high-performance permanent magnets for motors. **Tier-2** magnet
  pure-play.

- **Niron Magnetics (private)** — US startup developing **rare-earth-free**
  (iron-nitride) permanent magnets — a potential way to de-risk the
  magnet bottleneck for future robot motors. **Pure-play** materials
  startup.

- **USA Rare Earth (private — verify status)** — US rare-earth and magnet
  startup building domestic magnet capacity; may have listed, so verify.
  **Pure-play** magnet-supply hopeful.

- **Zollner Elektronik (private)** — Large German private EMS firm.
  **Deep pure-play** contract manufacturer, common for European
  industrial hardware.

- **Regional EMS shops & job-machine shops (private)** — The long tail of
  smaller private contract manufacturers and metal/casting shops that
  build low-to-mid-volume robots — the realistic first manufacturing
  partner for an early-stage robot startup.

---

## How this maps to our stack

Each layer above plugs into a specific part of our project:

- **Layer 1 (integrators)** is the role *we* would play if we built and
  sold the finished shelf-stocking robot — assembling everyone below.
- **Layer 2 (mobile base)** is what **Nav2** drives; an AMR from MiR,
  Clearpath, or similar is the candidate body.
- **Layer 3 (arms)** is what **MoveIt 2** plans motions for; a Universal
  Robots or Franka arm is the candidate limb.
- **Layer 4 (grippers)** is what our **grasping layer** (analytical →
  AnyGrasp) commands; a Robotiq or Schunk parallel-jaw gripper fits v1.
- **Layers 5 (actuators) + 13 (mechanical) + 14 (materials)** are inside
  the arm and base — we buy them indirectly, bundled into the hardware.
- **Layers 6–7 (RGB-D + lidar)** feed our **perception** layer
  (FoundationPose / geometric) and Nav2's obstacle avoidance.
- **Layer 8 (compute)** runs the whole **ROS 2** stack on the robot — a
  NVIDIA Jetson is the default brain.
- **Layer 9 (semiconductors)** is what every smart part is ultimately
  made of.
- **Layer 10 (batteries)** powers the mobile base.
- **Layer 11 (software/sim/AI)** *is* our stack — ROS 2, Gazebo/Isaac
  Sim, Nav2, MoveIt 2, perception, grasping, behavior-tree
  orchestration.
- **Layer 12 (cloud/fleet/twin)** is how we would operate many robots
  across many stores after deployment, and it loops back to the
  simulation work in `01-simulation`.

Keep the v1 framing in mind: for a first build we lean on **off-the-
shelf** parts from these layers (see `04-off-the-shelf-hardware.md`)
rather than designing anything custom this deep in the chain.

> **Disclaimer (read last).** Everything above — tickers, exchanges,
> "public vs. private" labels, valuations, and ownership — drifts and was
> accurate only to roughly **early 2026**. Several companies are likely
> to IPO, be acquired, or change names soon. Always re-verify before
> quoting any figure or making a decision based on it.
