#!/bin/bash
# Calibrate/check ARES-1 per arc.md — ops phase, no hardware
set -e
source /opt/ros/jazzy/setup.bash
[ -f install/setup.bash ] && source install/setup.bash
echo "== URDF ares1 2430mm 447kg 26-DOF =="
xacro src/ares1_description/urdf/ares1.urdf.xacro > /tmp/ares1_cal.urdf
check_urdf /tmp/ares1_cal.urdf
echo "== mass check (target 447kg) =="
python3 -c "import xml.etree.ElementTree as ET; r=ET.parse('/tmp/ares1_cal.urdf').getroot(); print('masses', round(sum(float(m.attrib['value']) for m in r.findall('.//mass')),1), 'kg', 'links', len(r.findall('.//link')), 'joints', len(r.findall('.//joint')))"
echo "== worlds =="
ls -lh src/acsr_gazebo/worlds/*.sdf
echo "== mujoco =="
ls -lh mujoco/ares1.xml 2>&1 | head -n 5
echo "== colcon ares1 ==="
colcon build --symlink-install --packages-select ares1_description acsr_gazebo 2>&1 | tail -n 3
echo "== pytest =="
python3 -m pytest tests/ -q
echo "== battery eval =="
python3 scripts/eval_battery.py | head -n 10
echo "== perception eval =="
python3 scripts/eval_perception.py | head -n 12
echo "== calibrate done =="
