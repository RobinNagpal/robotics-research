# 07 — Gemini plans the task (a frontier model writes the steps)

> Checklist exercise: **Layer 5 — "ask a frontier model to plan the
> task" (the second of two stretch exercises).**
> See [`../08-learning-checklist.md`](../08-learning-checklist.md).

**This is a stretch / optional exercise.** The previous exercise
([`06-run-smolvla-in-sim.md`](06-run-smolvla-in-sim.md)) ran an *open*
model that you downloaded and that output robot *movements*. This one is
different in two ways: the model is **closed** (you cannot download it;
you reach it over the internet), and it gives you back a **text plan**,
not motion. Treat it as an eye-opener about what the biggest models can
do, not as a required step. It does not move any arm.

## What this program proves

So far the *order* of the steps — drive to the tray, remove the cap,
grab the vial, place it — was something you decided and wrote down by
hand. This exercise asks a very large, very capable model to do that
thinking for you: you show it a **photo of the workbench** plus a typed
instruction, and it writes back a **step-by-step plan** in plain
English.

The model is **Gemini Robotics-ER**, made by Google DeepMind. "Gemini"
is the name of Google's family of large models; "Robotics-ER" is the
member built for robots, where **ER** stands for **embodied reasoning**
("embodied" means "thinking about a physical body in a real space," as
opposed to only handling text). It is the model's job to look at a
scene and reason about *how a robot would act in it*.

This is a **frontier** model — one of the largest and most capable
available — and it is **closed**: its trained numbers are kept private,
so you cannot download and run it the way you ran SmolVLA. Instead you
reach it through an **Application Programming Interface** (a way for one
program to ask an online service to do something and send back an
answer; people shorten the name to "API"). Google offers this particular
one through **Google AI Studio**, their website for trying and calling
Gemini models. Reaching a closed model through its Application
Programming Interface is the normal, accessible way to *touch* one of
these frontier systems without owning a data centre.

The plan that comes back is just **text**. It does not drive the arm. But
it is exactly the kind of step list you could later hand to the
**behaviour tree** — the decision-making structure built in
[`09-per-vial-loop.md`](09-per-vial-loop.md) — to actually carry out.
(A **behaviour
tree** is a tidy way of organising "do this, then this; if that fails,
try this instead." The orchestration write-up linked at the bottom
explains it.)

If you can send a picture and a sentence to a frontier model and read
back a sensible plan, you have proven you can touch the closed model
frontier — and you have seen the split between a model that *plans* (this
exercise) and a model that *moves* (the previous one).

> **Honesty note.** Hosted models change fast. Model names (for example
> `gemini-robotics-er-1.5`), the exact library, the way access is granted,
> and even the website can all change between the time this was written
> and the time you read it. The program below teaches the *shape* of the
> task; expect to adjust the model name or a method against the current
> documentation: <https://ai.google.dev/> and the Gemini Robotics pages
> linked from it. Access to the Robotics-ER model in particular may be
> gated; if you cannot get it, the same code shape works against a general
> Gemini vision model so you can still see the idea.

## What you need first

- **Python**, version 3.10 or newer.
- Google's official Python library for Gemini, named **`google-genai`**,
  installed with the Python installer:
  ```bash
  pip install google-genai
  ```
  (Check the current documentation for the package name — it has changed
  once already.)
- An **Application Programming Interface key** for the Gemini service. A
  **key** is a long secret string of letters and numbers — like a
  password — that proves *you* are the one making the request, so the
  service knows whom to bill and trust. You get one for free (within
  limits) by signing in to Google AI Studio at
  <https://aistudio.google.com/> and clicking "Get API key."
- A **photo of your workbench** saved as a file named `workbench.jpg`,
  showing the arm, the tray, and the vial. A phone photo is fine.

**Keep your key secret.** Anyone who has your key can make requests that
are billed to you, so you must never paste it into your code or share it.
The standard safe trick — used below — is to put the key in an
**environment variable**: a named value that lives in your terminal
session, *outside* the program, so the program can read it without the
secret ever being written into the file. You set it once per terminal
like this (paste your real key in place of the example):

```bash
export GEMINI_API_KEY="paste-your-secret-key-here"
```

The word `export` makes that named value visible to programs you launch
from this terminal. Because the key lives in the terminal and not in the
file, you can safely share or publish `gemini_plan.py` without leaking
it.

## The whole program

Save this as a file named `gemini_plan.py`:

```python
import os
from google import genai
from google.genai import types


def main():
    api_key = os.environ["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)

    with open("workbench.jpg", "rb") as photo_file:
        image_bytes = photo_file.read()

    image_part = types.Part.from_bytes(
        data=image_bytes, mime_type="image/jpeg")

    instruction = (
        "You are planning for a small desktop robot arm. "
        "Looking at this workbench photo, write a numbered, "
        "step-by-step plan for how to load vial QC-007 into "
        "tray slot A3. Keep each step short and physical."
    )

    response = client.models.generate_content(
        model="gemini-robotics-er-1.5",
        contents=[image_part, instruction])

    print("The model's plan:\n")
    print(response.text)


if __name__ == "__main__":
    main()
```

## Every line explained

**`import os`**
The word `import` means "bring in a library of ready-made code so I can
use it." `os` is Python's built-in library for talking to the operating
system; we need it for one job — reading the secret key out of the
environment variable.

**`from google import genai`**
This brings in Google's Gemini library, named `genai` (short for
"generative artificial intelligence"). It holds the tools for connecting
to the Gemini service and asking it questions.

**`from google.genai import types`**
This brings in a helper piece of that same library, called `types`. It
holds small building-block shapes we need — in particular the one that
wraps a picture so the model can read it. Bringing it in separately just
lets us write the shorter name `types` below.

**`def main():`**
The word `def` begins a named block of instructions (a "function"). We
name this one `main`; it holds the whole program and runs when we launch
the file.

**`api_key = os.environ["GEMINI_API_KEY"]`**
This reads the secret key out of the environment variable you set in the
terminal. `os.environ` is a lookup table of all the named values in your
terminal session; the square brackets with `"GEMINI_API_KEY"` pull out
the one by that name. We store it in `api_key`. Notice the secret itself
never appears in the file — only the *name* of where to find it does.

**`client = genai.Client(api_key=api_key)`**
This builds a **client** — the object that knows how to talk to the
Gemini service over the internet. We hand it the key so every request it
sends is signed as ours. Think of the client as an open phone line to
Google's model; we save it in `client` and make all our requests through
it.

**`with open("workbench.jpg", "rb") as photo_file:`**
This opens the workbench photo so we can read it. `open` opens a file;
`"workbench.jpg"` is its name; `"rb"` means "read, in binary" — that is,
read the raw bytes of an image rather than treating it as text. The
`with ... as photo_file:` form opens the file, lets us use it as
`photo_file` inside the indented block, and **closes it for us
automatically** the moment we are done — the tidy, leak-free way to
handle files.

**`image_bytes = photo_file.read()`**
This reads the entire photo into memory as a long string of raw bytes,
stored in `image_bytes`. Bytes are just the computer's most basic units
of data; an image is, underneath, a big pile of them.

**`image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")`**
This wraps the raw photo bytes into a **part** — one piece of the message
we will send. `from_bytes` builds that part from the bytes we just read.
`mime_type="image/jpeg"` is a label telling the service "these bytes are
a JPEG photo," so it knows how to decode them. We store the wrapped photo
in `image_part`. (If your photo is a PNG file instead, the label would be
`"image/png"`.)

**`instruction = ( ... )`**
This stores the typed, plain-English **instruction** we want the model to
plan for. The several quoted lines inside the brackets are simply glued
together into one longer sentence (Python joins adjacent strings like
that automatically). We tell the model what kind of robot it is planning
for, ask for a numbered step-by-step plan, and name our concrete goal:
load vial QC-007 into tray slot A3. The more specific the instruction,
the more useful the plan.

**`response = client.models.generate_content(model="gemini-robotics-er-1.5", contents=[image_part, instruction])`**
This is the heart of the exercise: it sends our request and waits for the
answer. **`generate_content`** means "look at what I give you and produce
a response." We hand it two things. `model="gemini-robotics-er-1.5"`
names which model to use — the embodied-reasoning Gemini (this exact name
is the part most likely to have changed; check the current docs). The
`contents=[image_part, instruction]` is a list holding *both* the wrapped
photo and the typed instruction together — the model reads the picture
and the words as one combined question. The whole answer comes back in
`response`.

**`print("The model's plan:\n")`**
This prints a heading so the output is easy to read. The `\n` on the end
is a "new line" mark, adding a blank line after the heading.

**`print(response.text)`**
The answer object holds the model's written reply in a slot named `text`.
This line prints that text — the step-by-step plan — to your terminal.
Remember: this is **words**, a plan you (or later, the behaviour tree)
could act on. It is not robot motion.

**`if __name__ == "__main__":`**
A standard Python guard meaning "only run the next line if this file was
launched directly, not imported by another file." It keeps the program
from starting itself unexpectedly when reused.

**`main()`**
This finally calls the `main` function, setting everything above in
motion.

## How to run it, and how you know it worked

First, in the same terminal, set your secret key (once per terminal
session) and make sure `workbench.jpg` is in the current folder:

```bash
export GEMINI_API_KEY="paste-your-secret-key-here"
python3 gemini_plan.py
```

The program sends your photo and instruction to Google's service, waits a
moment, and prints back a numbered plan — something along the lines of
"1. Move the arm above tray slot A3. 2. Open the gripper. 3. Lower onto
vial QC-007 ..." The exact wording will vary every time; that is normal
for these models.

**Done when:** you see a sensible, numbered, step-by-step plan printed in
your terminal that refers to the workbench, the vial QC-007, and tray
slot A3. You have now reached a closed frontier model through its
Application Programming Interface and gotten a plan back.

**If it does not run:** that is expected on this fast-moving stack. The
most common problems are (1) a `KeyError` about `GEMINI_API_KEY` — you
forgot to `export` the key in *this* terminal; (2) a "model not found" or
"permission" error — the model name has changed or access to Robotics-ER
is gated, so substitute the current name (or a general Gemini vision
model) from the documentation; or (3) the library being imported a
different way — check <https://ai.google.dev/> for the current import
line. Reading and understanding the shape of the program is itself a
valid outcome for a stretch exercise.

## Where this fits

- This is the second of the two **Layer 5** stretch exercises in
  [`../08-learning-checklist.md`](../08-learning-checklist.md). The first,
  [`06-run-smolvla-in-sim.md`](06-run-smolvla-in-sim.md), ran an *open*
  model that output motion; this one calls a *closed* model that outputs a
  *plan*.
- The deeper write-up comparing open and closed Vision-Language-Action
  models — and where Gemini Robotics-ER sits as the "frontier we track" —
  is
  [`../05-mycobot-280-impl/foundation-models.md`](../05-mycobot-280-impl/foundation-models.md).
- A text plan like this is meant to feed the decision-making layer. The
  deeper write-up of how steps are sequenced, and how a behaviour tree
  runs them with error handling, is
  [`../05-mycobot-280-impl/01-only-code/07-orchestration-and-task-logic.md`](../05-mycobot-280-impl/01-only-code/07-orchestration-and-task-logic.md).
  For version 1 we write the step order by hand and treat a planning model
  like this one as a later milestone.
</content>
</invoke>
