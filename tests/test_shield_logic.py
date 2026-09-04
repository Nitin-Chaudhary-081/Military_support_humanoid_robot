import sys
sys.path.insert(0, 'src/shield_controller')
from shield_controller.shield_logic import desired_position, ShieldInput, STOWED, DEPLOYED, is_deployed

def test_deploy_on_high_threat():
    assert desired_position(ShieldInput(3), STOWED)==DEPLOYED
    assert desired_position(ShieldInput(2), STOWED)==DEPLOYED

def test_retract_only_on_zero():
    assert desired_position(ShieldInput(0), DEPLOYED)==STOWED
    assert desired_position(ShieldInput(1), DEPLOYED)==DEPLOYED  # hysteresis holds

def test_stowed_stays_stowed_low():
    assert desired_position(ShieldInput(0), STOWED)==STOWED

def test_is_deployed():
    assert is_deployed(1.2)==True
    assert is_deployed(0.2)==False
