# 14 — The whole loop, one vial start to finish (Capstone)

> Checklist exercise: **Part C — "the whole loop, one vial start to
> finish."**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

## What this program proves

Every earlier file in this folder taught **one** skill in isolation: make
a world, offer a service, plan a reach, see a marker, close a grip, read
a barcode, keep an audit trail. This last file does the thing the whole
project exists to demonstrate: it **chains those skills into one
unbroken run** that handles a single vial from start to finish, and
narrates every step out loud as it goes.

This is the program you **screen-record for the sales pitch**. When
someone asks "what does your robot actually do?", you press play and they
watch: the robot reads its instructions, finds the vial, picks it up and
*proves* it is holding it, has the cap removed, places the vial in the
correct tray slot, *proves* it is seated, and writes a permanent,
time-stamped audit line for every one of those steps — including the
exact sensor reading that allowed each step to happen.

The single most important idea here is **gating**. The robot does not
just *do* each step and hope; before it moves on, it checks a sensor and
will only continue if the reading falls inside an allowed band. And it
does not merely act on that reading privately — it *records* it, so the
audit trail later shows not only "the step happened" but "the step was
allowed because the wrist-force reading was 7.2, which was inside the
band." That is the difference between a demo that looks impressive and a
system a regulated laboratory could actually trust.

To keep this file self-contained and runnable on any computer, the real
subsystems from files 01–11 are represented by small, clearly-labelled
**stub functions** — placeholders that stand in for the real thing and
return a believable value. Each stub is marked with the file it would be
replaced by. When you wire in the genuine subsystems later, you swap the
body of each stub and the surrounding loop stays exactly the same.

> **Disclaimer.** This is a **teaching program**. The stubs always
> succeed and always return in-band readings, so the happy path is easy
> to watch. A real run must handle a stub *failing* its gate (a grip that
> slips, a vial that will not seat) by retrying or stopping — that
> failure-handling logic is the subject of file 09, the per-vial loop.
> Here we keep the spotlight on the *shape* of the end-to-end run.

## What you need first

The capstone reports each step to the mock records system from file 10,
so that you finish with a real audit trail on disk. You need two things:

- **The file-10 service running.** In its own terminal, start it exactly
  as that file describes:
  ```bash
  uvicorn mock_lims:app
  ```
  Leave it running. Our capstone will send it one `POST /event` per step.
- **The `requests` library** — a small, very common Python library for
  *sending* web requests from inside a program (the same job `curl` does
  from the terminal, but called from Python code). Install it with
  Python's package installer:
  ```bash
  pip install requests
  ```

If you would rather run the capstone entirely on its own, with no second
terminal, see the note at the end of "Every line explained": the audit
step can be switched to write to a local append-only file instead.

## The whole program

Save this as a file named `hello_cell.py`:

```python
import requests

LIMS_URL = "http://127.0.0.1:8000"

FORCE_BAND = (5.0, 12.0)


def fetch_worklist():
    reply = requests.get(LIMS_URL + "/worklist")
    return reply.json()["worklist"]


def audit(sample, step, result, sensor):
    requests.post(LIMS_URL + "/event", json={
        "sample": sample,
        "step": step,
        "result": result,
        "sensor": sensor,
    })


def locate_vial(slot):                    # file 04 — see the tray
    print(f"  Located the vial near slot {slot}.")
    return True


def pick_vial():                          # file 05 — grab the vial
    print("  Closed the grip on the vial.")
    return True


def check_held():                         # file 11 — subscribe to a sense
    return 7.2


def call_decap():                         # file 02 — the mock decapper
    print("  Asked the decap service to remove the cap.")
    return True


def place_in_slot(slot):                  # file 03 — reach the vial
    print(f"  Moved the vial over slot {slot} and released.")
    return True


def check_seated():                       # file 11 — subscribe to a sense
    return 9.4


def in_band(value):
    low, high = FORCE_BAND
    return low <= value <= high


def run_one_vial(sample, slot):
    print(f"== Starting vial {sample} -> slot {slot} ==")

    locate_vial(slot)
    audit(sample, "locate_vial", "ok", f"vision_lock=yes,slot={slot}")

    pick_vial()
    held = check_held()
    if not in_band(held):
        audit(sample, "pick_vial", "FAILED", f"wrist_force={held}")
        print(f"  ABORT: wrist_force {held} was outside the band.")
        return False
    print(f"  Step allowed because wrist_force = {held} "
          f"was inside the band {FORCE_BAND}.")
    audit(sample, "pick_vial", "ok", f"wrist_force={held}")

    call_decap()
    audit(sample, "call_decap", "ok", "decap_reply=cap_removed")

    place_in_slot(slot)
    seated = check_seated()
    if not in_band(seated):
        audit(sample, "place_in_slot", "FAILED", f"wrist_force={seated}")
        print(f"  ABORT: seating force {seated} was outside the band.")
        return False
    print(f"  Step allowed because wrist_force = {seated} "
          f"was inside the band {FORCE_BAND}.")
    audit(sample, "place_in_slot", "ok", f"wrist_force={seated}")

    print(f"== Finished vial {sample}: placed and verified in {slot}. ==")
    return True


def main():
    worklist = fetch_worklist()
    first = worklist[0]
    run_one_vial(first["sample"], first["slot"])


if __name__ == "__main__":
    main()
```

## Every line explained

**`import requests`**
The word `import` means "bring in a library of ready-made code so I can
use it." `requests` is the common Python library for *sending* web
requests from inside a program — it lets our capstone fetch the worklist
from the file-10 service and post each audit event to it.

**`LIMS_URL = "http://127.0.0.1:8000"`**
Stores the web address of the records system from file 10. `127.0.0.1`
always means "this same computer," and `8000` is the numbered door
(the **port**) the file-10 service listens on. Keeping the address in one
clearly-named label means we never have to retype it.
(`LIMS` is the short name for the Laboratory Information Management
System — the software a lab uses to track samples and results — that file
10 builds.)

**`FORCE_BAND = (5.0, 12.0)`**
Stores the allowed band for the wrist-force reading, as a pair: a lowest
acceptable value of 5.0 and a highest of 12.0. (The units are *newtons*,
the standard measure of force; a gentle but firm grip on a small glass
vial lands in this range.) Any reading below 5.0 suggests the robot is
holding nothing; any reading above 12.0 suggests it is crushing the vial.
This single pair is the rule every gate in the program checks against.

**`def fetch_worklist():`**
The word `def` begins a named block of instructions (a **function**).
This one asks the records system for the worklist.

**`reply = requests.get(LIMS_URL + "/worklist")`**
Sends a **GET** request (the "just read me something, change nothing"
kind) to the `/worklist` address of the file-10 service, and stores the
service's answer in `reply`.

**`return reply.json()["worklist"]`**
The reply arrives as **JSON** (JavaScript Object Notation — a plain-text
way of writing labelled data). `.json()` turns that text back into normal
Python data; `["worklist"]` pulls out the list stored under the label
`worklist`; and `return` hands that list back to whoever called the
function.

**`def audit(sample, step, result, sensor):`**
Begins the one helper that records a step to the audit trail. It takes
four pieces of information: which `sample`, which `step`, the `result`,
and the gating `sensor` reading that allowed it.

**`requests.post(LIMS_URL + "/event", json={ ... })`**
Sends a **POST** request (the "here is information, please record it"
kind) to the `/event` address of the file-10 service. The `json={...}`
part is the data we send: a labelled bundle pairing each field name with
its value. The file-10 service writes this as one new, permanent,
time-stamped row in its append-only audit table. Every call to `audit`
below leaves exactly one such unchangeable footprint.

**`def locate_vial(slot):  # file 04 — see the tray`**
A **stub** — a placeholder standing in for a real subsystem. In the
finished system this is where the perception code from **file 04 (see the
tray)** would find the printed marker and measure where the vial is. The
comment names the file it represents.

**`print(f"  Located the vial near slot {slot}.")`**
Prints a line of narration to the terminal so a viewer watching the
screen recording can follow along. The `f"..."` is a Python **f-string**:
text with the value of `slot` slotted in where `{slot}` appears.

**`return True`**
The stub reports success. A real subsystem would return success only
after it actually located the vial; here we always succeed to keep the
demonstration on its happy path.

**`def pick_vial():  # file 05 — grab the vial`**
The stub for the grasp. In the real system this is the grip-and-close
logic from **file 05 (grab the vial)**.

**`print("  Closed the grip on the vial.")`** and **`return True`**
Narrate the action and report success, as above.

**`def check_held():  # file 11 — subscribe to a sense`**
The stub for *measuring* the grip. In the real system this reads the
wrist-force sensor — the work of **file 11 (subscribe to a sense)**, which
turns a live sensor stream into a single number.

**`return 7.2`**
Returns a believable in-band wrist-force reading, 7.2 newtons. This is the
number the next gate will check, and the number the audit trail will
record as the reason the pick step was allowed.

**`def call_decap():  # file 02 — the mock decapper`**
The stub for removing the cap. In the real system this sends the `decap`
request to the cap-remover service built in **file 02 (the mock
decapper)** and waits for the "cap removed" reply.

**`print("  Asked the decap service to remove the cap.")`** and
**`return True`**
Narrate and report success.

**`def place_in_slot(slot):  # file 03 — reach the vial`**
The stub for putting the vial down. In the real system this is the
collision-free arm motion from **file 03 (reach the vial)**, moving the
vial over the target slot and releasing it.

**`print(...)`** and **`return True`**
Narrate the placement and report success.

**`def check_seated():  # file 11 — subscribe to a sense`**
The stub for confirming the vial is properly seated in its slot — again a
sensor reading, the territory of **file 11**.

**`return 9.4`**
Returns a believable in-band reading, 9.4 newtons: enough downward contact
force to show the vial is resting in the slot, not perched on the rim.

**`def in_band(value):`**
Begins the small function that decides whether a sensor reading is
acceptable — the heart of **gating**.

**`low, high = FORCE_BAND`**
Unpacks the allowed band into two named values: `low` (5.0) and `high`
(12.0).

**`return low <= value <= high`**
Returns `True` only if the reading sits at or above the low limit *and* at
or below the high limit — that is, inside the band. This one line is the
rule every gate uses.

**`def run_one_vial(sample, slot):`**
Begins the main routine that walks a single vial through the whole loop,
from locating it to confirming it is placed. It takes the sample name and
its target slot.

**`print(f"== Starting vial {sample} -> slot {slot} ==")`**
Prints a clear banner so the start of the run is obvious in the recording.

**`locate_vial(slot)`**
Runs the locate step (file 04's job).

**`audit(sample, "locate_vial", "ok", f"vision_lock=yes,slot={slot}")`**
Records that step to the audit trail, noting it succeeded and the sensing
evidence that backed it (a confirmed vision lock on the given slot).

**`pick_vial()`**
Runs the grasp step (file 05's job).

**`held = check_held()`**
Reads the wrist-force sensor and stores the number in `held` — here, 7.2.
This is the gating reading for the pick step.

**`if not in_band(held):`**
Begins the **gate**. It asks: is the held-force reading *outside* the
allowed band? If so, the indented lines below run — the step is refused.

**`audit(sample, "pick_vial", "FAILED", f"wrist_force={held}")`**
Records the failure to the audit trail, *including the out-of-band reading
that caused it*, so the record explains exactly why the run stopped.

**`print(f"  ABORT: wrist_force {held} was outside the band.")`** and
**`return False`**
Narrate the abort for the viewer and stop the routine early, handing back
`False` to mean "this vial did not finish." (With our stub returning 7.2
this branch never runs, but it shows where real failure-handling — file
09's per-vial retry logic — would attach.)

**`print(f"  Step allowed because wrist_force = {held} was inside the band {FORCE_BAND}.")`**
This is the line that makes gating *visible*. When the reading is in band,
the program says, in plain words, *why* the step is allowed to continue —
naming the exact reading and the band it fell inside. This is the sentence
that makes the demonstration convincing.

**`audit(sample, "pick_vial", "ok", f"wrist_force={held}")`**
Records the successful pick, with the in-band reading that allowed it, to
the permanent audit trail.

**`call_decap()`** and **`audit(sample, "call_decap", "ok", "decap_reply=cap_removed")`**
Runs the cap-removal step (file 02's job) and records it, noting the
service's "cap removed" reply as the evidence that it succeeded.

**`place_in_slot(slot)`**
Runs the placement step (file 03's job).

**`seated = check_seated()`**
Reads the seating force and stores it in `seated` — here, 9.4. This is the
gating reading for the placement step.

**`if not in_band(seated): ...`**
The second **gate**, identical in shape to the first: if the seating force
is out of band, record the failure with its reading, narrate the abort,
and stop. This guards against a vial that did not settle into its slot.

**`print(f"  Step allowed because wrist_force = {seated} was inside the band {FORCE_BAND}.")`**
Again makes the gate visible: the placement is allowed because the seating
force fell inside the band.

**`audit(sample, "place_in_slot", "ok", f"wrist_force={seated}")`**
Records the successful, verified placement to the audit trail.

**`print(f"== Finished vial {sample}: placed and verified in {slot}. ==")`**
Prints the closing banner — the moment the screen recording can end on.

**`return True`**
Reports that this vial finished the whole loop successfully.

**`def main():`**
Begins the program's starting routine.

**`worklist = fetch_worklist()`**
Asks the records system for the worklist, exactly as a real robot would —
it does not invent its own work.

**`first = worklist[0]`**
Takes the first row of the worklist. The square-bracket `[0]` means "item
number zero," which is how Python counts the first item. From file 10 this
row is sample `QC-007` bound for slot `A3`.

**`run_one_vial(first["sample"], first["slot"])`**
Runs the whole loop on that one vial, reading the sample name and slot out
of the worklist row by their labels.

**`if __name__ == "__main__":`**
A standard Python guard meaning "only run the next line if this file was
launched directly, rather than imported by another file." It keeps the
program from starting itself unexpectedly when reused.

**`main()`**
Finally calls the starting routine, setting the whole run in motion.

**Staying fully self-contained (optional):** if you would rather not run
the file-10 service in a second terminal, replace the body of the `audit`
helper with a line that appends to a local file, for example using
Python's built-in file tools to *open the file in append mode* (a mode
that can only add to the end, never overwrite) and write one line per
event. That keeps the same append-only, tamper-evident spirit while
needing nothing but this single file.

## How to run it, and how you know it worked

In one terminal, start the records system from file 10 and leave it
running:

```bash
uvicorn mock_lims:app
```

In a second terminal, run the capstone:

```bash
python3 hello_cell.py
```

You should see a clear start-to-finish narration scroll past, something
like:

```
== Starting vial QC-007 -> slot A3 ==
  Located the vial near slot A3.
  Closed the grip on the vial.
  Step allowed because wrist_force = 7.2 was inside the band (5.0, 12.0).
  Asked the decap service to remove the cap.
  Moved the vial over slot A3 and released.
  Step allowed because wrist_force = 9.4 was inside the band (5.0, 12.0).
== Finished vial QC-007: placed and verified in A3. ==
```

Then confirm the run left a permanent record. Ask the file-10 database
directly (using the bundled command-line tool from that file):

```bash
sqlite3 audit.db "SELECT step, result, sensor FROM audit;"
```

You should see one row per step — `locate_vial`, `pick_vial`,
`call_decap`, `place_in_slot` — each marked `ok` and each carrying the
sensor reading that allowed it, for example `wrist_force=7.2`.

**Done when:** running `hello_cell.py` narrates the full vial loop start
to finish on screen, **and** the file-10 audit table afterwards holds one
unchangeable, time-stamped row for every step, each with its gating sensor
value. That recording, plus that audit trail, *is* the demonstration the
whole project was building toward.

## Where this fits

- This is the runnable version of the **Part C** capstone exercise in
  [`../07-learning-checklist.md`](../07-learning-checklist.md).
- It stitches together the earlier hello worlds, each of which would
  replace a stub here:
  - the world it all runs in — [`01-spawn-the-cell.md`](01-spawn-the-cell.md);
  - the cap-removal service — [`02-mock-decapper.md`](02-mock-decapper.md);
  - reaching and placing — [`03-reach-the-vial.md`](03-reach-the-vial.md)
    (made continuous and self-checking in
    [`12-keep-the-world-current.md`](12-keep-the-world-current.md) and
    [`13-watch-the-move.md`](13-watch-the-move.md));
  - seeing the tray — `04-see-the-tray.md`;
  - grabbing the vial — [`05-grab-the-vial.md`](05-grab-the-vial.md);
  - reading the vial's identity — [`08-read-the-vial-id.md`](08-read-the-vial-id.md);
  - the decision-tree logic that retries on failure — `09-per-vial-loop.md`;
  - the worklist and audit trail — [`10-mock-lims-and-audit.md`](10-mock-lims-and-audit.md);
  - turning a sensor reading into a pass/fail gate — `11-subscribe-to-a-sense.md`.
- The deeper write-up of how these pieces are orchestrated into one task
  is
  [`../04-mycobot-280-impl/01-only-code/07-orchestration-and-task-logic.md`](../04-mycobot-280-impl/01-only-code/07-orchestration-and-task-logic.md).
