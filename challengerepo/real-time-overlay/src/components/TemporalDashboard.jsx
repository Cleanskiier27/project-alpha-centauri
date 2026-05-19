import React, { useState, useEffect, useRef } from 'react';
import { Clock, Globe, Zap, Navigation, ShieldAlert, Cpu } from 'lucide-react';

/**
 * 🌌 Temporal Galactic Dashboard (4D Visualization)
 * Part of Phase 14: Galactic Scale
 * Purpose: Visualize relativistic data transit and stellar drift across centuries.
 */

const TemporalDashboard = () => {
  const [simulatedYear, setSimulatedYear] = useState(2026);
  const [timeDilation, setTimeDilation] = useState(1.0);
  const [activeBundles, setActiveBundles] = useState([]);
  const [galacticStatus, setGalacticStatus] = useState('SYNCED');

  // Simulated Star Data (Derived from GalaxyMap)
  const [stars, setStars] = useState([
    { name: 'Sol', x: 0, y: 0, z: 0, drift: { x: 0, y: 0, z: 0 } },
    { name: 'Proxima Centauri', x: 1.3, y: 0.8, z: -0.9, drift: { x: 0.000005, y: 0.000003, z: -0.000002 } },
    { name: 'Sirius A', x: 2.6, y: 0.3, z: -1.9, drift: { x: 0.000008, y: -0.000001, z: 0.000004 } },
    { name: 'Vega', x: 7.8, y: -2.3, z: 4.1, drift: { x: -0.000002, y: 0.000005, z: 0.000001 } }
  ]);

  useEffect(() => {
    // Fetch active DTN bundles from API
    const fetchBundles = async () => {
      try {
        const res = await fetch('/api/dtn/forward/GALAXY-CENTER');
        const data = await res.json();
        if (data.bundles) setActiveBundles(data.bundles);
      } catch (err) {
        console.warn('DTN API offline, using mock bundles');
        setActiveBundles([
          { bundleId: 'NB-BNDL-MOCK-1', source: 'LUNAR-ALPHA', destination: 'MARS-BETA', status: 'stored' }
        ]);
      }
    };

    // Fetch star data from API
    const fetchStars = async () => {
      try {
        const res = await fetch('/api/realtime/star-positions');
        const data = await res.json();
        if (Array.isArray(data)) setStars(data);
      } catch (err) {
        console.warn('Star API offline');
      }
    };

    fetchBundles();
    fetchStars();
    const interval = setInterval(() => {
        fetchBundles();
        fetchStars();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const calculatePosition = (star, year) => {
    const yearsElapsed = year - 2026;
    return {
      x: (star.x + star.drift.x * yearsElapsed).toFixed(6),
      y: (star.y + star.drift.y * yearsElapsed).toFixed(6),
      z: (star.z + star.drift.z * yearsElapsed).toFixed(6)
    };
  };

  return (
    <div className="flex flex-col h-full bg-black/40 rounded-lg overflow-hidden border border-[#00f0ff]/20">
      {/* Header */}
      <div className="bg-gradient-to-r from-[#00d2ff]/20 to-[#9d50bb]/20 p-4 border-b border-[#00f0ff]/30 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Navigation className="text-[#00f0ff]" size={24} />
          <div>
            <h2 className="text-lg font-bold text-white tracking-widest uppercase">Temporal Galactic Dashboard</h2>
            <p className="text-[10px] text-[#00f0ff]/70 font-mono">PHASE 14 // LORENTZ-SYNC: ENABLED</p>
          </div>
        </div>
        <div className="flex items-center gap-6">
          <div className="text-right">
            <p className="text-[10px] text-gray-400 uppercase">Simulation Epoch</p>
            <p className="text-xl font-bold text-[#00f0ff] font-mono">{simulatedYear}</p>
          </div>
          <div className="bg-black/40 px-3 py-1 rounded border border-[#00f0ff]/30">
            <p className="text-[8px] text-gray-500 uppercase">Status</p>
            <p className="text-xs font-bold text-[#00ff00]">{galacticStatus}</p>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Panel: 4D Star Map */}
        <div className="flex-1 p-6 relative overflow-hidden bg-[radial-gradient(circle_at_center,_#111_0%,_#000_100%)]">
            {/* Grid Overlay */}
            <div className="absolute inset-0 opacity-10 pointer-events-none" style={{
                backgroundImage: 'linear-gradient(#00f0ff 1px, transparent 1px), linear-gradient(90deg, #00f0ff 1px, transparent 1px)',
                backgroundSize: '40px 40px'
            }}></div>

            {/* Stars Visualization */}
            <div className="relative w-full h-full flex items-center justify-center">
                {stars.map((star, idx) => {
                    const pos = calculatePosition(star, simulatedYear);
                    // Simple projection for 2D UI
                    const left = 50 + parseFloat(pos.x) * 10;
                    const top = 50 + parseFloat(pos.y) * 10;
                    
                    return (
                        <div key={star.name} className="absolute transition-all duration-500 group" style={{
                            left: `${left}%`,
                            top: `${top}%`
                        }}>
                            <div className="w-2 h-2 rounded-full bg-white shadow-[0_0_10px_white] cursor-pointer"></div>
                            <div className="absolute top-4 left-4 whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity bg-black/80 p-2 rounded border border-[#00f0ff]/50 z-20">
                                <p className="text-xs font-bold text-white">{star.name}</p>
                                <p className="text-[10px] text-[#00f0ff]">X: {pos.x} LY</p>
                                <p className="text-[10px] text-[#00f0ff]">Y: {pos.y} LY</p>
                                <p className="text-[10px] text-[#00f0ff]">Z: {pos.z} LY</p>
                            </div>
                        </div>
                    );
                })}
                
                {/* Sol Center */}
                <div className="w-4 h-4 rounded-full bg-yellow-400 shadow-[0_0_20px_#FDB813] z-10"></div>
                <p className="absolute mt-8 text-[10px] font-bold text-yellow-400">SOL SYSTEM</p>
            </div>

            {/* Timeline Slider */}
            <div className="absolute bottom-6 left-6 right-6 glass-panel p-4 flex items-center gap-4">
                <Clock className="text-[#00f0ff]" size={18} />
                <div className="flex-1">
                    <div className="flex justify-between text-[10px] text-gray-500 mb-1 font-mono">
                        <span>2026</span>
                        <span>SIMULATED EPOCH</span>
                        <span>3026</span>
                    </div>
                    <input 
                        type="range" 
                        min="2026" 
                        max="3026" 
                        value={simulatedYear}
                        onChange={(e) => setSimulatedYear(parseInt(e.target.value))}
                        className="w-full accent-[#00f0ff] bg-white/10 rounded-lg h-1 appearance-none cursor-pointer"
                    />
                </div>
                <div className="w-20 text-center font-mono text-sm text-[#00f0ff]">
                    +{simulatedYear - 2026}Y
                </div>
            </div>
        </div>

        {/* Right Panel: Relativistic & DTN Metrics */}
        <div className="w-80 border-l border-[#00f0ff]/20 flex flex-col gap-4 p-4 overflow-auto bg-black/20">
            {/* Relativistic Stats */}
            <div className="space-y-3">
                <div className="flex items-center gap-2 border-b border-white/10 pb-1">
                    <Zap className="text-yellow-400" size={14} />
                    <h3 className="text-xs font-bold text-white uppercase tracking-tighter">Relativistic Metrics</h3>
                </div>
                <div className="grid grid-cols-2 gap-2">
                    <div className="bg-white/5 p-2 rounded">
                        <p className="text-[8px] text-gray-500">GAMMA (γ)</p>
                        <p className="text-sm font-bold text-yellow-400">1.154</p>
                    </div>
                    <div className="bg-white/5 p-2 rounded">
                        <p className="text-[8px] text-gray-500">VELOCITY</p>
                        <p className="text-sm font-bold text-[#00f0ff]">0.50c</p>
                    </div>
                </div>
                <div className="bg-white/5 p-3 rounded border border-yellow-400/20">
                    <p className="text-[10px] text-gray-400 mb-1">TIME DILATION FACTOR</p>
                    <div className="h-1 bg-white/10 rounded-full overflow-hidden">
                        <div className="h-full bg-yellow-400 w-1/2"></div>
                    </div>
                    <p className="text-[9px] text-yellow-400 mt-1">Traveler experiences 1 year per 1.15 years Earth time.</p>
                </div>
            </div>

            {/* DTN Bundle Queue */}
            <div className="flex-1 flex flex-col min-h-0">
                <div className="flex items-center gap-2 border-b border-white/10 pb-1 mb-2">
                    <Globe className="text-[#9d50bb]" size={14} />
                    <h3 className="text-xs font-bold text-white uppercase tracking-tighter">Interstellar Bundles</h3>
                </div>
                <div className="flex-1 overflow-auto space-y-2 pr-1">
                    {activeBundles.length > 0 ? activeBundles.map(bundle => (
                        <div key={bundle.bundleId} className="bg-white/5 p-2 rounded border-l-2 border-[#9d50bb] text-[10px]">
                            <div className="flex justify-between font-bold text-white mb-1">
                                <span>{bundle.bundleId}</span>
                                <span className="text-[#00ff00] text-[8px]">{bundle.status.toUpperCase()}</span>
                            </div>
                            <div className="flex justify-between text-gray-500">
                                <span>FROM: {bundle.source}</span>
                                <span>TO: {bundle.destination}</span>
                            </div>
                        </div>
                    )) : (
                        <p className="text-[10px] text-gray-600 text-center italic mt-4">No bundles in transit</p>
                    )}
                </div>
            </div>

            {/* Quantum Health */}
            <div className="pt-2 border-t border-white/10">
                <div className="flex justify-between items-center mb-1">
                    <span className="text-[9px] text-gray-400">QUANTUM ENTANGLEMENT STABILITY</span>
                    <span className="text-[9px] text-[#00ff00]">99.98%</span>
                </div>
                <div className="h-1 bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full bg-[#00ff00] w-[99.98%] animate-pulse"></div>
                </div>
            </div>
        </div>
      </div>
    </div>
  );
};

export default TemporalDashboard;
