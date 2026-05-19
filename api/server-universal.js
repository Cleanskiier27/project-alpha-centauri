import express from 'express';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Optional performance packages with fallbacks
let compression = null;
let helmet = null;

try {
  compression = (await import('compression')).default;
} catch {
  console.warn('⚠️  compression module not found');
}

try {
  helmet = (await import('helmet')).default;
} catch {
  console.warn('⚠️  helmet module not found');
}

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
const PORT = process.env.PORT || 3001;

// Apply optional middleware
if (compression) app.use(compression());
if (helmet) app.use(helmet());

// Required middleware
app.use(express.json({ limit: '100mb' }));
app.use(express.urlencoded({ extended: true, limit: '100mb' }));

// Performance: Load specs with error handling
let specsCache = null;
let specsCacheTTL = 0;
const CACHE_DURATION = 300000; // 5 minutes

function loadSpecs() {
  try {
    const specsPath = path.resolve(__dirname, '../data/system-specifications.json');
    if (fs.existsSync(specsPath)) {
      specsCache = JSON.parse(fs.readFileSync(specsPath, 'utf8'));
      specsCacheTTL = Date.now() + CACHE_DURATION;
      console.log('✓ Specs loaded from:', specsPath);
    } else {
      console.warn('⚠️  Specs file not found:', specsPath);
      specsCache = { error: 'Specs not found' };
    }
  } catch (error) {
    console.error('Error loading specs:', error.message);
    specsCache = { error: 'Failed to load specs' };
  }
}

// Load specs on startup
loadSpecs();

// ============================================
// MOUNT SUB-ROUTERS (Formal Building Blocks)
// ============================================

const subRouters = [
  { path: '/api/devices', file: './devices.js' },
  { path: '/api/dtn', file: './interstellar-dtn.js' },
  { path: '/api/quantum', file: './quantum-hub.js' },
  { path: '/api/ai', file: './ai-requests.js' },
  { path: '/api/gpu', file: './gpu-stats.js' },
  { path: '/api/recycle', file: './recycle.js' }
];

for (const { path: routePath, file } of subRouters) {
  try {
    const { default: router } = await import(file);
    app.use(routePath, router);
    console.log(`✓ Mounted router: ${routePath} from ${file}`);
  } catch (err) {
    console.warn(`⚠️  Failed to mount router ${routePath}:`, err.message);
  }
}

// ============================================
// CORE ROUTES
// ============================================

app.get('/api/specs', (req, res) => {
  res.set('Cache-Control', 'public, max-age=300');
  
  // Reload if expired
  if (Date.now() > specsCacheTTL) {
    loadSpecs();
  }
  
  if (specsCache) {
    res.json(specsCache);
  } else {
    res.status(500).json({ error: 'Specs unavailable' });
  }
});

app.get('/api/specs/:section', (req, res) => {
  res.set('Cache-Control', 'public, max-age=300');
  
  if (Date.now() > specsCacheTTL) {
    loadSpecs();
  }
  
  const section = req.params.section?.toLowerCase();
  if (specsCache && specsCache[section]) {
    res.json({ [section]: specsCache[section] });
  } else {
    res.status(404).json({ error: 'Section not found' });
  }
});

app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    galactic_sync: true
  });
});

app.get('/api/health/detailed', (req, res) => {
  res.set('Cache-Control', 'public, max-age=5');
  
  const memUsage = process.memoryUsage();
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memory: {
      heapUsed: Math.round(memUsage.heapUsed / 1024 / 1024),
      heapTotal: Math.round(memUsage.heapTotal / 1024 / 1024)
    },
    routers: subRouters.map(r => r.path)
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({ error: 'Not found', path: req.path });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Error:', err.message);
  res.status(500).json({ error: 'Internal server error', details: err.message });
});

// Start server
const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`\n🚀 API Server running at http://localhost:${PORT}`);
  console.log(`⚡ Features:`);
  if (compression) console.log(`   ✓ Compression enabled`);
  if (helmet) console.log(`   ✓ Security headers enabled`);
  console.log(`   ✓ Health checks: /health, /api/health/detailed`);
  console.log(`   ✓ Specs: /api/specs`);
  console.log(`   ✓ Galactic Routers: ${subRouters.length} paths registered\n`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Shutting down...');
  server.close(() => {
    console.log('API Server closed');
    process.exit(0);
  });
});

