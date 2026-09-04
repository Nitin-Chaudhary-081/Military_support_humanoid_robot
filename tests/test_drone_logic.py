import sys
sys.path.insert(0, 'src/drone_coordinator')
from drone_coordinator.drone_logic import mesh_status, DroneState, next_positions

def test_coverage_two_drones():
    ds=[DroneState(1,True,[0,0,35],80,0.9), DroneState(2,True,[0,0,35],80,0.9)]
    m=mesh_status(ds)
    assert m['coverage_deg']==360 and m['active']==2

def test_degraded_on_low_link():
    ds=[DroneState(1,True,[0,0,35],80,0.3), DroneState(2,True,[0,0,35],80,0.9)]
    assert mesh_status(ds)['degraded']==True

def test_next_positions_length():
    assert len(next_positions(0.0))==2
    assert len(next_positions(0.0)[0])==3
