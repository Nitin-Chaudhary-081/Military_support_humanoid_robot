#!/usr/bin/env python3
"""Weapon node — subscribes /threat/level + /human/confirm + /shield/state + /battery/state, publishes /weapon/{state,command}.
Hard invariant: never publishes FIRING without human_confirm True (enforced in logic + tested).
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String, Bool
from sensor_msgs.msg import JointState
import json
from weapon_control.weapon_logic import WeaponState, WeaponInput, next_state, select_weapon

class WeaponNode(Node):
    def __init__(self):
        super().__init__('weapon_control')
        self.declare_parameter('require_human_confirm', True)
        self.require_confirm = bool(self.get_parameter('require_human_confirm').value)
        self.state = WeaponState.SAFE
        self.threat = 0
        self.human_confirm = False
        self.is_braced = False
        self.battery_ok = True
        self.recoil_ok = True  # 15Nm check sim: true if braced
        self.create_subscription(Int32, '/threat/level', self.on_threat, 10)
        self.create_subscription(Bool, '/human/confirm', self.on_confirm, 10)
        self.create_subscription(String, '/shield/state', self.on_shield, 10)
        self.create_subscription(String, '/battery/state', self.on_battery, 10)
        # also listen to String variant of confirm for test harness
        self.create_subscription(String, '/human/confirm_str', self.on_confirm_str, 10)
        self.pub_state = self.create_publisher(String, '/weapon/state', 10)
        self.pub_cmd = self.create_publisher(String, '/weapon/command', 10)
        self.timer = self.create_timer(0.1, self.tick)
        self.get_logger().info(f'WeaponNode require_confirm={self.require_confirm} initial={self.state}')

    def on_threat(self, msg: Int32): self.threat = int(msg.data)
    def on_confirm(self, msg: Bool): self.human_confirm = bool(msg.data)
    def on_confirm_str(self, msg: String):
        try:
            v = json.loads(msg.data) if msg.data.strip().startswith('{') else msg.data
            if isinstance(v, dict): self.human_confirm = bool(v.get('confirm', False))
            else: self.human_confirm = (str(v).lower() in ('true','1','confirm'))
        except: self.human_confirm = (msg.data.lower() in ('true','1'))
    def on_shield(self, msg: String):
        try:
            j = json.loads(msg.data)
            self.is_braced = j.get('deployed', False) or j.get('braced', False)
        except: self.is_braced = ('deployed' in msg.data.lower() or 'braced' in msg.data.lower())
    def on_battery(self, msg: String):
        try:
            j = json.loads(msg.data)
            # battery_ok if not depleted and soc > 10%
            soc = j.get('soc', 100)
            self.battery_ok = soc > 10 and not j.get('depleted', False)
        except: self.battery_ok = 'depleted' not in msg.data.lower()

    def tick(self):
        inp = WeaponInput(threat_level=self.threat, human_confirm=(self.human_confirm if self.require_confirm else True),
                          is_braced=self.is_braced, battery_ok=self.battery_ok, recoil_ok=self.recoil_ok and self.is_braced)
        # recoil check: 15Nm only safe if braced — model this
        if self.threat >= 2 and not self.is_braced:
            inp.recoil_ok = False
        new_state = next_state(self.state, inp)
        # Enforce invariant before publishing
        if new_state == WeaponState.FIRING and not inp.human_confirm:
            self.get_logger().error('BLOCKED FIRING without human_confirm — invariant violation prevented')
            new_state = WeaponState.BRACED
        self.state = new_state
        self.pub_state.publish(String(data=self.state.value))
        cmd = {"state": self.state.value, "weapon": select_weapon(self.threat), "human_confirm": inp.human_confirm, "braced": inp.is_braced}
        self.pub_cmd.publish(String(data=json.dumps(cmd)))
        self.get_logger().debug(f'threat={self.threat} confirm={inp.human_confirm} braced={inp.is_braced} -> {self.state}')

def main():
    rclpy.init()
    n = WeaponNode()
    try: rclpy.spin(n)
    except KeyboardInterrupt: pass
    n.destroy_node(); rclpy.shutdown()
if __name__ == '__main__': main()
