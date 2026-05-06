# 🚀 Preciseliens PLLC Deployment Checkpoints
## Universal Mission Control Suite // v2026.05

This document outlines the **Sharepoints** and **Seps** required to deploy the Preciseliens / NetworkBuster software suite into production.

---

### 1. 📂 Separation of Concerns (Sharepoints)
The software is architected into three distinct execution layers:
- **Core Production Server:** `server.js` (Node/Express) - Manages all routing and asset delivery.
- **Mission Engines:** Python-based background services (Kernel Bridge, Arch Matrix, NASA Host).
- **Visualization Layer:** Vite-built React application (`/dist` assets) for the UI/UX.

---

### 2. ⚙️ Environment Configuration
Ensure the following variables are set in your production environment (or `.env` file):
```env
PORT=3000
SERVICE_NAME="Preciseliens Mission Control"
CORS_ORIGINS="https://yourdomain.com,http://localhost:3000"
AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;..."
```

---

### 3. 🏗️ Build & Setup Sequence (The "Seps")
To make the software work from a fresh clone, follow these exact steps:

1. **Build the Overlay:**
   ```powershell
   npm run build:overlay
   ```
   *This compiles the React/Vite app into production-ready static assets in `challengerepo/real-time-overlay/dist/`.*

2. **Initialize Python Environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install flask flask-cors requests waitress psutil
   ```

3. **Start Mission Engines (Background):**
   - **Kernel Bridge:** `python tools/python/kernel_telemetry_bridge.py` (Port 9002)
   - **Arch Matrix:** `python tools/python/arch_matrix_vm.py` (Port 9001)

4. **Launch Production Server:**
   ```powershell
   npm start
   ```

---

### 4. 🌐 Verified Production Routes
Once the build is complete and servers are active, the following entry points are live:
- **Main Mission Control:** [http://localhost:3000/os](http://localhost:3000/os)
- **Built World View:** [http://localhost:3000/worldview](http://localhost:3000/worldview)
- **Marketplace Hub:** [http://localhost:3000/marketplace](http://localhost:3000/marketplace)

---

### 5. 🛠️ Maintenance & Git
- **Update Logic:** After modifying React components, you **must** re-run `npm run build:overlay` for changes to appear on the production server.
- **Git Strategy:** Keep the `dist/` directories tracked for rapid deployment, but ensure `node_modules/` and `.venv/` are strictly ignored via `.gitignore`.

**Status:** 🟢 SYSTEM READY FOR WORLDWIDE DEPLOYMENT
