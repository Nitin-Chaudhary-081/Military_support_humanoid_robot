# ARES-1 — Autonomous Reconnaissance & Engagement System

> **Mission:** Shield & striker bipedal robot per `arc.md` v1.0 — 2.43 m, 447 kg, 26-DOF, mesh-based URDF, soldier protection + surveillance + engagement with human kill-switch.
> **Status:** Simulation Phase — URDF Development — ROS2 Jazzy | MuJoCo | Foxglove — no hardware.

## Spec (from `arc.md` + `goal.md`)
- **Body:** 2.43 m (foot80+shin480+knee60+thigh520+hip60+pelvis180+abdomen220+chest380+neck120+head240+dome90), 447 kg detailed budget `arc.md:263` (Ti-6Al-4V, 7075-T6, AISI4340, B₄C, UHMWPE) `arc.md:291`
- **Shield:** 1.2×0.7×0.048 m (25 B₄C +15 UHMWPE +8 Ti) 18 kg 0.84m², arm 420mm Maxon EC-i40 80:1 0→105° 0.3s `arc.md:306`
- **Weapons:** SCAR-H 7.62 NATO 410/880mm 4.6kg 30×4 carousel + M320 40mm 230mm 1.5kg 8× belt + 6× Spike SR 4kg 50–800m HEAT 400mm in carbon pods 400×80×80 `arc.md:356` (~38kg)
- **Drones:** Fixed-wing VTOL 1.4kg 900mm 800m 45min bay 340×160×70 + Quad 0.85kg Ø150 prop 400m 22min bay 210×210×90 `arc.md:416` (vs old 2×6kg)
- **Armour:** 27kg ceramic/UHMWPE per-zone + blast 20RHA+10UHMWPE STANAG L3 `arc.md:478`, separate `<link>` plates for Foxglove toggle
- **Joints:** 26-DOF `arc.md:509` neck2 shoulders6 elbows2 wrists4 hips6 knees2 ankles4 (torques 60–360 N·m)
- **Sensors:** Livox MID-360 10Hz + D435i 30fps + Boson 640 60Hz + IMX477 rear 60fps + VN-100 IMU 800Hz + acoustic 4×MEMS + foot 6-axis 1kHz + 14 encoders 1kHz `arc.md:530` on `/ares1/sensors/...`
- **Compute:** Orin 275 TOPS + i7-1370P +14×STM32F4 + STM32H7 +2TB NVMe `arc.md:563`, YOLOv8n + RTAB-Map + Nav2 + Legged Gym
- **Meshes:** 16 STL `head 800 — foot 500` faces `arc.md:612`, `package://ares1_description/meshes/visual/<part>.stl` scale 1, collision `_col.stl`
- **Sim:** MuJoCo 3.x `mujoco/ares1.xml` + Gazebo Harmonic + Isaac Lab `arc.md:655` + Foxglove 8765

## Quickstart
```bash
# prerequisites: ROS 2 Jazzy + Gz Sim 8.x + foxglove_bridge (source setup.bash)
sudo apt install ros-jazzy-foxglove-bridge  # for browser viz
sudo rosdep init; rosdep update; rosdep install --from-paths src --ignore-src -r -y

colcon build --symlink-install
source install/setup.bash
ros2 launch acsr_bringup acsr_full.launch.py world:=battlefield_rubble use_foxglove:=true
# -> then open https://app.foxglove.dev and connect ws://localhost:8765 (see docs/foxglove.md)
# or minimal without Gz:
ros2 launch acsr_gazebo acsr_world.launch.py
ros2 launch acsr_bringup foxglove.launch.py  # bridge only

# nodes (mock-safe without hardware):
ros2 run threat_manager threat_node --ros-args -p input_topic:=/camera/image_raw
ros2 run shield_controller shield_node
ros2 run weapon_control weapon_node  # NEVER fires without human_confirm:=true
ros2 run drone_coordinator drone_node
ros2 run battery_manager battery_node

# tests:
colcon test --pytest-args -v && colcon test-result --verbose
pytest tests/ -v
```

## Workspace Layout
```
src/
  ares1_description/   URDF/Xacro ares1 (2430mm 447kg 26-DOF) + meshes/visual/*.stl (16) + meshes/collision/*_col.stl + config/ares1_controllers.yaml
  acsr_gazebo/        Gz worlds (flat/rubble/slope/crater) + bridge.yaml + spawn ares1
  acsr_bringup/       Full launch (world+ares1+nodes+foxglove) + foxglove_display.launch.py (static robot without Gz)
    config/foxglove_bridge.yaml (0.0.0.0:8765) + foxglove/acsr_layout.json
  threat_manager/     YOLOv8n → /ares1/sensors/... → /ares1/ai/threat_level 0→3
  weapon_control/     arm→brace→confirm→fire 26-DOF bridge
  shield_controller/  pivot 0→105° 0.3s
  drone_coordinator/  VTOL 1.4kg + quad 0.85kg bays 340×160×70 / 210×210×90
  battery_manager/    48kWh 96V 110kg 800A peak + glycol + supercap backup
  acsr_nav/           Nav2 + Legged Gym policy `/ares1/navigation/footstep_plan`
mujoco/ares1.xml      MJCF placeholder MuJoCo 3.x (meshdir visual)
config/ares1_params.yaml  (alias params.yaml per arc.md)
scripts/              gen_ares1_meshes.py + calibrate.sh + eval_*.py + foxglove_aws.sh
docs/                 architecture.md (ares1 graph) + foxglove.md (VPS) + ops.md + field_test.md + arc.md spec
```

## Safety & Ethics
- **Human-confirm gate** enforced in `weapon_control` — autonomous fire is blocked in code and tested.
- Simulation only. No physical weapons driven. All topics/mockable.
- Battery model quantifies endurance gap; does not hide it.

## Engineering State
Managed via `.engineering/` (Engineering Intelligence):
```bash
node /home/ubuntu/engineering-intelligence/bin/engineering.js status
node /home/ubuntu/engineering-intelligence/bin/engineering.js verify
node /home/ubuntu/engineering-intelligence/bin/engineering.js progress
node /home/ubuntu/engineering-intelligence/bin/engineering.js handoff --md
```

## Lifecycle (robotics-project)
`model → simulate → implement → integrate → validate → ops`

## Browser Viz (Foxglove)
```bash
ros2 launch acsr_bringup foxglove.launch.py   # ws://0.0.0.0:8765
# open https://app.foxglove.dev -> ws://localhost:8765 -> import src/acsr_bringup/config/foxglove/acsr_layout.json
```
See `docs/foxglove.md` for SSH tunnel, topics, and troubleshooting.

## References
- goal.md — authoritative vision + three hard problems
- .engineering/lifecycle.yaml — durable phase state
- docs/architecture.md — graph & dataflow
- docs/foxglove.md — Foxglove browser bridge
