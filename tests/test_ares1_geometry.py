import subprocess, pathlib, xml.etree.ElementTree as ET, json

def test_ares1_urdf_exists_and_meshes():
    assert pathlib.Path('src/ares1_description/urdf/ares1.urdf.xacro').exists()
    # old 16 meshes deleted entirely per user, replaced with 159 detailed loose parts from Drive FBX
    parts = list(pathlib.Path('src/ares1_description/meshes/visual').glob('part_*.stl'))
    assert len(parts) >= 100, f"expected >=100 detailed parts, got {len(parts)}"
    for p in parts[:3]:
        assert p.exists()
        assert pathlib.Path(f'src/ares1_description/meshes/collision/{p.stem}_col.stl').exists(), f"missing collision {p.stem}_col.stl"
    assert pathlib.Path('mujoco/ares1.xml').exists(), "MJCF placeholder missing"

def test_ares1_xacro_and_mass_budget():
    r = subprocess.run(['xacro','src/ares1_description/urdf/ares1.urdf.xacro'], capture_output=True, text=True)
    assert r.returncode==0, r.stderr
    xml = r.stdout
    assert 'ares1' in xml and 'base_link' in xml
    root = ET.fromstring(xml)
    links = root.findall('link'); joints = root.findall('joint')
    assert len(links) >= 50, f"expected >=50 links with armour, got {len(links)}"
    assert len(joints) >= 50, f"expected >=50 joints, got {len(joints)}"
    # detailed 159 loose parts from Drive FBX now replace old 16 (keep 4 weapon meshes re-added)
    assert 'part_' in xml, "detailed 159 parts missing in URDF"
    assert xml.count('part_') >= 100, f"expected >=100 part refs, got {xml.count('part_')}"
    # mass 447kg full (402 base + weapons) — weapons re-added
    s = sum(float(m.attrib['value']) for m in root.findall('.//mass'))
    assert 440 < s < 455, f"mass {s} not 447 full with weapons"
    # height: check dome exists
    assert root.find(".//link[@name='sensor_dome']") is not None
    # weapons re-added
    assert root.find(".//link[@name='shield']") is not None, "shield should exist with weapons"
    assert root.find(".//link[@name='pod_left']") is not None
    assert root.find(".//link[@name='drone_fixed_wing']") is not None
    assert root.find(".//link[@name='left_rifle']") is not None
    # 26-DOF joints per table 509 must exist
    required = ["neck_yaw","neck_pitch","left_shoulder_yaw","left_shoulder_roll","left_shoulder_pitch","left_elbow","left_wrist_pitch","left_wrist_roll",
                "right_shoulder_yaw","right_shoulder_roll","right_shoulder_pitch","right_elbow","right_wrist_pitch","right_wrist_roll",
                "left_hip_yaw","left_hip_roll","left_hip_pitch","left_knee","left_ankle_pitch","left_ankle_roll",
                "right_hip_yaw","right_hip_roll","right_hip_pitch","right_knee","right_ankle_pitch","right_ankle_roll"]
    joint_names = {j.attrib['name'] for j in joints}
    for n in required:
        assert n in joint_names, f"missing DOF {n}"
    # armour separate links
    assert root.find(".//link[@name='armour_chest_front']") is not None
    assert root.find(".//link[@name='armour_head_front']") is not None

def test_ares1_controllers_26dof():
    import yaml
    p = pathlib.Path('src/ares1_description/config/ares1_controllers.yaml')
    assert p.exists()
    data = yaml.safe_load(p.read_text())
    j = data['ares1_controller']['ros__parameters']['joints']
    assert len(j) == 26, f"expected 26 joints, got {len(j)}"
    assert 'neck_yaw' in j and 'left_knee' in j and 'right_ankle_roll' in j
    # weapons re-added: shield/pod controllers present
    assert data['shield_controller']['ros__parameters']['joints'] == ['shield_pivot']
    assert 'pod_left_joint' in data['pod_controller']['ros__parameters']['joints']
    # check torque-relevant joints present per arc.md 509
    assert 'left_shoulder_pitch' in j

def test_ares1_sensors():
    r = subprocess.run(['xacro','src/ares1_description/urdf/ares1.urdf.xacro'], capture_output=True, text=True)
    xml = r.stdout
    assert '/ares1/sensors/lidar/points' in xml  # Livox MID-360
    assert '/ares1/sensors/camera/front/image' in xml
    assert '/ares1/sensors/imu/data' in xml
    assert '/ares1/sensors/foot/left/ft' in xml
    assert '/ares1/sensors/acoustic/direction' in xml

def test_mujoco_placeholder():
    txt = pathlib.Path('mujoco/ares1.xml').read_text()
    assert '<mujoco' in txt and 'ares1' in txt
    assert 'meshdir="../src/ares1_description/meshes/visual"' in txt
