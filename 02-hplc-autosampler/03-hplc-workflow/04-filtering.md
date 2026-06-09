# Step 4 — Filtering

> **In one line:** strain out tiny solid bits from the liquid, so they
> cannot block or damage the delicate machine.

This is the fourth of the eight steps (see the
[overview](README.md)). It follows
[Step 3 — Dilution](03-dilution.md).

## The words you need here

- **Filter** — to pass a liquid through a fine barrier that lets the
  liquid through but **traps solid bits**. You already know the idea
  from a coffee filter or a tea strainer: liquid coffee passes, the
  grounds stay behind.
- **Particles** — tiny solid pieces floating in the liquid: specks of
  undissolved powder, dust, or (for food) bits of pulp. Often too small
  to see clearly, but big enough to cause trouble inside the machine.
- **Syringe** — a tube with a plunger you push, the same shape as the
  one a nurse uses (but with **no needle** here). You use it to push the
  liquid forward with gentle pressure.
- **Syringe filter** — a small round plastic disc that screws onto the
  end of the syringe. Inside it is a very fine **membrane** (a thin
  skin full of microscopic holes). When you push the liquid through, the
  liquid passes but the particles are caught on the membrane.
- **Membrane / pore size** — the fine skin inside the filter. Its holes
  are incredibly small, often **0.45 or 0.22 micrometres** (a
  micrometre is a thousandth of a millimetre). Anything bigger than the
  holes cannot get through.
- **The column** — the heart of the HPLC machine: a tube tightly packed
  with very fine material that does the actual separating. It is easily
  **clogged** by particles, like a fine sieve getting blocked by grit.
  Protecting the column is the main reason this step exists.

## Why we do this

Inside the HPLC, liquid is forced at **very high pressure** through that
tightly packed column. If even small particles go in, they jam the
packing, the pressure climbs, and an expensive column can be **ruined**.
A clogged column is one of the most costly, most avoidable accidents in
the lab. Filtering is the cheap, quick insurance that prevents it. The
rule is simple and strict: **nothing enters the machine unfiltered.**

## What you actually do (the general routine)

1. Draw the diluted liquid up into the syringe.
2. Screw the **syringe filter** onto the end.
3. **Push gently** on the plunger. The liquid is forced through the
   membrane; particles stay trapped inside the filter.
4. Catch the now-clean liquid in the destination container (often
   straight into the final vial — see [Step 5](05-transfer-to-vial.md)).
5. A common refinement: **let the first few drops go to waste** before
   collecting, so any loose specks are flushed out first.

## Paracetamol example (the easy case)

Paracetamol's liquid is already nearly clear, so filtering is fast and
trouble-free.

- You draw the diluted paracetamol solution into the syringe.
- You push it through a **0.45 µm** syringe filter.
- The first ~0.5 mL is pushed to waste (to rinse the filter), then the
  clean stream is collected.
- One filter handles each sample easily, because there is very little
  solid to catch. The filter does not clog.

## Ketchup example (the hard case)

Ketchup's extract is the opposite — it is **full of pulp**, so a single
filter would block almost immediately. This is why food gets an extra
preparatory step **before** the syringe filter:

- **Centrifuge first.** A **centrifuge** is a machine that spins the
  tubes very fast in a circle. The spinning flings the heavy solids down
  to the bottom of the tube, leaving clearer liquid on top. (This is the
  same force that pushes you outward on a fast merry-go-round.) The word
  for this packed-down solid layer is a **pellet**; the clear liquid
  above it is the **supernatant**.
- **Then carefully pour off** that clearer top liquid.
- **Then filter** that liquid through the syringe filter, just like the
  drug — now it will pass without instantly clogging.

So ketchup needs **spin → pour off → filter**, where paracetamol needs
only **filter**. The thick, pulpy nature of food shows up here as real
extra work.

## What can go wrong

- **Skipping the filter** → particles reach the column and may destroy
  it. This is the cardinal sin of sample prep.
- **Filter clogs** (common with food) → you cannot push the liquid
  through; you may need to centrifuge first or use more filters.
- **Pushing too hard** → the filter can burst or leak.
- **Not flushing the first drops** → a few loose specks slip into the
  clean liquid.

## For the robot arm

Filtering is **medium** difficulty to automate. The arm must line the
syringe up over the right container and push the plunger with
**controlled, steady force** — not so little that nothing flows, not so
much that the filter bursts. That "press with the right firmness" skill
(force control) is very doable for a modern arm, but it is more than just
moving to a position. The clean paracetamol case is straightforward; the
ketchup case, with its extra centrifuge-and-pour-off, is harder and
messier to chain together.

## Objects needed in the simulation scene

Beyond the **shared workcell** (arm, gripper, table, overhead + wrist
cameras, a YOLO object detector, racks), this step adds:

| Object | What it is | Mock node / topic |
|---|---|---|
| **Syringe** | The plunger tube that pushes liquid through the filter | — |
| **Syringe filter** | A fine membrane disc (~0.45/0.22 µm) | — |
| **Centrifuge tube** | A capped tube for the ketchup-only clarify step | — |
| **Centrifuge station** | A mock that "spins down" solids before filtering (ketchup only) | `mock_centrifuge` → `/mock_centrifuge/run` |
| **Filter station** | A mock that reports rising back-pressure so the twin can handle clogs and filter swaps | `mock_filter` → `/mock_filter/push`, `/mock_filter/pressure` |
| **Destination 2 mL vial** | Often filtered *straight into* the final vial | shared with Stage 4 |

These are **Stage 3** of the ketchup scene's
[object list](../04-mycobot-280-impl/01-simulation/01-ketchup-experiment-objects.md).

---

**Next step:** the liquid is finally clean — now we put it into the tiny
glass bottle the machine reads from → [Step 5 — Transfer to vial](05-transfer-to-vial.md).
