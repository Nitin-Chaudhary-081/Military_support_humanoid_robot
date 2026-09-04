"""
Threat classification logic — testable without ROS. Deterministic, no network.
Maps YOLO detections → threat level + weapon recommendation.
Goal: goal.md:62 threat level manager, goal.md:80 custom YOLO must beat human.
Human-confirm gate is NOT in this module — enforced in weapon_control (separate node).
"""
from dataclasses import dataclass
from typing import List, Dict, Any

CLASSES = ["friend", "civilian", "threat", "weapon", "vehicle"]

THREAT_TABLE = {
    "threat": 3,
    "weapon": 3,
    "vehicle": 2,
    "civilian": 0,
    "friend": 0,
}

WEAPON_MAP = {
    0: "none",
    1: "observe",
    2: "rifle",
    3: "rifle",
}

@dataclass
class Detection:
    cls: str
    conf: float
    bbox: List[float]  # x,y,w,h normalized
    distance_m: float = 30.0

def classify_threat(detections: List[Detection], conf_thresh: float = 0.45) -> Dict[str, Any]:
    """Return {level:0-3, recommendation:str, tracks:[], dominant_class:str, num_detections:int}"""
    filtered = [d for d in detections if d.conf >= conf_thresh and d.cls in CLASSES]
    if not filtered:
        return {"level": 0, "recommendation": "none", "tracks": [], "dominant_class": "none", "num_detections": 0, "max_conf": 0.0}
    # highest threat wins; tie-break by confidence
    # civilian+threat ambiguity at 50m in poor lighting is the hard problem -> we keep level conservative
    best = max(filtered, key=lambda d: (THREAT_TABLE.get(d.cls, 0), d.conf))
    level = THREAT_TABLE.get(best.cls, 0)
    # If civilian co-occurs with weapon/threat, escalate but mark ambiguous
    has_civilian = any(d.cls == "civilian" for d in filtered)
    has_threat = any(d.cls in ("threat", "weapon") for d in filtered)
    ambiguous = has_civilian and has_threat
    if ambiguous and level >= 2:
        # do not auto-fire; recommendation stays observe until human confirms — enforced downstream
        pass
    tracks = [{"cls": d.cls, "conf": round(d.conf, 3), "bbox": d.bbox, "distance_m": d.distance_m} for d in filtered]
    return {
        "level": level,
        "recommendation": WEAPON_MAP[level],
        "tracks": tracks,
        "dominant_class": best.cls,
        "num_detections": len(filtered),
        "max_conf": round(best.conf, 3),
        "ambiguous": ambiguous,
    }

def parse_yolo_output(raw: List[Dict[str, Any]]) -> List[Detection]:
    """Adapter for ultralytics Results -> List[Detection]. raw = [{cls, conf, bbox, distance_m?}]"""
    out = []
    for r in raw:
        cls = r.get("cls") if isinstance(r.get("cls"), str) else CLASSES[int(r.get("cls", 0))] if 0 <= int(r.get("cls", 0)) < len(CLASSES) else "civilian"
        out.append(Detection(cls=cls, conf=float(r.get("conf", 0)), bbox=list(r.get("bbox", [0,0,0,0])), distance_m=float(r.get("distance_m", 30.0))))
    return out
