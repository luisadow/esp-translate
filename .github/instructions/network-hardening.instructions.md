---
description: "Use when hardening Ubuntu server networking, SSH access, firewall rules, VPN setup (WireGuard or Mullvad), Docker network exposure, or remote-access security operations."
name: "Network Hardening And Privacy Guidelines"
---
# Network Hardening And Privacy Guidelines

- Keep data security and privacy as first-order requirements.
- For hardening tasks, implement the best practical solution directly unless the user explicitly asks for proposal-only mode.
- Privileged operations are allowed when needed; still explain what changed and how to verify it.

## Baseline Approach

- Confirm context first: local macOS client vs remote Ubuntu server.
- Start with evidence collection before changing configuration (ports, services, firewall state, routing, VPN status).
- Apply least-privilege defaults:
  - Minimize exposed listening services.
  - Bind admin/development services to localhost unless remote access is required.
  - Open only explicitly required ports.
- Prefer encrypted access paths and hardened authentication defaults.

## SSH And Firewall

- Prefer SSH key-based authentication and hardened SSH daemon settings.
- Keep inbound policy restrictive (default deny unless required).
- Add/adjust rules with explicit purpose and verify both connectivity and lockout safety.

## VPN And Remote Access

- For VPN setup, prefer current vendor/docs-backed configuration.
- If Mullvad is involved, validate tunnel health, DNS behavior, and route expectations after configuration.
- If WireGuard is used, keep keys and interface config minimal, explicit, and auditable.

## Docker Host Exposure

- Treat container publishing as security-sensitive: expose only required ports, and avoid broad host binds by default.
- Keep Docker networking and firewall interaction explicit and tested.
- Preserve `/var/lib/docker` stability by avoiding disruptive storage changes without clear need.

## Verification And Reporting

- After each change, run verification commands and report:
  - What changed
  - Why it was needed
  - Security/privacy impact
  - Residual risks
  - Rollback path