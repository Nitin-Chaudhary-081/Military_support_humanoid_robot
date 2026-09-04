#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String, Float64
import json
from shield_controller.shield_logic import desired_position, is_deployed, ShieldInput, STOWED, DEPLOYED

class ShieldNode(Node):
    def __init__(self):
        super().__init__('shield_controller')
        self.threat = 0
        self.pos = STOWED
        self.create_subscription(Int32, '/threat/level', self.on_threat, 10)
        self.pub_state = self.create_publisher(String, '/shield/state', 10)
        self.pub_cmd = self.create_publisher(Float64, '/shield/command', 10)
        self.pub_joint = self.create_publisher(Float64, '/shield_controller/command', 10)
        self.timer = self.create_timer(0.2, self.tick)
        self.get_logger().info('ShieldNode ready 0=stowed 1.57=deployed')

    def on_threat(self, msg: Int32): self.threat = int(msg.data)
    def tick(self):
        desired = desired_position(ShieldInput(threat_level=self.threat), self.pos)
        # Simulate actuator: move 0.3 rad per tick toward desired
        step = 0.3
        if abs(desired - self.pos) > 0.02:
            self.pos += step if desired > self.pos else -step
            self.pos = max(STOWED, min(DEPLOYED, self.pos))
        msg = {"position": round(self.pos,3), "deployed": is_deployed(self.pos), "stowed": self.pos < 0.1, "threat": self.threat, "braced": is_deployed(self.pos)}
        self.pub_state.publish(String(data=json.dumps(msg)))
        self.pub_cmd.publish(Float64(data=float(self.pos)))
        self.get_logger().debug(f'threat={self.threat} pos={self.pos:.2f} dep={msg["deployed"]}')

def main():
    rclpy.init()
    n = ShieldNode()
    try: rclpy.spin(n)
    except KeyboardInterrupt: pass
    n.destroy_node(); rclpy.shutdown()
if __name__ == '__main__': main()
