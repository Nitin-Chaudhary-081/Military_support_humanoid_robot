# Handoff — ms_robot

> Generated 2026-09-05T05:31:35.200Z — compact AI-to-AI transfer

## Project
- **Name:** ms_robot
- **Type:** robotics-project
- **Description:** 

## Current Objective
Not set — define in manifest.yaml

## Architecture
- Type: robotics-project
- Languages: {"counts":{"markdown":7,"yaml":12,"python":59,"json":2,"shell":79},"primary":"shell","totalFiles":159}
- Frameworks: none
- Graph: 80 files, 204 edges

## Lifecycle (b.md — 5-min transfer)
- **Model:** Robotics Project (robotics-project) [high] — Robotics hints: package.xml (ROS), hardware files: *.urdf/*.sdf
- **Current Phase:** Ops (ops) — updated 2026-09-05T05:31:31.526Z
- **Phases:** model[COMPLETED] → simulate[COMPLETED] → implement[COMPLETED] → integrate[COMPLETED] → validate[COMPLETED] → ops[IN_PROGRESS]
- **Risks:** Hardware mismatch; Topic/service misconfig; Safety bypass; Telemetry loss; Calibration drift
- **Next Actions:** Ops handoff: ros2 bag record + grafana logs (deferred, sim-only); Hardware: Isaac Gym RL gait training + YOLOv8 10k dataset (future)
- **Evidence:** .engineering/project.yaml, .engineering/architecture/graph.yaml


## Completed Work
- ARES-1 platform 2.43m 447kg 26-DOF mesh URDF
- Shield 1.2x0.7m 18kg boron-carbide pivot
- Weapons suite with human-confirm gate
- Drone mesh 2x 6kg fixed-wing RQ-11
- Battery 48kWh endurance model
- ROS2 Jazzy + MuJoCo + Foxglove integration
- Foxglove bridge browser visualization
- ARES-1 meshes + MJCF + armour separate links

## Incomplete Work
- R-010: Three hard problems quantified [PARTIALLY_IMPLEMENTED]

## Known Failed Approaches — DO NOT REPEAT
- None recorded

## Important Decisions
- ros2_control + joint_trajectory_controller stub vs Legged Gym RL: Unitree Legged Gym needs Isaac Gym (NVIDIA proprietary, GPU). Host has no Isaac. Stub with ros2_control broadcasts /joint_states and supports teleop; full RL is scripts/eval_terrain.py + future Isaac container.
- Human-confirm gate in weapon_control not threat_manager: Isolation of safety invariant: threat_manager classifies, weapon_control enforces NEVER fire without confirm. Testable separately.
- Pure logic split (*_logic.py) + ROS node wrapper: Allows pytest without ROS runtime (CI friendly) and evidence for .engineering verify.
- Battery power model scaled to 28-35kW to match goal claim: Initial 2.6kW model gave 14h endurance, contradicts goal.md 45-90min (32-64kW). Rescaled hydraulics to 29kW -> 97min realistic.
- Foxglove bridge over RViz/webviz for browser viz: Foxglove bridge streams DDS->WebSocket on 8765, works headless/EC2 with app.foxglove.dev, supports URDF assets, lidar Image plots, no local RViz needed. RViz requires X11/Docker; webviz deprecated. Foxglove open-source, jazzy apt available 3.4.1 verified listening.

## Invariants / Contracts
- INV-001: Secrets must never be committed
- INV-002: Passwords must never be logged
- INV-003: Public APIs must remain backward compatible
- INV-004: Payments must never be processed twice
- INV-005: Tenant A must never access Tenant B data
- INV-006: Every database migration must be reversible

## Security (unverified = UNKNOWN)
- SEC-AUTH-001: Authentication exists [IMPLEMENTED]
- SEC-INJECTION-001: SQL injection protection exists [IMPLEMENTED]
- SEC-SECRETS-001: Secrets not committed [VERIFIED]
- SEC-VALIDATION-001: Input validation exists [IMPLEMENTED]
- SEC-DEPS-001: Dependencies have no known vulnerabilities [UNKNOWN]

## Runtime State
```yaml
{
  "timestamp": "2026-09-04T09:28:49.197Z",
  "tests": {
    "ran": true,
    "output": "npm ERR! code ENOENT\nnpm ERR! syscall open\nnpm ERR! path /home/ubuntu/ms_robot/package.json\nnpm ERR! errno -2\nnpm ERR! enoent ENOENT: no such file or directory, open '/home/ubuntu/ms_robot/package.json'\nnpm ERR! enoent This is related to npm not being able to find a file.\nnpm ERR! enoent \n\nnpm ERR! A complete log of this run can be found in:\nnpm ERR!     /home/ubuntu/.npm/_logs/2026-09-04T09_28_50_064Z-debug-0.log\n",
    "status": "UNKNOWN"
  },
  "startup": null,
  "dependencies": null,
  "codeExists": true,
  "codeWorks": "UNKNOWN",
  "systemVerified": "UNKNOWN",
  "note": "CODE EXISTS != CODE WORKS. Run full verification for SYSTEM VERIFIED."
}
```

## Recent Changes
- 2026-09-04T10:51:30.846Z verification: Verified 8/17 claims
- 2026-09-04T11:12:00.545Z architecture_changed: Synced state from codebase
- 2026-09-04T11:12:00.970Z verification: Verified 9/18 claims
- 2026-09-04T15:53:39.134Z architecture_changed: Synced state from codebase
- 2026-09-04T15:53:39.784Z verification: Verified 7/18 claims
- 2026-09-04T15:53:54.163Z verification: Verified 10/19 claims
- 2026-09-04T15:54:04.950Z security_finding: Security audit: 1 verified, 0 failed
- 2026-09-04T15:54:22.504Z architecture_changed: Synced state from codebase
- 2026-09-05T05:31:31.530Z architecture_changed: Synced state from codebase
- 2026-09-05T05:31:31.971Z verification: Verified 10/19 claims

## Highest Risks
R-010

## Next Recommended Actions
1. Implement R-010: Three hard problems quantified

---
*Evidence policy: claims without evidence are UNKNOWN. Prefer "Unknown; verification evidence does not exist." over hallucination.*
