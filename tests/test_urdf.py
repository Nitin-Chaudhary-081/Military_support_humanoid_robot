import subprocess, pathlib, xml.etree.ElementTree as ET

def test_urdf_exists():
    p=pathlib.Path('src/ares1_description/urdf/ares1.urdf.xacro')
    assert p.exists(), "URDF xacro missing"

def test_xacro_processes():
    r=subprocess.run(['xacro','src/ares1_description/urdf/ares1.urdf.xacro'], capture_output=True, text=True)
    assert r.returncode==0, r.stderr
    xml=r.stdout
    assert 'base_link' in xml # weapon-free clean no mounts
    root=ET.fromstring(xml)
    links=root.findall('link')
    joints=root.findall('joint')
    assert len(links) >= 12
    # weapon-free: no shield, verify 26-DOF still present
    assert root.find(".//joint[@name='left_shoulder_yaw']") is not None
    assert root.find(".//link[@name='shield']") is None

def test_urdf_mass_positive():
    r=subprocess.run(['xacro','src/ares1_description/urdf/ares1.urdf.xacro'], capture_output=True, text=True)
    root=ET.fromstring(r.stdout)
    masses=[float(m.attrib['value']) for m in root.findall('.//mass')]
    assert 395 < sum(masses) < 410  # 402kg weapon-free clean no mounts
