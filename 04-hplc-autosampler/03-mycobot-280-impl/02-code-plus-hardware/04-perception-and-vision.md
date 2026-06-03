# Layer 04 — Perception & 3D vision (code-plus-hardware)

> **Job:** Turn frames from a **real camera** bolted to the cell into the
> numbers the rest of the system needs — *where* each vial and tray slot
> truly is — coping with the noise, glare, and timing that hardware adds.

In "code-plus-hardware" mode the synthetic camera of the only-code file
is replaced by a physical one, so the toolbox grows to include the
**camera SDKs and drivers** that get pixels off the device. The vocabulary
is the same: an **RGB** frame is a plain colour image with no distance
data; an **RGB-D** frame adds a *depth* value per pixel (how far away it
is); a **point cloud** is the resulting set of 3-D `(x, y, z)` points; and
a **pose** is an object's position and orientation — six numbers — which
is what the arm in Layer 03 ultimately consumes. A **fiducial** such as an
**AprilTag** (a chunky black-and-white square, like a QR code, whose
corners give an instant 6-number pose) is even more valuable here because
it survives real-world noise well.

Real hardware forces in a list of new concerns that simulation hid:

- **Device drivers / SDKs** — software to open the camera, stream frames,
  and read calibration. Each vendor ships its own.
- **Hand-eye calibration** — measuring the fixed transform between the
  camera's frame and the robot's frame, so "the vial is *here* in the
  image" becomes "the vial is *here* for the gripper." Tools like
  **easy_handeye2** automate this. Get it wrong and every grasp is off.
- **Lighting and glass reflections** — clear glass vials and shiny caps
  glare, refract, and can read as missing or wrong-shaped depth. The
  single biggest real-world headache for this cell.
- **Real noise** — depth is speckled and edges jitter; you must filter and
  average where simulation gave clean numbers.
- **Frame-rate and latency** — frames arrive at a finite rate (~30–60
  FPS) and a real delay; if perception lags, the arm acts on stale data.

## The five at a glance

| Framework | Role | Tier | One-liner |
|---|---|---|---|
| librealsense / pyrealsense2 (Intel RealSense) + Open3D | RGB-D camera SDK + 3-D processing | Best-in-class | Accurate, well-supported depth camera feeding clean point clouds into Open3D. |
| Plain USB webcam + OpenCV | RGB-only camera via a generic driver | Cheapest | Any cheap webcam plus free 2-D vision — no depth, but nearly zero cost. |
| DepthAI (Luxonis OAK-D) + OpenCV/Open3D | Smart RGB-D camera with onboard AI | Best-practical | Cheap depth *and* on-camera neural inference, offloading the host. |
| Orbbec SDK (OrbbecSDK_ROS2) | Alternative RGB-D camera SDK | Alternative | Capable, low-cost depth cameras with maturing ROS 2 drivers. |
| OpenCV | Classic 2-D image processing | Alternative | The universal CPU library for frames, calibration, edges, and markers. |

## librealsense / pyrealsense2 (Intel RealSense)

**librealsense** is Intel's open-source SDK for the **RealSense** family
of **RGB-D** depth cameras (e.g. the D435/D435i); **pyrealsense2** is its
Python binding. It opens the camera, streams synchronised colour and depth,
exposes the factory calibration, and has a first-class ROS 2 wrapper
(`realsense-ros`). Its depth output drops straight into **Open3D** for
filtering and geometry fitting, so the pair forms a complete real-camera
perception stack. A D435 costs roughly `~$250–350` (re-check — prices
drift).

Its strength is **maturity and support**. RealSense has been the default
research depth camera for years, so drivers, tutorials, and answered
questions are everywhere, and the depth quality at close range is good
enough to fit the tray plane and confirm vial heights reliably. Paired
with Open3D you get accurate point clouds *and* a clean processing
library, which is why it is the best-in-class real-camera setup here.
Orbbec is genuinely interchangeable in this role; pick on price and
availability.

Its weakness, versus the others, is that it is a fairly **dumb sensor with
a price tag**. Unlike **DepthAI/OAK** it has no onboard AI — all
processing lands on your host CPU/GPU — and it costs more than a plain
**webcam** or many **Orbbec** units. Like every depth camera it struggles
with clear glass and shiny caps (reflections confuse the depth), so you
still lean on AprilTags and geometry rather than trusting raw depth on the
glass itself. And it does more than the cheapest tier needs if RGB-only
plus fiducials would already do the job.

## Plain USB webcam + OpenCV

The cheapest real-camera path is any **generic USB webcam** — opened
through the operating system's standard UVC driver, no vendor SDK — feeding
frames into **OpenCV**. You get **RGB only**: colour images with *no
depth*. OpenCV then does the 2-D work: undistort the frame (after a
one-time checkerboard calibration), find vial rims by shape and colour,
and — crucially — detect **AprilTags** to recover the tray's full 6-number
pose from that flat image. A usable webcam costs `~$15–50`.

Its appeal is obvious: **near-zero cost** and zero driver hassle. Webcams
are universal, OpenCV is free and CPU-only, and for a cell where the
critical fixtures wear AprilTags, a single calibrated RGB camera can
recover pose surprisingly well without any depth at all. As a fallback or
a second "is a vial present?" overview camera, it is hard to beat on price.

Its weakness, against the depth-capable four, is the **missing third
dimension**. With no depth it cannot build a point cloud, cannot directly
measure how tall a vial sits or whether one tipped, and leans entirely on
markers and 2-D assumptions — which is fragile if a vial is *not* tagged or
the scene shifts in height. RealSense, OAK, and Orbbec all give true
depth; the webcam does not. It is the right *cheapest* answer, not the
right *robust* one.

## DepthAI (Luxonis OAK-D) + OpenCV/Open3D

**DepthAI** is the open-source SDK for **Luxonis OAK** cameras (e.g. the
OAK-D and the cheaper **OAK-D Lite**). These are **RGB-D** cameras with a
twist: an onboard chip runs **neural-network inference on the camera
itself**, so object detection happens on-device and only results — not raw
pixels — need cross the USB link. Colour, depth, and detections stream out
together; OpenCV and Open3D handle whatever host-side 2-D and point-cloud
work remains. An OAK-D Lite runs roughly `~$100–150`.

It is the **best-practical** pick because it bundles three things at a low
price: **cheap depth**, **onboard AI** (run a small YOLO-style vial
detector without burdening or even owning a host GPU), and a normal RGB
stream for AprilTags and OpenCV. That offloading directly tackles the
hardware concerns above — less data over USB eases **latency**, and
on-camera inference frees the host. For a small team it delivers the most
real-world capability per dollar.

Its weakness, versus the others, is **polish and depth quality**. Its
SDK and tooling, while good, are less battle-worn than RealSense's mature
ecosystem, and its depth is generally a notch behind a RealSense or a
good Orbbec for fine accuracy. The on-device AI is powerful but adds a
model-conversion step a plain **webcam + OpenCV** never imposes. And it
shares the universal curse: glass and chrome caps still defeat depth, so
fiducials remain your anchor. The trade is worthwhile, but it is a trade.

## Orbbec SDK (OrbbecSDK_ROS2)

The **Orbbec SDK** drives Orbbec's family of **RGB-D** depth cameras (e.g.
Femto, Gemini), and **OrbbecSDK_ROS2** is the ROS 2 wrapper. Functionally
it occupies the same slot as RealSense — synchronised colour and depth,
factory calibration, point clouds into Open3D — and several Orbbec models
undercut RealSense on price, which is why Orbbec is the named co-leader for
the best-in-class slot above.

Its strength is **capable depth at competitive cost** with growing ROS 2
support, and the fact that, as the depth-camera market consolidated around
Orbbec, it has become a natural RealSense substitute. If a particular
Orbbec model gives you the resolution or range you need for less money, it
is an easy swap into the same Open3D pipeline.

Its weakness, against the other four, is **ecosystem maturity**. Its
community, documentation, and answered-question base are still thinner than
RealSense's deep bench, its ROS 2 driver is younger, and it offers no
onboard AI the way **DepthAI/OAK** does. Versus a **webcam** it is far more
capable but far more expensive, and versus **OpenCV** alone it is hardware
you must buy and calibrate. Solid and worth pricing, but it stays an
**Alternative**: choose it over RealSense chiefly on cost or availability,
not on a clearly better experience.

## OpenCV

**OpenCV** plays the same universal role here as in the only-code file: the
free, CPU-only, ubiquitous library for 2-D image work — reading frames,
**camera calibration** (the checkerboard step that makes real poses
metric), lens-distortion correction, edge/blob/contour finding, and
**AprilTag** detection. Whatever camera you choose above, OpenCV is the
layer that turns its colour frames into measurements, so it sits inside
every other option on this list.

Its strength is exactly that universality and zero cost. It is hardware-
agnostic, so the same OpenCV code runs whether the pixels came from a
RealSense, an OAK, an Orbbec, or a `~$20` webcam — invaluable when you
swap cameras. And it owns the calibration and fiducial steps that real,
hardware-grounded perception depends on, which simulation could take for
granted.

Its weakness, on its own, is that it is **2-D and unaware of depth
hardware**. It does not open or stream a depth sensor (that is the
vendor SDKs' job), has no native point-cloud tools (that is Open3D/PCL),
and does not *learn* objects (that is YOLO, or the OAK's onboard net). So
standing alone it is only ever half a real-camera pipeline — the
processing half — which is why it is listed as an **Alternative**
building block rather than a complete answer, even though nearly every
answer here contains it.

## Verdict

- **Best-in-class:** **RealSense (or Orbbec) RGB-D + Open3D** — an
  accurate, well-supported depth camera feeding clean point clouds into a
  capable 3-D library. RealSense for ecosystem maturity, Orbbec when cost
  or availability wins; they are interchangeable in this slot.
- **Cheapest:** a **plain USB webcam + OpenCV** (RGB-only, leaning on
  AprilTags) for almost nothing, or step up to an **OAK-D Lite via
  DepthAI** when you want cheap *depth* plus onboard AI.
- **Best-practical:** **OAK-D (DepthAI) + OpenCV/Open3D** — cheap depth,
  on-camera neural inference, and a normal RGB stream for fiducials, all
  at a low price that eases host load and latency. The most real-world
  capability per dollar for a small team.

Whichever camera you pick, budget for the hardware-only work that
simulation hid: **hand-eye calibration** (e.g. easy_handeye2), taming
**glass/cap reflections** with fiducials and geometry, **filtering real
depth noise**, and keeping **latency** low enough that the arm never acts
on a stale frame.

## See also

- [`README.md`](README.md) — the code-plus-hardware folder overview and the
  full list of development layers.
- [`../01-only-code/04-perception-and-vision.md`](../01-only-code/04-perception-and-vision.md)
  — the same layer in **pure simulation**, where synthetic frames are
  clean and the camera is part of the digital twin.
