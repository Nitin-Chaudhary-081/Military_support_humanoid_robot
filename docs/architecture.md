# Architecture — ARES-1 Simulation (arc.md v1.0)

## Graph (File → Component → Topic) per arc.md 14 + Appendix A
```
Sensors (Gz MuJoCo) ─┬─ /ares1/sensors/camera/front/image (D435i 30fps) ──> threat_manager YOLOv8n ──> /ares1/ai/threat_level 0→3 ─┬─> shield_controller ──> /ares1/actuators/shield/deploy ─┬─> weapon_control
                   │  /ares1/sensors/camera/thermal/image (Boson640 60Hz)     │                         │                        └─> /ares1/actuators/weapons/rifle/fire
                   │  /ares1/sensors/lidar/points (Livox MID-360 10Hz) ──> acsr_nav Nav2 + Legged Gym ──> /ares1/navigation/path │                        └─> /ares1/actuators/missiles/fire (6 × Spike SR)
                   │  /ares1/sensors/camera/rear/image (IMX477 60fps)     │                        └─> drone_coordinator XTDrone ──> /ares1/drones/drone1|2/command + telemetry (laser designator)
                   │  /ares1/sensors/imu/data (VN-100 800Hz)              │                                     
                   │  /ares1/sensors/acoustic/direction + foot FT 1kHz ───┘                                     
Battery (48kWh 96V 110kg + glycol + 2×supercap) ──> /battery/state + /ares1/sensors/imu → gates weapons (soc>10%)
URDF (ares1_description: 2430mm 447kg 26-DOF mesh STL) ──> Gz Harmonic + MuJoCo 3.x mujoco/ares1.xml + gz_ros2_control (ares1_controllers.yaml 26 joints) + joint_state_broadcaster + foxglove_bridge 8765
```

## Packages
- **ares1_description** 2430mm 447kg 26-DOF `arc.md:509` mesh `16 STL visual/collision` `2430=80+480+60+520+60+180+220+380+120+240+90`, inertias per weight budget `447kg` `Ti-6Al-4V/7075/4340/B₄C` `arc.md:291`, shield 1200×700×48 18kg pivot 0→105° 0.3s Maxon EC-i40 80:1 `arc.md:342`, weapons SCAR-H + M320 + 6× pods `arc.md:356`, drones 1.4kg VTOL +0.85kg quad bays `340×160×70 / 210×210×90` `arc.md:459`, armour 27kg separate `<link>` fixed `arc.md:478`, sensors 8 types `arc.md:530` → `/ares1/sensors/*`, `ares1_controllers.yaml` 26 joints
- **acsr_gazebo** 3 worlds (flat/rubble/slope) `bridge.yaml` spawn `ares1` via `ares1.urdf.xacro` + `ParameterValue`
- **acsr_bringup** `foxglove_display.launch.py` (static ares1 without Gz) + `acsr_full.launch.py` (Gz+ares1+foxglove) + `foxglove_bridge.yaml` 0.0.0.0:8765
- **mujoco/ares1.xml** MJCF placeholder MuJoCo 3.x `meshdir visual` `arc.md:655`
- **threat_manager** YOLOv8n fine-tuned `Subh775/Threat-Detection` + threat level `0→3`
- **weapon_control** human kill-switch invariant tested 26-DOF aware
- **shield_controller** 0.3s deploy acoustic or threat≥2
- **drone_coordinator** XTDrone mesh `VTOL 800m 45min + quad 400m 22min`
- **battery_manager** 48kWh 96V 800A peak 19.2kW cont + 2×supercap
- **acsr_nav** Nav2 + Legged Gym + MoveIt2

## Dataflow (INFERRED until runtime)
1. MuJoCo/Gz publish `/ares1/sensors/*` + `/clock` → `foxglove_bridge` → browser
2. threat_manager → `/ares1/ai/detections` + `threat_level` + `battle_map` RTAB-Map
3. shield 0→1.83 rad (105°) when acoustic or `threat≥2`
4. weapon needs `braced` + `human_confirm` + `soc>10%` → `SAFE..FIRING`, rifle 600RPM burst, missiles fire-and-forget EO+dronelaser
5. drones spring/pop eject → MAVLink 5GHz → laser designator → missile guidance
6. Nav2 `footstep_plan` from Legged Gym policy

## Verification Hooks
- `xacro src/ares1_description/urdf/ares1.urdf.xacro > /tmp/ares1.urdf && check_urdf /tmp/ares1.urdf` — expect `69 links 68 joints mass 447.1kg`
- `colcon build --symlink-install` + `pytest tests/test_ares1_geometry.py -v` (16 meshes + 26-DOF + sensors)
- `gz sim -r -v 1 src/acsr_gazebo/worlds/battlefield_rubble.sdf &` + `ros2 launch acsr_bringup foxglove_display.launch.py`
- `mujoco -- --mjcf mujoco/ares1.xml` (placeholder loads)
