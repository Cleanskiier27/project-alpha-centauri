import axios from 'axios';
import crypto from 'crypto';

/**
 * 🚀 1,000,000 Heartbeat (1M Milestone) Stress Test
 * Purpose: Validate the system's ability to handle galactic-scale telemetry.
 */

const TARGET_URL = process.env.TARGET_URL || 'http://localhost:3000/api/devices/register';
const CONCURRENT_REQUESTS = parseInt(process.env.CONCURRENT_REQUESTS) || 200; // Increased for 1M
const TOTAL_REQUESTS = parseInt(process.env.TOTAL_REQUESTS) || 1000000;
const REPORT_INTERVAL = 10000; // Report every 10k requests

console.log(`🌌 Starting GALACTIC STRESS TEST: ${TOTAL_REQUESTS} total beacons.`);
console.log(`📍 Target: ${TARGET_URL} | Concurrency: ${CONCURRENT_REQUESTS}`);

let successCount = 0;
let errorCount = 0;
let startTime = Date.now();

async function sendBeacon() {
  const payload = {
    hardwareId: crypto.randomBytes(12).toString('hex'),
    model: 'GALACTIC-BEACON-v14',
    firmwareVersion: '14.0.0-galactic',
    location: 'PROXIMA-CENTAURI-B',
    initialTelemetry: {
      latency: Math.floor(Math.random() * 5000), // Simulated interstellar delay (ms)
      signalStrength: Math.random().toFixed(4),
      galactic_sync: true
    }
  };

  try {
    await axios.post(TARGET_URL, payload, { 
        timeout: 10000,
        headers: { 'X-Galactic-Scale': 'true' }
    });
    successCount++;
  } catch (err) {
    if (errorCount === 0) console.error(`[ERROR SAMPLE] Code: ${err.code} | Message: ${err.message} | Response: ${err.response?.status || 'N/A'}`);
    errorCount++;
  }
}

async function runGalacticTest() {
  let activeTasks = [];
  
  for (let i = 0; i < TOTAL_REQUESTS; i++) {
    activeTasks.push(sendBeacon());
    
    if (activeTasks.length >= CONCURRENT_REQUESTS) {
      await Promise.all(activeTasks);
      activeTasks = [];
      
      if ((i + 1) % REPORT_INTERVAL === 0) {
        const progress = ((i + 1) / TOTAL_REQUESTS * 100).toFixed(2);
        const elapsed = (Date.now() - startTime) / 1000;
        const rps = (successCount / elapsed).toFixed(1);
        console.log(`[GALACTIC PROGRESS] ${progress}% | Success: ${successCount} | RPS: ${rps} | Time: ${elapsed.toFixed(1)}s`);
      }
    }
  }
  
  await Promise.all(activeTasks);
  
  const totalTime = (Date.now() - startTime) / 1000;
  const finalRps = (successCount / totalTime).toFixed(1);
  
  console.log('\n--- 🌌 GALACTIC STRESS TEST COMPLETE ---');
  console.log(`Total Beacons: ${TOTAL_REQUESTS}`);
  console.log(`Success: ${successCount}`);
  console.log(`Errors: ${errorCount}`);
  console.log(`Total Time: ${totalTime.toFixed(2)} seconds`);
  console.log(`Average Galactic Throughput: ${finalRps} req/sec`);
  console.log('----------------------------------------\n');

  if (successCount >= TOTAL_REQUESTS * 0.90) {
    console.log('✅ PASS: System met 90% galactic success threshold.');
  } else {
    console.log('❌ FAIL: System failed to meet galactic performance targets.');
    process.exit(1);
  }
}

runGalacticTest().catch(console.error);
