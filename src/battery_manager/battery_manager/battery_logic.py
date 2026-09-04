"""
Battery drain model — pure, testable. 48kWh pack, 450kg walker.
Power = base + locomotion + compute + weapons
goal.md:84 45-90min full-combat; solid-state +8%/yr.
"""
from dataclasses import dataclass

@dataclass
class Load:
    walking: bool = True
    velocity_ms: float = 1.2  # biped avg
    compute_w: float = 180.0  # Jetson Orin ~60W + sensors + comms + drone link ~120W
    firing: bool = False
    shield_deployed: bool = False
    drones_active: int = 0

def power_watts(load: Load) -> float:
    # Realistic 450kg hydraulic biped: ~20-35kW total draw.
    # goal.md:84 claims 48kWh -> 45-90min (32-64kW). Model targets 28-38kW full-combat.
    base = 1800.0  # hotel load: pumps, cooling, Jetson idle, comms
    loco = 0.0
    if load.walking:
        # Hydraulic biped scaling: ~8kW static + 14kW per m/s (450kg vs Unitree H1 ~47kg)
        loco = 8200.0 + 14000.0 * load.velocity_ms
    compute = load.compute_w + (load.drones_active * 120.0)  # drone video link + relay
    weapons = 1800.0 if load.firing else 0.0  # recoil compensation + turret
    shield = 400.0 if load.shield_deployed else 0.0  # actuator hold + gyro
    return base + loco + compute + weapons + shield

def endurance_minutes(capacity_kwh: float, load: Load) -> float:
    p = power_watts(load)
    if p <= 0: return 0.0
    return (capacity_kwh * 1000.0 / p) * 60.0

def solid_state_projection(capacity_kwh: float, years: int, rate: float = 0.08) -> float:
    return capacity_kwh * ((1 + rate) ** years)

def soc_after_minutes(start_soc_pct: float, capacity_kwh: float, load: Load, minutes: float) -> float:
    drain_kwh = power_watts(load) * (minutes / 60.0) / 1000.0
    drain_pct = (drain_kwh / capacity_kwh) * 100.0
    return max(0.0, start_soc_pct - drain_pct)
