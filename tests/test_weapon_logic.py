import sys
sys.path.insert(0, 'src/weapon_control')
from weapon_control.weapon_logic import WeaponState, WeaponInput, next_state

def test_never_fire_without_confirm():
    s=WeaponState.READY
    inp=WeaponInput(threat_level=3, human_confirm=False, is_braced=True, battery_ok=True, recoil_ok=True)
    assert next_state(s,inp) != WeaponState.FIRING
    # even from READY with high threat but no confirm, should go ARMED not FIRING
    assert next_state(s,inp) == WeaponState.ARMED

def test_safe_when_battery_fails():
    for st in WeaponState:
        inp=WeaponInput(threat_level=3, human_confirm=True, is_braced=True, battery_ok=False)
        assert next_state(st,inp)==WeaponState.SAFE

def test_recoil_requires_braced():
    s=WeaponState.ARMED
    # not braced -> stays ARMED, not BRACED
    assert next_state(s, WeaponInput(3,True,False,True,True))==WeaponState.ARMED
    assert next_state(s, WeaponInput(3,True,True,True,True))==WeaponState.BRACED

def test_full_chain_needs_human():
    # SAFE -> ARMED (threat 2)
    s=WeaponState.SAFE
    s=next_state(s, WeaponInput(2,False,False,True))
    assert s==WeaponState.ARMED
    # ARMED -> BRACED
    s=next_state(s, WeaponInput(2,False,True,True))
    assert s==WeaponState.BRACED
    # BRACED without confirm stays BRACED
    assert next_state(s, WeaponInput(2,False,True,True))==WeaponState.BRACED
    # with confirm -> READY
    s=next_state(s, WeaponInput(2,True,True,True))
    assert s==WeaponState.READY
    # READY with confirm+braced -> FIRING
    s2=next_state(s, WeaponInput(2,True,True,True))
    assert s2==WeaponState.FIRING

def test_firing_goes_cooldown():
    assert next_state(WeaponState.FIRING, WeaponInput(3,True,True,True))==WeaponState.COOLDOWN
    assert next_state(WeaponState.COOLDOWN, WeaponInput(3,True,True,True))==WeaponState.ARMED
    assert next_state(WeaponState.COOLDOWN, WeaponInput(0,True,True,True))==WeaponState.SAFE
