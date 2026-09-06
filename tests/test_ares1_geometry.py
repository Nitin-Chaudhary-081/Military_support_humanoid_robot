import subprocess, pathlib, xml.etree.ElementTree as ET, json

def test_ares1_urdf_exists_and_meshes():
    assert pathlib.Path('src/ares1_description/urdf/ares1.urdf.xacro').exists()
    for m in ["head","neck","chest","pelvis","shoulder_yoke","upper_arm","forearm","hand","thigh","shin","foot","shield","missile_pod","drone_fixed_wing","drone_quad","abdomen_ring"]:
        assert pathlib.Path(f'src/ares1_description/meshes/visual/{m}.stl').exists(), f"missing visual {m}.stl"
        assert pathlib.Path(f'src/ares1_description/meshes/collision/{m}_col.stl').exists(), f"missing collision {m}_col.stl"
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
    # mass 402kg weapon-free (447 - shield18 - pods26.4 - drones2.25 - rifle4.6 - launcher1.5 +7.7 chest)
    s = sum(float(m.attrib['value']) for m in root.findall('.//mass'))
    assert 395 < s < 410, f"mass {s} not 402 weapon-free"
    # height: check dome exists
    assert root.find(".//link[@name='sensor_dome']") is not None
    # weapon-free: shield/drones removed — no mounts
    assert root.find(".//link[@name='shield']") is None, "shield should be removed weapon-free"
    assert root.find(".//link[@name='pod_left']") is None
    assert root.find(".//link[@name='drone_fixed_wing']") is None
    assert root.find(".//link[@name='left_rifle']") is None
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
    # weapon-free: shield/pod controllers removed
    assert 'shield_controller' not in data and 'pod_controller' not in data
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
