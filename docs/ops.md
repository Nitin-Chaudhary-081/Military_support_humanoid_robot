# Ops Runbook — ACSR Simulation Deployment

> Lifecycle `ops` phase — calibration, logs, handoff to ops. Sim-only, no hardware.

## Quick Deploy (sim)
```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install && source install/setup.bash
ros2 launch acsr_bringup acsr_full.launch.py world:=battlefield_rubble
# verify:
ros2 topic echo /threat/level --once
ros2 topic echo /shield/state --once
ros2 topic echo /battery/state --once
ros2 topic echo /drone/mesh_status --once
```

## Calibration (`scripts/calibrate.sh`)
- **URDF:** `xacro src/acsr_description/urdf/acsr.urdf.xacro > /tmp/acsr.urdf && check_urdf /tmp/acsr.urdf`
- **Joints:** zero all 9 actuated joints via `ros2 topic pub /shield/command std_msgs/Float64 "{data: 0.0}" --once`
- **Sensors:** verify `/camera/image_raw` 1280×720 30Hz, `/lidar/points` 1024 samples 10Hz
- **Expected:** shield 0.0 stowed, battery soc 100% at start, no `FIRING` without `/human/confirm`

## Logs
- Build: `log/latest_build/`
- ROS log: `~/.ros/log/` (or `ros2 bag record /threat/level /weapon/state /battery/state`)
- Evaluate gaps:
```bash
python3 scripts/eval_terrain.py --world rubble --trials 100
python3 scripts/eval_battery.py
python3 scripts/eval_perception.py
```

## Safety Checks (validate phase must pass)
1. `pytest tests/test_weapon_logic.py::test_never_fire_without_confirm` — never fires without human
2. `pytest tests/test_integration.py::test_field_scenario_without_confirm_never_fires` — end-to-end gate
3. `ros2 run weapon_control weapon_node` — publish `FIRING` only if subscribed `/human/confirm true`, `Battery ok`, `braced`
4. Battery depleted (`soc <10%`) → weapon gates to `SAFE`

## Deployment Checklist
- [ ] `colcon build` clean (9 packages)
- [ ] `pytest -q` 31 passed
- [ ] `check_urdf` passes (root base_link 9 children)
- [ ] `gz sim --version` 8.11.0 present
- [ ] No secrets committed (`engineering security` VERIFIED)
- [ ] `handoff.md` current

## Incident Runbook
- **Fall:** check `/joint_states` velocity, lower `velocity_ms` 1.2→0.8, rerun `eval_terrain`
- **Perception ambiguous:** `/threat/tracks` has `"ambiguous":true` → require human confirm, no auto-fire
- **Battery warning:** `/battery/state` `depleted:true` → RTB (return to base), `soc` <10% gates weapons
- **Drone link degraded:** `/drone/mesh_status` `link_quality<0.5` → reduce range 60→30m or hold
- **Telemetry loss:** `ros2 topic hz /threat/level` → restart `threat_manager`

## Ownership
- Model: `acsr_description` (URDF owner)
- Sim: `acsr_gazebo` (worlds owner)
- Nodes: per-package maintainers (see `package.xml`)
- Ops logs: rotate daily, keep 7 days sim bag

## Out-of-Scope
Hardware bring-up, real rifle, Isaac Gym RL training — tracked as `R-010 PARTIALLY_IMPLEMENTED`.
