# 01 — How perception & vision models work

> **Goal of this page.** Open the box: what exactly goes in, what comes
> out, how these networks are shaped, how they are trained, and what they
> cost to run. Plain language, no maths. Builds on
> [`00-introduction.md`](00-introduction.md).

## Inputs and outputs, precisely

**Input**

- **One image** — a single camera frame. To a computer an image is just
  a **grid of pixels**: rows and columns of little coloured dots, each
  stored as three numbers (how much red, green, and blue it has). A
  typical frame might be 640 columns × 480 rows of these dots. That grid
  of numbers is the entire input.

That is it — no text, no instruction, no robot state. A plain detector
sees only pixels. (The exception, **open-vocabulary** detection, also
takes a line of text; see below.)

**Output — depends on the task**

For **object detection**, the output is a short list, one entry per
object found, where each entry has three parts:

- **Bounding box** — four numbers describing a rectangle: where its
  corners sit in the image (e.g. left, top, width, height). This is the
  "box around the object."
- **Class label** — *which* object it is, picked from the categories the
  model knows: `"cup"`, `"bottle"`, `"person"`.
- **Confidence score** — a number from 0 to 1 saying how sure the model
  is. `0.97` means "very confident this is a cup"; `0.41` means "maybe."
  You usually keep only detections above some threshold (say 0.5).

For **image segmentation**, instead of (or in addition to) a box, each
object gets a **mask**: a same-size grid that marks every pixel as
"belongs to this object" or "does not." Stack the boxes and masks and you
have a full description of the scene's contents.

```text
detection output (one row per object):
  box=[40,55,120,90]   label="mug"     confidence=0.94
  box=[210,30,80,160]  label="bottle"  confidence=0.88

segmentation output:
  mask for the mug     (a per-pixel yes/no map of the mug's shape)
  mask for the bottle  (likewise)
```

## How an image becomes boxes and labels

Two network designs dominate, and you will hear both names constantly.

- **Convolutional neural network (CNN).** A **convolutional neural
  network** is the classic image network. "Convolution" just means it
  slides a small window across the image looking for little patterns —
  edges, corners, textures — then combines those into bigger patterns
  (a wheel, a handle) and finally whole objects. It is a neural network
  (the layers idea from
  [`../01-basics/00-what-is-a-model.md`](../01-basics/00-what-is-a-model.md))
  specialised for the grid shape of an image. The famous **YOLO** family
  is built this way.
- **Transformer-based detectors.** Newer detectors borrow the
  **Transformer** — the same layer layout behind chat assistants
  (again see
  [`../01-basics/00-what-is-a-model.md`](../01-basics/00-what-is-a-model.md))
  — and apply it to image patches. Transformers are good at weighing up
  which parts of the picture matter together, which helps with cluttered
  scenes. Many open-vocabulary detectors are Transformer-based.

You do not have to choose; just know both exist, and the top-three page
says which each model uses.

### Open-vocabulary detection (detect things you name in text)

A normal detector only knows a fixed list of categories. An
**open-vocabulary** detector is multimodal (it takes an image **and**
text): you hand it a free-text phrase like `"the red mug ."` and it boxes
whatever matches that description, even a category it was never
explicitly trained to name. This is enormously useful in robotics, where
the next object to find changes from task to task. The trade-off is that
these models are heavier and slower than a plain fixed-category detector.

## The architecture, in plain language

```text
                       ┌──────────────────────────┐
 camera image ───────► │  backbone (CNN or         │
 (grid of pixels)      │  Transformer over patches)│──► boxes + labels
                       │                           │    + confidences
 (open-vocab only:     │                           │    (and/or masks)
  text phrase) ───────►│                           │
                       └──────────────────────────┘
```

- A **backbone** turns the pixel grid into a compact summary of "what
  patterns are where."
- A small output stage reads that summary and emits the boxes, labels,
  confidences, and — for segmentation models — the masks.

## How a perception model is trained

It follows the standard recipe from
[`../01-basics/00-what-is-a-model.md`](../01-basics/00-what-is-a-model.md):
learn from labelled examples.

- **The data** is a large pile of images where humans have already drawn
  the boxes (or masks) and written the labels. The most famous such
  dataset is **COCO** (short for **Common Objects in Context**): roughly
  ~330k images across ~80 everyday categories, each hand-annotated. Other
  big ones exist; COCO is the one you will see quoted everywhere.
- **Training** shows the network an image, lets it guess the boxes, then
  nudges its weights so its guesses move closer to the human labels —
  repeated millions of times. This heavy step is usually done once by a
  research lab; you simply download the finished weights (a
  **checkpoint**).
- Most teams **never train from scratch**. They take a model pre-trained
  on COCO and either use it as-is or **fine-tune** it on a few hundred of
  their own labelled images to learn a new object.

## What it costs to run (inference)

This is where perception models shine compared with the heavier models
elsewhere in this area.

- **Latency** — a small detector runs a single image in only a few
  milliseconds on a good GPU, and still comfortably in real time on a
  small on-robot computer. (Figures approximate and drift — re-check for
  the specific model and hardware.)
- **Frame rate** — small detectors hit tens of frames per second; "real
  time" usually means keeping up with a ~30-frames-per-second camera.
- **Hardware** — a tiny detector can run on a CPU or a small NVIDIA
  **Jetson**-class board; larger open-vocabulary or segmentation models
  want a proper GPU with a few gigabytes of memory. See
  [`../01-basics/03-running-models-hardware-and-tools.md`](../01-basics/03-running-models-hardware-and-tools.md).
- **"At the edge"** means running the model on the small computer
  *on the robot itself*, rather than sending images to a server — which
  small detectors are fast and light enough to do.

## Limitations and failure modes

- **Flat 2-D only** — boxes and masks live in the image; they say nothing
  about distance or 3-D orientation (that is pose estimation's job).
- **Fixed vocabulary** for plain detectors — unknown categories are
  simply missed; open-vocabulary models trade speed to fix this.
- **Confident errors** — clutter, glare, motion blur, or an object unlike
  anything in training can yield a wrong label with a high score.
- **Small / distant / overlapping objects** are the classic hard cases.

## Key terms used on this page

- **Pixel** — one coloured dot of an image; an image is a grid of them.
- **Bounding box** — the rectangle a detector draws around an object.
- **Class label** — the category name the model assigns ("cup").
- **Confidence score** — 0-to-1 number for how sure the model is.
- **Mask** — a per-pixel yes/no map of exactly which pixels are an
  object (the segmentation output).
- **Convolutional neural network (CNN)** — image network that slides
  small pattern-detectors across the pixels.
- **Open-vocabulary** — detection driven by free text you supply, not a
  fixed category list.
- **COCO (Common Objects in Context)** — the best-known labelled image
  dataset used to train detectors.
- **Intersection over union (IoU)** — the standard score for "how well
  does a predicted box overlap the true box": the area they share divided
  by the area they jointly cover; 1.0 is a perfect match.

## See also

- The three most famous perception models, with runnable sketches:
  [`02-top-three-models.md`](02-top-three-models.md).
- What feeds on these outputs next:
  [`../04-pose-estimation-models/00-introduction.md`](../04-pose-estimation-models/00-introduction.md).
