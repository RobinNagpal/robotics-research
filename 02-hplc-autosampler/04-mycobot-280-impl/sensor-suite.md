# Sensor suite — the real-world sensing that makes the cell work

> **Why this doc exists.** A reader of the per-part docs could come away
> thinking the myCobot 280 cell is "blind" — an arm that just replays
> taught poses. A real, *flawless* cell is the opposite: it is covered
> in sensors, and almost every motion is **gated by what a sensor just
> reported**. This doc is the **canonical sensor list** for the cell —
> what each sensor is, what it confirms, where it sits, how it is faked
> in simulation, and roughly what it costs. Every other doc in this
> folder refers back here instead of re-defining
> the suite.

> **Disclaimer.** Sensor models, prices, and "what's light enough for
> the 280" drift and are approximate (`~`) — re-verify before quoting or
> buying.

---

## The one design rule: keep the wrist light, push sensing off the arm

The myCobot 280 is a **desktop arm with ~250 g payload, ~280 mm reach,
and no joint force/torque sensing** (`~` figures — verify). That single
fact shapes the whole sensor layout:

- A wrist RGB-D camera or a wrist force/torque sensor can easily weigh
  **more than the vial the arm is supposed to carry**, eating the tiny
  payload and making the arm sag and miss.
- So the practical rule is: **the wrist carries only a tiny RGB
  module; everything heavy or depth-hungry is mounted *off* the arm** —
  fixed cameras on a frame, load cells and a balance in the stations,
  proximity sensors at each station, safety sensors around the cell.

This is also the honest argument for why a *production* cell may step up
to a **myCobot 320 / UR-class** arm (see
[`README.md`](README.md)):
a bigger arm can carry a real wrist RGB-D camera and a wrist force/torque
sensor, which simplifies the whole suite. On the 280 we design *around*
the payload limit; the digital twin is where we prove the off-arm layout
actually sees and feels everything it must.

---

## The suite at a glance

Counts assume the **simplest flawless v1**: **3 cameras**, gripper
feedback, station load sensing, presence + safety sensors, and the
base IMU. "Tier" is how essential it is for a *reliable* (not just
demo) cell.

| # | Sensor | What it confirms | Where it sits | Tier | Sim stand-in |
|---|--------|------------------|---------------|------|--------------|
| 1 | **Overhead RGB-D camera** | Rack inventory, tray slot occupancy + seating across the whole tray, gross arm/vial tracking, collision watch | Fixed frame above the bench | Essential | Gazebo `depth_camera` sensor |
| 2 | **Station camera (RGB or RGB-D)** | Cap on/off + seated, liquid level / meniscus, foam / spill | Fixed, side-on at decap/dispense | Essential | Gazebo `camera`/`depth_camera` |
| 3 | **Wrist (eye-in-hand) RGB camera** | Close alignment for pick & slot insertion; barcode/QR at the vial | Light module on the flange | Essential | Gazebo `camera` on a fixed joint |
| 4 | **Gripper servo feedback** (jaw width + motor current) | Grasp success, grip force, slip, missed pick | Inside the gripper (no extra HW) | Essential | `ros2_control` joint pos+effort; grasp-fix contact |
| 5 | **Decapper load cell / torque sense** | Decap / cap torque, cross-threading, stuck cap | In the decapper station | Recommended | Gazebo force-torque sensor on the cap joint |
| 6 | **Analytical balance** (gravimetric) | True dispensed mass; weight-presence of a vial | At the dispense / weigh station | Recommended | Reads the Part 04 fill-volume scalar as mass |
| 7 | **Station presence / proximity** (photoelectric / inductive) | Vial staged? gripper at station? tool docked? | One per station | Recommended | Gazebo logical-camera / contact sensor |
| 8 | **Liquid-level sensor** (capacitive / optical) | Liquid present in line/vial; over/underfill | On the dispenser line | Optional | The fill-volume scalar exposed as a level |
| 9 | **Homing / limit switches** | Arm at home; rail/turntable end-stops | Arm + any rail/turntable | Recommended | Joint-limit state |
| 10 | **Safety: light curtain / laser scanner** | A hand or obstacle entered the work zone | Around the cell boundary | Essential (real) | `/light_curtain_clear` topic |
| 11 | **Safety: door interlock + e-stop** | Enclosure closed; emergency stop pressed | On the enclosure | Essential (real) | `/door_closed`, `/estop` topics |
| 12 | **Base IMU / tilt** | Bench knocked, arm not level, vibration | The 280's base (M5 has one) | Optional | Gazebo `imu` sensor on the base link |

> **Two-witness habit.** Wherever it matters, a fact is confirmed by
> **two independent sensors** before the workflow trusts it — e.g. "vial
> is held" = gripper feedback (#4) **and** a wrist-camera glance (#3);
> "right fill" = balance (#6) **and** the level/meniscus check (#2/#8).
> A single sensor can lie; two rarely lie the same way. This is what
> turns "it usually works" into "flawless."

---

## How the sensors feed the workflow (sensor → gate)

Every step in the per-vial loop is opened or blocked by a sensor
reading. The Behavior Tree in
[`07-orchestration-and-task-logic.md`](07-orchestration-and-task-logic.md)
ticks each gate as a node; a FAIL branches to retry / quarantine / stop.

```
locate vial   ← overhead + wrist cameras (1,3)
pick vial     → [held?]      ← gripper feedback (4) + wrist glance (3)
go to decap   → [safe?]      ← light curtain + interlock (10,11)
decap         → [cap off?]   ← station cam (2) + load-cell torque (5)
dispense      → [right fill?]← balance (6) + level/meniscus (2,8)
recap         → [seated?]    ← station cam (2) + load-cell torque (5)
read barcode  → [matches?]   ← wrist camera (3)
place in slot → [seated?]    ← overhead cam (1) + presence (7)
(continuous)  → [level/ok?]  ← base IMU (12), limit switches (9)
```

So the arm is never "flying blind": it acts, a sensor confirms, and only
then does the next motion fire.

---

## What sensing simulation *can* and *can't* prove

**Can prove in open-source sim:** that every sensor exists as a ROS 2
topic, that the **gate logic** consumes it and branches correctly, that
the **off-arm layout** (overhead + station cameras, station load cells,
proximity) actually covers every station given the 280's short reach,
and that the **two-witness** cross-checks are wired. The simulator knows
ground truth, so we can grade each sensor reading against the true state.

**Cannot prove in sim (hardware bring-up only):** real optics on **clear
glass and shiny caps** (the single biggest headache — reflections,
meniscus glare, near-invisible clear liquid), real **depth noise**,
**hand-eye calibration** accuracy, real **grip force vs slip** on
borosilicate, real **decap torque**, and true **balance / level**
accuracy. Sim proves the *sensing logic and layout*; hardware proves the
*physics*.

---

## Sensor BOM (rough, hedged — re-verify)

For the **code-plus-hardware** build. In **only-code** every line below
is a free Gazebo plugin or mock topic — `~$0`.

| Sensor | Example part | ~Cost (USD) |
|--------|--------------|-------------|
| Overhead RGB-D | RealSense D435i / OAK-D / Orbbec Gemini | ~$150–350 |
| Station camera | OAK-D Lite / Orbbec / good webcam | ~$50–250 |
| Wrist RGB module | Elephant camera flange / small USB cam | ~$30–100 |
| Gripper feedback | Built into the Elephant gripper | ~$0 extra |
| Decapper load cell / torque | Load cell + HX711, or OEM decapper sense | ~$20–200 |
| Analytical balance | Lab balance w/ serial/USB | ~$300–2,000 |
| Proximity / photoelectric ×~4 | Inductive / photoelectric sensors | ~$10–40 each |
| Liquid-level sensor | Capacitive / optical level sense | ~$10–100 |
| Light curtain / laser scanner | Safety-rated curtain | ~$200–1,500 |
| Door interlock + e-stop | Safety switch + e-stop button | ~$30–150 |
| Base IMU | On-board (M5 base) | ~$0 extra |

The big swings are the **balance** and the **safety light curtain** —
both are where lab-grade and safety-rated parts cost real money. The
twin lets you decide which are truly needed *before* buying.

---

## How it connects

- **Cameras (1–3)** → the perception layer
  [`04-perception-and-vision.md`](04-perception-and-vision.md).
- **Gripper feedback + load cell (4,5)** → the grasping layer
  [`05-grasping-and-manipulation.md`](05-grasping-and-manipulation.md).
- **Balance + level (6,8)** → published by the sensing layer
  [`09-sensing-and-signal-acquisition.md`](09-sensing-and-signal-acquisition.md).
- **Presence + seating (7)** → fused into gates in
  [`10-sensor-fusion-and-gating.md`](10-sensor-fusion-and-gating.md).
- **Safety + IMU + limits (9–12)** → the orchestration layer
  [`07-orchestration-and-task-logic.md`](07-orchestration-and-task-logic.md);
  all sensor readings are logged for the audit trail in
  [`08-software-worklist-and-compliance.md`](08-software-worklist-and-compliance.md).
- **The reading/publishing of every sensor topic** → the middleware
  layer [`02-middleware-and-control.md`](02-middleware-and-control.md) and
  the sensing layer
  [`09-sensing-and-signal-acquisition.md`](09-sensing-and-signal-acquisition.md).
- Folder index: [`README.md`](README.md).
