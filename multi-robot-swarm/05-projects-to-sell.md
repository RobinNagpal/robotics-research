# Four Projects You Can Build and Sell

## 1. MAPF-as-a-service for small fleets (~3-4 weeks)

REST/gRPC service: send a warehouse map + a list of (start, goal,
priority) tuples; receive collision-free, time-optimal paths. Backed by
EECBS or LaCAM* under the hood.

- **Stack:** libMultiRobotPlanning or your own LaCAM* impl in C++/Rust,
  Python bindings, FastAPI.
- **Buyers:** mid-size warehouse operators with mixed-vendor AMRs that
  Symbotic / Geek+ doesn't serve.
- **Pricing:** $0.001-0.01 per agent-second routed; $2-10k/mo SaaS.

## 2. Drone-swarm coverage planner (~3 weeks)

Plan an N-drone coverage mission over an arbitrary polygon (search,
mapping, inspection) with constraints: battery, no-fly zones, comms
range. Output mission files for ArduPilot / PX4 + a sim preview.

- **Stack:** Polygon decomposition, multi-TSP, sim in Gazebo or
  Microsoft AirSim, MAVLink mission files.
- **Buyers:** inspection, agriculture, surveying, defense.
- **Pricing:** $3-10k/mission upfront; $1-3k/mo SaaS for recurring.

## 3. Multi-vendor AMR fleet dashboard (~4 weeks)

Sites running 2-5 different AMR brands have no single UI. Build an
Open-RMF-based gateway + observability dashboard (Foxglove + custom
React) that consolidates fleet state, traffic, alerts, KPIs.

- **Stack:** Open-RMF adapters, ROS2 bridges to vendor APIs, Foxglove,
  React/Tailwind UI, Postgres for KPIs.
- **Buyers:** 3PLs and manufacturers with heterogeneous fleets.
- **Pricing:** $20-100k installation + $1-5k/mo per site.

## 4. Drone-vs-AMR traffic light service (~3 weeks)

Indoor sites mixing drones (Verity-style) with floor AMRs need shared-
airspace coordination. Provide a small service that issues "stop /
go / yield" tokens via gRPC and visualizes in 3D.

- **Stack:** ROS2, simple zone-based MAPF, WebSocket dashboard.
- **Buyers:** larger warehouses experimenting with drone inventory.
- **Pricing:** $10-30k integration + recurring license.
