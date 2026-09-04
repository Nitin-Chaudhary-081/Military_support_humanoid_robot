# Autonomous Combat Support Robot (ACSR) — Simulation Platform

> **Mission:** Shield & striker bipedal robot that protects soldiers, flies 2 drones, and engages threats with human-in-loop confirmation.
> **Status:** Simulation-only (Gazebo/ROS 2). No hardware. No autonomous lethal action.

## Spec (from goal.md)
- 2.5 m, 450 kg bipedal hydraulic legs, 110 kg chest battery, low CoM
- Shield: 1.2×0.7 m boron-carbide 18 kg pivot arm (back ↔ deployed)
- Weapons: 7.62 mm rifle (15 Nm), 40 mm launcher, Spike-SR micro-missiles
- Drones: 2× 6 kg fixed-wing fold-flat (RQ-11 class)
- Compute: Jetson AGX Orin 275 TOPS — YOLOv8 60 FPS + Nav2 + ROS 2 Jazzy + Gz Sim
- Three hard problems: terrain (40%→85%), AI reliability, 48 kWh → 45–90 min

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
  acsr_description/   URDF/Xacro, meshes (2.5m biped + shield joint + sensor head)
  acsr_gazebo/        Gz worlds (flat/rubble/slope/crater), spawn + bridges
  acsr_bringup/       One-launch deployment + params + foxglove_bridge
    launch/foxglove.launch.py  -> ws://localhost:8765 browser bridge
    config/foxglove/acsr_layout.json  -> Foxglove Studio layout import
  threat_manager/     YOLOv8 → /threat/{level,tracks} (human-confirm gated)
  weapon_control/     arm→brace→confirm→fire state machine, 15 Nm check
  shield_controller/  pivot deploy/retract controller
  drone_coordinator/  2-UAV mesh, /drone_1/image
  battery_manager/    48 kWh drain model, /battery/state (45–90 min sim)
  acsr_nav/           Nav2 terrain-aware config
config/               global params
scripts/              gait eval, YOLO training, metrics + calibrate.sh
docs/foxglove.md      browser viz guide
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
