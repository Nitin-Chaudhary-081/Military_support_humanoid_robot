#!/usr/bin/env python3
"""Battery endurance table — proves 45-90min gap and 8%/yr curve. goal.md:84"""
import sys
sys.path.insert(0, 'src/battery_manager')
from battery_manager.battery_logic import power_watts, endurance_minutes, Load, solid_state_projection

def main():
    scenarios = [
        ("patrol slow", Load(walking=True, velocity_ms=0.8, compute_w=180, drones_active=0, shield_deployed=False, firing=False)),
        ("patrol + drones", Load(walking=True, velocity_ms=1.0, compute_w=180, drones_active=2, shield_deployed=False, firing=False)),
        ("full combat", Load(walking=True, velocity_ms=1.2, compute_w=220, drones_active=2, shield_deployed=True, firing=True)),
        ("static overwatch", Load(walking=False, velocity_ms=0.0, compute_w=180, drones_active=2, shield_deployed=False, firing=False)),
    ]
    print(f'{"scenario":<18} {"power W":>8} {"48kWh end (min)":>16} {"6yr solid-state (kWh)":>22} {"end 6yr (min)":>14}')
    print("-"*90)
    for name, load in scenarios:
        p = power_watts(load)
        e = endurance_minutes(48.0, load)
        cap6 = solid_state_projection(48.0, 6)
        e6 = endurance_minutes(cap6, load)
        print(f'{name:<18} {p:8.0f} {e:16.1f} {cap6:22.1f} {e6:14.1f}')
    print("\nSolid-state 8%/yr: 48 -> {:.1f} kWh in 6yr; full-combat 45-90min -> {:.0f}min (still short of 6-8h goal; needs fuel-cell or swap)".format(solid_state_projection(48,6), endurance_minutes(solid_state_projection(48,6), scenarios[2][1])))

if __name__ == '__main__': main()
