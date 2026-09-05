#!/usr/bin/env python3
"""Generate procedural trimesh STL placeholders for ARES-1 per arc.md 13.1/13.2
All dims in mm -> convert to meters for STL (scale 0.001 in URDF would double-scale, so we export in meters directly and use scale 1).
Uses trimesh creation primitives; repurposes box/cylinder where no exact primitive.
Targets: poly counts approx; not CAD-perfect but convex, collision-friendly.
"""
import trimesh
import numpy as np
import pathlib
import math

out_v = pathlib.Path("src/ares1_description/meshes/visual")
out_c = pathlib.Path("src/ares1_description/meshes/collision")
# ensure dirs
out_v.mkdir(parents=True, exist_ok=True)
out_c.mkdir(parents=True, exist_ok=True)

# In arc.md meshes are defined in mm, we work in meters (mm/1000)
def write_mesh(name, mesh, target_faces):
    # trimesh already has faces; we can subdivide or decimate? Keep as is, target is guideline
    mesh.export(out_v / f"{name}.stl")
    # collision decimated ~30% faces: simple export same for now; real decimation needs fast simplify -> just export same
    # For collision, create convex hull to reduce complexity
    try:
        hull = mesh.convex_hull
        hull.export(out_c / f"{name}_col.stl")
    except:
        mesh.export(out_c / f"{name}_col.stl")
    print(f"{name}: visual {len(mesh.faces)} faces, collision {len(mesh.faces)} -> files")

# 1 pelvis.stl — hexagonal prism 460x260x180 chamfered 12-face
def pelvis():
    # Use cylinder with 6 sides scaled to width/depth
    m = trimesh.creation.cylinder(radius=0.23, height=0.180, sections=6)
    # scale x/y to get width 460 and depth 260: radius 0.23 gives hex width ~0.46, depth ~0.40? approximate
    # Instead create box hex: use transform scale
    # hex with flat top: width = 2*r, depth ~ sqrt(3)*r
    # solve r for width 0.46 -> r=0.23, depth =0.398 too large vs 0.26, so scale y
    m.apply_scale([1.0, 0.65, 1.0])
    return m

# 2 chest.stl — trapezoidal prism 520->440 x 280 x 380, 1200 faces target
def chest():
    # Create trapezoidal prism via vertices
    top_w, bot_w, depth, height = 0.520, 0.440, 0.280, 0.380
    # 8 vertices
    vertices = np.array([
        [-top_w/2, -depth/2, height/2],
        [ top_w/2, -depth/2, height/2],
        [ top_w/2,  depth/2, height/2],
        [-top_w/2,  depth/2, height/2],
        [-bot_w/2, -depth/2, -height/2],
        [ bot_w/2, -depth/2, -height/2],
        [ bot_w/2,  depth/2, -height/2],
        [-bot_w/2,  depth/2, -height/2],
    ])
    faces = np.array([
        [0,1,2],[0,2,3], # top
        [4,7,6],[4,6,5], # bottom
        [0,4,5],[0,5,1], # front
        [1,5,6],[1,6,2], # right
        [2,6,7],[2,7,3], # back
        [3,7,4],[3,4,0], # left
    ])
    m = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
    return m

# 3 thigh — cylindrical flat front Ø200 L520 (20-sided) — origin at TOP (joint attachment) per visual-assembly fix
def thigh():
    m = trimesh.creation.cylinder(radius=0.10, height=0.520, sections=20)
    m.apply_translation([0, 0, -0.260])
    return m

# 4 shin — D-profile extrusion 160x140x480 (32 faces target) -> use box as proxy — origin at TOP
def shin():
    m = trimesh.creation.box(extents=[0.160, 0.140, 0.480])
    m.apply_translation([0, 0, -0.240])
    return m

# 5 foot — organic foot 380x200 heel80 toe40 — origin at ankle TOP (0,0,0) toe forward +X
def foot():
    heel = trimesh.creation.box(extents=[0.220, 0.200, 0.080])
    heel.apply_translation([-0.080, 0, 0.040])  # heel behind (-X)
    toe = trimesh.creation.box(extents=[0.160, 0.200, 0.040])
    toe.apply_translation([0.100, 0, 0.020])   # toe forward (+X)
    m = trimesh.util.concatenate([heel, toe])
    m.apply_translation([0, 0, -0.080])
    return m

# 6 abdomen_ring — 300 faces target, cylinder 360 outer 300 inner 60 height
def abdomen():
    m = trimesh.creation.cylinder(radius=0.180, height=0.060, sections=24)
    return m

# 7 shoulder_yoke — swept C-channel 640 span 80x120 ball housing 110
def shoulder_yoke():
    m = trimesh.creation.box(extents=[0.640, 0.120, 0.080])
    return m

# 8 upper_arm — octagonal tapered 120x100 ->100x85 L380 — origin at TOP (shoulder)
def upper_arm():
    m = trimesh.creation.cylinder(radius=0.060, height=0.380, sections=8)
    m.apply_translation([0, 0, -0.190])
    return m

# 9 forearm — rounded rect 100x85->90x75 L340 — origin at TOP (elbow)
def forearm():
    m = trimesh.creation.box(extents=[0.100, 0.085, 0.340])
    m.apply_translation([0, 0, -0.170])
    return m

# 10 hand — 4-finger fist 140x90x160 64 faces — origin at TOP (wrist)
def hand():
    m = trimesh.creation.box(extents=[0.140, 0.090, 0.160])
    m.apply_translation([0, 0, -0.080])
    return m

# 11 head — chamfered box 280x260x240 ONLY (dome removed; sensor_dome sphere provides visor per fix)
def head():
    m = trimesh.creation.box(extents=[0.280, 0.260, 0.240])
    return m

# 12 neck — tapered cylinder 70->90 diam 120 height
def neck():
    m = trimesh.creation.cylinder(radius=0.040, height=0.120, sections=16)
    return m

# 13 shield — flat plate 1200x700x48 (25+15+8) 300 faces
def shield():
    m = trimesh.creation.box(extents=[0.048, 0.700, 1.200])
    return m

# 14 missile_pod — 3-tube pod 400x80x80 each tube
def missile_pod():
    # 3 tubes side by side
    pods = []
    for i in [-1,0,1]:
        t = trimesh.creation.cylinder(radius=0.040, height=0.400, sections=12)
        t.apply_transform(trimesh.transformations.rotation_matrix(math.radians(90), [0,1,0]))
        t.apply_translation([0, i*0.080, 0])
        pods.append(t)
    m = trimesh.util.concatenate(pods)
    return m

# 15 drone_fixed_wing — folded 340x150x60 deployed 900
def drone_fixed_wing():
    m = trimesh.creation.box(extents=[0.340, 0.150, 0.060])
    return m

# 16 drone_quad — folded 200x200x80 prop 150
def drone_quad():
    m = trimesh.creation.box(extents=[0.200, 0.200, 0.080])
    return m

generators = {
    "pelvis": pelvis,
    "chest": chest,
    "thigh": thigh,
    "shin": shin,
    "foot": foot,
    "abdomen_ring": abdomen,
    "shoulder_yoke": shoulder_yoke,
    "upper_arm": upper_arm,
    "forearm": forearm,
    "hand": hand,
    "head": head,
    "neck": neck,
    "shield": shield,
    "missile_pod": missile_pod,
    "drone_fixed_wing": drone_fixed_wing,
    "drone_quad": drone_quad,
}

targets = {"head":800,"neck":200,"chest":1200,"abdomen_ring":300,"pelvis":600,"shoulder_yoke":400,"upper_arm":500,"forearm":400,"hand":800,"thigh":600,"shin":400,"foot":500,"shield":300,"missile_pod":400,"drone_fixed_wing":600,"drone_quad":400}

for name, fn in generators.items():
    try:
        mesh = fn()
        write_mesh(name, mesh, targets.get(name, 400))
    except Exception as e:
        print(f"FAILED {name}: {e}")
        raise
print("done 16 meshes")
