# 02 — Top three perception & vision models (with code)

> **Goal of this page.** Name the three most famous perception models you
> can actually download and run, compare them, and give a short, commented
> code sample for each. Builds on [`00-introduction.md`](00-introduction.md)
> and [`01-working.md`](01-working.md).
>
> **Read me first — all numbers are approximate and drift fast.**
> Speeds, licences and especially install/run commands change often. Treat
> every code block as a *teaching sketch* that shows the shape of the
> Application Programming Interface (API — the set of functions a library
> gives you), not a guaranteed-runnable script. Always check the model's
> current documentation. Unlike the heavier models elsewhere in this area,
> the first one here runs happily on a plain laptop.

## Why these three

These are the three best-known perception models, picked to cover the two
tasks from [`00-introduction.md`](00-introduction.md) — drawing boxes
versus tracing exact outlines — plus the newer "name it in text" style:

| Model | Maker | Task | ~Speed | Licence | Bottom line |
|---|---|---|---|---|---|
| **YOLO11** | Ultralytics | Object detection (boxes) | Real-time, ~hundreds of frames/sec on a GPU | AGPL-3.0 (paid licence for closed products) | The default detector to learn on — fast, tiny, runs on a laptop or on the robot |
| **SAM 2** | Meta | Promptable segmentation (exact masks) | ~Tens of frames/sec on a GPU | Apache-2.0 (permissive) | Click a point, get a pixel-perfect outline of *anything* — no fixed category list |
| **Grounding DINO** | IDEA-Research | Open-vocabulary detection (boxes from text) | ~A few to ~tens of frames/sec on a GPU | Apache-2.0 (permissive) | Box objects you describe in free text — heavier, but no retraining for new objects |

The tasks ("detection" vs "segmentation") and "open-vocabulary" are all
explained in [`00-introduction.md`](00-introduction.md) and
[`01-working.md`](01-working.md).

---

## 1. YOLO11 (You Only Look Once)

**What it is.** **YOLO** stands for **You Only Look Once** — the name
refers to its trick of finding every object in a single pass over the
image, which is why it is so fast. **YOLO11** is the current version from
the company **Ultralytics** (2024). It is a convolutional neural network
(the image-network design from [`01-working.md`](01-working.md)) trained
on the **COCO (Common Objects in Context)** dataset, so out of the box it
knows ~80 everyday categories (person, cup, bottle, chair...). It is the
standard starting point: one `pip install`, weights download themselves,
and it runs in real time even on modest hardware. The `n` in `yolo11n`
means **nano** — the smallest, fastest size; bigger sizes (`s`, `m`,
`l`, `x`) trade speed for accuracy.

**Install.**

```bash
# Runs on a plain CPU; a GPU just makes it faster. No GPU required.
pip install ultralytics          # pulls in PyTorch and everything else
```

**Minimal code to run it.**

```python
# Goal: hand YOLO11 one image and print the objects it found — a box, a
# label, and a confidence score for each. This is "inference": using a
# trained model, not training one.

from ultralytics import YOLO     # the Ultralytics library

# 1. Load a pretrained model. "yolo11n.pt" is the nano checkpoint (the
#    trained weights file); it auto-downloads the first time only, then
#    is cached on disk.
model = YOLO("yolo11n.pt")

# 2. Run detection on one image. Pass a file path (or a URL, or a folder).
#    "results" is a list with one entry per image you passed in.
results = model("image.jpg")

# 3. Read out what it found. results[0] is the first (here, only) image.
#    Each detected object is a "box" with three useful pieces:
for box in results[0].boxes:
    label = model.names[int(box.cls)]   # class name, e.g. "cup"
    confidence = float(box.conf)         # 0-to-1 sureness, e.g. 0.94
    xyxy = box.xyxy[0].tolist()          # rectangle corners: [x1,y1,x2,y2]
    print(f"{label}  conf={confidence:.2f}  box={xyxy}")

# 4. Pop open a window with the boxes drawn on the image, so you can see
#    the result instead of just reading numbers.
results[0].show()
```

**What you should see.** A few printed lines — one per object, e.g.
`cup  conf=0.94  box=[40.0, 55.0, 160.0, 145.0]` — and a window showing
your image with labelled rectangles drawn over each detected object.

---

## 2. Segment Anything Model 2 (SAM 2)

**What it is.** **SAM 2** — the second **Segment Anything Model**, from
Meta (2024) — does **promptable segmentation**: you give it a *prompt*
(most simply, a single point you click on an object) and it returns the
exact **mask** — the per-pixel outline — of whatever object that point
sits on. The magic is that it has **no fixed category list**: it will
outline *anything*, named or not. (It does not tell you *what* the object
is called — only its shape; pair it with a detector if you need labels.)
It also tracks objects across video frames. Two easy ways to run it: via
the same **Ultralytics** library, or via Meta's own **`sam2`** package.

**Install.**

```bash
# Easiest route reuses the Ultralytics library from model 1 above.
pip install ultralytics          # exposes a SAM wrapper too

# Alternative: Meta's own package (more features, more setup).
# pip install git+https://github.com/facebookresearch/sam2.git
```

**Minimal code to run it.**

```python
# Goal: hand SAM 2 one image plus one point, and get back the mask (the
# exact outline) of the object under that point. Teaching sketch — API
# names follow the Ultralytics SAM wrapper and may change.

from ultralytics import SAM      # the SAM wrapper in Ultralytics

# 1. Load a pretrained SAM 2 checkpoint (auto-downloads first time).
#    "_t" is the tiny size; larger sizes are slower but a touch sharper.
model = SAM("sam2_t.pt")

# 2. Tell it WHERE to look. "points" is one pixel location [x, y] you
#    would normally get from a mouse click or from a detector's box
#    centre. "labels=[1]" means "this point is ON the object I want"
#    (a 0 would mean "this point is background, avoid it").
results = model("image.jpg", points=[[400, 300]], labels=[1])

# 3. The result carries the mask: a same-size grid marking each pixel as
#    1 (part of the object) or 0 (not). Here we just report its shape.
mask = results[0].masks.data      # a tensor (array) of yes/no values
print("mask shape:", tuple(mask.shape))   # e.g. (1, 480, 640)

# 4. Draw the mask over the image in a window so you can see the outline.
results[0].show()
```

**What you should see.** A printed mask shape such as `(1, 480, 640)` —
one mask, the same height and width as your image — and a window showing
your image with the picked object shaded in, tracing its true outline
(not just a rectangle).

---

## 3. Grounding DINO

**What it is.** **Grounding DINO** (IDEA-Research, 2023) is an
**open-vocabulary** detector: instead of a fixed category list, you give
it a free-text phrase and it boxes whatever matches. Ask for
`"the red mug ."` and it returns a box around the red mug — even if "red
mug" was never one of its training categories. It is a Transformer-based
detector (the design from [`01-working.md`](01-working.md)) and is
heavier and slower than YOLO, which is the price of that flexibility.
("DINO" here is the detector's name, not the dinosaur; the leading dot
after each phrase is just how this model wants prompts separated.) The
tidiest way to run it is through Hugging Face's **`transformers`**
library.

**Install.**

```bash
# A GPU is recommended; it will run on CPU but slowly.
pip install transformers torch pillow   # loader + PyTorch + image handling
```

**Minimal code to run it.**

```python
# Goal: hand Grounding DINO one image plus a text phrase, and get boxes
# for the things the phrase names. Teaching sketch — check current docs.

from transformers import (AutoProcessor,
                          AutoModelForZeroShotObjectDetection)
from PIL import Image            # PIL = Python Imaging Library: opens images
import torch                     # PyTorch: runs the neural network

# 1. Download the processor (turns image + text into model inputs) and the
#    model weights from the Hugging Face hub (first run only, then cached).
model_id = "IDEA-Research/grounding-dino-tiny"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForZeroShotObjectDetection.from_pretrained(model_id)

# 2. Load the image, and write what you want to find as plain text. Each
#    phrase is lower-case and ends with " ." — the format this model wants.
image = Image.open("image.jpg")
text = "the red mug . a bottle ."

# 3. Pack image + text together and run the model (no_grad = "we're using
#    it, not training, so don't waste memory tracking gradients").
inputs = processor(images=image, text=text, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)

# 4. Turn raw outputs into clean boxes, keeping only confident ones. The
#    helper returns boxes, scores, and the matched text for each find.
results = processor.post_process_grounded_object_detection(
    outputs, inputs.input_ids,
    box_threshold=0.4,            # ignore boxes the model is unsure about
    text_threshold=0.3,           # ignore weak text matches
    target_sizes=[image.size[::-1]])   # scale boxes to the image's size

# 5. Print each match: the phrase it matched, its confidence, its box.
for label, score, box in zip(results[0]["labels"],
                             results[0]["scores"],
                             results[0]["boxes"]):
    print(f"{label}  conf={float(score):.2f}  box={box.tolist()}")
```

**What you should see.** One printed line per match, e.g.
`the red mug  conf=0.71  box=[120.0, 80.0, 240.0, 210.0]`. If your phrase
names nothing in the picture, you simply get no boxes back — that is the
model correctly saying "not here."

---

## Choosing between them

- **Fast everyday detection, runs anywhere (laptop or robot)** →
  **YOLO11**. Start here. (Mind the AGPL licence for closed products.)
- **Need the exact outline / to separate touching objects** → **SAM 2**.
  Pair it with a detector when you also need to know *what* each object
  is.
- **The object to find changes per task and is hard to pre-list** →
  **Grounding DINO**, so you can just describe it in text. Slower and
  hungrier, so reach for it only when a fixed category list will not do.

A common robotics combination is **Grounding DINO to find the named
object, then SAM 2 to get its precise mask** — text in, pixel-perfect
outline out.

## See also

- What these are and when to use them:
  [`00-introduction.md`](00-introduction.md).
- The mechanics behind the code: [`01-working.md`](01-working.md).
- What consumes these outputs next:
  [`../04-pose-estimation-models/00-introduction.md`](../04-pose-estimation-models/00-introduction.md)
  and
  [`../05-grasp-generation-models/00-introduction.md`](../05-grasp-generation-models/00-introduction.md).
- A hands-on perception exercise in this repo's autosampler project:
  [`../../03-hplc-autosampler/04-hello-worlds/04-see-the-tray.md`](../../03-hplc-autosampler/04-hello-worlds/04-see-the-tray.md).
