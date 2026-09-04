#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32, Float64
import json, time
from battery_manager.battery_logic import power_watts, endurance_minutes, Load, soc_after_minutes

class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_manager')
        self.declare_parameter('capacity_kwh', 48.0)
        self.declare_parameter('initial_soc', 100.0)
        self.capacity = float(self.get_parameter('capacity_kwh').value)
        self.soc = float(self.get_parameter('initial_soc').value)
        self.load = Load()
        self.create_subscription(String, '/threat/tracks', self.on_tracks_dummy, 10)
        self.create_subscription(String, '/shield/state', self.on_shield, 10)
        self.create_subscription(String, '/drone/mesh_status', self.on_drone, 10)
        self.create_subscription(String, '/weapon/state', self.on_weapon, 10)
        self.pub_state = self.create_publisher(String, '/battery/state', 10)
        self.pub_soc = self.create_publisher(Float64, '/battery/soc', 10)
        self.timer = self.create_timer(1.0, self.tick)
        self.t0 = time.time()
        self.get_logger().info(f'BatteryNode {self.capacity}kWh soc={self.soc}% — 45-90min model')
    def on_shield(self, msg: String):
        try: self.load.shield_deployed = json.loads(msg.data).get('deployed', False)
        except: pass
    def on_drone(self, msg: String):
        try: self.load.drones_active = json.loads(msg.data).get('mesh', {}).get('active', 0)
        except: pass
    def on_weapon(self, msg: String):
        self.load.firing = (msg.data.strip() == 'FIRING')
    def on_tracks_dummy(self, msg: String): pass
    def tick(self):
        p = power_watts(self.load)
        end = endurance_minutes(self.capacity, self.load)
        # drain per second
        drain_per_sec = p / 1000.0 / 3600.0  # kWh per sec
        drain_pct = (drain_per_sec / self.capacity) * 100.0 * 1.0  # per tick (1s)
        self.soc = max(0.0, self.soc - drain_pct)
        depleted = self.soc <= 5.0
        payload = {
            "soc": round(self.soc,2), "capacity_kwh": self.capacity, "power_w": round(p,1),
            "endurance_min": round(end,1), "depleted": depleted,
            "load": {"walking": self.load.walking, "velocity": self.load.velocity_ms, "compute": self.load.compute_w, "drones": self.load.drones_active, "shield": self.load.shield_deployed, "firing": self.load.firing},
            "ts": time.time(), "uptime_s": round(time.time()-self.t0,1)
        }
        self.pub_state.publish(String(data=json.dumps(payload)))
        self.pub_soc.publish(Float64(data=float(self.soc)))
        if depleted:
            self.get_logger().warn(f'Battery depleted soc={self.soc:.1f}% endurance {end:.1f}min — retreat required')

def main():
    rclpy.init()
    n = BatteryNode()
    try: rclpy.spin(n)
    except KeyboardInterrupt: pass
    n.destroy_node(); rclpy.shutdown()
if __name__ == '__main__': main()
