# Basic experimental hardware — a < $500 home rig

> **Job:** the cheapest, lightest real-world setup that lets you prove
> the *place-on-shelf* idea on your desk at home — pick a light object
> from a tray and set it on a shelf — using hobby parts that total
> **under ~$500**. This is a sanity check in the physical world, not a
> product. The serious work still happens in simulation first (see
> `03-high-level-tech.md`); this rig just lets you feel the real-world
> problems (calibration, grasp slippage, depth noise) cheaply.

New to a term (DoF, RGB-D, gripper, payload)? See `02-glossary.md`.

> **Prices are approximate (`~`) and drift.** They were spot-checked
> around mid-2026 from hobby vendors (Seeed Studio, Hiwonder, Luxonis,
> Amazon/AliExpress) and must be re-checked before you buy. Shipping and
> taxes are extra. Hedge everything.

---

## The trick that keeps it under $500

The single biggest cost saver: **use a laptop you already own as the
brain** (compute = $0) and **keep the arm bolted to the table** for the
first milestone. A wheeled base is the heaviest, most expensive, most
"tippy" part — and you don't need it to prove a *placement*. Move the
**tray and the shelf** around the fixed arm instead of moving the robot.
Add mobility later, only once the pick-and-place itself works.

So the recommended first build is a **fixed tabletop arm + a camera +
your laptop + a cardboard shelf** — roughly **$150–300 all in**. The
sections below give you choices for each part, then three complete
builds.

---

## 1. The arm (the one part worth spending on)

This is the heart of the rig: a small 6-DoF (six-joint) servo arm with a
gripper. Hobby arms use **serial-bus servos** (small geared motors
chained on one wire) — light, cheap, and good enough to lift a ~100–300 g
object like an empty can or a small box.

| Option | ~Price | DoF / payload | Software | Bottom line |
|--------|--------|---------------|----------|-------------|
| **SO-ARM100 / SO-ARM101** (Seeed / TheRobotStudio) | ~$120–150 single arm (servo kit; +~$35 printed parts, or print your own) | 6-DoF, ~?100–250 g | **LeRobot** (Hugging Face), ROS 2 community drivers | **Best pick.** Open-source, AI-ready, huge community, designed for exactly this kind of learning. Gripper included. |
| **Hiwonder xArm 1S / LeArm** | ~$110–150 | 5–6 servos, ~?100 g | Hiwonder SDK, Python; ROS 2 via community | Cheapest "just works" arm; metal gripper included; great for a first try. |
| **LewanSoul 6-DoF kit** | ~$150–180 | 6-DoF, ~?100 g | Arduino/Python | Same family as Hiwonder; well-documented, lots of tutorials. |
| **Elephant myCobot 280** | ~$700 (**over budget**) | 6-DoF, ~250 g | First-class ROS 2 / MoveIt | The "real" cobot experience, but blows the whole budget alone — mention only as a stretch upgrade. |

**Pick for v1:** the **SO-ARM101** if you want the AI/imitation-learning
path and an active community; the **Hiwonder xArm 1S** if you want the
absolute cheapest thing that grips and moves today. Both ship with a
gripper, so you usually don't buy one separately.

---

## 2. The gripper (usually already included)

The arm kits above come with a simple **parallel-ish servo gripper** —
two fingers that pinch — which is exactly right for a rigid test object
(an empty soup can, a small cereal box). You normally don't need to buy a
separate gripper. If you want to experiment:

- **Stock servo gripper** (included) — ~$0 extra. Fine for cans/boxes.
- **3D-printed fingertips** — ~$0–10 of filament. Add rubber/foam pads
  for grip; the cheapest way to improve reliability.
- **Tiny suction setup** — a 6 V vacuum pump + cup, ~$15–25. Good for
  flat-topped boxes; mirrors the "suction for flat items" idea in the
  real grasping layer (`03-stack/06-grasping.md`).

---

## 3. The "eyes" (camera / perception)

The arm needs to *see* the object and the shelf slot. Two honest tiers:

| Option | ~Price | Gives you | Bottom line |
|--------|--------|-----------|-------------|
| **A plain USB webcam** (or your phone as a webcam) | ~$0–40 | Color image only (2-D) | Start here. With a **known, fixed object** and a marker (e.g. an AprilTag/QR sticker) you can estimate pose well enough to place. Matches the "geometric / known-pose first" v1 framing. |
| **Luxonis OAK-D Lite** | ~$149 | **Depth + on-camera AI** over USB | The big upgrade: real RGB-D depth and object detection on the camera itself, so your laptop does less. Closest cheap stand-in for the project's RGB-D camera. |
| **Used Intel RealSense D435** | ~$150–200 (used) | RGB-D depth | Same sensor family the main stack assumes; only worth it if you find one cheap. |
| **Orbbec Gemini 335** | ~$250 (**half the budget**) | High-quality RGB-D | Better data, but eats too much of a $500 budget — skip for v1. |

**Pick for v1:** a **USB webcam + a printed marker** to start (cheapest,
and enough to prove placement with a known object), then add an **OAK-D
Lite** when you want true depth.

---

## 4. The base (optional — skip it first)

You only need this for the *mobility* half of the task, which is **not
required to prove a placement**. When you're ready:

| Option | ~Price | Bottom line |
|--------|--------|-------------|
| **No base (fixed arm)** | $0 | **Recommended for milestone 1.** Move the tray/shelf, not the robot. |
| **2WD/4WD hobby car kit** (acrylic chassis, DC motors, ESP32/Arduino) | ~$30–80 | Cheapest way to add driving; add wheel **encoders** (~$10–20) so it can measure how far it rolled. |
| **Kit with encoders + IMU** | ~$60–120 | Enough to run a basic ROS 2 differential-drive setup (the real-robot analogue of Nav2). |
| **Pre-built small ROS car** (Yahboom/Hiwonder) | ~$200+ | Easier, but combined with an arm it busts the budget and gets heavy/tippy. |

**Caution:** a servo arm is top-heavy. Bolting one onto a tiny car makes
it tip over easily and the small motors struggle with the weight. If you
go mobile, keep the arm small, the base wide, and the speeds low.

---

## 5. The brain (compute)

| Option | ~Price | Bottom line |
|--------|--------|-------------|
| **A laptop you already own** | $0 | **Recommended.** Runs Python / ROS 2, tethered to the arm by USB. Keeps you under budget. |
| **Raspberry Pi 5 (8 GB)** + power + SD | ~$80 + ~$30 | Makes the rig self-contained; needed if you want an untethered mobile robot. |
| **NVIDIA Jetson Orin Nano** | ~$250–500 (**over budget**) | Only if you want to run learned vision on-board; overkill for a first home test. |

---

## How the pieces work together

The flow mirrors the project's 9-step loop (`01-requirements.md`), just
shrunk to a desk:

```
  [USB webcam / OAK-D Lite]  →  sees the object + the shelf slot
            │  (sends image / depth to)
            ▼
  [your laptop running Python/ROS 2]
            │  1. find the object's pose (marker or depth)
            │  2. work out a grasp (fixed pinch for a known can)
            │  3. plan the arm's joint moves
            ▼
  [SO-ARM101 / Hiwonder arm]  →  reaches, the gripper closes
            │
            ▼
        lifts → moves over the shelf → opens gripper → places
            │
            ▼
  [webcam]  →  confirms the object is sitting on the shelf
```

In words: the camera reports **where** the object is; the laptop decides
**how** to grab it and **how** to move the joints; the arm executes the
pick, swings over to a cardboard "shelf," and releases. The same
camera then checks it landed — the home-scale version of the
`verify_placement` step. Everything is driven from the laptop over USB,
so there's nothing to power or charge.

---

## Three complete builds under $500

**Build A — Tabletop starter (recommended first).** Prove a placement
with the least money and risk.
- Hiwonder xArm 1S **or** SO-ARM101 (arm + gripper) — ~$130–150
- USB webcam + printed marker — ~$30
- Your laptop — $0
- Cardboard shelf, empty can/box as the product — ~$0–10
- **Total ≈ $160–190.**

**Build B — AI-ready / depth (best learning value).** Adds real depth
and the LeRobot imitation-learning path.
- SO-ARM101 (single follower arm) — ~$130–150
- OAK-D Lite (RGB-D + on-camera AI) — ~$149
- Your laptop — $0
- Shelf/props — ~$10
- **Total ≈ $290–310.** (Add a second SO-ARM as a *leader* for
  teleoperation/teaching for ~$120 more → still ≈ $410–430.)

**Build C — Mobile (stretch, adds the driving half).** Only after A or B
works; expect it to be tippy.
- Small servo arm + gripper — ~$130
- 4WD chassis kit with encoders — ~$90
- USB webcam — ~$30
- Raspberry Pi 5 (8 GB) + power + SD — ~$110
- Battery pack — ~$30
- **Total ≈ $390–420.**

---

## How this maps to the real stack

This rig is the bottom rung of the same ladder described in
`03-high-level-tech.md` and `04-off-the-shelf-hardware.md`:

- **Arm + gripper** → the manipulation layers (`03-stack/04-arm-motion-planning.md`,
  `03-stack/06-grasping.md`). Start with a **fixed pinch on a known
  object** — the "analytical / known-pose first" rule.
- **Webcam/OAK-D** → perception (`03-stack/05-perception.md`). Start
  **geometric** (a marker or simple depth), defer learned pose
  estimation.
- **Laptop + Python/ROS 2** → middleware + orchestration. You can run
  the *same* ROS 2 ideas here that you proved in simulation.
- **Optional base** → navigation (`03-stack/03-mobile-base-navigation.md`),
  added last.

Keep the v1 "keep it simple" framing: a fixed arm, a known object, a
marker, and your laptop is enough to feel the real-world placement
problem for **under $200** — and that is the whole point of this rig.

---

> **Sources & disclaimer.** Indicative prices from Seeed Studio /
> TheRobotStudio (SO-ARM100/101, ~$120–150 servo kit + ~$35 printed
> parts), Hiwonder (xArm 1S / LeArm, ~$110–150), Luxonis (OAK-D Lite,
> ~$149), Elephant Robotics (myCobot 280, ~$700), and typical
> Amazon/AliExpress hobby chassis and webcam listings. All figures are
> approximate, exclude shipping/tax, and **drift constantly** —
> re-verify before purchasing.
