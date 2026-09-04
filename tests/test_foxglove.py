import pathlib, subprocess, xml.etree.ElementTree as ET

def test_foxglove_config_exists():
    p = pathlib.Path("src/acsr_bringup/config/foxglove_bridge.yaml")
    assert p.exists(), "foxglove_bridge.yaml missing"
    txt = p.read_text()
    assert "8765" in txt and "use_sim_time" in txt

def test_foxglove_launch_exists():
    assert pathlib.Path("src/acsr_bringup/launch/foxglove.launch.py").exists()
    assert pathlib.Path("src/acsr_bringup/launch/acsr_full.launch.py").exists()
    txt = pathlib.Path("src/acsr_bringup/launch/acsr_full.launch.py").read_text()
    assert "foxglove_bridge" in txt and "use_foxglove" in txt

def test_foxglove_layout_exists():
    p = pathlib.Path("src/acsr_bringup/config/foxglove/acsr_layout.json")
    assert p.exists()
    import json
    j = json.loads(p.read_text())
    assert "configById" in j and "3D" in j["configById"]

def test_foxglove_bridge_installed():
    r = subprocess.run(["bash","-lc","source /opt/ros/jazzy/setup.bash && ros2 pkg list | grep foxglove_bridge"], capture_output=True, text=True)
    assert "foxglove_bridge" in r.stdout

def test_foxglove_yaml_valid():
    import yaml
    y = yaml.safe_load(pathlib.Path("src/acsr_bringup/config/foxglove_bridge.yaml").read_text())
    assert "/**" in y
    params = y["/**"]["ros__parameters"]
    assert params["port"] == 8765
    assert isinstance(params["topic_whitelist"], list)
