import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const ADVICE_POOL = [
    "🚀 Scalability is the key to galactic dominance. Ensure your core systems can handle 1M+ heartbeats.",
    "💡 Innovation isn't just about code; it's about solving the right problems for the right frontier.",
    "🛡️ Security is the foundation of trust. Never compromise on the GATES protocol.",
    "📊 Data-driven decisions outperform intuition. Monitor your telemetry like a hawk.",
    "🌊 Fluidity in architecture allows you to pivot when the lunar landscape shifts.",
    "🤖 AI is your multiplier. Train your models on high-quality terrestrial data before deploying to orbit.",
    "🛰️ Connectivity is the lifeblood of the fleet. Keep the Wormhole open and latency low.",
    "💰 Strategic reinvestment of mining rewards accelerates Phase 14 goals. Check your ledger regularly.",
    "🌍 Remember: NetworkBuster is everywhere. Design for interstellar compatibility.",
    "🧘 Focus on the 'Neural Core'. A balanced system is a resilient system."
];

function getAdvice() {
    console.log('\n' + '='.repeat(60));
    console.log('🌟 NETWORKBUSTER GROWTH ADVISOR 🌟');
    console.log('='.repeat(60));
    
    const randomAdvice = ADVICE_POOL[Math.floor(Math.random() * ADVICE_POOL.length)];
    
    console.log(`\n> ${randomAdvice}\n`);
    console.log('='.repeat(60));
    console.log('Stay focused, Captain Middleton. The stars are waiting.');
    console.log('='.repeat(60) + '\n');
}

getAdvice();
