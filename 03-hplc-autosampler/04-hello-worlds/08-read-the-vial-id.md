# 08 — Read the vial identifier (Identification)

> Checklist exercise: **Layer 6 — "read the vial identifier."**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

## What this program proves

Every glass vial that goes into the machine carries a small printed
code — usually a **Quick Response code** (the square dotted pattern a
phone camera can read). That code is not the chemistry; it is just a
short piece of text, a **sample identifier** such as `QC-007`. The
machine's job is to *read* that text off the label and then *look it up*
in the **worklist** — the list of samples to process and which tray slot
each one belongs in.

This program proves that whole read-then-look-up idea on your computer,
with no robot and no camera. It does three things in order:

1. It **generates** (creates from scratch) a Quick Response code image
   for the sample identifier `QC-007` and saves it as a label picture.
2. It **decodes** (reads back) that picture, recovering the text
   `QC-007` from the dotted pattern.
3. It **looks up** that text in a small worklist and prints the tray
   slot the sample belongs in — or flags the vial for quarantine if the
   code is not in the worklist at all.

Once you can read a code and decide what it means, you have the piece
that keeps the wrong sample from ever being processed. A real cell would
read the code from a live camera image; here we make our own image so
the whole exercise runs by itself.

> This is teaching code: it stands in for a real camera and label
> printer so you can see the read-and-look-up logic on its own. The
> live-camera version lives in the deeper write-up linked at the bottom.

## What you need first

This exercise needs **no robot and no simulator** — it is plain Python.
You only need three small libraries (a **library** is a bundle of
ready-made code you bring into your program):

- `qrcode` — makes Quick Response code images.
- `pyzbar` — reads Quick Response codes (and barcodes) back out of an
  image. It leans on a system component named **ZBar**, which on most
  Linux machines you install once with your package manager.
- `Pillow` — a general imaging library used to open and hand the picture
  to the reader. Its import name is `PIL`, for historical reasons.

Install them like this:

```bash
sudo apt install libzbar0          # the ZBar component pyzbar needs
pip install qrcode pyzbar pillow   # the three Python libraries
```

## The whole program

Save this as a file named `read_vial_id.py`:

```python
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image

WORKLIST = {
    "QC-007": "A3",
    "QC-008": "A4",
    "BLANK-1": "B1",
}


def make_label(sample_id, filename):
    image = qrcode.make(sample_id)
    image.save(filename)
    print(f"Wrote a label for {sample_id} to {filename}")


def read_label(filename):
    picture = Image.open(filename)
    found = decode(picture)
    if not found:
        return None
    raw_bytes = found[0].data
    text = raw_bytes.decode("utf-8")
    return text


def main():
    label_file = "qc007_label.png"
    make_label("QC-007", label_file)

    sample_id = read_label(label_file)
    print(f"Read code: {sample_id}")

    slot = WORKLIST.get(sample_id, None)
    if slot is None:
        print("UNKNOWN SAMPLE — quarantine")
    else:
        print(f"{sample_id} goes to slot {slot}")


if __name__ == "__main__":
    main()
```

## Every line explained

**`import qrcode`**
The word `import` means "bring in a library of ready-made code so I can
use it." `qrcode` is the library that can **generate** Quick Response
code images — that is, turn a piece of text into the square dotted
picture.

**`from pyzbar.pyzbar import decode`**
This brings in one specific tool, named `decode`, from the `pyzbar`
library. `decode` does the opposite job of generating: it **reads** a
code back out of a picture, recovering the original text. (Generating
means text-to-picture; decoding means picture-to-text.)

**`from PIL import Image`**
This brings in the `Image` tool from the Pillow imaging library. We use
it to open the saved picture file so the decoder has something to look
at. (`PIL` is just Pillow's import name.)

**`WORKLIST = { ... }`**
This creates a **dictionary** (a lookup table that maps a key to a
value). Here each key is a sample identifier, such as `"QC-007"`, and
each value is the tray slot that sample belongs in, such as `"A3"`. The
slot names like `A3` are tray positions — column letter, row number.
This small worklist is our stand-in for the real list of samples the
machine has been told to run.

**`"QC-007": "A3",`** (and the two lines like it)
Each of these is one entry in the dictionary: the text on the left of
the colon is the key (the code we expect to read), and the text on the
right is the value (the slot it maps to). We list three so that, when
the program reads `QC-007`, there is a real table to find it in.

**`def make_label(sample_id, filename):`**
The word `def` begins a named block of instructions (a "function"). This
one is called `make_label`. It takes two pieces of information handed to
it: `sample_id` (the text to encode, like `QC-007`) and `filename` (the
name of the picture file to write).

**`image = qrcode.make(sample_id)`**
This is the **generate** step. `qrcode.make(...)` takes the text and
builds a Quick Response code picture from it, which we store in `image`.
Nothing is saved to disk yet; the picture so far lives only in memory.

**`image.save(filename)`**
This writes the picture out to a real file on disk, under the name we
were given. After this line you have an actual label image you could
print and stick on a vial.

**`print(f"Wrote a label for {sample_id} to {filename}")`**
This prints a friendly status line so you can see the label was made.
The `f` just before the quotation marks makes it a **formatted string**:
anything inside curly braces, like `{sample_id}`, is replaced by its
real value when printed.

**`def read_label(filename):`**
Begins the second function, `read_label`. It takes the name of a picture
file and will hand back the text it reads out of it.

**`picture = Image.open(filename)`**
This opens the saved picture file and loads it into `picture`, ready to
be examined. Opening a file means reading it from disk into memory.

**`found = decode(picture)`**
This is the **decode** step. `decode(...)` scans the picture for any
Quick Response codes (or barcodes) and hands back a **list** of every
one it found. A list can hold zero, one, or many items; we store it in
`found`. A clear picture of one code gives a list with one item.

**`if not found:`**
This checks the special case where the list is *empty* — meaning the
decoder saw no code at all (a blank or unreadable picture). In Python an
empty list counts as "nothing," so `not found` is true exactly when
nothing was read.

**`return None`**
If nothing was read, we hand back `None`. `None` is Python's word for
"no value here." The caller will treat that as "could not read a code."
The word `return` ends the function and hands a value back.

**`raw_bytes = found[0].data`**
If we get here, at least one code was read. `found[0]` is the **first**
item in the list (counting starts at zero, so position zero is the
first). Its `.data` slot holds the encoded content — but as **bytes**,
not text. Bytes are raw computer storage: a sequence of numbers, not yet
interpreted as readable letters. We store those raw bytes in `raw_bytes`.

**`text = raw_bytes.decode("utf-8")`**
This turns the raw bytes into readable text. `.decode("utf-8")` says
"interpret these bytes as text using the standard `utf-8` rulebook for
turning numbers into letters." (This `.decode` is about bytes-to-text; do
not confuse it with the picture-reading `decode` further up — same word,
different job.) The result, the recovered string `QC-007`, is stored in
`text`.

**`return text`**
Hands the recovered text back to whoever called the function.

**`def main():`**
Begins the program's main routine — the steps that run when you launch
the file.

**`label_file = "qc007_label.png"`**
This picks the name of the picture file we will create and then read.
The ending `.png` marks it as an image file.

**`make_label("QC-007", label_file)`**
This calls the first function to actually make the label for sample
`QC-007` and save it under that filename.

**`sample_id = read_label(label_file)`**
This calls the second function to read the label back, and stores the
recovered text (or `None`, if nothing was readable) in `sample_id`.

**`print(f"Read code: {sample_id}")`**
Prints whatever code was read, so you can see the round trip worked:
the text that went in is the text that came back out.

**`slot = WORKLIST.get(sample_id, None)`**
This is the **dictionary lookup with a default**. `.get(key, default)`
means "find `key` in the dictionary and give me its value; but if the
key is not there at all, give me `default` instead of crashing." Here
the default is `None`. So if `sample_id` is in the worklist we get its
slot; if it is an unknown code, we safely get `None`. This is the
difference between a vial we recognise and one we do not.

**`if slot is None:`**
This checks whether the lookup came back empty — meaning the code was
not in the worklist (or no code was read at all). `is None` is the plain
way to test for "no value."

**`print("UNKNOWN SAMPLE — quarantine")`**
If the code is unknown, we say so and flag it for **quarantine** —
setting the vial aside instead of processing it. Refusing to act on an
unrecognised sample is exactly what keeps the wrong vial out of the run.

**`else:`** and **`print(f"{sample_id} goes to slot {slot}")`**
Otherwise — the code was found — we print the sample and the tray slot
it belongs in, which is the answer the rest of the machine needs.

**`if __name__ == "__main__":`**
A standard Python guard meaning "only run the next line if this file was
launched directly, rather than being imported by another file." It keeps
the program from starting itself when its functions are reused elsewhere.

**`main()`**
Finally calls the main routine, setting everything above in motion.

## How to run it, and how you know it worked

In a terminal, from the folder containing the file:

```bash
python3 read_vial_id.py
```

You should see three lines, roughly:

```
Wrote a label for QC-007 to qc007_label.png
Read code: QC-007
QC-007 goes to slot A3
```

A new picture file, `qc007_label.png`, will also appear in the folder —
open it and you will see the square dotted Quick Response code. That is
the very same label the program then read back.

**Try the failure case:** change the first argument of `make_label` from
`"QC-007"` to something not in the worklist, such as `"QC-999"`, and run
it again. This time the last line should read `UNKNOWN SAMPLE —
quarantine`, proving the safety check fires when a code is not
recognised.

**Done when:** the code you generate is read back as the same text *and*
a recognised code prints its slot while an unrecognised one is sent to
quarantine.

## Where this fits

- This is the runnable version of the **Layer 6** exercise in
  [`../07-learning-checklist.md`](../07-learning-checklist.md).
- The deeper write-up of identification — reading codes from a real
  camera image and matching them to the worklist — is
  [`../05-mycobot-280-impl/01-only-code/06-identification-and-barcode.md`](../05-mycobot-280-impl/01-only-code/06-identification-and-barcode.md).
- The capstone, [`14-hello-cell-capstone.md`](14-hello-cell-capstone.md),
  uses this read-and-look-up step to decide which slot each vial is for
  before the arm ever moves.
