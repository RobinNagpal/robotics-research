# HPLC workflow — the eight prep steps, one at a time

> **Job:** Take the eight sample-preparation steps from
> [`../03-lab-bench-new.md`](../03-lab-bench-new.md) and give each one
> its own deep, plain-language file. Every file explains the step from
> the very basics — **no lab experience assumed** — and walks it through
> the same two real examples: a **paracetamol tablet** (a medicine) and
> **tomato ketchup** (a food).

## Who this is for

Anyone. If you have never set foot in a lab, never heard these words,
or are reading in a second language, these files are written for you.
Sentences are kept short. Every special word is explained the first
time it is used. Wherever a number appears (like "5 milligrams"), treat
it as an *approximate, realistic example* (the `~` sign means "about") —
real labs follow an exact written recipe.

## The big picture in one paragraph

We have a **sample** (the thing we want to test). We want a machine
called **HPLC** to tell us *what is inside it* and *how much*. But the
machine cannot read a tablet or a spoon of ketchup directly. It can only
read a clean, watery liquid sitting in a tiny glass bottle called a
**vial**. So our whole job — these eight steps — is to turn the sample
into that clean liquid in that little bottle, correctly and tidily. The
machine does the rest by itself.

## The eight steps

Read them in order; each builds on the one before.

1. [**Weighing**](01-weighing.md) — measure out an exact, tiny amount
   of the sample.
2. [**Dissolution / extraction**](02-dissolution-and-extraction.md) —
   get the sample (or just the part we care about) into a liquid.
3. [**Dilution**](03-dilution.md) — make that liquid weaker so the
   machine can read it.
4. [**Filtering**](04-filtering.md) — strain out tiny solid bits that
   would block the machine.
5. [**Transfer to vial**](05-transfer-to-vial.md) — move the finished
   liquid into the little glass bottle.
6. [**Capping**](06-capping.md) — close the bottle with a lid.
7. [**Labeling**](07-labeling.md) — write on the bottle what is inside.
8. [**Placement in the autosampler**](08-placement-in-autosampler.md) —
   put the bottle into its numbered slot in the machine.

## A starter glossary (used across all eight files)

You do **not** need to memorise these — each file re-explains the words
it uses. This is just a quick reference.

| Word | Plain meaning |
|---|---|
| **Sample** | The thing we are testing (a tablet; a spoon of ketchup). |
| **Analyte** / **target** | The one substance we actually want to measure (the paracetamol molecule; the chemical "5-HMF" in ketchup). |
| **Matrix** | Everything *else* in the sample that we are **not** measuring (tablet glue and filler; tomato pulp and sugar). |
| **Solvent** | A liquid used to dissolve things (water, or alcohols called methanol and acetonitrile). |
| **Solution** | A liquid with something dissolved in it (like sugar stirred into tea). |
| **Concentration** | How "strong" a solution is — how much stuff is dissolved in a given amount of liquid (for example, milligrams per millilitre). |
| **Stock solution** | The first, strong solution we make, before we weaken it. |
| **Dilution** | Making a solution weaker by adding more solvent. |
| **Vial** | The small glass bottle (about 2 mL) that goes into the machine. |
| **Autosampler** | The part of the machine that holds many vials and feeds them in one by one. |
| **HPLC** | The analysis machine itself (full name: High-Performance Liquid Chromatography). |
| **mL** (millilitre) | A small unit of liquid volume. A teaspoon is about 5 mL. |
| **g / mg / µg** | Units of weight. 1 gram (g) = 1000 milligrams (mg); 1 mg = 1000 micrograms (µg). A grain of salt is roughly 1 mg. |
| **SOP** | "Standard Operating Procedure" — the exact written recipe a lab must follow every time. |

## Our two running examples

- **Paracetamol** (also called acetaminophen; sold as Panadol, Tylenol,
  and many own-brand painkillers). A clean, simple, solid tablet.
  *Question we are answering:* does it really contain the dose printed
  on the box?
- **Tomato ketchup.** A thick, messy food. *Question we are answering:*
  how much of a heat-marker chemical called **5-HMF** has formed in it?

Paracetamol is the **easy** case (clean and consistent). Ketchup is the
**hard** case (thick, full of pulp). Watching both side by side at every
step shows what makes a sample easy or hard to prepare — which is
exactly what we need to know before asking a robot arm to do any of it.

> Each file ends with a short **"For the robot arm"** note: how hard
> that one step is to automate, and why. That is the thread tying this
> primer back to the wider project.
