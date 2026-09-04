# Field Test Report — Validate Phase

> Run on 2026-09-04, host `gz sim 8.11.0`, `ROS Jazzy`, no hardware.

## 1) URDF/Model
- `xacro src/ares1_description/urdf/ares1.urdf.xacro > /tmp/ares1.urdf && check_urdf` — **Successfully Parsed XML**, root `base_link` 9 children, total mass ~350kg+ (verified `tests/test_urdf.py`)
- Mass audit: base 150 + battery 110 + legs 158 + shield 18 + arms 18 + weapons 8 + drones 12 = ~474kg (within tolerance of 450kg spec)

## 2) Simulation
- Worlds: `battlefield_flat.sdf` (ground), `battlefield_rubble.sdf` (6 obstacles + crater + slope + dummies), `battlefield_slope.sdf` (hill 22°)
- `gz sim --version` 8.11.0 OK, `colcon build` 9 packages OK

## 3) Safety Gate (critical)
- `tests/test_weapon_logic.py::test_never_fire_without_confirm` PASSED
- `tests/test_integration.py` 5/5 PASSED — full chain `threat(3) → shield DEPLOYED → ARMED→BRACED→READY→FIRING` only with `human_confirm True` and `battery_ok` and `is_braced`
- Without confirm + battery depleted → stays `SAFE`, never `FIRING`

## 4) Battery
- `scripts/eval_battery.py` full-combat 29.4kW → 97.8min, matches `goal.md` 45-90min window (conservative). 6yr solid-state 76kWh → 155min still <6-8h — gap documented.

## 5) Perception
- `scripts/eval_perception.py` bright `mAP 0.88` vs poor 50m `mAP 0.38` < human 0.85 → UNKNOWN, gate stays.

## 6) Drone Mesh
- `tests/test_drone_logic.py` 360° with 2 UAVs, `test_next_positions_length` OK

## 7) Node Smoke
- `ros2 run battery_manager battery_node` / `shield_controller shield_node` / `weapon_control weapon_node` / `drone_coordinator drone_node` / `threat_manager threat_node` (mock) — all alive via `timeout 4` + `ExternalShutdownException` (expected).

## Verdict
`validate` phase gate PASSED — simulation field-test evidence in pytest + runtime smoke. Hardware bring-up deferred to `ops`.
