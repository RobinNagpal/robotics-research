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

## Realistic scenario & use cases

> **Why this matters for automation.** Identification is the cell's
> chain-of-custody check: it proves the vial in the gripper is the one the
> worklist *thinks* it is, before it is placed and injected. Its
> automation value is catching a **mix-up** — the wrong vial in the wrong
> slot — that would otherwise silently corrupt a result, the exact failure
> a regulated lab spends the most money investigating after the fact.

**The scenario.** After grasping each vial, the cell reads its label at a
scan pose to confirm identity against the worklist. Across one 96-vial
tray it meets a barcode **curved around the cylindrical vial**, a tiny
**2D Data Matrix** code on a 2 mL vial next to a **1D Code 128** on
another, a **smudged, low-contrast** label, a code **partly occluded by
the gripper jaw**, and — critically — one vial whose **scanned ID does not
match** the worklist row it was about to fill. The cell must read each
robustly, recover from the no-reads, and **halt on the mismatch**.

The layer must therefore serve several **distinct use cases**:

1. **Decode a label on a curved vial.** Read a barcode wrapped around a
   2 mL cylinder despite the perspective distortion.
   - *How the solution handles it:* the OpenCV barcode/QR module decodes
     the head-on portion; if it fails, the arm **rotates the vial** in the
     gripper to present a flatter view and re-reads over several frames.

2. **Decode mixed symbologies.** Handle 1D (Code 128) and 2D (Data
   Matrix / QR) codes that coexist across a tray.
   - *How:* OpenCV leads and **ZBar** backs it up; between them they cover
     the common 1D and 2D lab symbologies without extra licences.

3. **No-read recovery.** Retry sensibly on occlusion, smudge, or glare
   rather than failing the vial outright.
   - *How:* lead OpenCV → fall back to ZBar → re-present at the dedicated
     scan pose for up to *N* attempts, then flag the vial for human review
     instead of guessing.

4. **Identity verification against the worklist — mismatch halt.** Confirm
   the decoded ID equals the expected worklist row; stop on disagreement.
   - *How:* orchestration (Layer 07) compares the decoded string to the
     worklist; a mismatch **halts the affected vial and raises an audit
     event** (Layer 08) — the single highest-value check in this layer.

5. **Link every read to the audit trail.** Record the decoded ID,
   timestamp, the frame used, and pass/fail per vial.
   - *How:* the decoded result plus its evidence frame is published to the
     LIMS/audit sink (Layer 08), satisfying ALCOA+ traceability.

**Where the pick flexes.** OpenCV + ZBar fallback (best-practical) reads
the clean, known codes an only-code twin renders and covers use cases 1–5
for free. Only if identification becomes the bottleneck at real-world
print quality and throughput — heavily degraded or warped labels at speed,
an extreme of use case 3 — does the paid **Dynamsoft** reader become worth
its licence.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for
identification — the cell's chain-of-custody check.

## Decode a label on a curved vial

A lab assistant glances at the label on each vial — often turning it in
their fingers to bring the barcode or printed ID into view around the
curved glass — to confirm which sample it is before placing it. This use
case is the cell doing the same: reading the barcode wrapped around a 2 mL
vial, rotating the vial in the gripper when one view isn't enough to
capture the whole code.

The bigger experiment is the HPLC batch, where every vial must be
traceable to a specific sample and end up in the slot its worklist row
names. The label is the link between the physical vial and its identity in
the records; if the cell can't read it reliably, it can't prove the right
sample went into the right slot. Reading curved labels is therefore a
basic competence, not an edge case.

The assistant reads a label on effectively every vial they handle — dozens
to a few hundred times a day — and curvature is the normal condition,
since lab labels wrap around small cylinders. The cell reads the label on
every vial at the scan step, using its own ability to rotate the vial
rather than relying on a special wrap-around scanner.

- **The moment:** the barcode is wrapped around a 2 mL cylinder, so only a
  narrow strip faces the camera head-on.
- **How, in depth:** the OpenCV barcode/QR module decodes the flat strip;
  if it fails, the arm **rotates the vial** in the gripper to present a
  better face and re-reads across several frames.
- **Edge case it survives:** a code that spans the curve so no single frame
  sees it whole — multi-frame reads from different rotations are combined
  until the full code is recovered.
- **Walkthrough:** (1) image the label head-on; (2) try an OpenCV decode on
  the flat strip; (3) if it fails, rotate the vial one step in the gripper;
  (4) re-image and combine reads until the full code resolves.
- **In the scene:** a vial turns slowly in the gripper in front of the
  scan camera, its barcode curling away around the glass; the software
  reads what it can of the flat middle, then nudges the vial round a few
  degrees and reads again until the whole code is pieced together.
- **Why it's done this way:** lab labels are wrapped around small
  cylinders, so a single head-on shot rarely sees the whole code; using
  the arm's own rotation to present more of the label makes reading a
  curved vial reliable without buying a wrap-around scanner.
- **In the full loop:** the scan happens after the pick (and dispense) and
  before the place — this is where the held vial's identity is read so
  Layer 07 can confirm it belongs in its slot.
- **Value:** curvature, the most common lab-label problem, is handled by
  motion the cell already has, not a special scanner.

### Meta code

This meta combines reading with motion, because a barcode on a cylinder
can't always be captured in one shot. The pipeline subscribes to the wrist
camera at the scan pose and, on each frame, tries to decode the label —
first as a 1-D barcode, then as a 2-D QR code, since either symbology might
be on the vial.

When a frame decodes successfully, the job is done and the ID is returned.
The interesting part is what happens when it doesn't: rather than declaring
failure, the pipeline uses the cell's own dexterity to present a different
face of the vial.

It commands the gripper or wrist to rotate the vial one small step, waits
for the motion and a fresh frame, and tries again. Because each rotation
brings a new strip of the curved label into the camera's flat view, a code
that no single frame could see whole is gradually brought into readable
position.

The loop is bounded by a maximum number of rotations, so a vial whose
label genuinely can't be read this way doesn't spin forever — it returns
empty-handed and hands off to the no-read recovery use case. The decoder
in pseudocode:

```text
# at the scan pose, for up to MAX_TURNS presented faces:
#     grab a wrist-camera frame
#     try an OpenCV barcode decode, then an OpenCV QR decode
#     got a code -> return the ID                        (done)
#     nothing -> rotate the vial one step in the gripper  (present a new face)
# exhausted the turns -> return None                      (hand to no-read recovery)
```

### Real code

A node that reads the label, rotating the vial between attempts to beat
the curve. **Illustrative teaching code** — re-verify before use; every
line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from sensor_msgs.msg import Image                       # the wrist-camera frame
from std_srvs.srv import Trigger                        # asks the wrist to rotate the vial a step
from cv_bridge import CvBridge                          # ROS Image <-> OpenCV array
import cv2                                              # OpenCV: the barcode + QR decoders

MAX_TURNS = 8                                           # presented faces to try (~45 deg per step)


class CurvedDecoder(Node):                              # reads a barcode wrapped around a vial
    def __init__(self):                                 # one-time setup
        super().__init__("curved_decoder")              # register on the ROS 2 graph
        self.bridge = CvBridge()                        # the one image converter we reuse
        self.bardet = cv2.barcode.BarcodeDetector()     # OpenCV's 1D barcode detector
        self.qrdet = cv2.QRCodeDetector()               # OpenCV's 2D QR detector
        self.frame = None                               # the most recent wrist frame
        self.turn = self.create_client(Trigger, "/wrist/rotate_step")  # turns the vial a notch
        self.create_subscription(                       # subscribe to the wrist camera...
            Image, "/wrist/image_raw", self.on_frame, 10)

    def on_frame(self, msg):                            # runs on each wrist-camera frame
        self.frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")  # ROS Image -> a colour OpenCV array

    def decode(self):                                   # try to read the label; return ID or None
        for _ in range(MAX_TURNS):                      # at most MAX_TURNS presented faces
            if self.frame is not None:                  # do we have a frame to try?
                ok, info, _, _ = self.bardet.detectAndDecode(self.frame)  # try a 1D barcode...
                if ok and info:                         # decoded one or more 1D codes?
                    return info[0]                      # return the first decoded string
                data, _, _ = self.qrdet.detectAndDecode(self.frame)  # ...else try a 2D QR
                if data:                                # got a QR payload?
                    return data                         # return it
            self.turn.call_async(Trigger.Request())     # no code this face -> rotate the vial a step
            rclpy.spin_once(self, timeout_sec=0.3)      # let the vial turn + a fresh frame arrive
        return None                                     # exhausted turns -> hand to no-read recovery
```

## No-read recovery

Every so often a lab assistant meets a label they can't read at a glance —
smudged, glared, or peeling. They don't give up or guess; they reposition
the vial, look again, and only if it's genuinely illegible do they set it
aside for follow-up. This use case gives the cell the same patience: it
retries a failed read with a second decoder and a fresh presentation
before, as a last resort, flagging the vial for a human.

The bigger experiment is the HPLC batch, which must keep flowing
overnight. A single hard-to-read label is not a reason to halt the whole
tray, but it is also not something to guess at — a guessed ID is worse
than no ID in a traceable record. The tiered retry resolves the common
transient failures automatically and reserves human attention only for the
truly unreadable.

For the assistant a problem label turns up occasionally — a handful of
times a day across many vials. The cell sees the same rate, so the
recovery ladder (second decoder, re-present, then flag) is a routine part
of the scan step rather than an exceptional path, keeping throughput up
while never inventing an identity.

- **The moment:** a label is smudged, glared, or half-hidden by the jaw and
  the first decode returns nothing.
- **How, in depth:** the pipeline leads with OpenCV, falls back to **ZBar**,
  then re-presents the vial at a dedicated scan pose for up to *N* attempts
  before flagging — never guessing an ID.
- **Edge case it survives:** a genuinely unreadable label — after the
  attempt budget the vial is parked for human review, so a bad label stops
  *that* vial without stalling the tray.
- **Walkthrough:** (1) decode with OpenCV; (2) fall back to ZBar; (3)
  re-present the vial at the scan pose up to *N* times; (4) flag it for
  human review if it is still unread.
- **In the scene:** the first glance at a smudged label comes back blank;
  the cell does not shrug and move on — it tries a second decoder,
  re-presents the vial at the scan pose, and only after several honest
  attempts sets the stubborn vial aside for a human.
- **Why it's done this way:** a smudge, glare, or bad angle will fail
  occasionally, and treating every miss as a hard stop would halt the tray
  constantly; a tiered retry lets common transient failures resolve
  themselves and reserves human attention for the genuinely unreadable.
- **In the full loop:** this keeps the per-vial cycle moving — a transient
  no-read would otherwise stall the place step, so recovery lets the loop
  reach the identity check without constant human help.
- **Value:** transient read failures self-heal; only the truly unreadable
  reach a human, keeping throughput up.

### Meta code

This meta is a ladder of increasingly effortful attempts, designed so that
cheap fixes are tried first and a human is bothered last. The first rung is
the primary decoder (OpenCV), which is already part of the vision stack and
handles the clean, common cases.

If that fails, the second rung is a different decoder library (ZBar) on the
same frame. Because the two decoders have different strengths — one may
read a marginal 1-D barcode the other misses — trying both for free catches
a good fraction of the failures the first alone would not.

If both decoders fail on the current view, the third rung re-presents the
vial: moving it back to the dedicated scan pose and capturing a fresh
frame, which clears up transient problems like a bad angle or a momentary
glare. This re-presentation is repeated up to a fixed budget of attempts.

Only when the whole ladder is exhausted does the pipeline flag the vial for
human review, never guessing an ID. The crucial property is that a guessed
identity — worse than none in a traceable record — is impossible by
construction. The recovery in pseudocode:

```text
# decode with OpenCV (primary)            -> success: return ID
# decode with ZBar/pyzbar (fallback)      -> success: return ID
# else re-present the vial at the scan pose and retry, up to N attempts
# still nothing after N -> FLAG the vial for human review (never guess an ID)
```

### Real code

A reader that tries OpenCV, falls back to ZBar, re-presents, then flags.
**Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import cv2                                              # OpenCV: the primary barcode/QR decoder
from pyzbar import pyzbar                                # ZBar: the fallback decoder

MAX_ATTEMPTS = 4                                        # re-present the vial up to this many times


def _opencv(frame):                                    # try OpenCV first (already in the vision stack)
    ok, info, _, _ = cv2.barcode.BarcodeDetector().detectAndDecode(frame)  # 1D barcode attempt
    if ok and info:                                    # decoded a 1D code?
        return info[0]                                 # return the string
    data, _, _ = cv2.QRCodeDetector().detectAndDecode(frame)  # else try a 2D QR
    return data or None                                # the QR payload, or None if empty


def _zbar(frame):                                      # ZBar fallback (stronger on some 1D types)
    found = pyzbar.decode(frame)                        # decode everything ZBar can see
    return found[0].data.decode() if found else None    # the first code's text, or None


def read_id(grab_frame, re_present):                   # grab_frame() -> image; re_present() -> move
    for _ in range(MAX_ATTEMPTS):                       # try, then re-present, up to the budget
        frame = grab_frame()                            # capture a fresh wrist-camera frame
        code = _opencv(frame) or _zbar(frame)           # OpenCV first, then the ZBar fallback
        if code:                                        # either decoder succeeded?
            return code                                 # return the decoded ID
        re_present()                                    # nudge the vial back to the scan pose, retry
    return "FLAG_FOR_REVIEW"                            # exhausted -> a human checks this vial
```

## Identity verification against the worklist — mismatch halt

The most important check a lab assistant makes before committing a vial to
its slot is the simplest: does this vial's ID match what the worklist
expects for this position? It is the guard against the worst lab error — a
sample in the wrong place, producing a confident but wrong result. This
use case is the cell making that comparison mechanically, and halting the
vial if the decoded ID doesn't match.

The bigger experiment is the HPLC batch, where the instrument injects
whatever physically sits in each slot, in order, with no way of knowing if
a vial is misplaced. The entire chain of custody depends on the right
sample being in the right slot; verifying identity against the worklist
*before* the place is the last line of defence that makes that guarantee
mechanical rather than hopeful.

The assistant performs this match on every vial — hundreds of times a day
— and an actual mismatch is rare, but its cost is so high (a corrupted
result, a regulatory investigation) that the check is never skipped. The
cell does the same: it compares every scanned ID to the worklist on every
vial, quarantining and auditing the rare mismatch the moment it appears.

- **The moment:** vial 53 decodes to an ID the worklist doesn't expect in
  that slot — a sample mix-up.
- **How, in depth:** orchestration compares the decoded string to the
  worklist row; a mismatch **halts that vial and raises an audit event**
  (Layer 08) before the place action ever runs.
- **Edge case it survives:** two vials accidentally swapped between nests —
  each fails its own slot check, so *both* are caught rather than silently
  injected in the wrong order.
- **Walkthrough:** (1) decode the vial's ID; (2) look up the expected ID
  for that slot in the worklist; (3) compare the two; (4) on a mismatch,
  halt the vial and raise an audit event before any place action.
- **In the scene:** a vial's barcode resolves to an ID that doesn't belong
  in the slot it is about to fill; the arm stops dead, the vial is set
  aside, and a flag goes up — a wrong sample caught in the act, before it
  could ever become a wrong result.
- **Why it's done this way:** a sample injected in the wrong slot produces
  a confident but wrong result — the error regulated labs fear most and
  spend the most investigating; verifying identity against the worklist
  before placing is the guard that makes that error impossible to commit
  silently.
- **In the full loop:** this is the gate between read and place — its
  verdict tells Layer 07 whether to place the vial or quarantine it, the
  last identity check before the vial joins the tray for the instrument.
- **Value:** the highest-cost lab error — wrong sample, wrong result — is
  caught mechanically, the core reason a regulated lab would trust the cell.

### Meta code

This meta is a deliberately simple comparison sitting at a critical
junction. On startup the pipeline loads the worklist — the authoritative
mapping from each tray slot to the sample ID that belongs there — into a
lookup table, so the expected identity for any slot is instantly
available.

When a vial is scanned at a given slot, the pipeline takes the decoded ID
and the slot, looks up what the worklist expects for that slot, and
compares the two strings. There is no fuzzy matching: the identity either
matches the plan exactly or it does not.

On a match, the pipeline issues a PLACE verdict and the per-vial cycle
proceeds to seat the vial. On a mismatch — the wrong sample for this slot —
it does two things at once: it issues a QUARANTINE verdict so orchestration
sets the vial aside rather than placing it, and it writes the discrepancy
(slot, expected, decoded) to the tamper-evident audit trail.

That audit write is what makes the catch defensible later: there is a
permanent, unalterable record that a mismatch was detected and the vial was
not injected. The gate in pseudocode:

```text
# load the worklist: slot -> expected sample ID
# when a vial is scanned at slot S with decoded id D:
#     expected = worklist[S]
#     D == expected -> PLACE (allow it onto the tray)
#     D != expected -> QUARANTINE this vial AND:
#         emit an audit event (Layer 08) {slot, expected, decoded}   (tamper-evident)
#         never place a mis-identified vial
```

### Real code

A node that compares each scanned ID to the worklist and halts on a
mismatch. **Illustrative teaching code** — re-verify before use; every
line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import String                         # scanned "slot:id" in; verdict out
import csv                                              # to load the worklist file


class IdentityGate(Node):                               # confirms a scanned vial belongs in its slot
    def __init__(self):                                 # one-time setup
        super().__init__("identity_gate")               # register on the ROS 2 graph
        self.expected = self._load("worklist.csv")      # slot -> expected sample ID
        self.verdict = self.create_publisher(String, "/identity/verdict", 10)  # PLACE / QUARANTINE
        self.audit = self.create_publisher(String, "/audit/event", 10)  # tamper-evident audit (L08)
        self.create_subscription(                       # listen for scan results...
            String, "/scan/result", self.on_scan, 10)   # ..."slot:decoded_id" messages

    def _load(self, path):                              # read slot->id pairs from the worklist
        with open(path) as fh:                          # open the worklist CSV
            return {row["slot"]: row["sample_id"]       # build {slot: expected sample ID}
                    for row in csv.DictReader(fh)}       # one entry per worklist row

    def on_scan(self, msg):                             # runs on each scanned vial
        slot, decoded = msg.data.split(":")             # "A3:ABC-123" -> ("A3", "ABC-123")
        expected = self.expected.get(slot)              # what the worklist expects in that slot
        if decoded == expected:                         # identity matches the plan?
            self.verdict.publish(String(data=f"PLACE:{slot}"))  # allow the place
        else:                                           # a mix-up: wrong vial for this slot
            self.audit.publish(String(                  # record it tamper-evidently for the trail
                data=f"MISMATCH slot={slot} expected={expected} decoded={decoded}"))
            self.verdict.publish(String(data=f"QUARANTINE:{slot}"))  # halt: do NOT place this vial


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(IdentityGate()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## See also

- Folder overview: [`README.md`](README.md)
