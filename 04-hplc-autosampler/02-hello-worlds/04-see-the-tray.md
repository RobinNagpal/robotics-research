# 04 — See the tray (Perception & vision)

> Checklist exercise: **Layer 4 — "see the tray."**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

## What this program proves

So far the arm has been told *where* the vial is by us typing in
numbers. In the real laboratory the robot has to **work out where things
are by looking** — with a camera, from a picture. This exercise is the
first taste of that. It takes a single saved photograph of the sample
tray and answers two questions about it, using nothing but the picture:

1. **Where is the tray?** We stick a printed square marker on the tray —
   an **AprilTag**: a chunky black-and-white pattern, like a sturdier
   barcode, designed so a computer can spot it easily and read exactly
   where it is and which one it is. The program finds the tag, prints
   its **identifying number**, and prints where its centre sits in the
   picture.
2. **Where is the vial?** As a bonus, the program finds the round rim of
   the **2 millilitre glass vial** (a small glass cylinder, about twelve
   millimetres across) by hunting for a circle in the same picture, and
   draws a ring on it.

This is the whole idea of **perception**: turning a flat picture into
useful facts about where real things are. Once a robot can do this, it
no longer needs a human to type in positions — it can *see*.

The best part: this program needs **no robot and no simulator**. It runs
entirely on your laptop against a saved photograph named `tray.png`. You
can do this exercise on a train.

> Teaching-code note: this example is deliberately stripped down, and the
> exact names and numbers in vision software drift between versions.
> Treat it as a clear illustration of the idea, not a guaranteed
> copy-paste for your particular photograph — the circle-finding settings
> in particular almost always need tuning to your own image.

## What you need first

You need **Python** (the programming language this is written in) and two
free libraries installed. A **library** is a bundle of ready-made code
someone else wrote that you borrow rather than writing yourself.

- **`pupil_apriltags`** — a library that finds AprilTags in a picture.
- **`opencv-python`** — the Python edition of **OpenCV**, which is short
  for the **Open Source Computer Vision library** (a large free toolkit
  for working with images). We also rely on **NumPy** (short for
  "Numerical Python," a library for handling grids of numbers), which
  installs alongside it.

Install all three from a terminal with Python's package installer:

```bash
pip install pupil-apriltags opencv-python numpy
```

You also need a photograph of the tray saved next to the program as
`tray.png`. Any reasonably lit, head-on photo of a tray with an AprilTag
printed and stuck on it (and a vial in view) will do. The ending `.png`
marks it as a **Portable Network Graphics** file, a common lossless image
format.

## The whole program

Save this as a file named `see_the_tray.py`:

```python
import cv2
import numpy
from pupil_apriltags import Detector


IMAGE_FILE = "tray.png"


def find_apriltags(grey_image):
    detector = Detector(families="tag36h11")
    tags = detector.detect(grey_image)
    print(f"Found {len(tags)} AprilTag(s).")
    for tag in tags:
        centre_x, centre_y = tag.center
        print(
            f"  Tag id {tag.tag_id}: "
            f"centre at x={centre_x:.0f}, y={centre_y:.0f} pixels"
        )
    return tags


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

    find_apriltags(grey_image)
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

**`from pupil_apriltags import Detector`**
This brings in one specific tool, called `Detector`, from the
`pupil_apriltags` library. A **detector** is a ready-made finder: you
hand it a picture and it hands back a list of every AprilTag it spotted.

**`IMAGE_FILE = "tray.png"`**
This stores the filename of our photograph under a clearly-named constant
(a value we set once and reuse). Keeping it here at the top means you
change the filename in one obvious place if your photo is named something
else.

**`def find_apriltags(grey_image):`**
`def` begins a named block of instructions (a "function"). This one is
named `find_apriltags`, and it expects to be handed `grey_image` — the
photograph after it has been turned to shades of grey. (The AprilTag
finder works on a plain black-grey-white version of the picture, not a
colour one.)

**`detector = Detector(families="tag36h11")`**
This builds the AprilTag finder. The setting `families="tag36h11"` names
which *style* of tag to look for. AprilTags come in several families
(think of them as different alphabets of patterns); `tag36h11` is the
most common one. We must tell the finder which family our printed tag
belongs to, or it will not recognise it.

**`tags = detector.detect(grey_image)`**
This is the actual looking. We hand the finder our grey picture; it scans
it and returns a list of every tag it found. We store that list in
`tags`. Each item in the list is one tag, carrying facts about it — most
importantly which tag it is and exactly where it sits.

**`print(f"Found {len(tags)} AprilTag(s).")`**
This prints a summary line to the terminal. `print(...)` shows text on
screen. `len(tags)` counts how many items are in the list (`len` is short
for "length"). The `f"..."` is an *f-string*, a Python way to drop a
value into the middle of text. So if it found one tag, this prints
`Found 1 AprilTag(s).`

**`for tag in tags:`**
This begins a **loop** — it runs the indented lines below once for *each*
tag in the list, calling the current one `tag` each time around. If three
tags were found, the lines below run three times.

**`centre_x, centre_y = tag.center`**
Each tag carries a `center` — the exact spot in the picture where the
middle of the tag sits, given as two numbers. We pull those two numbers
apart into `centre_x` (how far across, left to right) and `centre_y` (how
far down, top to bottom). These positions are measured in **pixels**: a
pixel is one single dot of the picture, and a coordinate is just "how
many dots across, how many dots down." The top-left corner of the picture
is the zero point.

**`print(f"  Tag id {tag.tag_id}: centre at x={centre_x:.0f}, y={centre_y:.0f} pixels")`**
This prints the facts about this one tag. `tag.tag_id` is the tag's
**identifying number** — every AprilTag has a number baked into its
pattern, so the robot can tell one tag from another (tag 5 on the tray,
tag 9 on the bin, and so on). The `:.0f` after each centre value means
"show this as a whole number, no decimals," to keep the line tidy. Where
a tag's position is reported, we have effectively found a **fiducial
marker** — a deliberately-placed reference object whose known position
lets a robot orient itself. ("Fiducial" just means "trusted point of
reference.") The full position-and-direction of a real object in space is
called its **pose**; the AprilTag is the easiest honest way to recover
one from a picture.

**`return tags`**
The word `return` hands the list of found tags back to whoever called
this function, in case they want to use it. (Here we mainly wanted the
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
Like the tag finder, it works on a plain grey image, not colour.

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
`COLOR_BGR2GRAY` means "from blue-green-red colour to plain grey." Both
detectors below work on this grey copy, while the colour original is kept
for drawing on.

**`find_apriltags(grey_image)`**
This runs our first function on the grey picture: find and print the
AprilTags.

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
Found 1 AprilTag(s).
  Tag id 3: centre at x=412, y=255 pixels
  Vial rim: centre x=620, y=300, radius=18 pixels
Saved the marked-up picture as tray_marked.png.
```

Then open `tray_marked.png` and you will see a green ring drawn around the
vial's rim.

If no tag is found, check that the tag in the photo is the `tag36h11`
family and is well lit and in focus. If no circle is found (or too many
are), adjust `minRadius`, `maxRadius`, and `param2` to match how big and
how clear the vial looks in *your* photo — circle-finding almost always
needs this tuning.

**Done when:** the program prints at least one AprilTag's identifying
number and centre position, and either prints the vial rim's position or
draws a ring on it in the saved picture. You have now pulled real facts
about where things are out of a flat photograph — the foundation of every
"the robot looks and then acts" step later in the project.

## Where this fits

- This is the runnable version of the **Layer 4** exercise in
  [`../07-learning-checklist.md`](../07-learning-checklist.md).
- The deeper write-up of perception and vision (cameras, depth, and why
  we lean on markers first) is
  [`../04-mycobot-280-impl/01-only-code/04-perception-and-vision.md`](../04-mycobot-280-impl/01-only-code/04-perception-and-vision.md).
- The capstone, [`12-hello-cell-capstone.md`](12-hello-cell-capstone.md),
  uses this same "look at the tray, find the marker and the vial" step to
  decide where to send the arm in the full pick-and-place loop.
