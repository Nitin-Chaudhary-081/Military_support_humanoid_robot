import subprocess, pathlib, xml.etree.ElementTree as ET

def test_urdf_exists():
    p=pathlib.Path('src/acsr_description/urdf/acsr.urdf.xacro')
    assert p.exists(), "URDF xacro missing"

def test_xacro_processes():
    r=subprocess.run(['xacro','src/acsr_description/urdf/acsr.urdf.xacro'], capture_output=True, text=True)
    assert r.returncode==0, r.stderr
    xml=r.stdout
    assert 'base_link' in xml and 'shield_pivot' in xml
    root=ET.fromstring(xml)
    links=root.findall('link')
    joints=root.findall('joint')
    assert len(links) >= 12
    # shield is revolute with limits
    shield=[j for j in joints if j.attrib.get('name')=='shield_pivot'][0]
    assert shield.attrib['type']=='revolute'
    lim=shield.find('limit')
    assert float(lim.attrib['upper']) > 1.5

def test_urdf_mass_positive():
    r=subprocess.run(['xacro','src/acsr_description/urdf/acsr.urdf.xacro'], capture_output=True, text=True)
    root=ET.fromstring(r.stdout)
    masses=[float(m.attrib['value']) for m in root.findall('.//mass')]
    assert sum(masses) > 400  # 450kg spec approx
