import express from 'express';
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';

const router = express.Router();
const BUNDLE_STORAGE = path.join(process.cwd(), 'data', 'dtn-bundles');

// Ensure storage exists
if (!fs.existsSync(BUNDLE_STORAGE)) fs.mkdirSync(BUNDLE_STORAGE, { recursive: true });

/**
 * 🛰️ DTN Bundle Protocol (BPv7 inspired)
 * Purpose: Handle high-latency "Store-and-Forward" data transit.
 */

// POST /api/dtn/bundle
// Send a data bundle into the galactic mesh
router.post('/bundle', (req, res) => {
    const { source, destination, payload, ttl = 31536000 } = req.body || {}; // Default TTL 1 year
    
    if (!source || !destination || !payload) {
        return res.status(400).json({ error: 'Incomplete bundle metadata' });
    }

    const bundleId = `NB-BNDL-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
    const bundle = {
        bundleId,
        source,
        destination,
        timestamp: new Date().toISOString(),
        ttl,
        status: 'stored',
        payload
    };

    // Store bundle locally (Store-and-Forward)
    const fn = path.join(BUNDLE_STORAGE, `${bundleId}.json`);
    fs.writeFileSync(fn, JSON.stringify(bundle, null, 2), 'utf8');

    console.log(`📡 Bundle ${bundleId} stored for forwarding to ${destination}`);
    res.status(202).json({ bundleId, status: 'stored', hint: 'Link availability pending' });
});

// GET /api/dtn/forward
// Fetch pending bundles for a specific destination/next-hop
router.get('/forward/:nextHop', (req, res) => {
    const { nextHop } = req.params;
    
    try {
        const files = fs.readdirSync(BUNDLE_STORAGE).filter(f => f.endsWith('.json'));
        const bundles = files.map(f => JSON.parse(fs.readFileSync(path.join(BUNDLE_STORAGE, f), 'utf8')));
        
        // Filter bundles destined for this hop
        const eligible = bundles.filter(b => b.destination === nextHop && b.status === 'stored');
        
        res.json({ count: eligible.length, bundles: eligible });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// PATCH /api/dtn/bundle/:id
// Mark bundle as delivered or forwarded
router.patch('/bundle/:id', (req, res) => {
    const { id } = req.params;
    const { status } = req.body;
    
    const fn = path.join(BUNDLE_STORAGE, `${id}.json`);
    if (!fs.existsSync(fn)) return res.status(404).json({ error: 'Bundle not found' });
    
    const bundle = JSON.parse(fs.readFileSync(fn, 'utf8'));
    bundle.status = status;
    bundle.updatedAt = new Date().toISOString();
    
    fs.writeFileSync(fn, JSON.stringify(bundle, null, 2), 'utf8');
    res.json({ success: true, bundle });
});

export default router;
