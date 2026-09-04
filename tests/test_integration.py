"""Integration: safety gate end-to-end (threat -> shield -> weapon) + battery gate.
Runs without Gz/ros2 daemon — exercises combined logic as field-test proxy.
Validates validate-phase safety invariant in one process.
"""
import sys
sys.path.insert(0, 'src/threat_manager')
sys.path.insert(0, 'src/shield_controller')
sys.path.insert(0, 'src/weapon_control')
sys.path.insert(0, 'src/battery_manager')
sys.path.insert(0, 'src/drone_coordinator')

from threat_manager.threat_logic import classify_threat, Detection
from shield_controller.shield_logic import desired_position, ShieldInput, STOWED, DEPLOYED
from weapon_control.weapon_logic import WeaponState, WeaponInput, next_state
from battery_manager.battery_logic import power_watts, Load
from drone_coordinator.drone_logic import mesh_status, DroneState

def test_field_scenario_full_combat_with_confirm():
    # Step 1: camera sees threat weapon at 30m
    threat = classify_threat([Detection('weapon', 0.82, [0.6,0.5,0.2,0.4], 30.0)])
    assert threat['level'] == 3

    # Step 2: shield should deploy
    pos = desired_position(ShieldInput(threat_level=threat['level']), STOWED)
    assert pos == DEPLOYED

    # Step 3: weapon chain requires braced+human
    is_braced = pos > 0.8
    s = WeaponState.SAFE
    s = next_state(s, WeaponInput(threat_level=threat['level'], human_confirm=False, is_braced=is_braced, battery_ok=True, recoil_ok=is_braced))
    assert s == WeaponState.ARMED
    s = next_state(s, WeaponInput(threat_level=threat['level'], human_confirm=False, is_braced=is_braced, battery_ok=True, recoil_ok=is_braced))
    assert s == WeaponState.BRACED
    # without confirm stays braced
    assert next_state(s, WeaponInput(3, False, True, True)) == WeaponState.BRACED
    # with confirm becomes ready then firing
    s = next_state(s, WeaponInput(3, True, True, True))
    assert s == WeaponState.READY
    s = next_state(s, WeaponInput(3, True, True, True))
    assert s == WeaponState.FIRING

def test_field_scenario_without_confirm_never_fires():
    threat = classify_threat([Detection('threat', 0.9, [0.5,0.5,0.2,0.3], 20)])
    pos = desired_position(ShieldInput(threat_level=threat['level']), STOWED)
    is_braced = pos == DEPLOYED
    s = WeaponState.READY
    # human revokes confirm -> must not fire
    s2 = next_state(s, WeaponInput(threat_level=3, human_confirm=False, is_braced=is_braced, battery_ok=True, recoil_ok=True))
    assert s2 != WeaponState.FIRING

def test_field_battery_gates_weapon():
    # Depleted battery prevents firing even with confirm+braced
    s = WeaponState.READY
    s2 = next_state(s, WeaponInput(threat_level=3, human_confirm=True, is_braced=True, battery_ok=False))
    assert s2 == WeaponState.SAFE

def test_field_drone_mesh_with_shield_battery():
    # Drone mesh integrates with battery drain
    drones = [DroneState(1, True, [60,0,35], 80, 0.9), DroneState(2, True, [-60,0,35], 80, 0.85)]
    m = mesh_status(drones)
    assert m['coverage_deg'] == 360
    # battery with drones drains faster
    p_no_drone = power_watts(Load(walking=True, velocity_ms=1.0, drones_active=0))
    p_drone = power_watts(Load(walking=True, velocity_ms=1.0, drones_active=2))
    assert p_drone > p_no_drone

def test_ambiguous_civilian_blocks_escalation_recommendation():
    # Civilian + weapon ambiguous -> threat manager flags but weapon still needs confirm
    r = classify_threat([Detection('civilian', 0.78, [0.4,0.4,0.15,0.4], 50), Detection('weapon', 0.62, [0.42,0.4,0.12,0.3], 50)])
    assert r['ambiguous'] is True
    assert r['level'] == 3
    # weapon still needs human
    s = WeaponState.BRACED
    assert next_state(s, WeaponInput(r['level'], False, True, True)) == WeaponState.BRACED
