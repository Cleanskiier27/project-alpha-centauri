#!/usr/bin/env python3
"""
NetworkBuster Mission Runner
Complete system simulation demonstrating all integrated capabilities
"""

import sys
import time
import subprocess
import platform
from pathlib import Path
from datetime import datetime

# Import available modules
try:
    from security_verification import UserVerification, SecurityLevel
    SECURITY_AVAILABLE = True
except ImportError:
    SECURITY_AVAILABLE = False
    print("⚠️  Security module unavailable")

try:
    from drone_flight_system import DroneState, UnbreakableAutopilot, ScanAlgorithms
    DRONE_AVAILABLE = True
except ImportError:
    DRONE_AVAILABLE = False
    print("⚠️  Drone system unavailable")

try:
    from system_health import SystemHealthMonitor
    HEALTH_AVAILABLE = True
except ImportError:
    HEALTH_AVAILABLE = False
    print("⚠️  Health monitor unavailable")


class NetworkBusterMission:
    """Complete NetworkBuster mission orchestrator."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.mission_status = "INITIALIZING"
        self.mission_log = []
        self.authenticated_user = None
        self.security_level = 0
        
    def log_event(self, event, status="INFO"):
        """Log mission event."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {status}: {event}"
        self.mission_log.append(log_entry)
        
        if status == "ERROR":
            print(f"❌ {event}")
        elif status == "SUCCESS":
            print(f"✅ {event}")
        elif status == "WARNING":
            print(f"⚠️  {event}")
        else:
            print(f"ℹ️  {event}")
    
    def print_header(self, title):
        """Print formatted section header."""
        print("\n" + "═" * 70)
        print(f"  {title}")
        print("═" * 70)
    
    def run_phase_1_authentication(self):
        """Phase 1: Security & Authentication."""
        self.print_header("PHASE 1: SECURITY & AUTHENTICATION")
        
        if not SECURITY_AVAILABLE:
            self.log_event("Security module not available, running in open mode", "WARNING")
            return True
        
        print("\n🔐 Initiating secure authentication...")
        verifier = UserVerification()
        
        # Check for existing session
        session = verifier.load_session()
        
        if not session:
            print("No active session found. Authenticating as admin...")
            success, session = verifier.authenticate(
                username="admin",
                password="admin123",
                interactive=False
            )
            
            if not success:
                self.log_event("Authentication failed", "ERROR")
                return False
        
        self.authenticated_user = session['username']
        self.security_level = session['level']
        
        self.log_event(f"Authenticated as {self.authenticated_user} (Level {self.security_level})", "SUCCESS")
        
        # Verify operator clearance
        if not verifier.require_level(SecurityLevel.OPERATOR):
            self.log_event("Insufficient clearance for mission operations", "ERROR")
            return False
        
        self.log_event("Security clearance verified", "SUCCESS")
        return True
    
    def run_phase_2_system_check(self):
        """Phase 2: System Health & Environment Check."""
        self.print_header("PHASE 2: SYSTEM HEALTH CHECK")
        
        # Platform info
        system_info = {
            "Platform": platform.system(),
            "Version": platform.version(),
            "Architecture": platform.machine(),
            "Python": platform.python_version(),
            "Processor": platform.processor(),
        }
        
        print("\n🖥️  System Information:")
        for key, value in system_info.items():
            print(f"  {key}: {value}")
        
        self.log_event(f"Running on {system_info['Platform']} {system_info['Architecture']}", "SUCCESS")
        
        # Check Node.js availability
        print("\n🔍 Checking Node.js installation...")
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                node_version = result.stdout.strip()
                print(f"  ✓ Node.js {node_version} detected")
                self.log_event(f"Node.js {node_version} available", "SUCCESS")
            else:
                self.log_event("Node.js not found", "WARNING")
        except Exception as e:
            self.log_event(f"Node.js check failed: {e}", "WARNING")
        
        # Check Python environment
        print("\n🐍 Python Environment:")
        print(f"  Python: {sys.version}")
        print(f"  Executable: {sys.executable}")
        
        # Check critical modules
        modules = ["pathlib", "subprocess", "platform", "datetime"]
        print("\n📦 Module Status:")
        for module in modules:
            try:
                __import__(module)
                print(f"  ✓ {module}")
            except ImportError:
                print(f"  ✗ {module} (missing)")
        
        self.log_event("System health check completed", "SUCCESS")
        return True
    
    def run_phase_3_drone_operations(self):
        """Phase 3: Autonomous Drone Operations."""
        self.print_header("PHASE 3: DRONE FLIGHT OPERATIONS")
        
        if not DRONE_AVAILABLE:
            self.log_event("Drone system not available", "WARNING")
            return True
        
        print("\n🚁 Initializing autonomous drone system...")
        time.sleep(1)
        
        # Create drone fleet
        drones = []
        for i, drone_id in enumerate(["ALPHA-1", "BETA-2"], 1):
            drone = DroneState(drone_id=drone_id)
            drones.append(drone)
            print(f"  ✓ Drone {drone_id} initialized")
        
        self.log_event(f"Initialized {len(drones)} drone units", "SUCCESS")
        
        # Mission 1: Reconnaissance
        print("\n📡 MISSION 1: Reconnaissance Spiral Scan")
        print("-" * 70)
        drone1 = drones[0]
        autopilot1 = UnbreakableAutopilot(drone1)
        
        path1 = ScanAlgorithms.generate_spiral_search(0, 0, 40, spacing=10.0)
        print(f"Generated {len(path1)} waypoints for recon pattern")
        autopilot1.execute_pattern("RECON_SPIRAL", path1[:10])  # Execute 10 waypoints
        
        self.log_event(f"Drone {drone1.id} completed reconnaissance", "SUCCESS")
        
        time.sleep(1)
        
        # Mission 2: Detailed Mapping
        print("\n🗺️  MISSION 2: Grid Mapping Scan")
        print("-" * 70)
        drone2 = drones[1] if len(drones) > 1 else drones[0]
        drone2.battery = 100.0
        drone2.integrity = 100.0
        autopilot2 = UnbreakableAutopilot(drone2)
        
        path2 = ScanAlgorithms.generate_grid_raster(40, 40, altitude=18.0, density=12.0)
        print(f"Generated {len(path2)} waypoints for grid pattern")
        autopilot2.execute_pattern("GRID_MAP", path2[:8])  # Execute 8 waypoints
        
        self.log_event(f"Drone {drone2.id} completed mapping mission", "SUCCESS")
        
        # Fleet status
        print("\n" + "─" * 70)
        print("  FLEET STATUS REPORT")
        print("─" * 70)
        for drone in drones:
            print(f"\n  {drone.id}:")
            print(f"    Battery: {drone.battery:.1f}%")
            print(f"    Integrity: {drone.integrity}%")
            print(f"    Status: {drone.status}")
            print(f"    Position: ({drone.position['x']:.1f}, {drone.position['y']:.1f}, {drone.position['z']:.1f})")
        
        self.log_event("All drone operations completed successfully", "SUCCESS")
        return True
    
    def run_phase_4_network_monitoring(self):
        """Phase 4: Network & Port Monitoring."""
        self.print_header("PHASE 4: NETWORK MONITORING")
        
        print("\n🔌 Checking NetworkBuster server ports...")
        
        ports = [
            (3000, "Web Server"),
            (3001, "API Server"),
            (3002, "Audio Stream")
        ]
        
        for port, name in ports:
            if platform.system() == "Windows":
                result = subprocess.run([
                    "powershell", "-Command",
                    f"Get-NetTCPConnection -LocalPort {port} -State Listen -ErrorAction SilentlyContinue"
                ], capture_output=True, text=True)
                is_active = bool(result.stdout.strip())
            else:
                result = subprocess.run(
                    f"ss -tlnp 2>/dev/null | grep :{port} || netstat -tlnp 2>/dev/null | grep :{port}",
                    shell=True, capture_output=True, text=True
                )
                is_active = bool(result.stdout.strip())
            
            status = "🟢 ACTIVE" if is_active else "⚪ INACTIVE"
            print(f"  Port {port} ({name}): {status}")
            
            if is_active:
                self.log_event(f"{name} (:{port}) is running", "SUCCESS")
            else:
                self.log_event(f"{name} (:{port}) is not running", "WARNING")
        
        return True
    
    def run_phase_5_data_collection(self):
        """Phase 5: Data Collection & Analysis."""
        self.print_header("PHASE 5: DATA COLLECTION & ANALYSIS")
        
        print("\n📊 Collecting mission telemetry...")
        
        # Simulated data collection
        data_points = {
            "Total Mission Duration": f"{(datetime.now() - self.start_time).total_seconds():.1f}s",
            "Log Entries": len(self.mission_log),
            "Security Level": self.security_level,
            "Authenticated User": self.authenticated_user or "N/A",
            "Platform": platform.system(),
            "Python Version": platform.python_version(),
        }
        
        print("\n📈 Mission Metrics:")
        for key, value in data_points.items():
            print(f"  {key}: {value}")
        
        self.log_event("Data collection completed", "SUCCESS")
        return True
    
    def generate_mission_report(self):
        """Generate final mission report."""
        self.print_header("MISSION COMPLETE - FINAL REPORT")
        
        duration = (datetime.now() - self.start_time).total_seconds()
        
        print(f"\n⏱️  Mission Duration: {duration:.2f} seconds")
        print(f"📋 Total Events: {len(self.mission_log)}")
        
        # Count event types
        success_count = sum(1 for log in self.mission_log if "SUCCESS" in log)
        warning_count = sum(1 for log in self.mission_log if "WARNING" in log)
        error_count = sum(1 for log in self.mission_log if "ERROR" in log)
        
        print(f"\n📊 Event Summary:")
        print(f"  ✅ Success: {success_count}")
        print(f"  ⚠️  Warning: {warning_count}")
        print(f"  ❌ Error: {error_count}")
        
        print(f"\n📝 Mission Log:")
        print("─" * 70)
        for log in self.mission_log:
            print(f"  {log}")
        
        # Final status
        if error_count == 0:
            self.mission_status = "COMPLETED - ALL SYSTEMS NOMINAL"
            print(f"\n🎯 Status: {self.mission_status}")
        elif error_count < 3:
            self.mission_status = "COMPLETED WITH WARNINGS"
            print(f"\n⚠️  Status: {self.mission_status}")
        else:
            self.mission_status = "COMPLETED WITH ERRORS"
            print(f"\n❌ Status: {self.mission_status}")
        
        print("\n" + "═" * 70)
        print("  NETWORKBUSTER MISSION TERMINATED")
        print("═" * 70)
    
    def execute_full_mission(self):
        """Execute complete mission sequence."""
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + "  NETWORKBUSTER INTEGRATED MISSION SEQUENCE".center(68) + "║")
        print("║" + f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(68) + "║")
        print("╚" + "═" * 68 + "╝")
        
        self.mission_status = "IN PROGRESS"
        
        try:
            # Phase 1: Authentication
            if not self.run_phase_1_authentication():
                self.log_event("Mission aborted - authentication failure", "ERROR")
                return False
            
            time.sleep(1)
            
            # Phase 2: System Check
            if not self.run_phase_2_system_check():
                self.log_event("Mission aborted - system check failure", "ERROR")
                return False
            
            time.sleep(1)
            
            # Phase 3: Drone Operations
            if not self.run_phase_3_drone_operations():
                self.log_event("Drone operations failed", "WARNING")
            
            time.sleep(1)
            
            # Phase 4: Network Monitoring
            if not self.run_phase_4_network_monitoring():
                self.log_event("Network monitoring incomplete", "WARNING")
            
            time.sleep(1)
            
            # Phase 5: Data Collection
            if not self.run_phase_5_data_collection():
                self.log_event("Data collection incomplete", "WARNING")
            
            # Final Report
            self.generate_mission_report()
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️  MISSION INTERRUPTED BY USER")
            self.mission_status = "ABORTED"
            self.log_event("Mission manually aborted", "WARNING")
            return False
            
        except Exception as e:
            print(f"\n\n❌ CRITICAL ERROR: {e}")
            self.mission_status = "FAILED"
            self.log_event(f"Mission failed: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    mission = NetworkBusterMission()
    mission.execute_full_mission()


if __name__ == "__main__":
    main()
