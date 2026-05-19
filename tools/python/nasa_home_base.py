#!/usr/bin/env python3
"""
NASA Home Base Mission Control
NetworkBuster Integration Package - Fleet Strategy Edition
"""

import sys
import time
import json
import requests
import subprocess
import webbrowser
import threading
from datetime import datetime
from pathlib import Path

# Check for required packages
try:
    from flask import Flask, render_template_string, jsonify, request
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("⚠️  Flask not available. Install with: pip install flask")

class NASAHomeBase:
    """NASA Home Base Mission Control System"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.ports = {
            'web': {'port': 3000, 'name': 'Web Server', 'status': 'offline'},
            'api': {'port': 3001, 'name': 'API Server', 'status': 'offline'},
            'audio': {'port': 3002, 'name': 'Audio Stream', 'status': 'offline'},
            'mission': {'port': 5000, 'name': 'Mission Control', 'status': 'offline'},
            'map': {'port': 6000, 'name': 'Network Map', 'status': 'offline'},
            'launcher': {'port': 7000, 'name': 'Universal Launcher', 'status': 'offline'},
            'tracer': {'port': 8000, 'name': 'API Tracer', 'status': 'offline'}
        }
        self.artemis_status = {
            'mission': 'Artemis II',
            'status': 'Nominal',
            'phase': 'Lunar Insertion',
            'crew': ['Cmdr. Network', 'Pilot Buster'],
            'fuel': '85%',
            'velocity': '3.2 km/s'
        }
        self.mission_start_time = datetime.now()
        self.mission_log = []
        
    def get_artemis_data(self):
        """Get Artemis mission data"""
        return self.artemis_status

    def log_event(self, event, level='INFO'):
        """Log mission event"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {level}: {event}"
        self.mission_log.append(log_entry)
        print(f"  {log_entry}")
        
    def check_port_status(self, port):
        """Check if a port is active"""
        try:
            response = requests.get(f'http://localhost:{port}/api/health', timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def check_all_ports(self):
        """Check status of all NetworkBuster ports"""
        for service, info in self.ports.items():
            is_active = self.check_port_status(info['port'])
            info['status'] = 'online' if is_active else 'offline'
            
    def open_dashboard(self, service='web'):
        """Open service dashboard in browser"""
        port = self.ports[service]['port']
        url = f'http://localhost:{port}'
        self.log_event(f"Opening {service} dashboard: {url}", 'ACTION')
        webbrowser.open(url)
        
    def get_system_status(self):
        """Get comprehensive system status"""
        self.check_all_ports()
        
        online_count = sum(1 for p in self.ports.values() if p['status'] == 'online')
        uptime = (datetime.now() - self.mission_start_time).total_seconds()
        
        return {
            'mission_time': uptime,
            'ports': self.ports,
            'online_services': online_count,
            'total_services': len(self.ports),
            'status': 'NOMINAL' if online_count == len(self.ports) else 'DEGRADED'
        }

if FLASK_AVAILABLE:
    app = Flask(__name__)
    home_base = NASAHomeBase()
    
    @app.route('/api/residents/collective')
    def api_residents_collective():
        from resident_strategy_engine import StrategicWealthManager
        manager = StrategicWealthManager()
        return jsonify(manager.get_collective_telemetry())

    @app.route('/api/mission/path', methods=['POST'])
    def api_mission_path():
        try:
            from mission_control_engine import engine as mc_engine
            data = request.json or {}
            origin = data.get('origin', 'sol')
            destination = data.get('destination', 'proxima')
            speed = float(data.get('speed', 0.5))
            
            result = mc_engine.calculate_interstellar_path(origin, destination, speed)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    MISSION_CONTROL_HTML = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>NASA Mission Control | Fleet Strategy | OLED-ISO-MC</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;900&display=swap');
            
            :root { 
                --bg: #000000; /* PURE OLED BLACK */
                --neon-blue: #00d4ff; 
                --neon-green: #00ff88; 
                --neon-orange: #ffaa00; 
                --neon-purple: #bc13fe; 
                --mc-border: #333333;
                --mc-button-bg: #1a1a1a;
            }
            
            body { 
                background: var(--bg);
                color: #ffffff; 
                font-family: 'Inter', sans-serif; 
                margin: 0; 
                padding: 40px; 
                overflow-x: hidden;
            }

            .glass { 
                background: rgba(10, 10, 10, 0.95); 
                border: 2px solid #222; 
                box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.05);
                border-radius: 0;
                padding: 35px; 
                position: relative;
            }

            .mc-button {
                background: var(--mc-button-bg);
                border: 4px solid #000;
                border-top-color: #444;
                border-left-color: #444;
                border-bottom-color: #111;
                border-right-color: #111;
                color: #fff;
                font-family: 'Press Start 2P', cursive;
                font-size: 11px;
                padding: 18px;
                cursor: pointer;
                text-shadow: 2px 2px #000;
                width: 100%;
                image-rendering: pixelated;
                transition: transform 0.1s;
            }
            .mc-button:hover { background: #2a2a2a; border-top-color: #555; border-left-color: #555; }
            .mc-button:active { transform: scale(0.98); border-color: #111 #444 #444 #111; }

            .header { 
                display: flex; 
                justify-content: space-between; 
                align-items: center; 
                margin-bottom: 45px; 
                border: 4px solid var(--neon-blue); 
                padding: 30px 40px;
                background: #000;
                box-shadow: 0 0 35px rgba(0, 212, 255, 0.15);
            }

            .header h2 {
                font-family: 'Press Start 2P', cursive;
                font-size: 18px;
                text-shadow: 4px 4px #000;
                margin: 0;
                color: var(--neon-blue);
                letter-spacing: 2px;
            }

            .mission-grid { display: grid; grid-template-columns: 420px 1fr 420px; gap: 40px; min-height: calc(100vh - 250px); }
            
            .telemetry-card { 
                margin-bottom: 30px; 
                border-left: 10px solid var(--neon-green);
                background: rgba(0, 255, 136, 0.01);
            }

            .stat-val { 
                font-size: 3rem; 
                font-weight: 900; 
                color: var(--neon-green); 
                font-family: 'Inter', sans-serif;
                text-shadow: 0 0 25px rgba(0, 255, 136, 0.2);
            }

            .stat-label { 
                font-family: 'Press Start 2P', cursive;
                font-size: 10px; 
                color: #555; 
                text-transform: uppercase; 
                margin-bottom: 15px;
                letter-spacing: 3px;
            }

            .map-container { 
                width: 100%; 
                height: 100%; 
                position: relative; 
                background: #000;
                border: 4px solid #1a1a1a;
                overflow: hidden; 
                display: flex; 
                flex-direction: column; 
            }

            .log-box { 
                height: 100%; 
                overflow-y: auto; 
                font-family: 'Inter', sans-serif; 
                font-size: 0.95rem; 
                color: #777; 
                background: #000; 
                padding: 25px;
            }

            .resident-card {
                padding: 25px;
                border: 4px solid #222;
                margin-bottom: 25px;
                background: #050505;
                transition: border-color 0.3s;
            }
            .resident-card:hover { border-color: var(--neon-blue); }
            .resident-card h3 { font-family: 'Press Start 2P'; font-size: 14px; color: var(--neon-blue); margin-top: 0; margin-bottom: 15px; }
            .strat-tag { font-family: 'Press Start 2P'; font-size: 9px; padding: 8px 12px; background: var(--neon-purple); color: #fff; margin-bottom: 15px; display: inline-block; }

            ::-webkit-scrollbar { width: 10px; }
            ::-webkit-scrollbar-track { background: #000; }
            ::-webkit-scrollbar-thumb { background: #1a1a1a; }
            ::-webkit-scrollbar-thumb:hover { background: #222; }
        </style>
    </head>
    <body>
        <div class="header">
            <h2>🛰️ NETWORKBUSTER // FLEET_STRATEGY_4D</h2>
            <div id="clock" style="font-family: 'Press Start 2P'; font-size: 12px; color: var(--neon-orange);">00:00:00 UTC</div>
        </div>
        <div class="mission-grid">
            <div class="sidebar">
                <div class="glass telemetry-card">
                    <div class="stat-label">System Phase</div>
                    <div class="stat-val" id="phase" style="color: var(--neon-blue);">FLEET_SYNC</div>
                </div>
                <button class="mc-button" onclick="loadFleet()" style="margin-bottom: 30px;">REFRESH_FLEET_DATA</button>
                
                <div class="glass" style="border-color: var(--neon-orange); padding: 25px;">
                    <h4 style="font-family: 'Press Start 2P'; font-size: 10px; color: var(--neon-orange); margin-top: 0; margin-bottom: 25px;">TARGET_SITE_SCAN</h4>
                    <div style="width: 100%; height: 250px; border: 4px solid #1a1a1a; background: #000; overflow: hidden;">
                        <iframe 
                            width="100%" 
                            height="100%" 
                            frameborder="0" 
                            style="border:0; filter: invert(90%) hue-rotate(180deg) brightness(0.8) contrast(1.2);" 
                            src="https://www.google.com/maps?q=324+Fir+Dr&output=embed" 
                            allowfullscreen>
                        </iframe>
                    </div>
                    <div class="stat-label" style="margin-top: 20px; color: var(--neon-orange);">LOC: 324 FIR DR</div>
                </div>
            </div>
            
            <div class="map-container">
                <div id="fleet-telemetry" style="padding: 40px; background: #000; height: 100%; overflow-y: auto;">
                    <div class="stat-label" style="color: #333; margin-bottom: 35px; font-size: 12px;">COLLECTIVE_RESIDENT_FLEET_TELEMETRY</div>
                    <div id="resident-grid"></div>
                </div>
            </div>
            
            <div class="sidebar">
                <div class="glass" style="height: calc(100% - 80px); border-right: 10px solid var(--neon-purple);">
                    <div class="stat-label" style="margin-bottom: 25px;">Strategy Log</div>
                    <div id="logs" class="log-box"></div>
                </div>
            </div>
        </div>
        <script>
            function updateClock() {
                document.getElementById('clock').textContent = new Date().toISOString().split('T')[1].split('.')[0] + ' UTC';
            }
            function addLog(m) {
                const l = document.getElementById('logs');
                const e = document.createElement('div');
                e.style.padding = '12px 0';
                e.style.borderBottom = '1px solid #111';
                e.innerHTML = `<span style="color: #333">[${new Date().toLocaleTimeString()}]</span> <span style="color: var(--neon-blue)">STRAT_</span> ${m}`;
                l.prepend(e);
            }
            async function loadFleet() {
                addLog(`SCANNING_RESIDENT_COORDINATES...`);
                try {
                    const resp = await fetch('/api/residents/collective');
                    const data = await resp.json();
                    
                    const grid = document.getElementById('resident-grid');
                    grid.innerHTML = '';
                    
                    data.forEach(report => {
                        const card = document.createElement('div');
                        card.className = 'resident-card';
                        card.innerHTML = `
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <div>
                                    <h3>${report.resident.name}</h3>
                                    <span class="strat-tag">${report.strategic_maneuver.title}</span>
                                </div>
                                <div style="text-align: right;">
                                    <div class="stat-label" style="margin-bottom: 8px;">Altitude</div>
                                    <div style="color: var(--neon-green); font-weight: 900; font-size: 1.5rem;">${report.resident.percentile}%</div>
                                </div>
                            </div>
                            <div style="margin: 20px 0; color: #888; font-size: 0.95rem; line-height: 1.6;">
                                <strong style="color: #fff">Terrain:</strong> ${report.current_terrain}<br>
                                <strong style="color: #fff">Maneuver:</strong> ${report.strategic_maneuver.maneuver}
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid #222; padding-top: 20px; margin-top: 10px;">
                                <div>
                                    <div class="stat-label" style="margin-bottom: 8px;">10Y Outlook</div>
                                    <div style="color: var(--neon-blue); font-weight: 900; font-size: 1.8rem;">$${report['10_year_outlook'].toLocaleString()}</div>
                                </div>
                                <div style="color: var(--neon-orange); font-size: 0.8rem; font-family: 'Press Start 2P';">THRUST_REQ: ${report.strategic_maneuver.required_thrust}G</div>
                            </div>
                        `;
                        grid.appendChild(card);
                    });
                    
                    addLog(`FLEET_SYNC_COMPLETE: ${data.length} RESIDENTS_TRACKED`);
                } catch (e) {
                    addLog(`SYNC_FAILURE: ${e.message.toUpperCase()}`);
                }
            }
            setInterval(updateClock, 1000);
            loadFleet();
            addLog('FLEET_ENGINE_ONLINE');
            addLog('OLED_MC_REFINED_SYNC');
        </script>
    </body>
    </html>
    """
    
    @app.route('/')
    def index():
        return render_template_string(MISSION_CONTROL_HTML)
    
    @app.route('/api/status')
    def api_status():
        return jsonify(home_base.get_system_status())

    @app.route('/api/artemis/status')
    def artemis_status():
        return jsonify(home_base.get_artemis_data())
    
    @app.route('/api/open/<service>')
    def api_open_service(service):
        if service in home_base.ports:
            home_base.open_dashboard(service)
            return jsonify({'success': True, 'message': f'Opened {service} dashboard'})
        return jsonify({'success': False, 'message': 'Service not found'}), 404

def run_mission_control(port=5000):
    if not FLASK_AVAILABLE:
        return
    
    print("\n" + "="*60)
    print("🚀 NASA HOME BASE MISSION CONTROL // FLEET STRATEGY EDITION")
    print("="*60)
    
    home_base.check_all_ports()
    threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        pass

def main():
    port = 5000
    if len(sys.argv) > 2 and sys.argv[1] == '--port':
        port = int(sys.argv[2])
    run_mission_control(port)

if __name__ == "__main__":
    main()
