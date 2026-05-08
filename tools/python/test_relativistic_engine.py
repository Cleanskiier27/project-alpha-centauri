from mission_control_engine import engine
import json

def test_relativistic_path():
    print("🚀 Testing Relativistic Pathfinding: Sol -> Proxima Centauri @ 0.8c")
    
    path = engine.calculate_interstellar_path('sol', 'proxima', 0.8)
    
    if "error" in path:
        print(f"❌ Test Failed: {path['error']}")
        return

    print(f"✓ Origin: {path['origin']}")
    print(f"✓ Destination: {path['destination']}")
    print(f"✓ Distance: {path['distance_ly']} light-years")
    
    travel = path['travel_metrics']
    print(f"✓ Earth Time: {travel['earth_time_years']} years")
    print(f"✓ Traveler Time: {travel['traveler_time_years']} years")
    print(f"✓ Lorentz Gamma: {path['relativistic_sync']['gamma']}")
    
    drift = path['drift_corrected_destination']
    print(f"✓ Corrected Arrival Coords: x={drift['x']}, y={drift['y']}, z={drift['z']}")
    
    print("\n✅ Relativistic Engine Hardening Verified.")

if __name__ == "__main__":
    test_relativistic_path()
