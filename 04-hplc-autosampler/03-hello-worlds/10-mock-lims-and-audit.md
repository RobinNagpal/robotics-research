# 10 — The mock records system and tamper-evident log (Software & compliance)

> Checklist exercise: **Layer 8 — "the mock records system and
> tamper-evident log."**
> See [`../08-learning-checklist.md`](../08-learning-checklist.md).

## What this program proves

A laboratory that works under government rules cannot just *do* the work
— it must also keep a trustworthy written record that proves *what* was
done, *when*, and *whether each step was allowed to happen*. Two things
follow from that, and this program builds both:

1. **Handing the robot its instructions.** A real lab keeps its list of
   samples in **a Laboratory Information Management System** (the software
   a lab uses to track samples and results; people often shorten its name
   to the three letters "L-I-M-S"). The robot does not invent its own
   work — it asks the records system, "what should I do next?" and is
   handed a **worklist**: a list of samples paired with the tray slot
   each one belongs in.
2. **Keeping a permanent record.** As the robot performs each step, it
   reports back to the records system, which writes a new line into **an
   audit trail** (a permanent, time-stamped record of everything that
   happened, that you are not allowed to secretly change). Crucially, the
   record stores not only *what* the robot did but *the sensor reading
   that allowed the step to proceed* — for example, the force the wrist
   felt when it confirmed it was holding the vial.

This program is a tiny **web service**: a program that sits waiting and
answers requests that arrive over the network, the same way a website
answers your browser. Other programs (including the capstone in file 14)
send it requests to fetch the worklist and to record events.

Once you can do this, you have proven the part of the system that auditors
care about most: the robot is told what to do from one trusted place, and
every action it takes leaves an unchangeable footprint.

> **Disclaimer.** This is a **teaching program**. A real compliant
> records system adds user log-ins, electronic signatures, encryption,
> and a tamper-proof checksum on every row. We build only the smallest
> version that shows the *idea* — a worklist out, an append-only audit
> trail in. Treat it as a sketch, not a finished regulated product.

## What you need first

This program does not need the robot framework at all — it is ordinary
Python. You need three things, two of which come built into Python:

- **FastAPI** — a library (a bundle of ready-made code) for building
  small web services in Python. Install it, together with **Uvicorn**
  (the small program that actually runs a FastAPI service and listens for
  network requests), with Python's package installer:

  ```bash
  pip install fastapi uvicorn
  ```

- **`sqlite3`** — a tiny database that stores its data in a single
  ordinary file on disk. (A **database** is an organised store of
  information you can add to and search.) It ships *inside* Python, so
  there is nothing to install.

- **`curl`** — a command-line tool for sending a request to a web service
  from a terminal, used here only to test. It comes with most systems
  already.

A couple of words used throughout, defined once:

- **A web service** is a program that waits for requests arriving over
  the network and sends back answers. **An endpoint** is one named
  "door" into that service — one specific question it knows how to
  answer, reached by its web address.
- Requests come in two everyday kinds. **`GET`** means "give me some
  information, but do not change anything" (like opening a page). **`POST`**
  means "here is some information; please record it" (like submitting a
  form). We use `GET` to fetch the worklist and `POST` to record an event.
- **A table** in a database is a grid, like a spreadsheet: fixed columns
  across the top, and one **row** per thing stored. Our audit table has
  one row per step the robot performed.

## The whole program

Save this as a file named `mock_lims.py`:

```python
import sqlite3
import datetime
from fastapi import FastAPI
from pydantic import BaseModel

DATABASE_FILE = "audit.db"

app = FastAPI(title="Mock LIMS and audit trail")


def get_connection():
    return sqlite3.connect(DATABASE_FILE)


def setup_database():
    connection = get_connection()
    connection.execute(
        "CREATE TABLE IF NOT EXISTS audit ("
        "  id        INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  recorded  TEXT NOT NULL,"
        "  sample    TEXT NOT NULL,"
        "  step      TEXT NOT NULL,"
        "  result    TEXT NOT NULL,"
        "  sensor    TEXT NOT NULL)")
    connection.commit()
    connection.close()


setup_database()

WORKLIST = [
    {"sample": "QC-007", "slot": "A3"},
    {"sample": "QC-008", "slot": "A4"},
]


class Event(BaseModel):
    sample: str
    step: str
    result: str
    sensor: str


@app.get("/worklist")
def get_worklist():
    return {"worklist": WORKLIST}


@app.post("/event")
def record_event(event: Event):
    recorded = datetime.datetime.now(
        datetime.timezone.utc).isoformat()
    connection = get_connection()
    connection.execute(
        "INSERT INTO audit "
        "(recorded, sample, step, result, sensor) "
        "VALUES (?, ?, ?, ?, ?)",
        (recorded, event.sample, event.step,
         event.result, event.sensor))
    connection.commit()
    connection.close()
    return {"stored": True, "recorded": recorded}
```

## Every line explained

**`import sqlite3`**
Brings in Python's built-in tiny database library. The word `import`
means "load a bundle of ready-made code so I can use it." This one lets
us create the audit table and write rows into it.

**`import datetime`**
Brings in Python's built-in library for working with dates and times. We
use it to stamp each audit row with the exact moment it was recorded — a
record without a time stamp is almost worthless to an auditor.

**`from fastapi import FastAPI`**
From the FastAPI library, brings in the one main tool, also called
`FastAPI`. It is the object that represents our whole web service; we
attach our endpoints to it.

**`from pydantic import BaseModel`**
Brings in `BaseModel` from a library called Pydantic, which installs
automatically alongside FastAPI. `BaseModel` lets us describe, in plain
Python, the *shape* of the information a `POST` request must carry — which
fields it must include — so that FastAPI can check incoming requests for
us and reject malformed ones.

**`DATABASE_FILE = "audit.db"`**
Stores, in a clearly-named label, the filename of the single file the
database lives in. Writing it once here means we never risk mistyping it
later. The ending `.db` is just a conventional name for a database file.

**`app = FastAPI(title="Mock LIMS and audit trail")`**
Creates the actual web service and stores it in `app`. The `title` is a
human-readable label that shows up in FastAPI's automatic documentation
page. From here on, everything we attach to `app` becomes part of the
service.

**`def get_connection():`**
`def` begins a named block of instructions (a "function"). This little
helper's only job is to open a fresh connection to the database file and
hand it back, so the rest of the code does not repeat that step.

**`return sqlite3.connect(DATABASE_FILE)`**
`sqlite3.connect(...)` opens (creating it if absent) the database file and
returns a **connection** — the live link through which we send commands to
the database. `return` hands that connection back to whoever called the
helper.

**`def setup_database():`**
Begins the function that makes sure the audit table exists before the
service starts taking requests. It runs once, at start-up.

**`connection = get_connection()`**
Calls the helper above to open the database, saving the live link in
`connection`.

**`connection.execute("CREATE TABLE IF NOT EXISTS audit (...)")`**
Sends a command to the database, written in **SQL** (Structured Query
Language — the standard wording used to talk to databases). `CREATE TABLE
IF NOT EXISTS audit` means "make a table called `audit`, but only if one
does not already exist," so it is safe to run every time the program
starts. The columns inside the brackets define what each row holds:

- **`id INTEGER PRIMARY KEY AUTOINCREMENT`** — a plain counting number
  that the database fills in automatically, going up by one for every row
  (1, 2, 3, …). It gives every row a unique label and, helpfully, records
  the *order* rows were added in.
- **`recorded TEXT NOT NULL`** — the time stamp, stored as text. `NOT
  NULL` means "this column may never be left blank."
- **`sample TEXT NOT NULL`** — which sample the step concerned, for
  example `QC-007`.
- **`step TEXT NOT NULL`** — the name of the step, for example
  `pick_vial`.
- **`result TEXT NOT NULL`** — how the step turned out, for example
  `ok` or `failed`.
- **`sensor TEXT NOT NULL`** — the gating sensor reading: the measurement
  that *allowed* the step to proceed, for example `wrist_force=7.2`.

Notice what the columns do **not** include: there is no "edited by" or
"last changed" column, because rows are never meant to change.

**`connection.commit()`**
Databases hold proposed changes in waiting until you `commit`, which means
"make these changes permanent now." Without this line the new table would
be forgotten when the connection closes.

**`connection.close()`**
Politely shuts the live link to the database, freeing it up. You open a
connection, do your work, commit, and close — every time.

**`setup_database()`**
Actually *calls* the set-up function we just defined, so the table is
guaranteed to exist the moment the program is loaded, before any request
can arrive.

**`WORKLIST = [ {"sample": "QC-007", "slot": "A3"}, {"sample": "QC-008", "slot": "A4"} ]`**
Stores the worklist itself: a list (the square brackets) of two entries.
Each entry is a small labelled bundle (the curly brackets) pairing a
sample name with the tray slot it belongs in. In a real system this would
be read from the lab's central database; here we simply fix two rows so
the example runs on its own. The first pairs sample `QC-007` with slot
`A3` — the very job the capstone in file 14 carries out.

**`class Event(BaseModel):`**
Begins the description of the *shape* a recorded event must have. The word
`class` starts a blueprint; building it on `BaseModel` lets FastAPI use it
to check incoming `POST` requests. The four indented lines list the four
fields every event must carry, each labelled with its kind (`str` means
"a piece of text"):

- **`sample: str`** — which sample the event is about.
- **`step: str`** — which step was performed.
- **`result: str`** — how it turned out.
- **`sensor: str`** — the gating sensor reading that allowed it.

If a request to record an event leaves any of these out, FastAPI refuses
it before our own code even runs.

**`@app.get("/worklist")`**
This line, beginning with the `@` symbol, is a **decorator** — a label
attached to the function just below it. It tells FastAPI: "when a `GET`
request arrives at the address `/worklist`, run the following function."
In other words, it wires up our first endpoint. Recall `GET` means
"give me information, change nothing."

**`def get_worklist():`**
The function that answers a request for the worklist. It takes no
information in — fetching the list requires nothing from the caller.

**`return {"worklist": WORKLIST}`**
Hands back the worklist. FastAPI automatically turns this labelled Python
bundle into **JSON** (JavaScript Object Notation — a plain-text way of
writing labelled data that almost every program can read) and sends it
over the network as the reply.

**`@app.post("/event")`**
The decorator for our second endpoint: "when a `POST` request arrives at
the address `/event`, run the function below." `POST` is the kind that
*records* something, which is exactly what writing an audit row is.

**`def record_event(event: Event):`**
The function that records one event. Writing `event: Event` tells FastAPI
to read the information out of the incoming request, check that it matches
the `Event` shape defined above, and hand it to us neatly as `event`.

**`recorded = datetime.datetime.now(datetime.timezone.utc).isoformat()`**
Captures the current moment. `datetime.datetime.now(...)` asks for the
present time; passing `datetime.timezone.utc` records it in **Coordinated
Universal Time** (the single worldwide reference clock, so a record made in
one country lines up with one made in another). `.isoformat()` turns that
moment into a standard, sortable piece of text such as
`2026-06-03T14:05:09.123456+00:00`. We store it in `recorded`. The records
system stamps the time itself, rather than trusting the robot to report
it, so the time cannot be faked by the caller.

**`connection = get_connection()`**
Opens a fresh database connection for this one event.

**`connection.execute("INSERT INTO audit (...) VALUES (?, ?, ?, ?, ?)", (...))`**
The heart of the audit trail. `INSERT INTO audit` is the SQL command that
**adds a new row** — and only ever adds; it never overwrites an existing
one. It is followed by the list of columns we are filling, then `VALUES`
and five question marks. Each `?` is a safe placeholder; the actual values
are supplied separately, in the bundle on the next argument
(`recorded`, then the event's `sample`, `step`, `result`, and `sensor`).
Passing the values separately like this — rather than gluing them into the
command text — is the standard way to stop a maliciously crafted value
from tampering with the command itself. This single `INSERT` is what makes
the table **append-only**: throughout the whole program there is no
`UPDATE` (change a row) and no `DELETE` (remove a row) anywhere, so once a
row is written it stays exactly as written. That unchangeability is what
the words **append-only** and **tamper-evident** mean, and it is the core
of an audit trail.

**`connection.commit()`**
Makes the new row permanent. Until this runs, the row is only proposed.

**`connection.close()`**
Closes this event's connection.

**`return {"stored": True, "recorded": recorded}`**
Sends back a short confirmation: a yes/no flag that the row was stored,
and the exact time stamp that was written, so the caller has a receipt of
when its action was recorded.

### Why a regulator cares

In the United States, electronic records in a regulated lab must satisfy
a rule called **21 CFR Part 11** (a United States Food and Drug
Administration regulation — its name is just the part and section number
in the federal rulebook — that requires electronic records to be
trustworthy, with the same weight as a signature on paper). Part 11 expects
records to be attributable (you can tell who or what did each step),
time-stamped, and protected from undetected change. An audit trail that
can only ever *grow* — never be quietly edited or erased — is the simplest
honest way to meet that "protected from undetected change" expectation,
which is exactly why our table refuses to update or delete.

## How to run it, and how you know it worked

Open **two** terminal windows.

- **Terminal one** — start the service:
  ```bash
  uvicorn mock_lims:app
  ```
  Here `uvicorn` is the program that runs the service; `mock_lims:app`
  means "inside the file `mock_lims.py`, run the web service named `app`."
  You should see a line ending in `Uvicorn running on
  http://127.0.0.1:8000`. That web address is your own computer
  (`127.0.0.1`) on door number `8000`.

- **Terminal two** — first fetch the worklist:
  ```bash
  curl http://127.0.0.1:8000/worklist
  ```
  `curl` sends a `GET` request (its default) to the `/worklist` endpoint.
  You should get back the two worklist rows, including
  `{"sample":"QC-007","slot":"A3"}`.

  Then record one event:
  ```bash
  curl -X POST http://127.0.0.1:8000/event \
    -H "Content-Type: application/json" \
    -d '{"sample":"QC-007","step":"check_held",
         "result":"ok","sensor":"wrist_force=7.2"}'
  ```
  `-X POST` chooses the `POST` kind; `-H "Content-Type: application/json"`
  tells the service the data is written as JSON; `-d '...'` is the data
  itself. You should get back `{"stored":true,"recorded":"..."}` with a
  time stamp.

To prove the trail really persisted, read it straight from the database
file with the bundled command-line tool:

```bash
sqlite3 audit.db "SELECT * FROM audit;"
```

`SELECT * FROM audit` is the SQL for "show me every column of every row in
the `audit` table." You will see your recorded step, its result, its
sensor reading, and the time stamp. Run another `POST`, list again, and
notice the old rows are untouched and a new one is simply appended.

**Done when:** `GET /worklist` returns the worklist, `POST /event` stores
a time-stamped row, and repeated events only ever *add* rows — the earlier
ones never change. You have built the smallest honest version of a
compliant records system: instructions out, an unchangeable audit trail
in.

## Where this fits

- This is the runnable version of the **Layer 8** exercise in
  [`../08-learning-checklist.md`](../08-learning-checklist.md).
- The deeper write-up of the software and compliance layer (worklists,
  records systems, and what a regulated lab demands) is
  [`../05-mycobot-280-impl/01-only-code/08-software-worklist-and-compliance.md`](../05-mycobot-280-impl/01-only-code/08-software-worklist-and-compliance.md).
- The capstone,
  [`14-hello-cell-capstone.md`](14-hello-cell-capstone.md), reads the
  worklist from this service and reports every completed step back to its
  `/event` endpoint, so the whole demonstration run leaves an audit trail.
