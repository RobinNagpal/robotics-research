# GOAL

## Strategy: services first, products later

1. **Before we build anything of our own, we should first do services
   for robotics companies.** Services teach us the domain, pay the
   bills, and de-risk what we eventually build ourselves.

2. **To offer services, we pick 2–3 isolated layers** — pieces of the
   robotics stack that can be worked on independently and whose work can
   be **outsourced** (handed to us as a self-contained job).

3. **The two layers on our list:**
   - **a) Simulation scenes** — building simulation scenes with
     different scenarios.
   - **b) Synthetic data** — creating synthetic data for testing.

We will do both, starting with the **ketchup** example and then maybe
the **paracetamol** example, both explained in
[`02-hplc-autosampler/02-lab-bench-new.md`](02-hplc-autosampler/02-lab-bench-new.md).

The full service catalogs — which services we can sell, to which
companies on the [outreach list](04-outreach/01-companies.md), how an
offshore services company would deliver them, and what to learn first
— are worked out in [`SIMULATION-SERVICES.md`](SIMULATION-SERVICES.md)
(Task A) and
[`SYNTHETIC-DATA-SERVICES.md`](SYNTHETIC-DATA-SERVICES.md) (Task B).

---

## Checklist

### Task A — Simulation scenes

- [ ] Build the **ketchup** scene (objects + workcell layout) — [object list](02-hplc-autosampler/04-mycobot-280-impl/01-simulation/01-ketchup-experiment-objects.md)
- [ ] Add different scenarios / variations to the ketchup scene
- [ ] Build the **paracetamol** scene
- [ ] Add different scenarios / variations to the paracetamol scene
- [ ] Package the scenes so they can be handed off / reused

### Task B — Synthetic data for testing

- [ ] Generate synthetic data from the **ketchup** scene
- [ ] Label / format the data for testing
- [ ] Generate synthetic data from the **paracetamol** scene
- [ ] Verify the data is usable for testing
- [ ] Package the dataset so it can be handed off / reused
