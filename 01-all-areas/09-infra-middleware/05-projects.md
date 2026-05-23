# Four Projects You Can Build and Sell

## 1. ROS2 + DDS audit and tuning service (~2-3 weeks)

Customer ships a topology + workload description (or a recorded run);
you produce a tuning report: QoS profile recommendations per topic,
DDS implementation choice (Cyclone vs Fast vs Zenoh), network config,
and a tuned launch file set.

- **Stack:** Cyclone DDS, Fast DDS, Zenoh, profilers (perf, eBPF,
  ros2 doctor / topic delay), Foxglove for visualization.
- **Buyers:** robotics startups whose ROS2 graph is slow or flaky.
- **Pricing:** $5-15k per audit; retainer for ongoing.

## 2. MCAP-based regression-test SaaS (~4 weeks)

Customer uploads a corpus of MCAP recordings + a candidate perception /
planning binary. Your service spins up workers, replays bags through
the binary, compares outputs against baseline, and reports regressions
in a PR-friendly format.

- **Stack:** MCAP, foxglove-cli, GitHub Actions integration, S3-backed
  storage, Postgres for metrics, simple React dashboard.
- **Buyers:** any robotics team with a multi-developer codebase and
  flaky deploys.
- **Pricing:** $500-5k/mo per repo + per-replay compute.

## 3. Fleet observability stack-in-a-box (~3-4 weeks)

A turnkey Docker compose + Terraform module that gives a customer a
private Foxglove-style dashboard + Prometheus + Grafana + log-storage
backend with auth, retention, and alerts. Sits behind their VPN.

- **Stack:** Foxglove OSS, MCAP, Prometheus, Grafana, OpenTelemetry,
  Authentik / Keycloak, Terraform.
- **Buyers:** robotics teams that don't want to ship telemetry to a
  vendor SaaS (defense, regulated industries).
- **Pricing:** $25-100k installation + recurring support.

## 4. OTA + safe-rollback platform for ROS2 robots (~4 weeks)

Mender / RAUC-based OTA with A/B partitions, cohort-based gradual
rollouts, health checks, and one-button rollback. Built specifically
for ROS2 + Jetson stacks.

- **Stack:** Mender or RAUC, ostree, systemd, Cyclone DDS health
  probes, small management UI.
- **Buyers:** any robotics company shipping more than 10 robots that
  doesn't want to build OTA in-house.
- **Pricing:** $25k-150k licensing per company; per-fleet recurring.
