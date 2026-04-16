# 🚀 NEURAL CODER OS : BOOT PROTOCOLS

This guide addresses the boot options and port configurations for the **Neural Coder OS** and the **Aerospace Host Server**.

## 🔌 Port Mapping & Conflicts

By default, both the **Node.js Relay** and the **Python Aerospace Host** attempt to bind to port `3000`. To run both simultaneously, you must assign unique ports.

### Option 1: Neural Coder OS (Node.js/Socket.io)
Standard OS environment with UI and telemetry relay.
- **Default Port**: `3000`
- **Boot Command**: 
  ```powershell
  cd artemis-r-navigation
  npm run dev
  ```

### Option 2: Aerospace Host (Python/FastAPI)
Direct backend for raw telemetry data and agent tasks.
- **Default Port**: `3000` (Change to `8000` to avoid conflicts)
- **Boot Command**:
  ```powershell
  # Standard boot
  python mission_host.py
  
  # Boot with custom port (if updated)
  $env:PORT=8000; python mission_host.py
  ```

---

## 🛠 Troubleshooting Boot Errors

### `[Errno 10048] address already in use`
This occurs when another process (usually the Node server) is already on port 3000.
1. **Identify Listener**: `netstat -ano | findstr :3000`
2. **Kill Process**: `taskkill /F /PID <PID>`
3. **Or Change Port**: Set the `PORT` environment variable before running the Python script.

## 🧠 Diagnostic Boot Modes

| Flag | Effect |
| :--- | :--- |
| `--debug` | Enables verbose FastAPI logging |
| `--reload` | Hot-reloading enabled for Python development |
| `--no-ui` | Boots the Aerospace Host without the WebGL interface |

---
*Neural Coder OS v2.1.0 - Boot System Stable*
