# Antigravity Module (Matter Compiler)
## NetworkBuster Core Subsystem

The **Antigravity** module is a foundational component of the NetworkBuster platform, specializing in the **Matter Compiler** logic and hardware integration for security key initialization.

### 🛰️ Sub-Modules & Components
- **`app/`**: Kotlin Android application for Antigravity diagnostics and control.
- **Hardware Schematics**: [RESTRICTED ACCESS] - Consult project lead for secure vault credentials.

### 🛠️ Development & Integration
- **Matter Compiler Integration**: Logic for serializing and programming security tokens.
- **Cloud Connectivity**: Uses `gcloud` and `firebase` for telemetry; see `scripts/` for authentication setup.
- **Build System**: Uses Gradle CLI. Ensure Android SDK is configured in your environment.

### 🚀 Getting Started
1. Request access to the Hardware Schematics from the security lead.
2. Add `google-services.json` to `app/` (do not commit).
3. Build using `./gradlew assembleDebug`.