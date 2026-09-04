# Project: Autonomous Combat Support Robot (ACSR)

## Project Vision & Purpose

### Mission
> **To build an autonomous ground combat robot that protects human soldiers and reduces human death on the battlefield.**

The robot acts as both **shield and striker** — it physically absorbs incoming fire, carries two surveillance drones to expand the squad's awareness, and engages hostile targets while keeping humans out of the line of fire. Its ultimate goal is to move humans out of the most dangerous frontline roles entirely, replacing flesh-and-blood soldiers in lethal zones with a machine that can be rebuilt.

### The End Goal
1. **A 2.5-meter, 450 kg autonomous bipedal combat robot** that walks any terrain.
2. **Human-out-of-the-loop threat response** — the AI identifies and tracks threats faster than a human, with the human confirming lethal action.
3. **Squad force multiplication** — one robot + two drones extends the awareness and striking range of an entire infantry squad.
4. **A deployable, field-ready system** solving the three hardest problems: terrain navigation, AI decision reliability, and battery endurance.

---

## Problem Statement — Why This Is Needed

Human soldiers face unacceptable risk in modern combat:

- **Direct fire exposure** — soldiers must close with the enemy, taking fire in the process.
- **Bounded human awareness** — a human sees what's in front of them; they cannot watch 360° or see over hills, walls, and rooftops.
- **Human physical limits** — exhaustion, fear, hesitation, and panic degrade performance under fire. Autonomous AI never freezes.
- **The human cost** — every soldier killed or wounded is a permanent, irreplaceable loss to a unit and a nation.

**The gap:** Existing military robots are single-purpose and disconnected — sentry guns (Samsung SGR-A1), experimental walkers (Boston Dynamics Atlas), and micro-drones (Black Hornet) all exist *separately*. No system combines full protection, full awareness, and full firepower into **one integrated autonomous unit**. That integration is what this project builds.

---

## Design Overview

### Platform Specification

| Attribute | Value |
|-----------|-------|
| Height | 2.5 m |
| Weight | 450 kg |
| Locomotion | Bipedal hydraulic legs |
| Center of mass | Low (110 kg chest battery) |
| Operational load | Full combat patrol |

### The Shield System
- **Material:** Boron carbide — the same material used in US military body armor and Bradley IFV protection.
- **Size:** 1.2 m × 0.7 m
- **Weight:** 18 kg
- **Stops:** Rifle rounds and shrapnel
- **Mechanism:** Strapped to the back while moving (like a soldier's pack); swings forward on a pivot arm and deploys when under fire. Same bracing geometry used by riot police shields.
- **Actuation:** Shoulder actuators handle the pivot easily — far stronger than the 10–15 kg shields real soldiers carry.

### The Weapons Suite
| System | Notes |
|--------|-------|
| 7.62 mm assault rifle | ~15 Nm recoil torque — absorbed by braced stance + gyroscopic stabilization |
| 40 mm grenade launcher | Underslung, proven M203/M320 geometry |
| Micro-missiles | Based on Spike SR (4 kg, one-hand size) |
| Drone mesh | Two fold-flat surveillance drones (6 kg), fixed-wing for wide-area (RQ-11 Raven class) |

### The AI & Compute
- **Perception:** LiDAR sensor head + multi-camera vision
- **Compute:** NVIDIA Jetson AGX Orin (275 TOPS) — runs YOLOv8 object detection at 60+ FPS while simultaneously handling navigation, sensor fusion, and drone coordination.
- **Decision logic:** Threat level manager node that processes sensor data, coordinates drones, classifies targets, and selects weapon response.

### Real-World Equivalent
DARPA's **Squad X** program already gives autonomous robots threat identification, terrain navigation, and soldier coordination — the closest existing program to this concept.

---

## The Three Hard Problems (The Real Engineering Work)

These three problems are the only gap between this design and a deployable system. Everything else — physics, mechanics, weapons, shield, drones — is proven technology.

### 1. Terrain Navigation
**The problem:** Battlefields are mud, rubble, craters, slopes, and debris. A 450 kg robot that falls is catastrophic — it cannot right itself under fire and becomes an obstacle blocking the soldiers it protects. Atlas falls on flat ground; rough terrain is exponentially harder.

**The path:** Adaptive gait learning via reinforcement learning (Unitree Legged Gym / ETH Zurich approach). If solved, the robot moves from "works in ~40% of scenarios" to "85%+". The remaining 15% — vertical cliffs, deep water — no ground robot handles.

### 2. AI Decision Reliability
**The problem:** Distinguishing a civilian holding a phone from a soldier holding a weapon at 50 m in poor lighting is currently beyond autonomous AI. Every military that has tested this hits the same wall. This is the legal and ethical blocker for autonomous weapons worldwide.

**The path:** A custom-trained YOLOv8 model + a threat-level manager that passes a documented reliability threshold **above human soldier performance**. This is the biggest unlock — it transforms the robot from a support unit into a genuine frontline autonomous combatant.

### 3. Battery Endurance
**The problem:** 48 kWh sounds large, but a 450 kg robot walking, running actuators, firing weapons, and streaming drone video simultaneously draws enormous current. Realistic full-combat runtime: **45–90 minutes**, not 4 hours.

**The path:** Solid-state battery density improves ~8%/year. Pushing that curve — or adding a small hydrogen fuel cell as a range extender — extends runtime to 6–8 hours, making the robot truly self-sufficient for a full combat patrol.

---

## The Open-Source Software Stack

We build on proven open-source foundations — assembling modules and writing the glue code between them, exactly how real robotics engineering works.

| Layer | Tool | Role |
|-------|------|------|
| **Simulation** | Gazebo | Cost-free testing of 1000s of scenarios before touching hardware |
| **Locomotion** | Unitree Legged Gym (RL) | Train bipedal gait — how Unitree, ANYbotics, ETH Zurich built their walkers |
| **Perception** | YOLOv8 (custom-trained) | Threat / friend / civilian / object detection |
| **Navigation** | Nav2 | Terrain-aware path planning |
| **Middleware** | ROS 2 | All nodes communicate — perception, locomotion, drones, weapons, shield |
| **Custom nodes** | Threat manager, weapon control, shield deployment | The glue code that makes it a single integrated system |

### Compute Hardware
- **NVIDIA Jetson AGX Orin** (275 TOPS, 64 GB) — the standard for serious military robotics teams.
- Runs YOLOv8 at 60 FPS + navigation + sensor fusion + drone coordination simultaneously.

### Build Phases (Simulation First)
1. **Simulation only** — Gazebo + full robot model. Costs nothing, breaks nothing.
2. **Gait training** — reinforcement learning in Legged Gym.
3. **Perception** — train + validate the YOLOv8 threat model.
4. **Drone coordination** — mesh integration with both UAVs.
5. **Physical hardware** — only after software is proven in simulation.

### Design Principle
> **The software stack is battery-agnostic.** As battery technology improves, the software needs zero changes. Software is solved once; hardware endurance is a material science problem on a separate track.

---

## What Success Looks Like

A 2.5 m, 450 kg autonomous combat robot that:
- Walks any terrain without falling
- Makes threat decisions faster and more reliably than a human
- Runs 6–8 hours on a single charge
- Protects soldiers behind a deployable boron-carbide shield
- Flies two surveillance drones for 360° awareness
- Engages targets with rifle, grenades, and micro-missiles
- Does all of this **without breaking a single physics rule**

Every component exists today. The three hard problems are the only engineering gap. This is not science fiction — it is an engineering roadmap built on proven, fielded technology and open-source foundations.



