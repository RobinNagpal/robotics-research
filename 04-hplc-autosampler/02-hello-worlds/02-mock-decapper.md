# 02 — The mock decapper (Middleware & control)

> Checklist exercise: **Layer 2 — "the mock decapper."**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

## What this program proves

In the real machine, a separate device unscrews the cap off each glass
vial, and a weighing scale reports how heavy the vial is. While you are
still building everything in simulation, you do not have those devices —
so you write small stand-in programs that *pretend* to be them and that
talk over the network exactly the way the real ones eventually will.

This program is one such stand-in. It does two things at once:

1. It offers a **request-and-reply** called `decap`. Any other program
   can send the message "please remove the cap" and will get back the
   answer "cap removed."
2. It continuously **broadcasts** a pretend weight reading (12.5 grams)
   on a named channel called `balance/mass`, once per second, the way a
   real scale would stream its measurement.

Once you can do this, you have learned the single most reused pattern in
the whole robot: small programs that answer requests and broadcast
readings. Every fake station in this project (the cap remover, the liquid
dispenser, the scale, the barcode reader) is just a variation of this
file.

## What you need first

You need **the Robot Operating System, version 2** installed. This is
*not* an operating system like Windows or macOS; it is a free toolkit
that lets the many small programs on a robot find each other and pass
messages. (Its common written name is "ROS 2." We will keep calling it
"the robot framework.") Install one of its released versions — for
example the version named **Jazzy** — by following the official
instructions for your computer, then, in a terminal window, make its
commands available with:

```bash
source /opt/ros/jazzy/setup.bash
```

That `source` command loads the robot framework's commands into your
current terminal session. You will run it once in every new terminal.

## The whole program

Save this as a file named `decapper_station.py`:

```python
import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
from std_msgs.msg import Float64


class DecapperStation(Node):
    def __init__(self):
        super().__init__("decapper_station")
        self.decap_service = self.create_service(
            Trigger, "decap", self.handle_decap_request)
        self.mass_publisher = self.create_publisher(
            Float64, "balance/mass", 10)
        self.timer = self.create_timer(1.0, self.publish_mass)
        self.current_mass_grams = 12.5
        self.get_logger().info("Decapper station is ready.")

    def handle_decap_request(self, request, response):
        self.get_logger().info("A request to remove the cap arrived.")
        response.success = True
        response.message = "cap removed"
        return response

    def publish_mass(self):
        reading = Float64()
        reading.data = self.current_mass_grams
        self.mass_publisher.publish(reading)


def main():
    rclpy.init()
    station = DecapperStation()
    rclpy.spin(station)
    station.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

## Every line explained

**`import rclpy`**
The word `import` means "bring in a library of ready-made code so I can
use it." `rclpy` is the name of the robot framework's Python library;
the name is short for "Robot Client Library for Python." This single line
gives your program the ability to join the robot's network of programs.

**`from rclpy.node import Node`**
This brings in one specific tool from that library, called `Node`. A
**node** is the framework's word for "one small program that does one
job." By bringing in `Node`, we can build our own node on top of it.

**`from std_srvs.srv import Trigger`**
This brings in a ready-made *message shape* called `Trigger`. The robot
framework requires that every request-and-reply has an agreed shape for
the question and the answer. `Trigger` is the simplest such shape: the
question carries no information at all (it is just a nudge — "do your
thing"), and the answer carries two pieces of information, a yes/no flag
and a short text note. `std_srvs` means "standard services," a collection
of common shapes that ships with the framework.

**`from std_msgs.msg import Float64`**
This brings in another ready-made shape, called `Float64`, used for the
readings we broadcast. `Float64` simply holds **one decimal number** (the
"64" refers to how much computer memory it uses, which gives it plenty of
precision). We will put the weight, 12.5, inside one of these.

**`class DecapperStation(Node):`**
The word `class` starts the definition of our own node. Think of a class
as a blueprint. We name our blueprint `DecapperStation`. The `(Node)`
part means "build this blueprint on top of the framework's `Node`
blueprint," so our station automatically inherits the ability to talk on
the network.

**`def __init__(self):`**
`def` begins a named block of instructions (a "function"). The special
name `__init__` means "the set-up steps that run once, automatically, the
moment this station is created." The word `self` is how the code refers
to *this particular station* while setting it up; every line inside uses
it.

**`super().__init__("decapper_station")`**
This runs the framework's own set-up first and, while doing so, registers
our station on the network under the human-readable name
`"decapper_station"`. After this line, the rest of the robot can see that
a program by that name exists.

**`self.decap_service = self.create_service(Trigger, "decap", self.handle_decap_request)`**
This creates the **request-and-reply** offering. We hand
`create_service` three things: the message shape it should expect
(`Trigger`), the public name other programs will use to reach it
(`"decap"`), and the name of the function to run whenever a request
arrives (`self.handle_decap_request`, defined further down). From now on,
any program that sends a request to `decap` will trigger that function.

**`self.mass_publisher = self.create_publisher(Float64, "balance/mass", 10)`**
This creates the **broadcaster** for the weight readings. We tell
`create_publisher` the shape of each reading (`Float64`), the public name
of the channel (`"balance/mass"`), and the number `10`. That `10` is the
size of a small holding queue: if readings are produced faster than the
network can carry them, up to ten will wait in line rather than being
lost. We save the broadcaster in `self.mass_publisher` so we can use it
later.

**`self.timer = self.create_timer(1.0, self.publish_mass)`**
A **timer** is an alarm clock that goes off repeatedly. This one is set
to `1.0` seconds, and each time it goes off it runs the function
`self.publish_mass`. The effect: our station sends a fresh weight reading
once every second, on its own, forever, without us asking.

**`self.current_mass_grams = 12.5`**
This stores the pretend weight, 12.5 grams, inside the station so the
broadcasting function can read it. A real scale would update this number
from a physical measurement; here we simply fix it.

**`self.get_logger().info("Decapper station is ready.")`**
This prints a friendly status line to the terminal. `get_logger()` is the
framework's built-in way of printing tidy, time-stamped messages;
`.info(...)` marks this one as ordinary information (as opposed to a
warning or an error). Seeing this line tells you the set-up finished.

**`def handle_decap_request(self, request, response):`**
This begins the function that runs every time a "please remove the cap"
request arrives. The framework hands it two things: `request` (the
incoming question — empty, for a `Trigger`) and `response` (a blank
answer for us to fill in and hand back).

**`self.get_logger().info("A request to remove the cap arrived.")`**
A status line so that, when you test the program, you can *see* the
moment a request was received.

**`response.success = True`**
We fill in the yes/no flag of the answer. `True` means "yes, it worked."
(In a real device this is where you would only say `True` after the cap
actually came off.)

**`response.message = "cap removed"`**
We fill in the short text note of the answer, a human-readable summary.

**`return response`**
The word `return` hands the finished answer back to the framework, which
delivers it to whoever asked. The request-and-reply is now complete.

**`def publish_mass(self):`**
This begins the function the timer runs once per second to broadcast a
weight.

**`reading = Float64()`**
This makes one empty reading of the decimal-number shape, ready to be
filled in. The empty pair of brackets means "make a new one."

**`reading.data = self.current_mass_grams`**
The `Float64` shape holds its number in a slot named `data`. Here we copy
our stored weight, 12.5, into that slot.

**`self.mass_publisher.publish(reading)`**
This sends the filled-in reading out onto the `balance/mass` channel for
anyone who is listening. This is the actual broadcast.

**`def main():`**
This begins the program's main starting routine — the steps that run when
you launch the file.

**`rclpy.init()`**
This starts up the connection to the robot framework. Nothing can talk on
the network until this has run, so it always comes first.

**`station = DecapperStation()`**
This builds one copy of our station from the blueprint. Building it
automatically runs the `__init__` set-up steps described above, so as
soon as this line finishes, the service and the broadcaster are live.

**`rclpy.spin(station)`**
The word **spin** means "keep this program alive and responsive, handing
it incoming requests and firing its timer, until it is told to stop."
Without this line the program would build the station and then
immediately end. Execution stays on this line, looping, until you press
the keys to stop it.

**`station.destroy_node()`**
After you stop the program, this politely removes the station from the
network, freeing up its name and resources.

**`rclpy.shutdown()`**
This closes the connection to the robot framework cleanly — the mirror
image of `rclpy.init()`.

**`if __name__ == "__main__":`**
This is a standard Python guard meaning "only run the next line if this
file was launched directly (rather than being imported by another file)."
It prevents the program from starting itself unexpectedly when reused.

**`main()`**
This finally calls the starting routine, setting everything above in
motion.

## How to run it, and how you know it worked

Open **three** terminal windows. In each, first load the robot
framework's commands with `source /opt/ros/jazzy/setup.bash`.

- **Terminal one** — start the station:
  ```bash
  python3 decapper_station.py
  ```
  You should see `Decapper station is ready.`

- **Terminal two** — listen to the weight channel:
  ```bash
  ros2 topic echo /balance/mass
  ```
  Here `ros2` is the framework's command-line tool, `topic echo` means
  "print everything broadcast on this channel," and `/balance/mass` is
  the channel name. You should see `data: 12.5` appear once per second.

- **Terminal three** — send one "remove the cap" request:
  ```bash
  ros2 service call /decap std_srvs/srv/Trigger
  ```
  `service call` means "send one request and wait for the reply." You
  should get back `success=True, message='cap removed'`, and terminal one
  should print `A request to remove the cap arrived.`

**Done when:** you can both *call* `decap` and *watch* `balance/mass`
streaming from another window. You have now built the request/reply +
broadcast pattern that every mock station in this project reuses.

## Where this fits

- This is the runnable version of the **Layer 2** exercise in
  [`../07-learning-checklist.md`](../07-learning-checklist.md).
- The deeper write-up of this layer (and why the robot framework is the
  right choice) is
  [`../04-mycobot-280-impl/01-only-code/02-middleware-and-control.md`](../04-mycobot-280-impl/01-only-code/02-middleware-and-control.md).
- The capstone, [`14-hello-cell-capstone.md`](14-hello-cell-capstone.md),
  calls this very `decap` service as one step of the full loop.
