/**
 * AETHER-TELEMETRY v1.0.0
 * Backend uplink for Starlite API and Git Synchronization.
 */

export class AetherUplink {
    constructor(apiBase = "http://localhost:8000") {
        this.apiBase = apiBase;
        this.status = "DISCONNECTED";
    }

    async pulse(agentData) {
        try {
            const response = await fetch(`${this.apiBase}/status`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    timestamp: Date.now(),
                    agents: agentData
                })
            });
            this.status = "CONNECTED";
            return await response.json();
        } catch (e) {
            this.status = "ERROR";
            console.warn("Aether Uplink Failed:", e);
        }
    }

    /**
     * TRIGGER RECURSIVE GIT SYNC
     */
    async syncGates() {
        console.log("[Aether-Uplink] Triggering 60s Git Cycle...");
        // This targets the server.js endpoint we created earlier
        return fetch('/api/restart', { method: 'POST' }); 
    }
}
