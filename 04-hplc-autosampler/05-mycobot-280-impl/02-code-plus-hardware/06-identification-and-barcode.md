# Layer 06 — Identification & barcode (code-plus-hardware)

> **Job:** Read the barcode or QR code on each real HPLC vial, decode it
> to a unique ID, and trace that vial through the prep → load loop — and,
> where needed, *print and apply* the label in the first place.
>
> **Mode — code plus hardware.** A real **scanner** is now an option, not
> just software decoding of camera frames. That widens the toolbox: a
> dedicated scanning device can do the read in hardware, or you can keep
> decoding frames from the arm's wrist camera in software, or you can
> add a **label printer** so the cell labels blanks itself. We choose
> across all three.

Terms first. A **1D barcode** is the striped pattern read along one line
(Code 128, EAN-13); a **2D barcode** (a **QR code** or DataMatrix) packs
data into a grid and fits more into a smaller label — which is why small
vials favour it. To **decode** is to recover the code's text from an
image. **Read-rate** is the fraction of presented codes that decode on
the first try; on the bench it is hurt by curved glass, glare, blur, and
bad angles, so it is the number that matters most here. A few extra
hardware terms: a **USB-HID keyboard-wedge** scanner pretends to be a
keyboard and "types" the decoded text wherever the cursor is — **HID**
is the USB profile for keyboards/mice, so no driver or SDK is needed. An
**SDK** is a vendor software kit that exposes the scanner's full
features to your code. **ZPL** (Zebra Programming Language) is the
command language most label printers speak.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| Industrial vision scanner SDK (Cognex DataMan / Zebra / Honeywell) | Dedicated rugged reader + SDK | `Best-in-class` | Top read-rate on curved glass, rugged — but pricey. |
| USB-HID scanner as keyboard-wedge (no SDK) | Plug-in hardware reader | `Cheapest` | ~$30, types the ID with zero code or driver. |
| pyzbar / ZBar on the real wrist camera | Software decode of arm-camera frames | `Best-practical` | Free, reuses the camera you have; pair behind a USB-HID scanner. |
| zxing-cpp on the real camera | Software decode, broader symbologies | `Alternative` | Wider code support than ZBar; still no scanner robustness. |
| Label-printer library (ZPL via `zebra` / `python-escpos`) | In-line label *printing* | `Alternative` | Creates and applies the ID; complements, not replaces, reading. |

## Industrial vision scanner SDK (Cognex DataMan / Zebra / Honeywell)

These are purpose-built fixed-mount or handheld code readers — Cognex
DataMan, Zebra's fixed industrial scanners, Honeywell's vision readers —
each paired with a vendor **SDK** that exposes triggering, image
capture, decode results, and read diagnostics to your code. They combine
a tuned camera, controllable lighting, and a hardened decode engine in
one rugged box designed to run on a line for years.

Where it shines: **read-rate and reliability are the best here**,
especially on the hard cases this cell actually produces — a QR code
curving around cylindrical glass, glare from the vial's shoulder, a
small DataMatrix at an angle. Built-in, aimable lighting and autofocus
optics solve the **fixturing and lighting** problem that plagues the
software-on-camera options, and the SDK gives you proper read/no-read
signals and image logging for traceability. For a regulated,
trace-everything HPLC workflow, that determinism is worth a lot.

Where it is bad versus the others: it is **expensive and heavier to
integrate**. A single industrial reader runs ~$1,000–$5,000+ (re-check),
versus ~$30 for a **USB-HID scanner** or $0 of extra hardware for
**pyzbar on the wrist camera**. Each vendor SDK is its own integration
and licence, less portable than free **zxing-cpp** or **ZBar**. And it
only *reads* — it does nothing for labelling, where the **label-printer
library** is needed. It is the right answer when read-rate on curved
glass is the project's risk, and overkill otherwise.

## USB-HID scanner as keyboard-wedge (no SDK)

A commodity USB barcode scanner configured as a **keyboard-wedge**
appears to the computer as a USB keyboard: aim, trigger, and it "types"
the decoded string (usually followed by Enter) into whatever has focus.
There is no driver, no SDK, and no library — you read the text as if it
came from the keyboard, or from a serial port if you prefer that mode.

Where it shines: it is the **cheapest and simplest** real reader by a
wide margin — ~$30, working in minutes, with effectively zero code. Its
dedicated decode chip and (often) aiming illumination give it a
materially better read-rate than **pyzbar/ZBar on the wrist camera** on
ordinary labels, because it is a real scanner rather than a
general-purpose camera. For a small team that just needs reliable IDs at
a fixed scan station, it is remarkable value.

Where it is bad versus the others: it is **inflexible and blind to your
software**. The keyboard-wedge model gives you only the decoded string —
no image, no read-confidence, no logging — so you cannot diagnose a
**no-read** or audit a frame the way a **Cognex/Zebra SDK** lets you,
which is a real gap for traceability. Cheap units also struggle with
**curved glass and glare** more than an industrial reader, and a handheld
unit needs a person or a fixturing jig since the arm cannot pull its
trigger. It is the cheapest path to *a* read, not the most controllable
one — pair it with software fallback rather than trusting it alone.

## pyzbar / ZBar on the real wrist camera

This option buys no scanner at all: it points the camera already mounted
near the gripper at the vial and decodes the frame in software with
ZBar, reached from Python through **pyzbar**. It is the direct
continuation of the only-code approach, now fed real images instead of
rendered textures.

Where it shines: it is **free and reuses hardware you already have** for
perception, so it adds no cost and no new device. The arm can actively
position the vial in front of its own camera and re-photograph from
several angles until a read succeeds — a closed-loop trick a fixed
**USB-HID scanner** cannot do. As a **best-practical** layer it pairs
beautifully behind a cheap scanner: let the USB-HID unit do the routine
reads, and fall back to wrist-camera pyzbar (or a re-orient-and-retry)
when the scanner returns a no-read.

Where it is bad versus the others: its **bench read-rate is the weakest**
of the readers. A general-purpose camera with ambient lighting handles
**curved glass, glare, and blur** far worse than a **USB-HID scanner**
or an **industrial reader** with their tuned optics and aimed light, so
**fixturing and lighting** become your problem to solve. ZBar's
symbology list also trails **zxing-cpp's** (weak DataMatrix), and pyzbar
brings a native dependency. It is the ideal free *fallback and
verifier*, but leaning on it as the sole reader invites missed reads.

## zxing-cpp on the real camera

zxing-cpp is the modern C++ port of the ZXing toolkit, installable as a
Python wheel, decoding a broad set of 1D and 2D symbologies from camera
frames. In hardware mode it plays the same role as pyzbar — software
decode of the wrist camera — but with wider code support and generally
better tolerance of rotation and mild degradation.

Where it shines: it has the **widest free symbology coverage** of the
software options and is fast and actively maintained. If the vials carry
DataMatrix or a mix of code types that **ZBar** handles poorly, zxing-cpp
is the stronger free decoder, and it installs cleanly without pyzbar's
native-library friction. As a software fallback it is arguably a better
engine than ZBar.

Where it is bad versus the others: it shares the **fundamental limit of
all software-on-camera decode** — it cannot conjure read-rate that the
optics and lighting do not provide, so on **curved glass and glare** it
still trails a real **USB-HID** or **industrial** scanner. It adds a
dependency where **pyzbar** continues the only-code stack already in
place, and it offers none of the traceability signals of a vendor
**SDK**. A fine alternative engine for the camera path, but it does not
change the tiering — hence Alternative.

## Label-printer library (ZPL via `zebra` / `python-escpos`)

This option addresses the other half of identification: not reading an
existing code but **printing and applying** one. A label-printer library
— sending **ZPL** to a Zebra-class printer (via a `zebra` helper or raw
sockets), or driving a smaller printer through `python-escpos` — lets
the cell generate a unique ID, render it as a 1D or 2D code, and print a
label for a blank vial **in line**.

Where it shines: it is the **only option here that creates identity**
rather than consuming it. If incoming vials arrive unlabelled, nothing
the four readers do matters until a code exists — so the printer library
is what makes the whole trace-every-vial requirement achievable from
blanks. ZPL is a stable, well-documented language, and printing a fresh,
flat, high-contrast label sidesteps the **curved-glass read-rate**
problem at the source by giving every later read an easy target.

Where it is bad versus the others: it **does not read anything**, so it
cannot stand alone — it complements a reader, never replaces one. It also
introduces the genuinely hard mechanical problem of **label
application**: peeling and pressing an adhesive label squarely onto a
small cylindrical vial usually needs an applicator or a careful fixture,
which is real engineering the **USB-HID scanner** and camera options
avoid entirely. Essential when you must label blanks, irrelevant when
vials arrive pre-coded — so it sits as an Alternative alongside whichever
reader you pick.

## Bench realities to plan for

- **Curved glass and glare.** A code wrapped around a ~12 mm vial is the
  single biggest read-rate killer. Industrial readers handle it best;
  printing a small flat 2D code and reading it head-on helps every
  option.
- **Fixturing and lighting.** A fixed scan pose with controlled,
  off-axis light beats ambient room light. The arm can also re-present
  the vial to a fixed reader or to its own camera and retry.
- **Label application.** Printing is easy; applying a straight,
  bubble-free label to curved glass is not — budget for an applicator or
  jig if you label blanks in-line.

## Verdict

- **Best-in-class — Industrial vision scanner SDK (Cognex DataMan /
  Zebra / Honeywell).** The highest, most dependable read-rate on curved
  glass, with tuned lighting/optics and SDK-level read logging for
  traceability — the right call when read-rate is the risk, accepting
  ~$1,000–$5,000+ per unit (re-check) and a vendor SDK to integrate.
- **Cheapest — USB-HID scanner as keyboard-wedge (or pyzbar on the
  existing camera).** A ~$30 scanner that "types" the ID with zero SDK
  or driver, or free software decode reusing the wrist camera; gets you
  reliable reads fast, with no diagnostics and weaker performance on
  curved/ glare-heavy vials.
- **Best-practical — fixed USB-HID scanner + pyzbar software fallback.**
  Let the cheap dedicated scanner do the routine reads and fall back to
  wrist-camera pyzbar (with re-orient-and-retry) on a no-read — near-zero
  cost, good everyday read-rate, and a closed-loop second chance without
  paying for an industrial reader. Add a label-printer library only if
  vials arrive unlabelled.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (simulated camera, software decode only):
  [`../01-only-code/06-identification-and-barcode.md`](../01-only-code/06-identification-and-barcode.md)
