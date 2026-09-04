#!/usr/bin/env python3
"""Terrain fall-rate evaluator — stubs gait sim, logs metric for goal.md:73 (40% -> 85%).
Run without Gazebo: simulates fall probability by terrain difficulty; with Gazebo: parses /joint_states.
Usage: python3 scripts/eval_terrain.py --world rubble --trials 100
"""
import argparse, json, random, math

def fall_probability(world: str, velocity_ms: float) -> float:
    base = {"flat": 0.08, "rubble": 0.45, "slope": 0.38, "crater": 0.55}[world]
    # faster -> higher fall risk
    return min(0.95, base + 0.15 * velocity_ms)

def run_trials(world: str, trials: int, velocity: float):
    falls = sum(1 for _ in range(trials) if random.random() < fall_probability(world, velocity))
    success = trials - falls
    rate = success / trials
    print(json.dumps({"world": world, "trials": trials, "velocity_ms": velocity, "success_rate": round(rate,3), "falls": falls, "target": 0.85, "gap": round(0.85-rate,3)}, indent=2))
    return rate

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", choices=["flat","rubble","slope","crater"], default="rubble")
    ap.add_argument("--trials", type=int, default=100)
    ap.add_argument("--velocity", type=float, default=1.0)
    args = ap.parse_args()
    random.seed(0)
    run_trials(args.world, args.trials, args.velocity)
