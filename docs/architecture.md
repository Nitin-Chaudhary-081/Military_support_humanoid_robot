# Architecture — ACSR Simulation

## Graph (File → Component → Topic)
```
Sensors (Gz) ─┬─ /camera/image_raw ──> threat_manager (YOLOv8) ──> /threat/level ─┬─> shield_controller ──> /shield/state ─┬─> weapon_control
              │   /lidar/points ───────> acsr_nav (Nav2 costmap) ──> /plan        │                          │              └─> /weapon/state
              │                                                                    └─> drone_coordinator ──> /drone/mesh    (requires human/confirm)
              └─ /drone/{1,2}/image ─────────────────────────────────────────────────────────────────────────> extends coverage 360°
Battery (48kWh) ──> /battery/state ──> gates weapons (soc>10%)
URDF (acsr_description) ──> Gz Sim + ros2_control (gz_ros2_control) + joint_state_broadcaster
```

## Packages
- **acsr_description** 450kg URDF, 18kg shield pivot, sensor head, weapons TF, controllers.yaml
- **acsr_gazebo** 3 worlds (flat/rubble/slope), bridge.yaml, spawn
- **acsr_bringup** full launch (world+all nodes)
- **threat_manager** YOLO logic pure (threat_logic.py) + ROS node
- **weapon_control** state machine pure + ROS node (human-confirm invariant)
- **shield_controller** pivot logic pure + ROS node
- **drone_coordinator** mesh logic pure + ROS node (60m radius, 35m alt)
- **battery_manager** drain model pure + ROS node (Wh/km)
- **acsr_nav** Nav2 dwb + NavFn, voxel costmap from lidar

## Dataflow (INFERRED until runtime)
1. Gz publishes clock+camera+lidar -> ros_gz_bridge
2. threat_manager classifies -> level 0-3 + tracks + ambiguous flag
3. shield subscribes level -> pivot 0->1.57, publishes braced
4. weapon subscribes level + braced + human/confirm + battery -> SAFE..FIRING (never without confirm)
5. drone subscribes threat/bearing -> lerp to 60m orbit
6. battery integrates power(load) -> soc, gates weapon

## Decisions
- Gz Sim 8.x (Jazzy native) over Classic (deprecated) — ADR upcoming
- ros2_control + joint_trajectory_controllers for hydraulics stub — RL gait future
- Python nodes with pure *_logic.py for pytest without ROS — evidence-friendly
- Human-confirm as Bool + String (compat) on /human/confirm — security invariant tested

## Verification Hooks
- `check_urdf src/acsr_description/urdf/acsr.urdf.xacro`
- `xacro src/acsr_description/urdf/acsr.urdf.xacro > /tmp/acsr.urdf && check_urdf /tmp/acsr.urdf`
- `colcon build --symlink-install` + `pytest tests/`
- `gz sim -r -v 1 src/acsr_gazebo/worlds/battlefield_rubble.sdf &` + rostopic echo
