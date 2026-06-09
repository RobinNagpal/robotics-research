# Step 2 — Dissolution / extraction

> **In one line:** turn the weighed sample into a liquid, because the
> machine can only read liquids.

This is the second of the eight steps (see the
[overview](README.md)). It follows
[Step 1 — Weighing](01-weighing.md).

## The words you need here

- **Dissolve** — to make a solid disappear into a liquid by stirring it
  in, the way sugar "disappears" into hot tea. The solid is still there,
  but it is now spread evenly through the liquid as tiny invisible
  pieces. The result is called a **solution**.
- **Solvent** — the liquid that does the dissolving. Common lab solvents
  are plain **water**, and two clear alcohol-like liquids called
  **methanol** and **acetonitrile**. Which one you use depends on the
  sample (some things dissolve in water, some need methanol).
- **Extraction** — a gentler word for "pulling *one specific thing* out
  of a messy mixture." When the sample is complex (like food), we do not
  want to dissolve *everything*; we only want to coax out the one
  chemical we care about and leave the rest behind. That selective
  pulling-out is **extraction**.
- **Stock solution** — the first, strong solution you make at this step,
  before any weakening. ("Stock" here means "the original supply you
  draw from later.")
- **Beaker / flask** — glass containers. A **beaker** is a simple cup. A
  **flask** is a bottle with a narrow neck. We work in these (not in the
  tiny final vial) because they are roomy and easy to stir and pour.
- **Sonicate** — to place the container in a small bath that buzzes with
  sound waves (an **ultrasonic bath**). The buzzing shakes the liquid at
  a microscopic level and helps stubborn solids dissolve faster. Think
  of it as "stirring with sound."

## Why we do this

The HPLC machine pumps **liquid** through itself. It physically cannot
take a solid tablet or a paste. So before anything else, the part we
want to measure must be floating in a clear liquid. For a simple drug,
this means **dissolving** it. For a messy food, it means **extracting**
just the target chemical out of all the pulp and sugar.

This is also where the difference between our two examples becomes large
for the first time.

## What you actually do (the general routine)

1. Put the weighed sample into a beaker or flask.
2. Add a **measured** amount of the right solvent.
3. Help it mix: swirl by hand, stir, gently warm, or **sonicate**.
4. Wait until it looks **clear and even**, with nothing solid left
   floating (for a true dissolution) — or until the target has been
   pulled into the liquid (for an extraction).

## Paracetamol example (the easy case: dissolution)

Paracetamol dissolves nicely, so this step is quick and clean.

- Take the **~5 mg** of paracetamol powder you weighed.
- Add a measured amount of solvent — for example **10 mL** (millilitres)
  of **methanol**, because paracetamol dissolves well in methanol.
  (10 mL is about two teaspoons.)
- Swirl, or sonicate for a few minutes. The powder vanishes and you are
  left with a **clear, colourless liquid**.
- You now have a **stock solution**: 5 mg of paracetamol spread evenly
  through 10 mL of methanol. Because you know both numbers, you know its
  exact strength.
- You repeat this for each brand, each in its **own** container, and for
  the pure reference standard too.

Notice: nothing was thrown away. The whole tablet powder dissolved.
That is what makes a drug the *easy* case.

## Ketchup example (the hard case: extraction)

Ketchup will **not** politely dissolve — it is mostly pulp, water, sugar
and acid, and we only want one tiny chemical (5-HMF) out of all that. So
we **extract** instead of dissolve.

- Take the **~5 g** of ketchup you weighed into the beaker.
- Add a solvent — often **water** or a **mild acid solution** — that
  coaxes the 5-HMF (and some sugars) out of the thick paste and into the
  liquid.
- **Stir**, and possibly **warm gently**, to help the target leave the
  pulp and move into the liquid.
- The result is **not** a clear solution. It is a cloudy, pulpy mixture:
  the 5-HMF is now in the liquid, but the tomato solids are still
  floating around in it.

This is the key point: with ketchup, the end of this step is **messy**.
The good stuff is in the liquid, but so is a lot of unwanted pulp that we
must remove before going further. (That removal happens in
[Step 4 — Filtering](04-filtering.md), after a clarifying spin.)

## Why the two examples diverge here

| | Paracetamol | Ketchup |
|---|---|---|
| What we do | Dissolve everything | Extract one chemical |
| Solvent | Methanol | Water / mild acid |
| Result | Clear liquid | Cloudy, pulpy liquid |
| Anything left behind? | No — it all dissolves | Yes — pulp must be removed later |
| Difficulty | Easy | Harder, messier |

This single step is where "a clean tablet" and "a messy food" stop
looking alike.

## What can go wrong

- **Not fully dissolved** → some sample is still solid, so the liquid is
  weaker than you think.
- **Wrong solvent** → the target may not dissolve at all.
- **Too much heat** (especially for ketchup) → heat can *create more*
  5-HMF, changing the very thing you are trying to measure.
- **Uneven mixing** → the liquid is stronger in some spots than others,
  so the amount you take next is not representative.

## For the robot arm

The physical actions here — pouring a measured solvent, stirring,
moving a beaker into a sonicating bath — are **medium** difficulty: they
are mostly "move things and wait," which an arm can do. The genuinely
hard parts are **judgement** ("is it fully dissolved yet?") and the
**messiness of food** (pulp behaves differently every time). For a first
proof-of-concept, the clean paracetamol case is far more arm-friendly
than ketchup.

## Objects needed in the simulation scene

Beyond the **shared workcell** (arm, gripper, table, overhead + wrist
cameras, a YOLO object detector, racks), this step adds:

| Object | What it is | Mock node / topic |
|---|---|---|
| **Extraction beaker / flask** | The roomy prep vessel the work happens in | — |
| **Solvent reservoir** | Methanol (paracetamol) or water / dilute acid (ketchup) | — |
| **Stir bar / stir rod** | The stirring element that helps mixing | — |
| **Dispenser station** | A mock that "pours" a measured solvent volume | `mock_dispenser` → `/mock_dispenser/volume_ml` |
| **Heated mixer / sonicator** | A mock stir-and-heat station that raises a "done" flag (ketchup uses heat + a long dwell) | `mock_mixer` → `/mock_mixer/run`, `/mock_mixer/heat`, `/prep/dissolved` |

These are **Stage 1** of the ketchup scene's
[object list](../05-mycobot-280-impl/01-only-code/01-simulation/01-ketchup-experiment-objects.md).

---

**Next step:** our liquid is usually far too strong for the machine to
read, so we weaken it → [Step 3 — Dilution](03-dilution.md).
