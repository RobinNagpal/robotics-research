# 04 — See the tray (Perception & vision)

> Checklist exercise: **Layer 4 — "see the tray."**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

## What this program proves

So far the arm has been told *where* the vial is by us typing in
numbers. In the real laboratory the robot has to **work out where things
are by looking** — with a camera, from a picture. This exercise is the
first taste of that. It takes a single saved photograph of the sample
tray and answers two questions about it, using nothing but the picture:

1. **What is in the picture, and where?** We use **YOLO** (short for
   "You Only Look Once," a popular **object detector**: a program that
   has *learned*, from many example photos, to spot whole objects — a
   tray, a vial, a beaker — directly in a picture and draw a box around
   each one). The program runs YOLO on the photo, then prints how many
   objects it found, the **name** of each one, and the **box** that
   surrounds it.
2. **Where is the vial?** As a bonus, the program finds the round rim of
   the **2 millilitre glass vial** (a small glass cylinder, about twelve
   millimetres across) by hunting for a circle in the same picture, and
   draws a ring on it.

This is the whole idea of **perception**: turning a flat picture into
useful facts about where real things are. Once a robot can do this, it
no longer needs a human to type in positions — it can *see*. And note
what is *not* here: no printed markers, no stickers, no barcodes on the
tray. The robot recognises the real objects from their own appearance.

The best part: this program needs **no robot and no simulator**. It runs
entirely on your laptop against a saved photograph named `tray.png`. You
can do this exercise on a train.

> Teaching-code note: this example is deliberately stripped down, and the
> exact names and numbers in vision software drift between versions.
> Treat it as a clear illustration of the idea, not a guaranteed
> copy-paste for your particular photograph — the circle-finding settings
> in particular almost always need tuning to your own image.

> Where the trained model comes from: YOLO is a **learned** detector. It
> only knows the objects it was *trained* on, from labelled example
> images. Our plan is to generate those training images as **synthetic
> data** — thousands of automatically-labelled renders from the Gazebo
> twin of the cell, with the lighting, colours, and tray positions
> randomised so the model copes with the real bench. That pipeline is its
> own milestone; here we simply *use* a model and trust it exists. To try
> this today, the snippet below loads a small ready-made model
> (`yolo11n.pt`) so the code runs before our own model is trained.

## What you need first

You need **Python** (the programming language this is written in) and two
free libraries installed. A **library** is a bundle of ready-made code
someone else wrote that you borrow rather than writing yourself.

- **`ultralytics`** — the library that provides **YOLO**, the learned
  object detector we run to find things in the picture.
- **`opencv-python`** — the Python edition of **OpenCV**, which is short
  for the **Open Source Computer Vision library** (a large free toolkit
  for working with images). We also rely on **NumPy** (short for
  "Numerical Python," a library for handling grids of numbers), which
  installs alongside it.

Install all three from a terminal with Python's package installer:

```bash
pip install ultralytics opencv-python numpy
```

You also need a photograph of the tray saved next to the program as
`tray.png`. Any reasonably lit, head-on photo of a tray (with a vial in
view) will do — nothing has to be printed or stuck on it. The ending
`.png` marks it as a **Portable Network Graphics** file, a common
lossless image format.

## The whole program

Save this as a file named `see_the_tray.py`:

```python
import cv2
import numpy
from ultralytics import YOLO


IMAGE_FILE = "tray.png"
MODEL_FILE = "yolo11n.pt"   # swap for our own tray/vial model once trained


def find_objects(image_file):
    # Load the trained detector. yolo11n.pt is a small ready-made model
    # so this runs today; later we point MODEL_FILE at the model we
    # trained on synthetic pictures from the Gazebo twin.
    model = YOLO(MODEL_FILE)
    # Run the detector on the photograph. It returns a list of results,
    # one per image; we passed one image, so we take the first.
    results = model(image_file)
    result = results[0]
    boxes = result.boxes
    print(f"Found {len(boxes)} object(s).")
    for box in boxes:
        # Each box carries a class number; the model's .names table maps
        # that number to a human-readable label like "vial" or "tray".
        class_id = int(box.cls[0])
        label = result.names[class_id]
        confidence = float(box.conf[0])
        # The box edges come as four pixel numbers: left, top, right,
        # bottom (the corners of the rectangle around the object).
        left, top, right, bottom = box.xyxy[0]
        print(
            f"  {label} ({confidence:.0%} sure): "
            f"box left={left:.0f}, top={top:.0f}, "
            f"right={right:.0f}, bottom={bottom:.0f} pixels"
        )
    return result


def find_vial_rim(grey_image, colour_image):
    circles = cv2.HoughCircles(
        grey_image,
        cv2.HOUGH_GRADIENT,
        dp=1.0,
        minDist=50,
        param1=100,
        param2=30,
        minRadius=8,
        maxRadius=40,
    )
    if circles is None:
        print("No circular vial rim found.")
        return
    circles = numpy.uint16(numpy.around(circles))
    for x, y, radius in circles[0]:
        print(f"  Vial rim: centre x={x}, y={y}, radius={radius} pixels")
        cv2.circle(colour_image, (x, y), radius, (0, 255, 0), 2)


def main():
    colour_image = cv2.imread(IMAGE_FILE)
    if colour_image is None:
        print(f"Could not open {IMAGE_FILE}.")
        return
    grey_image = cv2.cvtColor(colour_image, cv2.COLOR_BGR2GRAY)

    find_objects(IMAGE_FILE)
    find_vial_rim(grey_image, colour_image)

    cv2.imwrite("tray_marked.png", colour_image)
    print("Saved the marked-up picture as tray_marked.png.")


if __name__ == "__main__":
    main()
```

## Every line explained

**`import cv2`**
The word `import` means "bring in a library of ready-made code so I can
use it." `cv2` is the name Python uses for **OpenCV** (the Open Source
Computer Vision library). This single line gives the program the ability
to open pictures, change their colour, find circles, and draw on them.

**`import numpy`**
This brings in **NumPy** (Numerical Python), the library for handling
grids of numbers. A picture, to a computer, *is* a grid of numbers — one
number per dot — so we will need this to do arithmetic on the results.

**`from ultralytics import YOLO`**
This brings in one specific tool, called `YOLO`, from the `ultralytics`
library. `YOLO` is a ready-made **object detector**: you load a trained
model into it, hand it a picture, and it hands back a list of every
object it recognised, each with a name and a box.

**`IMAGE_FILE = "tray.png"`**
This stores the filename of our photograph under a clearly-named constant
(a value we set once and reuse). Keeping it here at the top means you
change the filename in one obvious place if your photo is named something
else.

**`MODEL_FILE = "yolo11n.pt"`**
This stores the filename of the **trained model** — the file of learned
numbers that *is* the detector's knowledge. `yolo11n.pt` is a small
ready-made model so the code runs today. The `# swap ...` note reminds us
that, in the finished cell, this points at our own model — trained on
synthetic pictures rendered from the Gazebo twin — which knows our exact
trays, vials, and beakers. ("Synthetic" here means computer-generated
rather than photographed by hand.)

**`def find_objects(image_file):`**
`def` begins a named block of instructions (a "function"). This one is
named `find_objects`, and it expects to be handed `image_file` — the name
of the photograph to look at. (Unlike the bonus circle-finder below, YOLO
works straight from the colour picture file; it does not need a grey
copy.)

**`model = YOLO(MODEL_FILE)`**
This **loads the trained detector** from the model file into memory and
stores it in `model`. From here on, `model` is the finder we hand
pictures to.

**`results = model(image_file)`**
This is the actual looking. We hand the model our photograph; it scans it
and returns a list of results — one result per picture we gave it. We
store that list in `results`.

**`result = results[0]`**
We gave the model exactly one picture, so we reach into the list and take
the first (and only) result with `[0]`. This `result` holds everything
the detector found in our photo.

**`boxes = result.boxes`**
Inside the result sits a `boxes` collection: one entry for every object
the detector spotted, each carrying that object's name, its box, and how
sure the detector is. We pull it out into `boxes` for the lines below.

**`print(f"Found {len(boxes)} object(s).")`**
This prints a summary line to the terminal. `print(...)` shows text on
screen. `len(boxes)` counts how many objects are in the collection (`len`
is short for "length"). The `f"..."` is an *f-string*, a Python way to
drop a value into the middle of text. So if it found one object, this
prints `Found 1 object(s).`

**`for box in boxes:`**
This begins a **loop** — it runs the indented lines below once for *each*
object the detector found, calling the current one `box` each time
around. If three objects were found, the lines below run three times.

**`class_id = int(box.cls[0])`** and **`label = result.names[class_id]`**
Each detection records a **class number** — a plain integer code for
*what kind* of thing it is (say, `0` for tray, `1` for vial). We read
that number into `class_id`. The model also carries a `.names` table that
maps each number to a human-readable **label**; we look ours up and store
the word in `label`. So instead of "object 1" the robot can say "vial."

**`confidence = float(box.conf[0])`**
The detector also reports how **confident** it is in each find, as a
number between 0 and 1 (where 1 means completely sure). We read it into
`confidence`. This lets later code ignore shaky guesses and trust only
strong detections.

**`left, top, right, bottom = box.xyxy[0]`**
Each detection carries a **bounding box** — the rectangle drawn snugly
around the object — given as four numbers: the `left`, `top`, `right`,
and `bottom` edges. We pull those four apart into clearly-named values.
They are measured in **pixels**: a pixel is one single dot of the
picture, and a coordinate is just "how many dots across, how many dots
down," with the top-left corner of the picture as the zero point.

**`print(f"  {label} ... box left={left:.0f}, ...")`**
This prints the facts about this one object: its name, how sure the
detector is, and the four edges of its box. The `:.0%` shows the
confidence as a tidy percentage; the `:.0f` after each edge means "show
this as a whole number, no decimals." A 2-D box like this is the *start*
of perception, not the end. To send the arm somewhere we need the
object's **pose** — its full position and direction in real space. In the
cell we get there by reading the **depth** (how far away) at the box's
centre from an RGB-D camera (a camera that records colour *and* distance)
and deprojecting that pixel into 3-D. For a whole tray of vials we detect
the tray, then index each slot from the tray's known geometry. That
lifting step is its own milestone; this file stops at the 2-D find.

**`return result`**
The word `return` hands the whole result back to whoever called this
function, in case they want to use it. (Here we mainly wanted the
printout.)

**`def find_vial_rim(grey_image, colour_image):`**
This begins the second function, which hunts for the round rim of the
vial. It is handed two pictures: `grey_image` (to search in) and
`colour_image` (to draw the result on, so the ring shows up in colour).

**`circles = cv2.HoughCircles( ... )`**
This is the heart of the bonus task. `cv2.HoughCircles` is OpenCV's
**circle finder**. It uses a classic technique (named after its inventor,
Hough) that, in plain words, has every bright edge in the picture "vote"
for the circles it could belong to; spots that collect many votes are
declared circles. We hand it several settings, explained next, and it
returns a list of the circles it found, which we store in `circles`.

**`grey_image,`**
The first thing we hand the circle finder is the grey picture to search.
Unlike YOLO (which reads the colour file itself), this classic circle
finder works on a plain grey image, not colour.

**`cv2.HOUGH_GRADIENT,`**
This names *which* circle-finding method to use. `HOUGH_GRADIENT` is the
standard one built into OpenCV; you almost always pass exactly this.

**`dp=1.0,`**
A resolution setting. `1.0` tells the finder to work at the full detail
of the picture. Larger numbers make it faster but rougher. Leave it at
`1.0` to start.

**`minDist=50,`**
The smallest allowed gap, in pixels, between the centres of two separate
circles. Setting it to `50` says "do not report two circles whose middles
are closer than fifty dots apart" — this stops one real rim being
reported many times as a cluster of near-identical circles.

**`param1=100,`**
An internal sensitivity setting for deciding what counts as an edge in
the picture. `100` is a reasonable starting value; if no rim is found you
nudge this.

**`param2=30,`**
How many votes a circle needs before it is believed. Lower means more
circles found (including false ones); higher means fewer, surer circles.
`30` is a sensible middle.

**`minRadius=8,`** and **`maxRadius=40,`**
The smallest and largest circle size to accept, in pixels. We tell it the
vial rim is somewhere between eight and forty dots across in radius, so it
ignores tiny specks and large background curves. These two numbers depend
entirely on how big the vial looks in *your* photo, and are the first
things to adjust.

**`if circles is None:`**
After the search, `circles` either holds the found circles or the special
value `None`, which means "nothing found." This line checks for that
empty case.

**`print("No circular vial rim found.")`** and **`return`**
If nothing was found, we say so and `return` — which here means "stop this
function early and go back," since there is nothing more to do.

**`circles = numpy.uint16(numpy.around(circles))`**
The finder returns the circle positions as decimal numbers (like 142.7).
To draw and print them tidily we want plain whole numbers. `numpy.around`
rounds each value to the nearest whole number, and `numpy.uint16` then
stores them as whole numbers. We overwrite `circles` with this cleaned-up
version.

**`for x, y, radius in circles[0]:`**
A loop over the found circles. Each circle is described by three numbers,
which we pull apart into `x` (how far across its centre is), `y` (how far
down its centre is), and `radius` (how big it is, from centre to edge), all
in pixels. The `[0]` is a quirk of how the finder packages its answer; it
simply gets at the actual list of circles inside.

**`print(f"  Vial rim: centre x={x}, y={y}, radius={radius} pixels")`**
This prints the facts about one found circle: where its centre is and how
big it is, all in pixels.

**`cv2.circle(colour_image, (x, y), radius, (0, 255, 0), 2)`**
This **draws** a ring onto the colour picture so you can see what was
found. We hand `cv2.circle` the picture to draw on, the centre point
`(x, y)`, the `radius`, then the colour and the line thickness. The colour
`(0, 255, 0)` is given as three numbers for blue, green, and red
intensity from 0 to 255 — note OpenCV lists them in **blue-green-red**
order, the reverse of the usual **red-green-blue colour** order, so
`(0, 255, 0)` means pure green. The final `2` is the thickness of the
ring's line in pixels.

**`def main():`**
This begins the program's main routine — the steps that run when you
launch the file.

**`colour_image = cv2.imread(IMAGE_FILE)`**
This **opens and reads** the photograph from disk into memory.
`cv2.imread` ("image read") loads the file named in `IMAGE_FILE` and
hands back the picture as a grid of numbers, which we store in
`colour_image`. This is the full-colour version.

**`if colour_image is None:`** and the lines under it
If the file could not be opened (wrong name, wrong folder), `cv2.imread`
hands back `None`. We check for that, print a clear complaint, and
`return` to stop — far friendlier than crashing with a confusing error
later.

**`grey_image = cv2.cvtColor(colour_image, cv2.COLOR_BGR2GRAY)`**
This makes a **grey** copy of the picture. `cv2.cvtColor` ("convert
colour") changes a picture from one colour scheme to another;
`COLOR_BGR2GRAY` means "from blue-green-red colour to plain grey." The
bonus circle-finder below works on this grey copy, while the colour
original is kept for drawing on. (YOLO reads the colour file itself, so
it does not use the grey copy.)

**`find_objects(IMAGE_FILE)`**
This runs our first function on the photograph: find and print the
objects YOLO recognised.

**`find_vial_rim(grey_image, colour_image)`**
This runs our second function: find the vial's rim in the grey picture and
draw the result onto the colour picture.

**`cv2.imwrite("tray_marked.png", colour_image)`**
This **saves** the now-drawn-on colour picture to a new file named
`tray_marked.png`. `cv2.imwrite` ("image write") is the mirror image of
`imread`: it writes a picture from memory back out to disk. You open this
file afterwards to *see* the green ring on the vial.

**`print("Saved the marked-up picture as tray_marked.png.")`**
A friendly closing line so you know where to look for the result.

**`if __name__ == "__main__":`**
A standard Python guard meaning "only run the next line if this file was
launched directly (rather than being imported by another file)."

**`main()`**
Finally calls the main routine, setting everything above in motion.

## How to run it, and how you know it worked

Put a photograph named `tray.png` in the same folder as the program, then,
in a terminal in that folder, run:

```bash
python3 see_the_tray.py
```

You should see something like:

```
Found 2 object(s).
  tray (88% sure): box left=120, top=80, right=540, bottom=470 pixels
  vial (74% sure): box left=590, top=270, right=650, bottom=360 pixels
  Vial rim: centre x=620, y=300, radius=18 pixels
Saved the marked-up picture as tray_marked.png.
```

Then open `tray_marked.png` and you will see a green ring drawn around the
vial's rim.

If no objects are found, check that the photo is well lit and in focus,
and remember the ready-made `yolo11n.pt` model only knows everyday
objects — it may not recognise a lab tray until you swap in our own model
trained on synthetic pictures from the Gazebo twin. If no circle is found
(or too many are), adjust `minRadius`, `maxRadius`, and `param2` to match
how big and how clear the vial looks in *your* photo — circle-finding
almost always needs this tuning.

**Done when:** the program prints at least one detected object's name and
box, and either prints the vial rim's position or draws a ring on it in
the saved picture. You have now pulled real facts about where things are
out of a flat photograph — the foundation of every "the robot looks and
then acts" step later in the project.

## Where this fits

- This is the runnable version of the **Layer 4** exercise in
  [`../07-learning-checklist.md`](../07-learning-checklist.md).
- The deeper write-up of perception and vision (cameras, depth, and how
  we detect objects with YOLO) is
  [`../05-mycobot-280-impl/01-only-code/04-perception-and-vision.md`](../05-mycobot-280-impl/01-only-code/04-perception-and-vision.md).
- The capstone, [`14-hello-cell-capstone.md`](14-hello-cell-capstone.md),
  uses this same "look at the tray, detect the vial" step to decide where
  to send the arm in the full pick-and-place loop.
