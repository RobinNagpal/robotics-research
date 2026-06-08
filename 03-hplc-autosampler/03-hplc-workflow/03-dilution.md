# Step 3 — Dilution

> **In one line:** make the liquid weaker, in a careful and exact way,
> so the machine can read it accurately.

This is the third of the eight steps (see the
[overview](README.md)). It follows
[Step 2 — Dissolution / extraction](02-dissolution-and-extraction.md).

## The words you need here

- **Dilution** — making a liquid **weaker** by adding more solvent. You
  already do this in daily life: adding water to strong orange squash, or
  to a thick soup, is dilution. The amount of *stuff* stays the same, but
  it is now spread through *more* liquid, so each sip is weaker.
- **Concentration** — how "strong" the liquid is: how much target is
  packed into each millilitre. Diluting **lowers** the concentration.
- **Too concentrated** — too strong. If a liquid is too strong, the
  machine's detector is overwhelmed and cannot measure it properly
  (imagine trying to read a light that is blindingly bright — you cannot
  tell exactly how bright it is).
- **Dilution factor** — the "how many times weaker" number. If you make
  a liquid **10 times** weaker, the dilution factor is **10** (written
  "1:10," said "one in ten"). Make it 100 times weaker and it is
  "1:100." You must **record** this number, because later you multiply
  the machine's reading back by it to recover the real amount.
- **Pipette** — a precise tool for measuring and moving an exact small
  volume of liquid, like a very accurate eyedropper. **Volumetric**
  pipettes/flasks are the most exact kind.
- **µg/mL** ("micrograms per millilitre") — a common way to write a
  concentration: how many micrograms of target sit in one millilitre of
  liquid. (1 microgram = one millionth of a gram.)

## Why we do this

After Step 2, the liquid is usually **far too strong** for the machine.
The detector at the end of the HPLC has a "comfortable reading range,"
much like a camera that takes its best photos when the light is neither
too dark nor too bright. If the sample is too strong, the reading is
unreliable. So we deliberately weaken it to land inside that comfortable
range.

There is a second, equally important reason for the drug example:
**fairness**. To compare five brands against one reference standard, we
want them all entering the machine at the **same** strength. Then any
difference the machine sees is a real difference between products — not
just one being more diluted than another.

## What you actually do (the general routine)

1. Take a **small, exact** amount of your strong stock solution using a
   pipette (say, 1 mL).
2. Put it into a clean, larger container.
3. Add solvent up to a **known total volume** (say, up to 10 mL).
4. Mix well. You have now made it 10 times weaker — a 1:10 dilution.
5. **Write down the dilution factor.** This number is part of the answer.
6. If it is still too strong, repeat (dilute the dilution). Two or three
   rounds is normal.

## Paracetamol example (the easy case)

- Your stock solution from Step 2 is strong (5 mg in 10 mL). That is too
  concentrated to inject.
- Using a pipette, take a small, exact amount and add solvent to weaken
  it — aiming for a target strength of about **~100 µg/mL** (a typical
  comfortable reading level).
- Crucially, you bring **every brand** to that **same ~100 µg/mL**, and
  you match the **reference standard** to it too. Now they are all
  directly comparable — same strength going in.
- Record each dilution factor so you can convert the machine's reading
  back into "milligrams per tablet" at the end.

Because paracetamol's liquid is clean and clear, this is just careful,
repetitive measuring — exact, but not messy.

## Ketchup example (the hard case)

- The ketchup extract is much less predictable — you do not know in
  advance exactly how much 5-HMF is in it.
- So you often dilute it **a lot**, for example **1:10 or 1:100**
  (10 or 100 times weaker), to be safe and land in the readable range.
- Sometimes you have to **guess, run it, and adjust**: if the first try
  is still too strong, you dilute more and run again. Food samples need
  this trial-and-error more often than clean drugs do.

So the *action* is the same as for paracetamol, but the **uncertainty**
is higher: you are less sure of the right dilution up front.

## A simple picture of dilution factors

| You did this | Dilution factor | The liquid is now... |
|---|---|---|
| Took 1 mL, made it up to 10 mL | 1:10 (×10 weaker) | 10 times weaker |
| Then took 1 mL of *that*, up to 10 mL again | 1:100 (×100 weaker) | 100 times weaker |

At the end, the machine reads the **weak** liquid, and you **multiply
back** by the dilution factor to learn how strong the original was.

## What can go wrong

- **Imprecise volumes** → the single biggest source of error in the
  whole workflow. A pipette that draws slightly too much or too little
  throws off the final number.
- **Forgetting to record the dilution factor** → you cannot convert the
  reading back, so the result is useless.
- **Poor mixing** → the liquid is uneven, so your next small sample is
  not representative.
- **Wrong guess for ketchup** → too strong (unreadable) or too weak
  (target lost in the noise), forcing a re-run.

## For the robot arm

Dilution is **medium-to-hard** to automate, but for an interesting
reason: the difficulty lives in the **tool**, not the arm's muscles.
Measuring an exact volume is the job of a good **pipette** or
**liquid-handler**; the arm's role is to hold and operate that tool and
move liquids between containers in the right order. Get the tool right
and the arm's own job is mostly precise *positioning and choreography*.
This is exactly why the project treats "precise volume" as a tooling
question rather than an arm-precision question.

---

**Next step:** before the liquid can enter the machine, we must strain
out any tiny solid bits → [Step 4 — Filtering](04-filtering.md).
