Problem Summary
Your current robot has two different models mixed together:
Old model – Made of simple shapes (boxes, cylinders, spheres) for armour, joints, shoulder yoke, sensor dome, etc.
New human meshes – The detailed body parts (.stl / .obj) that you imported (pelvis, chest, arms, legs, head, etc.).
Because of this mix:
You still see many boxes and cylinders.
The human body parts appear in wrong positions and orientations.
The limbs and torso are not properly connected.
Root cause:
The joint origins and the local coordinate systems of the new human meshes do not match. The meshes were created with different pivot points and orientations than what the current URDF expects.
Goal
Make the robot show only the detailed human meshes, properly connected and oriented, without the old boxes/cylinders.
Solution Plan (for Coding Assistant)
Please do the following steps carefully:
1. Clean the URDF – Remove all primitive geometry
In src/ares1_description/urdf/ares1.urdf.xacro:
Delete every <geometry> that uses <box>, <cylinder>, or <sphere>.
Keep only the <mesh> geometries that point to the human body parts.
Also remove or comment out the armour links that only contain boxes (armour_chest_front, armour_back, armour_shoulder_caps, sensor_dome, etc.) if they are not needed for the visual model.
2. Fix mesh origins and joint transforms
For every human body part, the mesh origin must be aligned with its parent joint.
Typical corrections needed:
Link
Common fix needed
pelvis
Usually needs rotation (often rpy="0 0 1.5708")
chest
Check height and rotation relative to abdomen
upper_arm_L/R
Mesh origin is often at the shoulder, needs offset
forearm_L/R
Mesh origin usually at the elbow
thigh_L/R
Mesh origin usually at the hip
calf_L/R
Mesh origin usually at the knee
head
Needs correct height offset from neck
You will need to adjust both:
The <origin xyz="..." rpy="..."/> inside the <visual> and <collision> of each link
The <origin> of the joint that connects the link to its parent
3. Recommended workflow for the coding assistant
Load each mesh in a 3D tool (Blender / MeshLab / trimesh) and note:
Where the mesh origin currently is
The size (extents) of the mesh
Adjust the joint xyz offsets so the parts connect (e.g. bottom of thigh meets top of calf).
Adjust the rpy of the mesh so the part faces the correct direction.
Rebuild and test frequently in Foxglove after every few changes.
4. Temporary quick clean (if full alignment is too slow)
If a perfect kinematic alignment will take too long, first just remove all boxes/cylinders/spheres so only the human meshes remain. This will already look much better even if some parts are slightly floating.
