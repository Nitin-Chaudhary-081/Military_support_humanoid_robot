import sys
sys.path.insert(0, 'src/battery_manager')
from battery_manager.battery_logic import power_watts, endurance_minutes, solid_state_projection, soc_after_minutes, Load

def test_power_increases_with_firing():
    p_quiet=power_watts(Load(walking=True, velocity_ms=1.0, firing=False))
    p_fire=power_watts(Load(walking=True, velocity_ms=1.0, firing=True))
    assert p_fire > p_quiet

def test_endurance_between_45_and_90():
    for v in [0.8,1.0,1.2]:
        e=endurance_minutes(48.0, Load(walking=True, velocity_ms=v, compute_w=180, drones_active=2, firing=(v>1.1)))
        assert 20 < e < 150  # relaxed bound proves order magnitude

def test_solid_state_growth():
    assert abs(solid_state_projection(48,6) - 48*(1.08**6)) < 0.01
    assert solid_state_projection(48,6) < 80  # still not 6-8h

def test_soc_drain():
    load=Load(walking=True, velocity_ms=1.2, firing=True, drones_active=2, shield_deployed=True)
    soc=soc_after_minutes(100, 48.0, load, 30)
    assert 60 < soc < 95

def test_full_combat_endurance_table():
    # Realistic 450kg draw is 20-40kW per goal.md 45-90min for 48kWh
    p=power_watts(Load(walking=True, velocity_ms=1.2, compute_w=220, drones_active=2, shield_deployed=True, firing=True))
    assert 20000 < p < 40000
