# Off-the-shelf hardware — robots that can run this task

> The shelf-stocking task in `01-requirements.md` is **simulation-first**:
> you prove the pick-drive-place loop in a simulator before any hardware
> exists, so for v1 the hardware cost is genuinely **$0**. This file is
> for the *later* hardware-transfer milestone — a survey of mobile
> manipulators you can buy off the shelf and program for this task,
> with high-level prices.
>
> Because the whole stack (`03-high-level-tech.md`) is built on **ROS 2**,
> the same nodes run on any ROS 2-native robot below. New to a term
> (AMR, cobot, payload, 6-DoF)? See `02-glossary.md`.

---

## What "can run this task" means

The robot in `01-requirements.md` is a **mobile manipulator**: a wheeled
base that drives to the shelf, plus an arm with a gripper that picks a
product from a tray and places it on the shelf, guided by a depth camera.
So an off-the-shelf platform needs four things:

- a **mobile base** that maps and navigates (works with Nav2),
- an **arm** with enough reach and payload for the products
  (a 6- or 7-DoF arm; 1.5–6 kg payload covers most grocery items),
- a **gripper / end-effector** suited to the product (a parallel-jaw
  gripper for cans and boxes), and
- a **depth (RGB-D) camera** for perception.

Every option below ships with — or can be configured with — all four,
and exposes them over **ROS 2**, which is the only hard requirement for
running this stack unchanged.

**A note on all prices:** these are **approximate 2026 figures and they
drift**. Most of these robots are sold by quote, not list price, and the
final number depends heavily on the arm, gripper, and region. Re-check
every figure before quoting it. The robot is also **not the whole bill** —
see "What the price does *not* include" near the end.

---

## A. Western / established platforms

| Robot | Vendor | All-in ballpark | What you get | Fit for the shelf task |
|-------|--------|-----------------|--------------|------------------------|
| **Stretch 3** | Hello Robot (US) | **~$25k** (public list) | Mobile base + telescoping lift arm + wrist depth camera + gripper; ROS 2 + Nav2 standard | Best value and easiest start; reaches floor-to-shelf. Light (~1.5 kg payload), Cartesian arm — heavy/awkward items are out |
| **TIAGo / TIAGo Pro** | PAL Robotics (ES) | **~$55k–75k** (older list ~€50k w/ arm) | Base + 7-DoF arm + lifting torso + dual lidar + head camera; full ROS 2 | Best grocery-shelf *reach* of the group (torso lifts to ~1.5 m); ~3 kg payload; mature support |
| **RB-KAIROS+** | Robotnik (ES) | **~$80k–130k** | Industrial base + a **Universal Robots** arm (UR7e/12e/16e) + your gripper; ROS 2 | Heavier payloads, deployment-grade; price swings with the UR arm chosen |
| **MMO-700 / MMO-500** | Neobotix (DE) | **~$90k–150k** | **Omnidirectional** base + UR/KUKA arm + gripper; ROS 2 | Omni base drives sideways — useful in tight aisles; industrial-grade |
| **Fetch** | Fetch / Zebra (US) | **"<$100k"** (hist. ~$70k–100k) | Base + 7-DoF arm (6 kg) + telescoping spine (floor-to-~2 m) + gripper + lidar/3D cam; ROS | Closest to a real-store end state; **availability uncertain** post-Zebra acquisition — verify first |

**Bottom line (Western):** for cheap prototyping → **Stretch 3**; for the
best research-grade shelf reach → **TIAGo**; for an industrial UR-arm
build → **RB-KAIROS+** or **Neobotix**.

A DIY alternative to any turnkey buy: a **Clearpath Husky/Ridgeback base
+ a UR arm + a Robotiq gripper** — more assembly, more flexibility.

---

## B. China-based platforms

Chinese vendors offer comparable capability and generally undercut the
Western platforms. ROS 2 support is real but varies by model; weigh
documentation maturity, long-term software support, and import/lead-time
/regional-support cost alongside the sticker price.

### Industrial-grade (closest to the shelf task)

| Vendor | Product | All-in ballpark | Notes |
|--------|---------|-----------------|-------|
| **Dobot** | AMMR (AMB-300D / 300XS): AMR base + CR-series cobot arm | **~$36k–49k** | Turnkey SLAM nav + pick-and-place — the most "buy-it-and-go" option. Arms also sold alone (CR5A ~$24k, CR10A ~$33k) |
| **JAKA** | Zu-series cobot + AMR base (via integrator) | **~$25k–60k** | Strong cobot arms (supplies Toyota); base usually integrated by a partner. Quote only |
| **AUBO** | i-series cobot (i3/i5/i10) + AMR | **~$20k–50k** | Competitive mid-range cobots; mobile integration via partners. Arm alone ~$15k–20k |
| **Siasun / ESTUN / DUCO** | Various industrial mobile manipulators | **quote (~$40k–100k)** | Larger industrial players; priced like Western industrial systems but typically cheaper |

### Research / education-grade (cheaper, lighter payload)

| Vendor | Product | All-in ballpark | Notes |
|--------|---------|-----------------|-------|
| **AgileX Robotics** | Mobile base (Ranger/Scout/Tracer/Bunker) + arm; "Cobot Magic" research kits | **~$10k–40k** | Full ROS 2 mobile-manipulator kits. Their **PiPER** 6-DoF arm (~1.5 kg payload) is genuinely low-cost, **~$1.5k–3k** *(disregard a stray €62,400 listing — it looks like a mislabeled bundle/typo; verify directly)* |
| **Hiwonder** | JetArm Pro on Mecanum chassis (Jetson Orin) | **~$2k–6k** | ROS 1/2, 3D depth camera, AI vision. Tabletop-scale — great for **learning the loop**, too small for real grocery payloads |
| **iQuotient (IQR)** | "Little Mobile Manipulator" (Create3 base + arm + lidar + NUC) | **~$5k–10k** (est.) | ROS 2 research platform; small payload |

**Bottom line (China):** for a real shelf build on a budget → **Dobot
AMMR** (turnkey) or an **AgileX base + cobot arm**; for cheap
learning/prototyping → **Hiwonder JetArm Pro** or **iQuotient**.

---

## What the price does *not* include

The robot sticker is rarely the whole cost of running this task:

- **Gripper / end-effector** — if the stock gripper doesn't suit the
  product (cans, boxes), budget a parallel-jaw gripper with sensing:
  Robotiq ~$3k–10k, or Chinese options like DH-Robotics ~$1k–5k.
- **Onboard GPU compute** — only if you use the *learned* perception or
  grasping path (FoundationPose, AnyGrasp need a GPU). A Jetson Orin is
  **~$0.6k–2k**. The v1 geometric path (`03-stack/05-perception.md`,
  `03-stack/06-grasping.md`) runs CPU-only, so this is optional.
- **Integration & engineering time** — on a first hardware build this
  usually *dwarfs* the hardware cost.
- **Import, lead time, and regional support** — especially for overseas
  vendors, sometimes a bigger practical cost than the hardware.

---

## Rules of thumb

- **v1 is simulation-first** — start in **Gazebo Harmonic**
  (`03-stack/01-simulator.md`) on a CPU laptop you already own. Hardware
  cost for the current milestone is **$0**.
- To start cheap on real hardware → **~$25k** (Stretch 3), or even
  **~$2k–6k** for a tabletop learning rig (Hiwonder).
- For an industrial-grade build → **~$36k–49k** (Dobot AMMR) or
  **~$80k–130k** (RB-KAIROS+ / Neobotix / Fetch).
- Then add **~$5k–15k** for a suitable gripper + GPU compute, **plus**
  integration labor.

---

> **Sources & disclaimer.** Figures gathered from vendor sites and trade
> press (Hello Robot, PAL Robotics, Robotnik, Neobotix, IEEE Spectrum on
> Fetch; Dobot, AgileX, JAKA/AUBO industry roundups, Hiwonder,
> iQuotient/RobotShop). All prices are **approximate, quote-dependent,
> and subject to drift** — confirm with the vendor before relying on any
> number here.
