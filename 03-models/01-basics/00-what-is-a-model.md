# 00 — What a "model" actually is

> **Goal of this page.** By the end you should be able to say, in your
> own words, what people mean by "a model," "weights," "parameters," and
> "a neural network" — without any mathematics. We use everyday analogies
> and spell out every term.

## The one-sentence version

A **model** is a big mathematical function that turns an input (say, a
camera picture) into an output (say, "that is a cup"), where the
function's behaviour was **learned from examples** instead of written by
a programmer.

That is the whole idea. Everything below is detail.

## Rules-code versus a model

Normal software is **rules you write**:

```text
if the pixel is red and round:
    say "apple"
```

This works until the world surprises you — a green apple, odd lighting,
a half-hidden apple — and then you are writing endless special cases.

A **model** flips this around. You do **not** write the rule. You
collect thousands of labelled pictures ("this is an apple," "this is
not") and let a training process **discover the rule for you**. The
discovered rule lives inside the model as a huge pile of numbers.

## Weights and parameters (the "huge pile of numbers")

Inside a model are millions or billions of adjustable numbers called
**weights** (also called **parameters** — the two words are used
interchangeably). Think of them as the knobs on an enormous mixing
desk. Each knob nudges how strongly one piece of information affects the
next.

- When people say a model has **"7 billion parameters" (often written
  "7B")**, they mean it has roughly seven billion of these adjustable
  numbers. More parameters can mean a smarter model, but also a bigger,
  slower, more expensive one.
- **Training** is the process of turning all those knobs to the right
  settings.
- The final settings — the trained values of every weight — are saved to
  disk as a file (or set of files). That file is called the model's
  **weights** or a **checkpoint**. When you "download a model," this
  file is what you are downloading.

## Neural network, layers, and "deep learning"

The specific kind of function used today is a **neural network**: the
numbers are arranged in **layers**, and information flows from one layer
to the next, being reshaped at each step. The name is a loose analogy to
brain cells (neurons); do not read too much into it — it is mathematics,
not biology.

- **Deep learning** simply means "a neural network with many layers."
  "Deep" refers to the number of layers stacked up, nothing more.
- A **Transformer** is the most important network design of the last
  decade. It is the architecture behind large language models (the
  technology in chat assistants) and, increasingly, behind robot models
  too. You will see the word constantly. For now: a Transformer is a
  particular, very effective layout of layers that is good at weighing up
  which parts of the input matter most.

## What "multimodal" means

A model is **multimodal** if it accepts more than one *kind* (mode) of
input at once — for example, an image **and** a line of text. This
matters in robotics because a robot model often needs to take in a
camera picture *and* a typed instruction ("pick up the red mug") at the
same time. The vision-language-action models in
[`../02-vision-language-action-models/`](../02-vision-language-action-models/00-introduction.md)
are the headline example.

## What you now know

- A model is a function whose behaviour was **learned from data**.
- Its knowledge lives in millions/billions of **weights** (= parameters)
  saved as a **checkpoint** file.
- It is built from **layers**; "deep learning" just means "many layers";
  the **Transformer** is the dominant layer layout.
- **Multimodal** means it takes more than one kind of input.

Next: [`01-types-of-models-map.md`](01-types-of-models-map.md) sorts the
robotics models into families so the rest of this area has a map.
