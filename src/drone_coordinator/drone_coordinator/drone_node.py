#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32
from geometry_msgs.msg import PoseStamped
import json, math, time
from drone_coordinator.drone_logic import DroneState, mesh_status, next_positions

class DroneNode(Node):
    def __init__(self):
        super().__init__('drone_coordinator')
        self.threat = 0
        self.bearing = 0.0
        self.drones = [DroneState(id=1, deployed=False, pos=[0,0,0], battery_pct=100.0, link_quality=0.95),
                       DroneState(id=2, deployed=False, pos=[0,0,0], battery_pct=100.0, link_quality=0.95)]
        self.create_subscription(Int32, '/threat/level', self.on_threat, 10)
        self.create_subscription(String, '/threat/tracks', self.on_tracks, 10)
        self.pub_mesh = self.create_publisher(String, '/drone/mesh_status', 10)
        self.pub_poses = [self.create_publisher(PoseStamped, f'/drone_{i}/pose', 10) for i in (1,2)]
        self.pub_cmd = self.create_publisher(String, '/drone/command', 10)
        self.timer = self.create_timer(0.5, self.tick)
        self.get_logger().info('DroneNode 2-UAV mesh ready (fold-flat 6kg)')

    def on_threat(self, msg: Int32):
        self.threat = int(msg.data)
        # auto-deploy on threat >=1
        if self.threat >= 1:
            for d in self.drones: d.deployed = True
        elif self.threat == 0:
            # keep deployed for 30s simulated — simplified: stay deployed
            pass
    def on_tracks(self, msg: String):
        try:
            j = json.loads(msg.data)
            # estimate bearing from first track bbox x
            tracks = j.get('tracks', [])
            if tracks:
                x = tracks[0].get('bbox', [0.5,0,0,0])[0]
                self.bearing = (x - 0.5) * 120  # map 0-1 -> -60..60 deg
        except: pass
    def tick(self):
        # update positions toward desired
        desired = next_positions(self.bearing)
        for i, d in enumerate(self.drones):
            if d.deployed:
                # simple lerp 5m/s
                for k in range(3):
                    d.pos[k] += (desired[i][k] - d.pos[k]) * 0.2
                d.battery_pct = max(0, d.battery_pct - 0.02)  # drain
                # link quality degrades with distance
                dist = math.sqrt(sum(p**2 for p in d.pos))
                d.link_quality = max(0.2, 1.0 - dist/200.0)
                ps = PoseStamped()
                ps.header.frame_id = 'map'; ps.header.stamp = self.get_clock().now().to_msg()
                ps.pose.position.x, ps.pose.position.y, ps.pose.position.z = d.pos
                self.pub_poses[i].publish(ps)
        status = mesh_status(self.drones)
        payload = {"drones": [{"id": d.id, "deployed": d.deployed, "pos": [round(p,1) for p in d.pos], "battery": round(d.battery_pct,1), "link": round(d.link_quality,2)} for d in self.drones],
                   "mesh": status, "threat": self.threat, "bearing": round(self.bearing,1), "ts": time.time()}
        self.pub_mesh.publish(String(data=json.dumps(payload)))
        self.pub_cmd.publish(String(data=json.dumps({"action": "deploy" if self.threat>=1 else "hold", "desired": desired})))

def main():
    rclpy.init()
    n = DroneNode()
    try: rclpy.spin(n)
    except KeyboardInterrupt: pass
    n.destroy_node(); rclpy.shutdown()
if __name__ == '__main__': main()
