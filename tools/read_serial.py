#!/usr/bin/env python3
"""Read ESP32-S3 serial output with auto-reconnect.

This utility prefers a stable /dev/serial/by-id path so USB re-enumeration
(/dev/ttyACM0 -> /dev/ttyACM1, etc.) does not interrupt log collection.
"""

from __future__ import annotations

import argparse
import glob
import sys
import time

import serial
from serial import SerialException


DEFAULT_BY_ID_GLOB = "/dev/serial/by-id/usb-Espressif_USB_JTAG_serial_debug_unit_*"


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Read ESP32-S3 serial logs")
	parser.add_argument(
		"--port",
		help="Serial device path. If omitted, auto-detects by-id or ttyACM.",
	)
	parser.add_argument(
		"--baud",
		type=int,
		default=115200,
		help="Baud rate (default: 115200)",
	)
	parser.add_argument(
		"--retry-s",
		type=float,
		default=0.5,
		help="Reconnect retry delay in seconds (default: 0.5)",
	)
	parser.add_argument(
		"--id-glob",
		default=DEFAULT_BY_ID_GLOB,
		help="Glob pattern for stable by-id device lookup.",
	)
	return parser.parse_args()


def auto_detect_port(id_glob: str) -> str | None:
	by_id = sorted(glob.glob(id_glob))
	if by_id:
		return by_id[0]

	acm = sorted(glob.glob("/dev/ttyACM*"))
	if acm:
		return acm[-1]

	return None


def open_port(port: str, baud: int) -> serial.Serial:
	return serial.Serial(port=port, baudrate=baud, timeout=0.25)


def main() -> int:
	args = parse_args()
	ser: serial.Serial | None = None
	port_hint = args.port
	last_wait_log = 0.0
	permission_hint_logged = False

	try:
		while True:
			if ser is None:
				port = port_hint or auto_detect_port(args.id_glob)
				if not port:
					now = time.time()
					if now - last_wait_log > 2.0:
						print("[serial] waiting for ESP device...")
						last_wait_log = now
					time.sleep(args.retry_s)
					continue

				try:
					ser = open_port(port, args.baud)
					print(f"[serial] connected: {port} @ {args.baud}")
					permission_hint_logged = False
				except SerialException as exc:
					print(f"[serial] open failed for {port}: {exc}")
					if (
						not permission_hint_logged
						and "Permission denied" in str(exc)
					):
						print(
							"[serial] hint: run with serial permissions, "
							"e.g. 'sg dialout -c \"python tools/read_serial.py\"'"
						)
						permission_hint_logged = True
					time.sleep(args.retry_s)
					continue

			try:
				line = ser.readline()
				if not line:
					continue
				text = line.decode("utf-8", errors="replace").rstrip("\r\n")
				print(text)
				sys.stdout.flush()
			except SerialException as exc:
				print(f"[serial] disconnected: {exc}")
				try:
					ser.close()
				except Exception:
					pass
				ser = None
				# Re-run detection on next connect if no explicit port is set.
				if not args.port:
					port_hint = None
				time.sleep(args.retry_s)

	except KeyboardInterrupt:
		print("\n[serial] stopped")
	finally:
		if ser is not None:
			try:
				ser.close()
			except Exception:
				pass

	return 0


if __name__ == "__main__":
	raise SystemExit(main())