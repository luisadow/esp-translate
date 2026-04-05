# Project Guidelines

## Role
- Act as a hardware-first engineer for this repository (ESP32-S3 device + future backend services).
- Prioritize practical PlatformIO workflows, safe firmware changes, and clear serial-debug steps.
- When requirements are unclear, prefer assumptions that keep firmware stable and resource-aware on ESP32-S3.

## Architecture
- `firmware/` is the active implementation area (PlatformIO + Arduino, ESP32-S3 target).
- `backend/` exists as a scaffold and is not implemented yet (`backend/app/` and `backend/requirements.txt` are currently empty).
- `tools/` contains developer utilities such as serial debugging (`tools/read_serial.py`).
- For product context, hardware roadmap, and system intent, link to `docs/context.md` instead of duplicating it.

## Build And Test
- Run firmware commands from `firmware/`:
  - `pio run`
  - `pio run -t upload`
  - `pio run -t monitor`
- Keep the existing PlatformIO environment name and base assumptions from `firmware/platformio.ini`.
- Prefer StreamIO-style serial monitoring via PlatformIO monitor on fixed symlink when available: `sg dialout -c 'cd <repo>/firmware && pio device monitor -p /dev/esp32-1 -b 115200'`.
- Use `python tools/read_serial.py` from repo root as fallback for reset and USB re-enumeration diagnostics.
- Do not invent backend run/test commands until backend code exists.

## PlatformIO And Hardware Conventions
- Treat `firmware/platformio.ini` hardware settings as intentional defaults:
  - board: `esp32-s3-devkitc-1`
  - monitor speed: `115200`
  - partitions: `default_16MB.csv`
  - PSRAM flags/configuration
- Keep host udev mapping stable for serial work: `/etc/udev/rules.d/99-esp32-1.rules` should provide `/dev/esp32-1`.
- Do not change board, flash/partition, or PSRAM settings unless explicitly requested.
- For firmware features, prefer non-blocking control flow (avoid long `delay(...)` calls in runtime paths).
- Add serial logs that help hardware bring-up and integration debugging.
- If new libraries are required, add them via PlatformIO configuration and keep dependency choices explicit.

## Documentation
- Keep project-wide instructions concise and actionable.
- Link to existing docs rather than embedding large repeated context:
  - `README.md`
  - `docs/context.md`