"""Shield deploy logic — pure, testable. Pivot 0=stowed back, 1.57=deployed forward."""
from dataclasses import dataclass

STOWED = 0.0
DEPLOYED = 1.57
THRESH_DEPLOY = 2  # threat level >=2 deploys
THRESH_RETRACT = 1 # threat <1 retracts (hysteresis)

@dataclass
class ShieldInput:
    threat_level: int
    is_moving: bool = False  # if moving fast, keep stowed unless critical

def desired_position(inp: ShieldInput, current_pos: float) -> float:
    # Hysteresis: deploy at >=2, retract only when threat 0 and not moving under fire
    if inp.threat_level >= THRESH_DEPLOY:
        return DEPLOYED
    if inp.threat_level <= 0 and current_pos > 0.05:  # allow retract
        # if moving fast under low threat, retract to reduce drag
        return STOWED
    # threat 1 = hold position
    return current_pos

def is_deployed(pos: float) -> bool:
    return pos > 0.8
def is_stowed(pos: float) -> bool:
    return pos < 0.1
