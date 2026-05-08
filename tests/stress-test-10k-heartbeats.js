import axios from 'axios';
import crypto from 'crypto';

/**
 * 🚀 10,000 Heartbeat Load Test
 * Purpose: Validate the system's ability to handle high-frequency device registrations.
 */

const TARGET_URL = process.env.TARGET_URL || 'http://localhost:3000/api/devices/register';
const CONCURRENT_REQUESTS = parseInt(process.env.CONCURRENT_REQUESTS) || 100;
const TOTAL_REQUESTS = parseInt(process.env.TOTAL_REQUESTS) || 10000;

console.log(`📡 Starting Stress Test: ${TOTAL_REQUESTS} total requests at ${CONCURRENT_REQUESTS} concurrency.`);
console.log(`📍 Target: ${TARGET_URL}`);

let successCount = 0;
let errorCount = 0;
let startTime = Date.now();

async function sendRequest() {
  const payload = {
    hardwareId: crypto.randomBytes(8).toString('hex'),
    model: 'NB-LOAD-TESTER-v1',
    firmwareVersion: '1.0.0-stress',
    location: 'LUNAR-SURFACE-BETA',
    initialTelemetry: {
      battery: Math.floor(Math.random() * 100),
      temp: Math.floor(Math.random() * 50),
      heartbeat: true
    }
  };

  try {
    await axios.post(TARGET_URL, payload, { timeout: 5000 });
    successCount++;
  } catch (err) {
    errorCount++;
    // console.error(`Error: ${err.message}`);
  }
}

async function runTest() {
  const tasks = [];
  
  for (let i = 0; i < TOTAL_REQUESTS; i++) {
    tasks.push(sendRequest());
    
    if (tasks.length >= CONCURRENT_REQUESTS) {
      await Promise.all(tasks.splice(0, tasks.length));
      const progress = ((i + 1) / TOTAL_REQUESTS * 100).toFixed(1);
      const elapsed = (Date.now() - startTime) / 1000;
      const rps = (successCount / elapsed).toFixed(1);
      console.log(`[PROGRESS] ${progress}% | Success: ${successCount} | Errors: ${errorCount} | RPS: ${rps}`);
    }
  }
  
  await Promise.all(tasks);
  
  const totalTime = (Date.now() - startTime) / 1000;
  const finalRps = (successCount / totalTime).toFixed(1);
  
  console.log('\n--- 📊 STRESS TEST COMPLETE ---');
  console.log(`Total Requests: ${TOTAL_REQUESTS}`);
  console.log(`Success: ${successCount}`);
  console.log(`Errors: ${errorCount}`);
  console.log(`Total Time: ${totalTime.toFixed(2)} seconds`);
  console.log(`Average Throughput: ${finalRps} requests/sec`);
  console.log('-------------------------------\n');

  if (successCount >= TOTAL_REQUESTS * 0.95) {
    console.log('✅ PASS: System met 95% success threshold.');
  } else {
    console.log('❌ FAIL: System failed to meet performance targets.');
    process.exit(1);
  }
}

runTest().catch(console.error);
