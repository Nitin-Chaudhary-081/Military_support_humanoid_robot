"""Drone mesh logic — pure, testable."""
from dataclasses import dataclass
from typing import List
import math

@dataclass
class DroneState:
    id: int
    deployed: bool
    pos: List[float]  # x,y,z
    battery_pct: float
    link_quality: float  # 0-1

def mesh_status(drones: List[DroneState]) -> dict:
    active = [d for d in drones if d.deployed and d.battery_pct > 5]
    coverage_deg = 360 if len(active) >= 2 else 180 if len(active)==1 else 0
    # mesh link quality is min of active drones (weakest link)
    link = min((d.link_quality for d in active), default=0.0)
    return {"active": len(active), "total": len(drones), "coverage_deg": coverage_deg, "link_quality": round(link,2), "degraded": link < 0.5 if active else True}

def next_positions(threat_bearing_deg: float) -> List[List[float]]:
    # Two drones hold 60m radius, opposite sides biased toward threat — 360° coverage
    r = 60.0
    a1 = math.radians(threat_bearing_deg)
    a2 = math.radians((threat_bearing_deg + 180) % 360)
    return [[r*math.cos(a1), r*math.sin(a1), 35.0], [r*math.cos(a2), r*math.sin(a2), 35.0]]
