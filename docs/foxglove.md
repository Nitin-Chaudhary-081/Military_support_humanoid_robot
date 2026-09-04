# Foxglove — Browser Visualization for ACSR Sim

> Foxglove bridge streams all ROS 2 topics to a WebSocket so you can see the robot, lidar, camera, TF, battery, shield, weapons, drones without installing RViz.

## 1) Start the stack

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install && source install/setup.bash

# Full robot + foxglove (port 8765):
ros2 launch acsr_bringup acsr_full.launch.py world:=battlefield_rubble use_foxglove:=true

# Foxglove only (if robot already running):
ros2 launch acsr_bringup foxglove.launch.py port:=8765
# verify:
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" http://localhost:8765  # 426 expected (means port is listening)
ros2 node list | grep foxglove_bridge
ros2 topic list | grep -E "threat|shield|battery|drone|tf|camera|lidar"
```

## 2) Open in browser

- **Hosted (no install):** https://app.foxglove.dev → *Open connection* → `ws://localhost:8765`
  - If `ms_robot` runs on a remote EC2/VM, replace `localhost` with that host IP and open SSH tunnel: `ssh -L 8765:localhost:8765 ubuntu@<host>`
- **Local Studio:** https://foxglove.dev/download or `sudo snap install foxglove-studio` → same URL.

## 3) Recommended layout (import `foxglove/acsr_layout.json`)

Panels:
- **3D** → `/tf`, `Robot Model` (URDF from `acsr_description`), `/lidar/points` (PointCloud), ground plane
- **Image** → `/camera/image_raw`, `/drone_1/image`, `/drone_2/image`
- **Plot** → `/battery/soc`, `/shield/command`
- **Raw Messages** → `/threat/level` (Int32 0-3), `/threat/tracks` (JSON), `/weapon/state`, `/drone/mesh_status`, `/battery/state`
- **Teleop / Publish** → publish `std_msgs/Bool` to `/human/confirm` = `true` to arm (safety gate), `Float64` to `/shield/command`
- **Parameters** → `threat_manager conf_thresh`, `battery_manager capacity_kwh`

Preset file: `src/acsr_bringup/config/foxglove/acsr_layout.json` (auto-loaded if you `File → Import layout`).

## 4) Topics exposed by bridge

Bridge whitelists `['.*']` so every ACSR topic is visible:

| Topic | Type | Notes |
|-------|------|-------|
| `/tf`, `/tf_static` | `tf2_msgs/TFMessage` | Robot + shield `shield_pivot` + sensor head |
| `/joint_states` | `sensor_msgs/JointState` | 9 joints |
| `/camera/image_raw` | `sensor_msgs/Image` 1280×720 30Hz | Head camera |
| `/lidar/points` | `sensor_msgs/PointCloud2` | GPU lidar 60m |
| `/drone_1/image`, `/drone_2/image` | `sensor_msgs/Image` | Mesh cameras |
| `/threat/level` | `std_msgs/Int32` | 0 safe … 3 threat |
| `/threat/tracks` | `std_msgs/String` JSON | `level`, `tracks[]`, `ambiguous` |
| `/shield/state`, `/shield/command` | `String JSON` + `Float64` | 0.0 stowed → 1.57 deployed |
| `/weapon/state`, `/weapon/command` | `String` | `SAFE→ARMED→BRACED→READY→FIRING` (needs confirm) |
| `/battery/state`, `/battery/soc` | `String JSON` + `Float64` | soc 0-100, power 29kW |
| `/drone/mesh_status`, `/drone_1/pose`, `/drone_2/pose` | `String JSON` + `PoseStamped` | coverage 360° |
| `/foxglove_bridge/sysinfo` | `foxglove_msgs` | Bridge health |

## 5) Troubleshooting

- `port already in use` → `lsof -i :8765 && kill <pid>` or change `port:=8766`.
- No TF/robot model → `ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(xacro src/acsr_description/urdf/acsr.urdf.xacro)"` must be running (started by `acsr_full.launch.py`).
- Image black → `ros2 topic hz /camera/image_raw` must be >10Hz; Gz sensors publish only when `gz sim` is running (check `gz sim --version` 8.11.0).
- WSS required? Set `tls:=true certfile:=... keyfile:=...` in `foxglove_bridge.yaml`.
- Remote host: open Security Group TCP 8765 ingress or use SSH tunnel.

## 6) Headless CI

Bridge is `IfCondition(use_foxglove)` so `use_foxglove:=false` disables it for tests.

## 7) Architecture

`Gz Sim + ROS 2 nodes → DDS → foxglove_bridge (WebSocket 8765) → browser Foxglove Studio`
Config: `src/acsr_bringup/config/foxglove_bridge.yaml` (`use_sim_time: true`, whitelist `['.*']`).
