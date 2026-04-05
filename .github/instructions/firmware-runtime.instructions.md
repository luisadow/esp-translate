---
description: "Use when implementing or changing ESP32-S3 firmware runtime logic in PlatformIO/Arduino, including loop scheduling, I/O polling, serial diagnostics, and hardware integration code."
name: "Firmware Runtime Guidelines"
applyTo:
  - "firmware/src/**"
  - "firmware/include/**"
---
# Firmware Runtime Guidelines

- Keep runtime control flow non-blocking. Avoid long `delay(...)` usage in active code paths; prefer millis-based scheduling or short state-machine steps.
- Protect device stability first. Changes should minimize RAM churn and avoid large transient allocations in repeated loop paths.
- Add useful serial diagnostics for bring-up and integration debugging:
  - Log boot and subsystem initialization milestones.
  - Log recoverable hardware and communication errors with enough context to troubleshoot quickly.
  - Keep log volume practical for `115200` monitor speed.
- Prefer stable serial paths (`/dev/serial/by-id/...`) for monitoring and tools; avoid hard-coding volatile `/dev/ttyACM*` paths when auto-detection is feasible.
- For reset behavior validation, use `tools/read_serial.py` and confirm the sequence: disconnect event, reconnect event, and fresh `BOOT` logs with restarted uptime.
- Preserve hardware defaults from `firmware/platformio.ini` unless the task explicitly asks for config changes:
  - board: `esp32-s3-devkitc-1`
  - partitions: `default_16MB.csv`
  - PSRAM settings
- When adding dependencies, declare them explicitly in PlatformIO config and keep choices minimal.
- Prefer clear setup/loop boundaries:
  - `setup()`: one-time initialization, pin/peripheral checks, startup logs.
  - `loop()`: short, repeatable steps with predictable latency.
- For hardware-facing code, fail safely:
  - Validate peripheral init results.
  - Keep degraded behavior explicit (log and continue safely where possible).
  - Avoid silent failure paths.
- Link to existing project context instead of duplicating high-level product details: `docs/context.md`.