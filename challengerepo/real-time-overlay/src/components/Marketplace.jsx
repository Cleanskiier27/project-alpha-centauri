import React from 'react';
import { ShoppingCart, Package, Shield, Globe, Cpu, Zap } from 'lucide-react';

const Marketplace = () => {
    const items = [
        {
            id: 'sbir-payout',
            name: 'NASA SBIR Payout Package',
            description: 'Final documentation and technical deliverables for M2M milestones.',
            price: '$50,000,000',
            icon: <Package className="text-[#ffb400]" />,
            status: 'AVAILABLE'
        },
        {
            id: 'neural-sync',
            name: 'Preciseliens Neural Sync',
            description: 'Bi-directional telemetry cycles for multi-agent synchronization.',
            price: '2.5 ETH',
            icon: <Brain className="text-[#9d50bb]" />,
            status: 'ACTIVE'
        },
        {
            id: 'network-boost',
            name: 'NetworkBuster Suite V2',
            description: 'Advanced network path optimization and real-time monitoring.',
            price: '$9,999',
            icon: <Zap className="text-[#00f0ff]" />,
            status: 'READY'
        },
        {
            id: 'artemis-nav',
            name: 'Artemis Navigation Data',
            description: 'High-precision star tracking and trajectory data from NASA/ESA.',
            price: 'CONTRACT ONLY',
            icon: <Globe className="text-[#00ff9d]" />,
            status: 'RESTRICTED'
        }
    ];

    return (
        <div className="flex flex-col h-full gap-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white tracking-widest">PERSONALIZED MARKETPLACE</h2>
                    <p className="text-[#00f0ff]/60 text-sm">Welcome back, Andrew Middleton. Your custom procurement portal is active.</p>
                </div>
                <div className="glass-panel px-4 py-2 flex items-center gap-3">
                    <ShoppingCart className="text-[#00f0ff]" size={20} />
                    <span className="text-white font-mono">CREDITS: ∞</span>
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4 overflow-auto pb-4">
                {items.map((item) => (
                    <div key={item.id} className="glass-panel p-4 hover:border-[#00f0ff]/50 transition-colors group cursor-pointer">
                        <div className="flex justify-between items-start mb-4">
                            <div className="p-3 bg-white/5 rounded-lg group-hover:bg-[#00f0ff]/10 transition-colors">
                                {item.icon || <Cpu />}
                            </div>
                            <span className={`text-[10px] px-2 py-0.5 rounded border ${
                                item.status === 'AVAILABLE' ? 'border-[#00ff9d] text-[#00ff9d]' : 
                                item.status === 'RESTRICTED' ? 'border-[#ff4b2b] text-[#ff4b2b]' : 
                                'border-[#00f0ff] text-[#00f0ff]'
                            }`}>
                                {item.status}
                            </span>
                        </div>
                        <h3 className="text-white font-bold mb-1">{item.name}</h3>
                        <p className="text-gray-400 text-xs mb-4 line-clamp-2">{item.description}</p>
                        <div className="flex justify-between items-center mt-auto">
                            <span className="text-[#00f0ff] font-mono text-sm">{item.price}</span>
                            <button className="bg-[#00f0ff]/10 hover:bg-[#00f0ff]/20 text-[#00f0ff] text-[10px] font-bold px-3 py-1 rounded transition-colors uppercase">
                                Deploy
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-auto border-t border-white/10 pt-4 flex justify-between items-center text-[10px] text-gray-500">
                <div className="flex gap-4">
                    <span>LICENSE: PRECISELIENS-ENTERPRISE-2026</span>
                    <span>ORBITAL_ID: NB-7788-ALPHA</span>
                </div>
                <div className="text-[#00f0ff]">SYSTEMS NOMINAL</div>
            </div>
        </div>
    );
};

const Brain = ({ className }) => (
    <svg 
        xmlns="http://www.w3.org/2000/svg" 
        width="24" 
        height="24" 
        viewBox="0 0 24 24" 
        fill="none" 
        stroke="currentColor" 
        strokeWidth="2" 
        strokeLinecap="round" 
        strokeLinejoin="round" 
        className={className}
    >
        <path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .52 5.886 4 4 0 0 0 5.137 1.247L12 21l2.863-2.972a4 4 0 0 0 5.137-1.247 4 4 0 0 0 .52-5.886 4 4 0 0 0-2.526-5.77A3 3 0 1 0 12 5z" />
        <path d="M9 13a4.5 4.5 0 0 0 3-4" />
        <path d="M15 13a4.5 4.5 0 0 1-3-4" />
        <path d="M12 9v4" />
    </svg>
);

export default Marketplace;
