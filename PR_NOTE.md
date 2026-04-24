PR Notes — Add Network Boost utilities

Summary:
This PR adds a cross-platform ``Network Boost`` utility to improve network throughput and configuration for target systems. It includes hardened apply logic and generates robust restore scripts to revert changes.

Files to add to upstream (`Cleanskiier27/Final`):
- `scripts/network-boost.ps1` (Windows)
- `scripts/network-boost.sh` (Linux)
- `docs/NETWORK-BOOST.md` (documentation)
- `CONTRIBUTORS.md` (contributor entry)

Testing recommendations:
- Run dry-run and review outputs: (Windows) `powershell -File scripts\network-boost.ps1` (Linux) `bash ./scripts/network-boost.sh`
- Run apply in a controlled VM and verify `network-boost-restore.*` contents and restore operations.
- Validate that installer integration is opt-in (checkbox) and uses non-interactive apply with `-Apply -Confirm:$false`.

Security & Safety:
- Scripts are designed to be reversible and non-destructive; restore scripts are generated with previous values and best-effort commands.
- Scripts log all operations to `network-boost.log` and recommend reboot where appropriate.

Maintainer notes:
- If merging, consider adding a small CI job that runs a dry-run, installs PSScriptAnalyzer/shellcheck, and verifies that restore scripts are generated when running apply in a controlled test runner.
- Optionally add an installer page and an entry in the main docs referencing the new tooling.

---

To apply this contribution automatically to upstream (fork + PR):
- Use the helper script `scripts/apply-to-upstream.sh` (Linux/macOS) or `scripts/apply-to-upstream.ps1` (Windows).
- Example (bash): `./scripts/apply-to-upstream.sh --upstream https://github.com/Cleanskiier27/Final.git --fork git@github.com:youruser/Final.git`
- Example (PowerShell): `.	ools\apply-to-upstream.ps1 -Upstream 'https://github.com/Cleanskiier27/Final.git' -Fork 'git@github.com:youruser/Final.git'`

The helper clones upstream, creates a branch, copies contribution files, commits, pushes to your fork, and uses `gh` (if available) to open a PR. If `gh` is not available, push to your fork and open a PR manually.

---

### PULL REQUEST #141: AUTONOMOUS FLIGHT KERNEL
- **Module**: `autonomous_flight_kernel.py`
- **Features**: Never-ending self-healing flight loop, strategic thought process.
- **Port**: 9002

### PULL REQUEST #144: HUB & MISSION CONTROL PORTALS
- **Routes**: `/hub` (Terrestrial Hub), `/lunar` (Lunar Mission Control)
- **Features**: 
  - **Terrestrial Hub**: Durango, CO uplink telemetry, network status, YOLO_OVERRIDE indicator.
  - **Lunar Mission Control**: Shackleton Crater HUD, atmospheric data, Firemind status, drone fleet tracking.
- **Integration**: Added to `public-landing.html` and `networkbuster_launcher.py`.

### PULL REQUEST #143: PUSH AGENT INTEGRATION
- **Module**: `push_agent.py`
- **Port**: 4501
- **Features**: Automated public distribution compilation, Git staging, and deployment readiness verification.
- **Integration**: Added to `networkbuster_launcher.py`.

### PULL REQUEST #142: AGI MUSIC & VIDEO INTEGRATION
- **Module**: `agi_music_video_host.py`
- **Visuals**: `agi_cinematic_overlay.html`
- **Port**: 4500
- **Features**: Algorithmic music synthesis, cinematic HUD overlay, real-time AGI telemetry.
- **Integration**: Added to `networkbuster_launcher.py`.