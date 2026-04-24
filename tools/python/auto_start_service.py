"""
NetworkBuster Auto-Start Service
Runs in background and auto-starts services on trigger events
"""

import os
import sys
import time
import subprocess
import psutil
from pathlib import Path
import ctypes

def is_admin():
    """Check if running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_port(port):
    """Check if port is in use"""
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.status == 'LISTEN':
            return True
    return False

def start_service(service_name, command, port):
    """Start a service if not already running"""
    if check_port(port):
        print(f"✅ {service_name} already running on port {port}")
        return True
    
    try:
        print(f"🚀 Starting {service_name}...")
        subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(2)
        
        if check_port(port):
            print(f"✅ {service_name} started successfully")
            return True
        else:
            print(f"⚠️  {service_name} may be starting...")
            return False
    except Exception as e:
        print(f"❌ Failed to start {service_name}: {e}")
        return False

def auto_start_all():
    """Automatically start all NetworkBuster services"""
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║  NetworkBuster Auto-Start Service                         ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    project_dir = Path(__file__).parent
    python_exe = project_dir / ".venv" / "Scripts" / "python.exe"
    
    services = [
        {
            'name': 'Web Server',
            'command': f'node "{project_dir}/server-universal.js"',
            'port': 3000,
            'delay': 0
        },
        {
            'name': 'API Server',
            'command': f'cd "{project_dir}/api" && node server-universal.js',
            'port': 3001,
            'delay': 2
        },
        {
            'name': 'Audio Stream',
            'command': f'node "{project_dir}/server-audio.js"',
            'port': 3002,
            'delay': 2
        },
        {
            'name': 'NetworkBuster AI',
            'command': f'"{python_exe}" "{project_dir}/networkbuster_ai.py"',
            'port': 4000,
            'delay': 2
        },
        {
            'name': 'Mission Control',
            'command': f'"{python_exe}" "{project_dir}/nasa_home_base.py"',
            'port': 5000,
            'delay': 2
        },
        {
            'name': 'Network Map',
            'command': f'"{python_exe}" "{project_dir}/network_map_viewer.py"',
            'port': 6000,
            'delay': 2
        },
        {
            'name': 'Universal Launcher',
            'command': f'"{python_exe}" "{project_dir}/universal_launcher.py"',
            'port': 7000,
            'delay': 2
        },
        {
            'name': 'API Tracer',
            'command': f'"{python_exe}" "{project_dir}/api_tracer.py"',
            'port': 8000,
            'delay': 2
        }
    ]
    
    started = 0
    for service in services:
        time.sleep(service['delay'])
        if start_service(service['name'], service['command'], service['port']):
            started += 1
    
    print(f"\n✅ Auto-start complete: {started}/{len(services)} services running")
    
    # Open dashboards after startup
    time.sleep(3)
    print("\n🌐 Opening Dashboards...")
    subprocess.Popen('start http://localhost:7000', shell=True)
    subprocess.Popen('start http://localhost:3000/control-panel', shell=True)
    
    return started

if __name__ == '__main__':
    # Check for admin if needed
    if len(sys.argv) > 1 and sys.argv[1] == '--admin' and not is_admin():
        print("⚠️  Requesting administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)
    
    auto_start_all()
    
    print("\n✨ Press Enter to exit...")
    input()
