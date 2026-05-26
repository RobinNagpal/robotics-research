# Requirements — Place items on a grocery shelf

> A mobile base + arm that is loaded with a tray of products and stocks
> them onto a grocery-store shelf. This file defines the **simplest
> viable version** — the smallest robot and the tightest set of
> assumptions that still produce a demo a grocery chain would recognize
> as "it stocked the shelf." Everything here is scoped to be built and
> proven **in simulation first** (see `02-high-level-tech.md`), then
> transferred.

The guiding rule: **cut every variable you can until exactly one hard
thing remains** — placing a rigid product into a known slot — and prove
that end to end before adding any complexity back.

---

## 1. Goal

Given a robot pre-loaded with a tray of identical products and a target
shelf, the robot drives to the shelf, picks one product at a time, and
places each into its assigned slot in the correct upright orientation,
until the tray is empty or the slot is full.

---

## 2. What "simplest" means (scope constraints)

These constraints are the whole point of the first build. Each one
removes an entire category of failure so the core pick-drive-place loop
can be proven.

- **One SKU per run.** The robot is loaded with a single product type
  (e.g. one kind of canned soup). No mixed trays, no sorting.
- **Rigid, regular packaging.** Cans, boxes, or bottles with a known,
  fixed geometry. No bags, shrink-wrap, produce, or deformable items.
- **Known product dimensions.** Size, weight, and grasp points are
  given up front, not discovered.
- **Known store layout.** Shelf positions, aisle width, and the target
  shelf height are part of the map. The robot is told *which* shelf and
  *which* slot — it does not search the store.
- **Open-faced shelf, single layer.** Place products side-by-side in
  one row on an empty shelf. No stacking, no pushing back existing
  product, no "facing" (pulling product forward).
- **Static environment during operation.** No shoppers or carts in the
  aisle while the robot works; if something enters, the robot
  **safe-stops** rather than re-plans around it.
- **Loaded by a human.** A person places the tray of products on the
  robot in a known fixture/pose. The robot does not pick from a pallet
  or restock its own tray.
- **One arm, one gripper.** A single manipulator with a simple parallel
  or suction gripper sized to the chosen SKU.

Anything outside these lines is a **non-goal for v1** (see §8).

---

## 3. Operating environment (the store)

- A single aisle with shelving units of standard grocery dimensions.
- Flat, hard floor; no ramps or thresholds.
- A known map of the aisle (occupancy grid + shelf locations).
- A **planogram** for the target shelf: which SKU goes where, the slot
  origin, and how many facings fit. For v1 this is a small static file,
  not a live retail-system integration.
- Adequate, roughly uniform lighting (simulation gives this for free;
  it becomes a real perception variable only on hardware).

---

## 4. The robot (conceptual hardware)

The simplest configuration that can do the task:

- **Mobile base:** differential-drive or holonomic, with a 2D lidar and
  wheel odometry for navigation. Payload enough to carry one loaded
  tray plus the arm.
- **Arm:** a single 5–6 DoF manipulator (e.g. a low-cost collaborative
  arm class) with reach from the tray to the target shelf heights in
  scope.
- **Gripper:** parallel-jaw *or* suction, chosen to match the SKU.
  Suction is often simpler for flat-topped boxes; parallel jaws for
  cans/bottles.
- **Camera:** one RGB-D camera, wrist-mounted (eye-in-hand) for slot and
  product localization. A second base-mounted camera is optional.
- **Compute:** one onboard computer running the full ROS 2 stack.

The robot is modeled as a **URDF/USD mobile manipulator** so the base
and arm are planned as one system (see tech doc).

---

## 5. Products in scope

- A single rigid SKU per run, e.g. a 400 g can, a cereal box, or a
  0.5 L bottle.
- Known: outer dimensions, weight, center of mass (approx), and a
  preferred grasp (top suction for boxes, side pinch for cans).
- Presented to the robot in a **known tray layout** — fixed positions
  and orientations, so the first pick does not require open-ended bin
  perception. (Relaxing this to a jumbled tray is a later milestone.)

---

## 6. Functional requirements

The task decomposed into the loop the robot must execute:

1. **Receive a job:** target shelf ID, slot/planogram entry, SKU,
   product count.
2. **Navigate to the shelf:** plan and drive from the start pose to a
   stable picking/placing pose in front of the target shelf, then
   localize precisely relative to the shelf face.
3. **Locate the next product** in the tray (from the known layout in
   v1; from perception later).
4. **Pick:** plan a collision-free arm trajectory, grasp the product,
   and confirm the grasp (gripper state / weight / vision).
5. **Locate the target slot** on the shelf using the wrist camera +
   planogram (slot origin + offset by how many already placed).
6. **Place:** move the product to the slot, set it down upright with
   light, controlled contact, and release.
7. **Verify:** confirm the product is in the slot and upright; log
   success/failure for that unit.
8. **Repeat** 3–7 until the tray is empty or the row is full.
9. **Report:** mark the job complete with a per-unit success log; on
   unrecoverable failure, safe-stop and flag for a human.

---

## 7. Non-functional requirements

- **Reliability:** target a high single-unit place success rate in sim
  (e.g. ≥95% over N runs) before any hardware talk. Define a failure as
  a drop, a missed slot, a knocked-over neighbor, or a collision.
- **Cycle time:** a target seconds-per-unit budget (e.g. 20–40 s/unit
  in v1). Speed is explicitly *not* a v1 priority — correctness is.
- **Safety:** any unexpected obstacle (shopper, cart, dropped item) →
  immediate motion stop; the robot never plans through a dynamic
  obstacle in v1.
- **Recoverability:** a failed pick or place is logged and skipped
  rather than retried indefinitely; the robot must never wedge itself.
- **Observability:** every run produces a log — per-unit outcome, cycle
  times, and the failure reason — so success rate is measurable, not
  anecdotal.

---

## 8. Explicit non-goals (deferred to later milestones)

Listed so scope creep is visible and intentional:

- Mixed SKUs / sorting a heterogeneous tray.
- Deformable or irregular items (bags, produce, shrink-wrap).
- Stacking, multi-row placement, or product "facing."
- Restocking from a pallet or the robot loading its own tray.
- Navigating a live store with moving shoppers (dynamic re-planning).
- Reading shelf labels / barcodes to *find* the correct slot.
- Removing or rearranging existing product already on the shelf.
- Multi-robot coordination.

Each is a clean follow-on once the core loop is solid.

---

## 9. Definition of done (the demo)

A credible v1 demo, runnable in simulation:

- Load the robot with a tray of one SKU.
- Issue a job for one shelf slot.
- The robot autonomously drives to the shelf and places **every**
  product into the correct slot, upright, without collisions.
- A log shows the per-unit success rate over repeated runs with
  randomized start poses and small perturbations to product/tray
  position.

If that runs reliably in sim with randomized conditions, it is the
foundation for a hardware pilot and a stocking-automation pitch.
