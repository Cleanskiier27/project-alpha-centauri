"""
Wealth Megastructure - Economic Physics Engine
Models the 'Wealth Mountain' as a literal megastructure with varying physical laws
based on the 2022 Survey of Consumer Finances (SCF) data.
"""

import math
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class TerrainNode:
    name: str
    elevation_range: tuple # (min_percentile, max_percentile)
    gravity_factor: float  # Affects debt-drag and mobility
    friction: float        # Affects compounding efficiency
    atmospheric_pressure: float # Affects volatility and risk-insulation
    median_net_worth: float

class WealthPhysicsEngine:
    """Realistic simulation of economic physics within the Megastructure"""
    
    TERRAINS = {
        "BASIN": TerrainNode(
            name="The Shallow Basin (Bottom 25%)",
            elevation_range=(0, 25),
            gravity_factor=2.5,   # Heavy debt gravity
            friction=0.9,         # High friction (fees, high interest)
            atmospheric_pressure=0.2, # Low insulation from shocks
            median_net_worth=3500.0   # Approximate median for this quartile
        ),
        "PLATEAU": TerrainNode(
            name="The Middle Plateau (25-75%)",
            elevation_range=(25, 75),
            gravity_factor=1.0,   # Standard gravity
            friction=0.5,         # Moderate friction (mortgages, standard rates)
            atmospheric_pressure=1.0, # Standard insulation
            median_net_worth=192900.0 # SCF 2022 Median
        ),
        "RIDGE": TerrainNode(
            name="The Upper Ridge (75-90%)",
            elevation_range=(75, 90),
            gravity_factor=0.5,   # Reduced gravity (access to credit/leverage)
            friction=0.2,         # Low friction (preferred rates, tax strategies)
            atmospheric_pressure=5.0, # High insulation (buffers)
            median_net_worth=793100.0 # SCF 2022 Median for 75-90%
        ),
        "PEAK": TerrainNode(
            name="The Vertical Wall (Top 1-10%)",
            elevation_range=(90, 100),
            gravity_factor=0.1,   # Near-zero gravity (capital-flight capability)
            friction=0.01,        # Frictionless (compounding as a physics engine)
            atmospheric_pressure=20.0, # Total insulation
            median_net_worth=3790000.0 # SCF 2022 Median for Top 10%
        )
    }

    @staticmethod
    def get_terrain_for_percentile(percentile: float) -> TerrainNode:
        if percentile < 25: return WealthPhysicsEngine.TERRAINS["BASIN"]
        if percentile < 75: return WealthPhysicsEngine.TERRAINS["PLATEAU"]
        if percentile < 90: return WealthPhysicsEngine.TERRAINS["RIDGE"]
        return WealthPhysicsEngine.TERRAINS["PEAK"]

    def calculate_compounding_vector(self, net_worth: float, percentile: float, rate: float, time_steps: int) -> Dict:
        """
        Calculates how wealth evolves based on local terrain physics.
        :param net_worth: Current capital
        :param percentile: Position on the mountain
        :param rate: Base return rate (e.g. 0.07 for 7%)
        :param time_steps: Years to simulate
        """
        terrain = self.get_terrain_for_percentile(percentile)
        
        # Physics modifiers
        effective_rate = rate * (1 - terrain.friction)
        drag = terrain.gravity_factor * 0.02 # Base drag per year
        
        # Volatility impact (Inverse of pressure)
        volatility_risk = (1.0 / terrain.atmospheric_pressure) * 0.1
        
        history = []
        current_wealth = net_worth
        
        for t in range(time_steps):
            # The Compounding Engine
            growth = current_wealth * effective_rate
            # The Gravity Engine (Debt/Maintenance/Expenses)
            maintenance_drag = current_wealth * drag
            
            # Net change
            current_wealth += (growth - maintenance_drag)
            
            # Random shock potential based on pressure
            if terrain.atmospheric_pressure < 1.0 and t % 5 == 0:
                shock = current_wealth * volatility_risk
                current_wealth -= shock # The Basin's "Broken Transmission" effect
            
            history.append(round(current_wealth, 2))
            
        return {
            "terrain": terrain.name,
            "final_wealth": round(current_wealth, 2),
            "effective_annual_yield": round(((current_wealth/net_worth)**(1/time_steps)-1)*100, 2) if net_worth > 0 else 0,
            "physics_metrics": {
                "gravity_drag": round(drag * 100, 2),
                "friction_loss": round(terrain.friction * 100, 2),
                "insulation_level": terrain.atmospheric_pressure
            },
            "projection": history
        }

    def simulate_mobility_climb(self, start_percentile: float, effort_factor: float, years: int) -> Dict:
        """
        Simulates the difficulty of moving between terrains.
        """
        current_p = start_percentile
        path = [current_p]
        
        for _ in range(years):
            terrain = self.get_terrain_for_percentile(current_p)
            # The steeper the terrain, the more effort required to increase percentile
            climb_difficulty = 1.0 + (current_p / 10.0) * terrain.gravity_factor
            
            progress = (effort_factor / climb_difficulty)
            current_p = min(99.9, current_p + progress)
            path.append(round(current_p, 2))
            
        return {
            "start_percentile": start_percentile,
            "end_percentile": round(current_p, 2),
            "terrain_reached": self.get_terrain_for_percentile(current_p).name,
            "mobility_path": path
        }

if __name__ == "__main__":
    engine = WealthPhysicsEngine()
    
    print("--- Wealth Megastructure Physics Report ---")
    
    # Compare a Basin dweller vs a Peak dweller with the same base return
    basin_sim = engine.calculate_compounding_vector(10000, 10, 0.07, 20)
    peak_sim = engine.calculate_compounding_vector(10000, 95, 0.07, 20)
    
    print(f"Basin Simulation (10k, 20yrs): ${basin_sim['final_wealth']} (Yield: {basin_sim['effective_annual_yield']}%)")
    print(f"Peak Simulation (10k, 20yrs):  ${peak_sim['final_wealth']} (Yield: {peak_sim['effective_annual_yield']}%)")
    
    climb = engine.simulate_mobility_climb(10, 1.0, 30)
    print(f"Mobility Climb (30yrs from 10th percentile): End at {climb['end_percentile']}th percentile")
