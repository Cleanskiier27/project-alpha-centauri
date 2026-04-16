/**
 * AETHER-CORE FRAMEWORK v1.0.0
 * The definitive engine for Agentic Operating Systems.
 */

export class AetherOS {
    constructor(config = {}) {
        this.name = config.name || "AetherOS";
        this.version = "1.0.0";
        this.windows = new Map();
        this.agents = new Map();
        this.eventBus = new EventTarget();
        this.bootTime = Date.now();
        
        console.log(`[${this.name}] Initializing Aether-Core Framework...`);
    }

    /**
     * REGISTER AN AGENT
     * @param {string} name - Agent identifier
     * @param {object} logic - Agent behavioral hooks
     */
    registerAgent(name, logic) {
        this.agents.set(name, {
            status: 'IDLE',
            lastPulse: Date.now(),
            ...logic
        });
        this.emit('AGENT_REGISTERED', { name });
    }

    /**
     * EMIT EVENT TO BUS
     */
    emit(event, detail) {
        const ev = new CustomEvent(event, { detail });
        this.eventBus.dispatchEvent(ev);
        console.log(`[Aether-Bus] ${event}`, detail);
    }

    /**
     * LISTEN TO BUS
     */
    on(event, callback) {
        this.eventBus.addEventListener(event, (e) => callback(e.detail));
    }

    /**
     * SPAWN UI WINDOW
     */
    spawnWindow(id, title, options = {}) {
        const win = new AetherWindow(id, title, options);
        this.windows.set(id, win);
        this.emit('WINDOW_SPAWNED', { id, title });
        return win;
    }
}

class AetherWindow {
    constructor(id, title, options) {
        this.id = id;
        this.title = title;
        this.width = options.width || 400;
        this.height = options.height || 300;
        this.visible = true;
    }

    toggle() {
        this.visible = !this.visible;
        const el = document.getElementById(this.id);
        if (el) el.classList.toggle('hidden');
    }
}
