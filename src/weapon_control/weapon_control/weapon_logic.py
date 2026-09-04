"""
Weapon state machine — pure logic, no ROS, fully unit-tested.
Invariant: NEVER transitions to FIRING without human_confirm==True.
goal.md:52 rifle 15Nm absorbed by braced stance + gyro; underslung launcher; missiles.
"""
from dataclasses import dataclass
from enum import Enum

class WeaponState(str, Enum):
    SAFE = "SAFE"
    ARMED = "ARMED"
    BRACED = "BRACED"
    READY = "READY"
    FIRING = "FIRING"
    COOLDOWN = "COOLDOWN"

@dataclass
class WeaponInput:
    threat_level: int  # 0-3 from threat_manager
    human_confirm: bool
    is_braced: bool  # shield deployed or stance stable
    battery_ok: bool
    recoil_ok: bool = True  # 15Nm check passed

def next_state(current: WeaponState, inp: WeaponInput) -> WeaponState:
    # Safety: battery or recoil fails -> SAFE regardless
    if not inp.battery_ok or not inp.recoil_ok:
        return WeaponState.SAFE
    if current == WeaponState.SAFE:
        # arm only if threat present
        return WeaponState.ARMED if inp.threat_level >= 2 else WeaponState.SAFE
    if current == WeaponState.ARMED:
        # must brace before ready (shield or stable stance)
        return WeaponState.BRACED if inp.is_braced else WeaponState.ARMED
    if current == WeaponState.BRACED:
        # require human confirm to become ready
        if not inp.human_confirm:
            return WeaponState.BRACED
        return WeaponState.READY if inp.threat_level >= 2 else WeaponState.ARMED
    if current == WeaponState.READY:
        # firing only if all conditions hold this tick
        if inp.human_confirm and inp.is_braced and inp.threat_level >= 2 and inp.battery_ok and inp.recoil_ok:
            return WeaponState.FIRING
        # if threat dropped or human revoked
        if not inp.human_confirm or inp.threat_level < 2:
            return WeaponState.ARMED
        return WeaponState.READY
    if current == WeaponState.FIRING:
        return WeaponState.COOLDOWN
    if current == WeaponState.COOLDOWN:
        # cooldown 1 tick then back to armed if threat persists else safe
        return WeaponState.ARMED if inp.threat_level >= 2 else WeaponState.SAFE
    return WeaponState.SAFE

def select_weapon(threat_level: int) -> str:
    if threat_level >= 3:
        return "rifle"  # 7.62mm primary
    if threat_level == 2:
        return "rifle_or_grenade"
    return "none"
