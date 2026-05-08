import axios from 'axios';

/**
 * ⚛️ Quantum Relay Verification Test
 * Purpose: Verify the zero-latency control signal path.
 */

const HUB_URL = 'http://localhost:3000/api/quantum';

async function testQuantumRelay() {
    console.log('📡 Testing Quantum Relay Path...');
    
    try {
        // 1. Check Status
        const status = await axios.get(`${HUB_URL}/status`);
        console.log(`✓ Hub Stability: ${status.data.stability}`);
        
        // 2. Send Relay Signal
        const payload = {
            target: 'PROXIMA-NODE-A',
            command: 'INITIATE-GAIA-SYNC',
            priority: 'CRITICAL'
        };
        
        console.log('📤 Relaying High-Priority Signal...');
        const relay = await axios.post(`${HUB_URL}/relay`, payload);
        
        if (relay.data.status === 'RELAYED') {
            console.log(`✅ SUCCESS: Signal ${relay.data.signalId} relayed with ${relay.data.latency} latency.`);
        } else {
            console.log('❌ FAIL: Relay status unexpected:', relay.data.status);
        }
        
        // 3. Test Coherence Limit (Size Check)
        console.log('📤 Testing Coherence Limit (Large Payload)...');
        const largePayload = { 
            target: 'HUB', 
            command: 'OVERLOAD-TEST',
            data: 'A'.repeat(500) 
        };
        try {
            await axios.post(`${HUB_URL}/relay`, largePayload);
        } catch (err) {
            if (err.response?.status === 413) {
                console.log('✅ SUCCESS: Coherence limit enforced (413 Payload Too Large).');
            } else {
                throw err;
            }
        }
        
    } catch (err) {
        console.error('❌ TEST FAILED:', err.message);
        if (err.response) console.error('Response:', err.response.data);
        process.exit(1);
    }
}

testQuantumRelay();
