# ARES-1 — Autonomous Reconnaissance & Engagement System
## Complete Military Robot Design Specification
**Version:** 1.0.0  
**Classification:** Engineering Design Document  
**Author:** Nik  
**Platform:** ROS2 Jazzy | MuJoCo | Foxglove Studio  
**Status:** Simulation Phase — URDF Development  

---

## Table of Contents
1. [System Overview](#1-system-overview)
2. [Body Geometry & Shape Specification](#2-body-geometry--shape-specification)
3. [Full Dimensions & Weight Budget](#3-full-dimensions--weight-budget)
4. [Material Grades](#4-material-grades)
5. [Shield Specification](#5-shield-specification)
6. [Weapons Specification](#6-weapons-specification)
7. [Drone Specification](#7-drone-specification)
8. [Armour Specification](#8-armour-specification)
9. [Joint Specification](#9-joint-specification)
10. [Sensor Suite](#10-sensor-suite)
11. [Power System](#11-power-system)
12. [AI & Compute](#12-ai--compute)
13. [URDF Mesh Geometry Guide](#13-urdf-mesh-geometry-guide)
14. [Open-Source Stack](#14-open-source-stack)

---

## 1. System Overview

| Parameter | Value |
|-----------|-------|
| Designation | ARES-1 (Autonomous Reconnaissance & Engagement System) |
| Role | Autonomous combat support, soldier protection, surveillance |
| Locomotion | Bipedal walking — fully autonomous |
| Height | 2,500 mm (2.5 m) |
| Total mass | 447 kg |
| Power source | Solid-state lithium battery — 48 kWh |
| Operational endurance | 4 hours light duty / 90 min full combat load |
| Control mode | Fully autonomous AI — human kill-switch override |
| Threat levels | 0 (patrol) → 1 (alert) → 2 (armed) → 3 (active combat) |
| Drones carried | 2 × fold-flat UAV (back-mounted bays) |
| Communication | 5 GHz encrypted mesh — MAVLink bridge to drones |
| ROS version | ROS2 Jazzy |
| Simulation | MuJoCo 3.x + Gazebo Harmonic + Isaac Lab |

---

## 2. Body Geometry & Shape Specification

> **Mesh style guide:** All parts use multi-face convex meshes exported as `.stl` or `.obj`.  
> Each section below defines the base primitive, then the mesh detail layer on top.  
> In URDF: `<geometry><mesh filename="meshes/[part].stl" scale="1 1 1"/></geometry>`

---

### 2.1 Head

| Property | Value |
|----------|-------|
| Base primitive | Rounded box (chamfered edges, 8-face bevel) |
| Width × Depth × Height | 280 mm × 260 mm × 240 mm |
| Front face | Recessed visor slot — 220 mm × 60 mm — 15 mm deep |
| Visor material | Polycarbonate ballistic — 20 mm thick |
| Top dome | Hemispherical sensor dome — radius 90 mm — sits flush on top face |
| Side panels | 4 mm chamfer on all vertical edges |
| Rear | Flat plate — LiDAR aperture 80 mm diameter centred |
| Neck socket | Circular recess bottom face — diameter 80 mm × 40 mm deep |
| Mesh detail | 6-sided polygonal profile — 24 faces total |
| Colour (sim) | Matte dark grey — RGB (45, 45, 48) |

---

### 2.2 Neck

| Property | Value |
|----------|-------|
| Shape | Tapered cylinder — wider at base |
| Top diameter | 70 mm |
| Bottom diameter | 90 mm |
| Height | 120 mm |
| Wall thickness | 12 mm |
| Internal routing | Flex cable conduit — 30 mm diameter channel |
| Mesh detail | 16-sided polygon cylinder |
| DOF | 2 — yaw ±90°, pitch ±30° |

---

### 2.3 Torso (Chest + Abdomen combined)

#### 2.3.1 Chest Block

| Property | Value |
|----------|-------|
| Base shape | Trapezoidal prism — wider at top |
| Top width | 520 mm |
| Bottom width | 440 mm |
| Depth | 280 mm |
| Height | 380 mm |
| Front face detail | Central battery access panel 200 mm × 120 mm recessed 8 mm |
| Front face detail | 2× hexagonal ventilation grilles — 60 mm hex each side |
| Side faces | Shoulder mount flanges — 40 mm protrusion, 6× M12 bolt holes |
| Rear | Drone bay openings — 2× rectangular slots 340 mm × 160 mm |
| Rear | Shield mount rail — 60 mm × 40 mm channel, length 360 mm |
| Mesh detail | 32-face mesh — all edges chamfered 5 mm |

#### 2.3.2 Abdomen

| Property | Value |
|----------|-------|
| Shape | Segmented cylinder — 3 rings (vertebra-style) |
| Diameter | 360 mm outer, 300 mm inner |
| Height per ring | 60 mm |
| Total height | 220 mm (3 rings + 2 gaps of 25 mm) |
| Gap material | High-tensile rubber bellows — 25 mm compressed |
| Function | Allows ±15° flex in pitch and ±10° in roll |
| Mesh detail | 24-sided polygon rings |

---

### 2.4 Pelvis

| Property | Value |
|----------|-------|
| Shape | Wide hexagonal prism |
| Width | 460 mm |
| Depth | 260 mm |
| Height | 180 mm |
| Hip socket left | Spherical recess — 90 mm diameter — offset 180 mm from centre |
| Hip socket right | Spherical recess — 90 mm diameter — offset 180 mm from centre |
| Rear | Shield lower mount point — 40 mm eyebolt socket |
| Mesh detail | 12-face chamfered hex prism |

---

### 2.5 Shoulder Assembly

| Property | Value |
|----------|-------|
| Shoulder yoke shape | Curved swept extrusion — C-channel profile |
| Total span | 640 mm (centre to centre of ball joints) |
| Yoke height | 80 mm |
| Yoke depth | 120 mm |
| Ball joint housing | Spherical shell — 110 mm outer diameter — 6061 aluminium |
| Missile pod mount | Top face of yoke — 3× tube brackets each side |
| Mesh detail | Swept profile — 48 faces |
| DOF per shoulder | 3 — pitch ±180°, roll ±90°, yaw ±45° |

---

### 2.6 Upper Arm

| Property | Value |
|----------|-------|
| Shape | Tapered octagonal prism |
| Top cross-section | 120 mm × 100 mm |
| Bottom cross-section | 100 mm × 85 mm |
| Length | 380 mm |
| Wall thickness | 8 mm titanium shell |
| Elbow end | Cylindrical pin joint housing — 85 mm diameter |
| Front face | Recessed armour panel slot — 4 mm |
| Mesh detail | 8-sided tapered prism — 48 faces |

---

### 2.7 Forearm

| Property | Value |
|----------|-------|
| Shape | Rounded rectangular prism — ergonomic taper |
| Top width × depth | 100 mm × 85 mm |
| Bottom width × depth | 90 mm × 75 mm |
| Length | 340 mm |
| Underside | Cannon mount rail — 80 mm × 40 mm T-slot |
| Top face | Grenade magazine slot — 60 mm × 200 mm |
| Mesh detail | 16-face rounded prism |

---

### 2.8 Hand / Fist

| Property | Value |
|----------|-------|
| Shape | Blocky 4-finger fist — partially articulated |
| Overall width | 140 mm |
| Overall depth | 90 mm |
| Overall height | 160 mm |
| Finger count | 4 rigid finger blocks + 1 opposable thumb |
| Finger shape | Rounded rectangular blocks — 30 mm × 25 mm × 70 mm each |
| Grip channel | 35 mm diameter circular grip — for weapon handle |
| Wrist joint | 2 DOF — pitch ±60°, roll ±30° |
| Mesh detail | 64-face articulated fist mesh |

---

### 2.9 Thigh

| Property | Value |
|----------|-------|
| Shape | Cylindrical with front flat face |
| Outer diameter | 200 mm |
| Flat front face | 160 mm wide chord — cut flat for armour panel |
| Length | 520 mm |
| Wall thickness | 10 mm |
| Hip end | Ball socket cup — 95 mm diameter |
| Knee end | Dual-hinge pin housing — 100 mm wide |
| Mesh detail | 20-sided cylinder with flat front — 60 faces |

---

### 2.10 Shin (Lower Leg)

| Property | Value |
|----------|-------|
| Shape | D-profile extrusion — flat front, curved rear |
| Width | 160 mm |
| Depth | 140 mm |
| Length | 480 mm |
| Front face | Flat — shin armour plate bonded directly |
| Rear | Curved — cable + hydraulic routing channel |
| Ankle end | Cylindrical pivot housing — 80 mm diameter |
| Mesh detail | D-profile sweep — 32 faces |

---

### 2.11 Foot

| Property | Value |
|----------|-------|
| Shape | Wide low-profile platform — heel + toe sections |
| Total length | 380 mm |
| Width | 200 mm |
| Heel height | 80 mm |
| Toe height | 40 mm |
| Toe section length | 160 mm |
| Heel section length | 220 mm |
| Sole | Rubberised anti-slip pad — 15 mm thick |
| Ankle connection | 2 DOF gimbal — pitch ±40°, roll ±20° |
| Mesh detail | 40-face organic foot shape |

---

## 3. Full Dimensions & Weight Budget

### 3.1 Height Breakdown

| Body segment | Height (mm) | Cumulative from ground (mm) |
|---|---|---|
| Foot (sole to ankle) | 80 | 80 |
| Shin | 480 | 560 |
| Knee joint | 60 | 620 |
| Thigh | 520 | 1140 |
| Hip joint | 60 | 1200 |
| Pelvis | 180 | 1380 |
| Abdomen | 220 | 1600 |
| Chest | 380 | 1980 |
| Neck | 120 | 2100 |
| Head | 240 | 2340 |
| Sensor dome | 90 | **2430 mm ≈ 2.5 m** |

---

### 3.2 Weight Budget

| Component | Material | Weight (kg) |
|---|---|---|
| Head + neck | Ti-6Al-4V + polycarbonate | 18 |
| Chest block | Ti-6Al-4V shell + internals | 32 |
| Abdomen rings | Aluminium 7075 + rubber bellows | 12 |
| Pelvis frame | Steel 4340 | 22 |
| Shoulder yoke × 2 | Ti-6Al-4V | 14 |
| Upper arm × 2 | Ti-6Al-4V | 12 |
| Forearm × 2 | Aluminium 7075 | 8 |
| Hand × 2 | Aluminium 7075 | 6 |
| Thigh × 2 | Steel 4340 | 28 |
| Shin × 2 | Steel 4340 | 20 |
| Foot × 2 | Aluminium 7075 + rubber | 10 |
| Battery pack (48 kWh) | Solid-state Li cells | 110 |
| AI compute + electronics | PCB + cooling | 18 |
| Hydraulic system | Lines + fluid + actuators | 30 |
| Wiring harness | Flex cable bundles | 8 |
| Shield (stowed) | Boron carbide + frame | 18 |
| Weapons + ammo | Steel + polymer | 38 |
| Drone × 2 (bays) | Carbon fibre + electronics | 24 |
| Armour panels (all) | Ceramic composite | 27 |
| Fasteners + misc | Steel | 12 |
| **TOTAL** | | **≈ 447 kg** |

---

## 4. Material Grades

| Material | Grade | Application | Key property |
|---|---|---|---|
| Titanium alloy | Ti-6Al-4V (Grade 5) | Head, chest, arms, shoulders | 950 MPa yield, light |
| Aluminium alloy | 7075-T6 | Forearms, feet, abdomen | 503 MPa yield, very light |
| Steel alloy | AISI 4340 | Pelvis, thighs, shins | 1080 MPa yield, high load |
| Boron carbide | B₄C — Grade A | Shield face plate | Stops 7.62mm AP rounds |
| Ceramic composite | Al₂O₃ / SiC mosaic | Body armour panels | Multi-hit capable |
| Polycarbonate | Lexan ballistic grade | Visor, sensor covers | Optical clarity + impact |
| Rubber bellows | EPDM high-tensile | Abdomen joints, sole | Flex + seal |
| Carbon fibre | T800 CFRP | Drone airframe | 6× steel strength, 70% lighter |

---

## 5. Shield Specification

### 5.1 Overview

| Parameter | Value |
|---|---|
| Type | Deployable back-mounted ballistic shield |
| Deploy mechanism | Motorised pivot arm — swings from back to front |
| Stow position | Flat against robot back — zero protrusion |
| Deploy time | 0.3 seconds — brushless DC pivot motor |
| Deploy trigger | Acoustic gunshot detected OR threat level ≥ 2 |

### 5.2 Shield Dimensions

| Parameter | Value |
|---|---|
| Height | 1,200 mm |
| Width | 700 mm |
| Thickness — face plate | 25 mm boron carbide |
| Thickness — backing | 15 mm UHMWPE (ultra-high-molecular-weight polyethylene) |
| Thickness — frame | 8 mm titanium frame |
| Total thickness | 48 mm |
| Total weight | 18 kg |
| Area covered | 0.84 m² — covers full soldier torso at 2m behind robot |

### 5.3 Protection Levels

| Threat | Protection | Standard |
|---|---|---|
| 7.62×39mm FMJ (AK-47) | ✓ Full stop | NIJ Level III |
| 7.62×51mm NATO M80 | ✓ Full stop | NIJ Level III |
| 7.62×51mm M61 AP | ✓ Full stop | NIJ Level III+ |
| .50 BMG | ✗ Not rated | — |
| IED shrapnel (50g @ 500 m/s) | ✓ Full stop | STANAG 4569 Level 2 |
| Fragmentation grenade (2m) | ✓ Full stop | MIL-DTL-46593 |

### 5.4 Pivot Arm Mechanism

| Parameter | Value |
|---|---|
| Arm length | 420 mm |
| Pivot point | Left chest shoulder socket — secondary mount |
| Motor | 200W brushless DC — Maxon EC-i 40 |
| Gear ratio | 80:1 planetary — for high torque |
| Lock mechanism | Spring-loaded pin — 3-point lock when deployed |
| Angle range | 0° (stowed) to 105° (fully deployed front) |
| Manual override | Pull cord — mechanical release |

---

## 6. Weapons Specification

### 6.1 Primary — Assault Rifle (Left Arm Mount)

| Parameter | Value |
|---|---|
| Weapon type | 7.62×51mm NATO battle rifle |
| Based on | Modified FN SCAR-H mechanism |
| Barrel length | 410 mm |
| Overall length | 880 mm (folded stock — robot does not need stock) |
| Weight (weapon only) | 4.6 kg |
| Magazine capacity | 30 rounds (× 4 magazines = 120 rounds carried) |
| Rate of fire | 600 RPM (semi or burst — AI controlled) |
| Mount type | Picatinny rail — bolts to forearm T-slot |
| Aiming system | Laser rangefinder + ballistic computer in robot AI |
| Recoil management | Hydraulic buffer in mount — absorbs 85% of recoil |
| Auto-reload | Magazine carousel — 4 mags auto-fed by robot hand |

### 6.2 Secondary — 40mm Grenade Launcher (Right Arm)

| Parameter | Value |
|---|---|
| Weapon type | 40mm underbarrel grenade launcher |
| Based on | M320 GLM single-shot mechanism |
| Barrel length | 230 mm |
| Weight | 1.5 kg |
| Grenade capacity | 8 × 40mm grenades — belt on waist |
| Grenade types | HE (high explosive), smoke, flashbang, thermite |
| Effective range | 350 m |
| Muzzle velocity | 76 m/s |
| Mount | Underside of right forearm — fixed rail |
| Reload mechanism | Auto-feed from waist grenade belt — motor driven |

### 6.3 Tertiary — Micro-Missile Pods (Shoulders)

| Parameter | Value |
|---|---|
| Weapon type | Shoulder-mounted micro-missile pods |
| Missiles per pod | 3 per shoulder = 6 total |
| Missile type | Based on Spike SR — fire-and-forget |
| Missile weight | 4 kg each |
| Warhead | Tandem HEAT — 400 mm RHA penetration |
| Range | 50 m minimum — 800 m maximum |
| Guidance | Electro-optical + drone laser designation |
| Pod dimensions | 400 mm × 80 mm × 80 mm per tube |
| Pod material | Carbon fibre composite — 1.2 kg per pod |
| Deploy angle | Pods tilt 0–45° elevation — motorised |
| Fire trigger | AI threat level 3 OR manual command |

### 6.4 Weapons Summary

| Weapon | Rounds | Weight | Range |
|---|---|---|---|
| Assault rifle (7.62 NATO) | 120 rounds | 4.6 kg | 600 m effective |
| Grenade launcher (40mm) | 8 grenades | 1.5 kg + grenades | 350 m |
| Micro-missiles × 6 | 6 missiles | 24 kg total | 800 m |
| **Total weapons load** | | **~38 kg** | |

---

## 7. Drone Specification

### 7.1 Drone 1 — Wide Area Surveillance (Fixed-Wing)

| Parameter | Value |
|---|---|
| Type | Fixed-wing VTOL UAV |
| Wingspan (folded) | 340 mm × 150 mm × 60 mm |
| Wingspan (deployed) | 900 mm |
| Weight | 1.4 kg |
| Airframe material | T800 carbon fibre — 1.2 mm shell |
| Flight time | 45 minutes at cruise |
| Cruise speed | 80 km/h |
| Max speed | 120 km/h |
| Operational range | 800 m from robot |
| Camera | Sony IMX477 — 12.3 MP — 4K60 video |
| Thermal camera | FLIR Lepton 3.5 — 160×120 — 8.7 Hz |
| Comms | 5 GHz encrypted MAVLink — 1 km range |
| Flight controller | PX4 on Pixhawk 6C Mini |
| Launch method | Spring-eject from left back bay — vertical deploy |
| Return | Auto-return-to-robot — lands on back bay |
| Bay dimensions | 340 mm × 160 mm × 70 mm |

### 7.2 Drone 2 — Close Target Tracking (Quadrotor)

| Parameter | Value |
|---|---|
| Type | Quadrotor UAV |
| Folded dimensions | 200 mm × 200 mm × 80 mm |
| Propeller diameter | 150 mm (folds flat) |
| Weight | 0.85 kg |
| Airframe material | T700 carbon fibre |
| Flight time | 22 minutes at hover |
| Max speed | 65 km/h |
| Operational range | 400 m from robot |
| Camera | 4K EO + laser spot designator |
| Thermal | FLIR Lepton 3.5 |
| Comms | 5 GHz mesh — feeds target GPS coords to robot |
| Flight controller | PX4 on Matek H743 |
| Launch method | Pop-up eject from right back bay |
| Special | Laser designator locks target for missile guidance |
| Bay dimensions | 210 mm × 210 mm × 90 mm |

### 7.3 Drone Bay Architecture

```
BACK OF ROBOT (top-down cross section)
┌─────────────────────────────────────────┐
│  [LEFT BAY — Fixed wing drone 1]        │
│  340mm × 160mm × 70mm                  │
│  Spring eject — upward launch           │
├─────────────────────────────────────────┤
│  [Shield mount rail — centre spine]     │
├─────────────────────────────────────────┤
│  [RIGHT BAY — Quadrotor drone 2]        │
│  210mm × 210mm × 90mm                  │
│  Pop-up eject — upward launch           │
└─────────────────────────────────────────┘
```

---

## 8. Armour Specification

### 8.1 Body Armour Layout

| Zone | Panel type | Material | Thickness | NIJ Level | Weight |
|---|---|---|---|---|---|
| Head front | Monolithic plate | Boron carbide B₄C | 20 mm | IV | 1.8 kg |
| Head sides | Spall liner | UHMWPE | 10 mm | IIIA | 0.6 kg |
| Chest front | Large curved plate | Ceramic/UHMWPE composite | 30 mm | IV | 6.2 kg |
| Chest sides | Side plates × 2 | Alumina ceramic mosaic | 20 mm | III+ | 2.8 kg |
| Back plate | Rear armour | UHMWPE + steel | 18 mm | III | 2.4 kg |
| Shoulder caps × 2 | Spaulder style | Alumina ceramic | 15 mm | III | 1.4 kg |
| Upper arm × 2 | Wrap-around | UHMWPE laminate | 8 mm | IIIA | 0.8 kg |
| Forearm × 2 | Vambrace style | Alumina ceramic | 12 mm | III | 1.0 kg |
| Thigh × 2 | Front plate | Ceramic composite | 18 mm | III+ | 2.2 kg |
| Shin × 2 | Full wrap | UHMWPE + ceramic | 15 mm | III | 1.6 kg |
| Foot × 2 | Sole blast plate | Steel 4340 | 20 mm | — | 2.4 kg |
| **Total armour** | | | | | **~27 kg** |

### 8.2 Ground Blast Protection (Underside)

| Parameter | Value |
|---|---|
| Underbelly plate | 20 mm RHA steel + 10 mm UHMWPE |
| Coverage | Full underside of pelvis + inner thigh |
| IED protection | Equivalent to STANAG 4569 Level 3 |
| Shock absorption | Hydraulic leg actuators absorb blast energy — 40 kN rated |

---

## 9. Joint Specification

| Joint | Type | DOF | Range | Peak Torque | Actuator |
|---|---|---|---|---|---|
| Neck pitch | Revolute | 1 | ±30° | 120 N·m | Maxon EC-i 40 |
| Neck yaw | Revolute | 1 | ±90° | 120 N·m | Maxon EC-i 40 |
| Shoulder pitch | Spherical | 1 | ±180° | 280 N·m | Custom brushless |
| Shoulder roll | Spherical | 1 | ±90° | 220 N·m | Custom brushless |
| Shoulder yaw | Spherical | 1 | ±45° | 180 N·m | Custom brushless |
| Elbow pitch | Revolute | 1 | 0–145° | 200 N·m | Maxon EC-i 52 |
| Wrist pitch | Revolute | 1 | ±60° | 80 N·m | Maxon EC-i 30 |
| Wrist roll | Revolute | 1 | ±30° | 60 N·m | Maxon EC-i 30 |
| Hip pitch | Spherical | 1 | ±90° | 360 N·m | Custom hydraulic |
| Hip roll | Spherical | 1 | ±45° | 280 N·m | Custom hydraulic |
| Hip yaw | Spherical | 1 | ±30° | 200 N·m | Custom hydraulic |
| Knee pitch | Revolute | 1 | 0–140° | 360 N·m | Custom hydraulic |
| Ankle pitch | Revolute | 1 | ±40° | 220 N·m | Custom hydraulic |
| Ankle roll | Revolute | 1 | ±20° | 160 N·m | Custom hydraulic |
| **Total DOF** | | **26** | | | |

---

## 10. Sensor Suite

| Sensor | Model | Location | Purpose | Data rate |
|---|---|---|---|---|
| 3D LiDAR | Livox MID-360 | Head top dome | 360° point cloud mapping | 10 Hz |
| Stereo camera front | Intel RealSense D435i | Head front visor | Depth + RGB — obstacle detection | 30 fps |
| Thermal camera | FLIR Boson 640 | Head front | Human heat signature — day/night | 60 Hz |
| Wide camera rear | Sony IMX477 | Head rear | Rear awareness — 120° FOV | 60 fps |
| IMU | VectorNav VN-100 | Chest internal | Balance + orientation | 800 Hz |
| Acoustic array | 4× MEMS mics | Head sides | Gunshot detection + direction | Continuous |
| Foot force sensors | 6-axis F/T sensor | Each foot | Ground contact + balance | 1000 Hz |
| Joint encoders | 14× magnetic encoders | All joints | Joint position + velocity | 1000 Hz |

---

## 11. Power System

| Parameter | Value |
|---|---|
| Battery type | Solid-state lithium — Samsung SDI next-gen cells |
| Capacity | 48 kWh |
| Nominal voltage | 96V DC bus |
| Peak discharge | 800A (76.8 kW peak) |
| Continuous discharge | 200A (19.2 kW) |
| Battery weight | 110 kg |
| Battery location | Chest core — centre of mass |
| Charging | 400V 3-phase — full charge in 2.5 hours |
| BMS | Custom battery management — cell balancing + thermal |
| Thermal management | Liquid cooling — glycol loop through chest |
| Emergency backup | 2× supercapacitor banks — 5 min emergency power |

---

## 12. AI & Compute

| Component | Spec | Role |
|---|---|---|
| Main AI board | NVIDIA Jetson AGX Orin 64GB | Vision + decision AI |
| Performance | 275 TOPS | Runs YOLOv8 + SLAM + Nav2 simultaneously |
| Secondary CPU | Intel Core i7-1370P | ROS2 real-time control |
| Actuator MCU | 14× STM32F4 | One per joint — real-time PWM |
| Drone comms MCU | STM32H7 | MAVLink bridge to both drones |
| Storage | 2TB NVMe SSD | Map data + mission logs |
| OS | Ubuntu 22.04 + ROS2 Jazzy | |
| AI frameworks | PyTorch 2.x + TensorRT | Inference optimisation |
| Vision model | YOLOv8n — fine-tuned threat detection | Gun, grenade, soldier, vehicle, civilian |
| SLAM | RTAB-Map + LiDAR | Live 3D battle map |
| Navigation | Nav2 + Legged Gym policy | Terrain-aware path planning |
| Threat AI | Custom threat level manager node | 0→1→2→3 escalation logic |

---

## 13. URDF Mesh Geometry Guide

> Use this section to build `.stl` mesh files in Blender / FreeCAD, then reference in URDF.

```xml
<!-- Example URDF link structure for chest -->
<link name="chest">
  <visual>
    <geometry>
      <mesh filename="package://ares1_description/meshes/visual/chest.stl"
            scale="0.001 0.001 0.001"/>
    </geometry>
    <material name="dark_grey">
      <color rgba="0.18 0.18 0.19 1.0"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <mesh filename="package://ares1_description/meshes/collision/chest_col.stl"
            scale="0.001 0.001 0.001"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="32.0"/>
    <inertia ixx="0.8" ixy="0.0" ixz="0.0"
             iyy="0.6" iyz="0.0" izz="0.5"/>
  </inertial>
</link>
```

### 13.1 Mesh File List

| Mesh file | Poly count (target) | Notes |
|---|---|---|
| `head.stl` | 800 faces | Chamfered box + dome |
| `neck.stl` | 200 faces | 16-sided tapered cylinder |
| `chest.stl` | 1200 faces | Trapezoidal — detail panels |
| `abdomen_ring.stl` | 300 faces | × 3 instances |
| `pelvis.stl` | 600 faces | Hexagonal prism |
| `shoulder_yoke.stl` | 400 faces | Swept C-channel |
| `upper_arm.stl` | 500 faces | Octagonal tapered |
| `forearm.stl` | 400 faces | Rounded rect tapered |
| `hand.stl` | 800 faces | 4-finger fist |
| `thigh.stl` | 600 faces | Cylinder + flat front |
| `shin.stl` | 400 faces | D-profile |
| `foot.stl` | 500 faces | Heel + toe organic |
| `shield.stl` | 300 faces | Flat plate + frame |
| `missile_pod.stl` | 400 faces | 3-tube pod |
| `drone_fixed_wing.stl` | 600 faces | Folded config |
| `drone_quad.stl` | 400 faces | Folded config |

### 13.2 Blender Modelling Order (Recommended)

```
1. pelvis.stl        ← anchor — everything else builds from here
2. chest.stl         ← largest visual piece
3. thigh × 2
4. shin × 2
5. foot × 2
6. abdomen rings × 3
7. shoulder_yoke
8. upper_arm × 2
9. forearm × 2
10. hand × 2
11. head
12. neck
13. shield
14. missile_pods × 2
15. drones × 2
```

---

## 14. Open-Source Stack

| Layer | Project | GitHub / Source | Modify for ARES-1 |
|---|---|---|---|
| Robot model | Unitree H1 URDF | `unitreerobotics/unitree_ros2` | Scale + add weapon/shield links |
| Physics sim | MuJoCo 3.x | `deepmind/mujoco` | Load H1 MJCF → modify |
| Full sim | Gazebo Harmonic | `gazebosim/gz-sim` | Military terrain worlds |
| AI training | Isaac Lab | `isaac-sim/IsaacLab` | Train gait + combat scenarios |
| Gait RL | Legged Gym | `leggedrobotics/legged_gym` | Define ARES-1 URDF → train |
| Vision | YOLOv8 | `ultralytics/ultralytics` | Fine-tune on weapon + threat data |
| Threat model | YOLOv8n pretrained | `Subh775/Threat-Detection-YOLOv8n` | Add civilian/soldier classes |
| SLAM | RTAB-Map | `introlab/rtabmap_ros` | LiDAR + stereo input |
| Navigation | Nav2 | `ros-navigation/navigation2` | Terrain-aware routing |
| Arm motion | MoveIt2 | `moveit/moveit2` | Shield deploy + weapon aim |
| Drone flight | PX4 Autopilot | `PX4/PX4-Autopilot` | Configure for body-launch |
| Drone coord | XTDrone | `robin-shaun/XTDrone` | 2-drone mesh coordination |
| Visualise | Foxglove Studio | `foxglove/studio` | Already using — extend panels |
| ROS bridge | rosbridge / foxglove-bridge | Already running on port 8765 | Add weapon + threat topics |

---

## Appendix A — ROS2 Topic Architecture

```
/ares1/
├── sensors/
│   ├── lidar/points          ← LiDAR point cloud
│   ├── camera/front/image    ← Front stereo RGB
│   ├── camera/thermal/image  ← Thermal camera
│   ├── imu/data              ← Balance + orientation
│   └── acoustic/direction    ← Gunshot bearing
├── ai/
│   ├── threat_level          ← 0/1/2/3 integer
│   ├── detections            ← YOLOv8 bounding boxes
│   └── battle_map            ← RTAB-Map 3D occupancy
├── actuators/
│   ├── shield/deploy         ← Bool — deploy/stow
│   ├── weapons/rifle/fire    ← Bool + aim vector
│   ├── weapons/grenade/fire  ← Bool + target coords
│   └── missiles/fire         ← Int (which pod) + target
├── drones/
│   ├── drone1/command        ← MAVLink waypoints
│   ├── drone1/telemetry      ← Position + battery
│   ├── drone2/command        ← MAVLink waypoints
│   └── drone2/telemetry      ← Position + laser lock
└── navigation/
    ├── goal_pose             ← Target destination
    ├── path                  ← Planned route
    └── footstep_plan         ← Legged gym policy output
```

---

## Appendix B — Colour Scheme (Simulation + Physical)

| Zone | Colour | RGB | Hex | Purpose |
|---|---|---|---|---|
| Primary body | Dark matte grey | (45, 45, 48) | `#2D2D30` | Low visibility |
| Armour panels | Flat black | (28, 28, 30) | `#1C1C1E` | Absorbs radar |
| Joints | Gunmetal | (72, 72, 76) | `#48484C` | Visible separation |
| Visor | Dark tinted blue | (20, 40, 80) | `#142850` | Polycarbonate tint |
| Weapon rails | Olive drab | (85, 90, 60) | `#555A3C` | Military standard |
| Shield front | Matte charcoal | (55, 55, 58) | `#37373A` | Non-reflective |
| Warning stripes | Amber | (220, 150, 20) | `#DC9614` | Joint safety zones |

---

*ARES-1 Design Specification v1.0.0 — Nik — September 2026*  
*Built on: ROS2 Jazzy | MuJoCo | Foxglove | Ubuntu 22.04*
