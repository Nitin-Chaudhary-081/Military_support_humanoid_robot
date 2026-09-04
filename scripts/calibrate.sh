#!/bin/bash
# Calibrate/check ACSR sim — ops phase, no hardware
set -e
source /opt/ros/jazzy/setup.bash
[ -f install/setup.bash ] && source install/setup.bash
echo "== URDF =="
xacro src/acsr_description/urdf/acsr.urdf.xacro > /tmp/acsr_cal.urdf
check_urdf /tmp/acsr_cal.urdf
echo "== mass check =="
python3 -c "import xml.etree.ElementTree as ET; r=ET.parse('/tmp/acsr_cal.urdf').getroot(); print('masses', round(sum(float(m.attrib['value']) for m in r.findall('.//mass')),1), 'kg')"
echo "== worlds =="
ls -lh src/acsr_gazebo/worlds/*.sdf
echo "== colcon =="
colcon build --symlink-install --packages-select acsr_description acsr_gazebo 2>&1 | tail -n 3
echo "== pytest =="
python3 -m pytest tests/ -q
echo "== battery eval =="
python3 scripts/eval_battery.py | head -n 10
echo "== perception eval =="
python3 scripts/eval_perception.py | head -n 12
echo "== calibrate done =="
