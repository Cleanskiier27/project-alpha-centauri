import express from 'express';
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';

const router = express.Router();
const BUNDLE_STORAGE = path.join(process.cwd(), 'data', 'dtn-bundles');

// Extreme TTL Constants (Galactic Scale)
const MAX_TTL_SECONDS = 50 * 365 * 24 * 60 * 60; // 50 Years
const DEFAULT_TTL = 31536000; // 1 Year

// Ensure storage exists
if (!fs.existsSync(BUNDLE_STORAGE)) fs.mkdirSync(BUNDLE_STORAGE, { recursive: true });

/**
 * 🛰️ DTN Bundle Protocol (BPv7 inspired)
 * Formal Building Block for Phase 14 Interstellar Data Transit.
 */

// Helper: Formal Bundle Validator
function validateBundle(bundle) {
    const errors = [];
    if (!bundle.source) errors.push('Missing source EID (Endpoint ID)');
    if (!bundle.destination) errors.push('Missing destination EID');
    if (!bundle.payload) errors.push('Missing payload');
    if (bundle.ttl && (bundle.ttl < 0 || bundle.ttl > MAX_TTL_SECONDS)) {
        errors.push(`TTL exceeds galactic limits (Max: ${MAX_TTL_SECONDS}s)`);
    }
    return errors;
}

// POST /api/dtn/bundle
// Send a data bundle into the galactic mesh
router.post('/bundle', (req, res) => {
    const { 
        source, 
        destination, 
        payload, 
        ttl = DEFAULT_TTL, 
        priority = 1,
        protocol = 'BPv7'
    } = req.body || {};
    
    const errors = validateBundle({ source, destination, payload, ttl });
    if (errors.length > 0) {
        return res.status(400).json({ error: 'Formal validation failed', details: errors });
    }

    const bundleId = `NB-BNDL-${Date.now()}-${crypto.randomBytes(4).toString('hex')}`;
    const bundle = {
        bundleId,
        protocol,
        source,
        destination,
        timestamp: new Date().toISOString(),
        ttl,
        expiresAt: new Date(Date.now() + ttl * 1000).toISOString(),
        priority, // 0: Low, 1: Standard, 2: Critical (Artemis/Mission Control)
        status: 'stored',
        hopCount: 0,
        payload
    };

    // Store bundle locally (Store-and-Forward)
    const fn = path.join(BUNDLE_STORAGE, `${bundleId}.json`);
    try {
        fs.writeFileSync(fn, JSON.stringify(bundle, null, 2), 'utf8');
        console.log(`📡 [DTN] Bundle ${bundleId} stored. Dest: ${destination} | Priority: ${priority}`);
        res.status(202).json({ 
            bundleId, 
            status: 'stored', 
            expiresAt: bundle.expiresAt,
            hint: 'Forwarding scheduled upon link availability' 
        });
    } catch (err) {
        res.status(500).json({ error: 'Storage failure', details: err.message });
    }
});

// GET /api/dtn/forward/:nextHop
// Fetch pending bundles for a specific destination/next-hop
router.get('/forward/:nextHop', (req, res) => {
    const { nextHop } = req.params;
    
    try {
        if (!fs.existsSync(BUNDLE_STORAGE)) return res.json({ count: 0, bundles: [] });
        
        const files = fs.readdirSync(BUNDLE_STORAGE).filter(f => f.endsWith('.json'));
        const bundles = files.map(f => JSON.parse(fs.readFileSync(path.join(BUNDLE_STORAGE, f), 'utf8')));
        
        // Filter: Destination match, stored status, and NOT EXPIRED
        const eligible = bundles.filter(b => {
            const isMatch = b.destination === nextHop || nextHop === 'any';
            const isPending = b.status === 'stored' || b.status === 'queued';
            const isNotExpired = new Date(b.expiresAt) > new Date();
            return isMatch && isPending && isNotExpired;
        });

        // Sort by Priority (Critical first)
        eligible.sort((a, b) => b.priority - a.priority);
        
        res.json({ 
            count: eligible.length, 
            nextHop,
            bundles: eligible,
            timestamp: new Date().toISOString()
        });
    } catch (err) {
        res.status(500).json({ error: 'Retrieval failure', details: err.message });
    }
});

// GET /api/dtn/bundle/:id
router.get('/bundle/:id', (req, res) => {
    const fn = path.join(BUNDLE_STORAGE, `${req.params.id}.json`);
    if (!fs.existsSync(fn)) return res.status(404).json({ error: 'Bundle not found' });
    
    try {
        const bundle = JSON.parse(fs.readFileSync(fn, 'utf8'));
        res.json(bundle);
    } catch (err) {
        res.status(500).json({ error: 'Read failure', details: err.message });
    }
});

// PATCH /api/dtn/bundle/:id
// Formal status transition
router.patch('/bundle/:id', (req, res) => {
    const { id } = req.params;
    const { status, nextHop } = req.body;
    
    const fn = path.join(BUNDLE_STORAGE, `${id}.json`);
    if (!fs.existsSync(fn)) return res.status(404).json({ error: 'Bundle not found' });
    
    try {
        const bundle = JSON.parse(fs.readFileSync(fn, 'utf8'));
        
        // Audit trail
        bundle.history = bundle.history || [];
        bundle.history.push({
            status: bundle.status,
            transitionedAt: new Date().toISOString(),
            node: process.env.NODE_ID || 'GATEWAY-PRIMARY'
        });

        bundle.status = status;
        if (nextHop) {
            bundle.lastHop = bundle.nextHop;
            bundle.nextHop = nextHop;
            bundle.hopCount++;
        }
        
        bundle.updatedAt = new Date().toISOString();
        
        fs.writeFileSync(fn, JSON.stringify(bundle, null, 2), 'utf8');
        res.json({ success: true, bundleId: id, status: bundle.status });
    } catch (err) {
        res.status(500).json({ error: 'Update failure', details: err.message });
    }
});

// DELETE /api/dtn/cleanup
// Purge expired bundles (Garbage Collection)
router.delete('/cleanup', (req, res) => {
    try {
        const files = fs.readdirSync(BUNDLE_STORAGE).filter(f => f.endsWith('.json'));
        let purged = 0;
        
        files.forEach(f => {
            const fp = path.join(BUNDLE_STORAGE, f);
            const bundle = JSON.parse(fs.readFileSync(fp, 'utf8'));
            if (new Date(bundle.expiresAt) < new Date()) {
                fs.unlinkSync(fp);
                purged++;
            }
        });
        
        res.json({ success: true, purgedCount: purged });
    } catch (err) {
        res.status(500).json({ error: 'Cleanup failure', details: err.message });
    }
});

export default router;

