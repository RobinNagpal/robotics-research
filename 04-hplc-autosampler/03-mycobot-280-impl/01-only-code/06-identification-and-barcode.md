# Layer 06 — Identification & barcode (only-code)

> **Job:** Read the barcode or QR code printed on each HPLC vial from a
> *simulated* camera image, decode it to a unique ID string, and hand
> that ID to the tracking logic — so every vial can be told apart and
> followed through the prep → load loop.
>
> **Mode — only code.** No real scanner and no real camera exist. The
> code on the vial is just a **texture** (an image painted onto the 3-D
> vial model) rendered by the simulator. A virtual camera grabs a frame,
> and a pure-software **decoder** (a library that finds a code in an
> image and turns its bars or squares back into the original text) does
> the work. We are choosing that decoder library.

A few terms up front. A **1D barcode** is the familiar pattern of
parallel black-and-white stripes (e.g. Code 128, EAN-13); it stores a
short string and is read along one line. A **2D barcode** packs data
into a grid of squares (e.g. a **QR code** or a DataMatrix) and holds
far more data in a smaller area, which is why tiny vial labels usually
use them. To **decode** is to locate the code in the image and recover
its text. **Read-rate** is the fraction of presented codes a library
successfully decodes — a blurry, angled, or glare-covered code lowers
it. In only-code mode we control the rendering, so read-rate is mostly
a question of how forgiving the library is to imperfect synthetic
frames.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| Dynamsoft Barcode Reader | Commercial decode SDK | `Best-in-class` | Highest read-rates and robustness on poor images — paid licence. |
| ZBar (via pyzbar) | Classic open-source decoder | `Cheapest` | Free, everywhere, a few lines of Python — but ageing. |
| OpenCV barcode/QR module | Decoder bundled with the vision stack | `Best-practical` | Free and already in your imports; pair with ZBar as fallback. |
| zxing-cpp | Modern C++ port of ZXing | `Alternative` | Broad symbology support, fast, clean Python wheels. |
| Quirc | Tiny QR-only decoder | `Alternative` | Minimal, fast, embeddable — QR only, nothing else. |

## Dynamsoft Barcode Reader

Dynamsoft Barcode Reader (DBR) is a **commercial** decode SDK with
bindings for Python, C/C++, .NET, JavaScript, and more. It is built for
industrial and logistics use, where codes arrive damaged, low-contrast,
warped onto curved surfaces, or partly obscured. Its decoding engine is
tuned far harder than the open-source options for those bad cases, and
it exposes a large set of tuning parameters (binarisation, deblurring,
region prediction) so you can squeeze read-rate out of difficult input.

Where it shines: **robustness and read-rate are the best on this list**.
On a marginal synthetic frame — a code rendered small, at a steep angle,
or with simulated motion blur — DBR will commonly decode what **ZBar**
and **Quirc** miss, and it supports essentially every 1D and 2D
symbology you might stamp on a vial. It also ships solid documentation
and commercial support, which matters if identification becomes a
project bottleneck.

Where it is bad versus the others: it is **proprietary and paid**
(per-developer/per-deployment licensing, typically ~hundreds to
~thousands of USD/year; re-check current pricing). For an only-code
project whose entire point is to de-risk cheaply, that cost is hard to
justify when you fully control the rendered image and can make codes
crisp and head-on. It also adds a licence-key dependency to your build —
where **ZBar**, the **OpenCV module**, **zxing-cpp**, and **Quirc** are
all free and key-free. It is the strongest engine, but the heaviest
commitment.

## ZBar (via pyzbar)

ZBar is a long-established open-source library that scans an image and
decodes common 1D barcodes and QR codes. In Python it is reached through
**pyzbar**, a thin wrapper: you load a frame with OpenCV or Pillow, pass
the array to `pyzbar.decode()`, and get back the decoded strings with
their positions — genuinely a handful of lines.

Where it shines: it is the **cheapest and most frictionless** decoder
here. It is free, packaged for essentially every OS, and so widely used
that almost any problem you hit already has an answer online. For an
only-code workflow where you render clean, well-lit codes onto the vial
texture and photograph them straight-on with the virtual camera, ZBar's
read-rate is perfectly adequate — the synthetic images are far kinder
than the real bench would be.

Where it is bad versus the others: it is **ageing and less robust**. On
blurry, rotated, or low-contrast frames its read-rate trails
**Dynamsoft** badly and trails **zxing-cpp** noticeably. Its symbology
list is narrower than zxing-cpp's or Dynamsoft's (DataMatrix support, in
particular, is weak), and pyzbar carries a native ZBar dependency that
can be fiddly to install on some platforms — whereas the **OpenCV
module** is already present and **zxing-cpp** ships clean wheels. It is
the right default for cheap, clean synthetic codes, not for stress
cases.

## OpenCV barcode/QR module

OpenCV is the computer-vision library this project already uses to grab
and process simulated camera frames. Recent OpenCV ships built-in
decoders — `QRCodeDetector` for QR codes and `BarcodeDetector` for 1D
barcodes (the latter backed by a contributed engine) — so you can detect
and decode a code with the same library you use for everything else, no
extra dependency.

Where it shines: it is the **best-practical** pick precisely because of
**zero added surface area**. The vision stack already imports OpenCV, so
identification becomes one more call on an object you already have — no
new install, no licence, no native-dependency headaches like pyzbar's.
Its QR and 1D decoders are competent on the clean, controlled frames an
only-code twin produces, and keeping the whole image pipeline inside one
library makes the code simpler to reason about and ship.

Where it is bad versus the others: its **symbology coverage and raw
read-rate sit in the middle**. It does not match **Dynamsoft's**
robustness on degraded images, and on some awkward 1D types its decoder
is less reliable than **zxing-cpp** or even **ZBar**. The pragmatic
answer is to lead with the OpenCV module and **fall back to ZBar** when
a frame fails to decode — two free libraries covering each other's gaps,
which together comfortably handle synthetic vials without paying for
Dynamsoft.

## zxing-cpp

zxing-cpp is a modern C++ re-implementation of ZXing ("zebra crossing"),
the well-known Java barcode toolkit. It decodes a broad set of 1D and 2D
symbologies, is actively maintained, and — importantly for this project
— publishes clean Python wheels, so `pip install zxing-cpp` gives you a
fast native decoder with no Java runtime and no system packages to chase.

Where it shines: it offers the **widest free symbology support** here
and is fast and well-maintained. Where **ZBar** struggles with
DataMatrix and feels dated, zxing-cpp handles a fuller modern code set
and tends to decode rotated or moderately degraded frames more reliably.
If you needed one free library to cover every code type you might render
on a vial, it is the strongest single open-source choice.

Where it is bad versus the others: for *this* job it is **redundant**.
On the clean synthetic frames of only-code mode, its extra robustness
over the **OpenCV module + ZBar** pairing rarely changes the outcome,
and unlike the OpenCV module it is a new dependency rather than something
already in your imports. It still cannot match **Dynamsoft's** ceiling
on truly bad images. It is an excellent fallback or replacement, but it
does not displace either the cheapest or the practical pick — hence
Alternative.

## Quirc

Quirc is a very small, fast, open-source library that does exactly one
thing: detect and decode **QR codes**. It is written in portable C with
no dependencies, which makes it trivial to embed and quick to run, and
there are thin Python bindings available.

Where it shines: it is **minimal and embeddable**. If your design fixes
QR as the only symbology and you want the leanest possible decoder — say
for a tight, dependency-averse build — Quirc is hard to beat on size and
simplicity, and on a clean rendered QR it decodes quickly and reliably.

Where it is bad versus the others: it is **QR-only**, full stop. It
cannot read any 1D barcode or DataMatrix, so the moment a vial carries
anything but a QR code it is useless — where **ZBar**, the **OpenCV
module**, **zxing-cpp**, and **Dynamsoft** all handle multiple
symbologies. Its robustness on poor frames is also modest, below
**zxing-cpp** and far below **Dynamsoft**. As a narrow QR helper it is
fine; as the project's identification layer it is too limited, so it
lands as an Alternative.

## Verdict

- **Best-in-class — Dynamsoft Barcode Reader.** The highest read-rates
  and the most robust decoding on poor or warped images, with broad
  symbology support and commercial backing — the right call only if
  identification becomes the bottleneck and the paid licence (~hundreds
  to ~thousands USD/year; re-check) is acceptable.
- **Cheapest — ZBar (via pyzbar).** Free, ubiquitous, and a few lines of
  Python; perfectly adequate on the clean, head-on codes an only-code
  twin renders, at the cost of weak performance on degraded frames and a
  fiddly native dependency.
- **Best-practical — OpenCV barcode/QR module, with ZBar as fallback.**
  Free and already inside the vision stack you import, so it adds no new
  surface area; lead with it and fall back to ZBar on any frame it
  misses, and you cover synthetic vials reliably without paying for
  Dynamsoft.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real scanner / camera in the loop):
  [`../02-code-plus-hardware/06-identification-and-barcode.md`](../02-code-plus-hardware/06-identification-and-barcode.md)
