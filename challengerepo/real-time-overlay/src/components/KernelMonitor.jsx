import React, { useState, useEffect } from 'react';
import { Activity, ShieldCheck, Zap, Server } from 'lucide-react';

const KernelMonitor = () => {
    const [telemetry, setTelemetry] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchTelemetry = async () => {
            try {
                // Use absolute path for development or relative for production proxy
                const res = await fetch('/api/kernel/telemetry');
                const data = await res.json();
                setTelemetry(data);
                setLoading(false);
            } catch (error) {
                console.error("Kernel telemetry fetch failed", error);
            }
        };

        const interval = setInterval(fetchTelemetry, 2000);
        fetchTelemetry();

        return () => clearInterval(interval);
    }, []);

    if (loading) return <div className="text-[10px] text-cyan-500 animate-pulse">CONNECTING TO KERNEL BRIDGE...</div>;

    return (
        <div className="flex flex-col gap-2 p-2 bg-black/40 rounded border border-white/5 font-mono">
            <div className="flex justify-between items-center border-b border-white/10 pb-1 mb-1">
                <div className="flex items-center gap-1">
                    <Activity size={12} className="text-[#00ff9d]" />
                    <span className="text-[10px] font-bold text-[#00ff9d]">KERNEL_ID: {telemetry.kernel.kernel_version}</span>
                </div>
                <span className="text-[9px] text-gray-500">{telemetry.cleanskiier_sync}</span>
            </div>

            <div className="grid grid-cols-2 gap-2">
                <div className="flex flex-col">
                    <span className="text-[8px] text-gray-400">THOUGHT_PROCESS</span>
                    <span className="text-[9px] text-cyan-400 truncate">{telemetry.kernel.thought_process}</span>
                </div>
                <div className="flex flex-col text-right">
                    <span className="text-[8px] text-gray-400">UPTIME</span>
                    <span className="text-[9px] text-white">{telemetry.kernel.uptime}s</span>
                </div>
            </div>

            <div className="mt-1">
                <div className="flex justify-between text-[8px] mb-1">
                    <span>KERNEL_LOAD</span>
                    <span>{telemetry.system.cpu_usage}%</span>
                </div>
                <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                    <div 
                        className="h-full bg-[#00ff9d] transition-all duration-500" 
                        style={{ width: `${telemetry.system.cpu_usage}%` }}
                    ></div>
                </div>
            </div>

            <div className="flex gap-2 mt-1">
                <div className="flex items-center gap-1 px-1.5 py-0.5 rounded bg-white/5 border border-white/10">
                    <ShieldCheck size={8} className="text-purple-400" />
                    <span className="text-[8px] text-purple-400">{telemetry.kernel.security_level}</span>
                </div>
                <div className="flex items-center gap-1 px-1.5 py-0.5 rounded bg-white/5 border border-white/10">
                    <Zap size={8} className="text-yellow-400" />
                    <span className="text-[8px] text-yellow-400">{telemetry.kernel.status}</span>
                </div>
            </div>
        </div>
    );
};

export default KernelMonitor;
