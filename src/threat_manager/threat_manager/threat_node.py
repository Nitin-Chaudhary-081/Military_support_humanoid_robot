#!/usr/bin/env python3
"""Threat manager ROS 2 node — subscribes to camera, runs YOLOv8 (or mock), publishes threat level.
Human-confirm is NOT here; weapon_control enforces it. Jetson Orin 275 TOPS target: 60 FPS via ultralytics.
If ultralytics not installed or no image, node runs in mock mode and still publishes heartbeats (testable headless).
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32, String
from sensor_msgs.msg import Image
import json, time, os

from threat_manager.threat_logic import classify_threat, parse_yolo_output, Detection

try:
    from ultralytics import YOLO
    HAS_YOLO = True
except Exception:
    HAS_YOLO = False

class ThreatNode(Node):
    def __init__(self):
        super().__init__('threat_manager')
        self.declare_parameter('conf_thresh', 0.45)
        self.declare_parameter('model', 'yolov8n')
        self.declare_parameter('input_topic', '/camera/image_raw')
        self.declare_parameter('mock', False)
        self.conf_thresh = float(self.get_parameter('conf_thresh').value)
        self.model_name = self.get_parameter('model').value
        self.mock = bool(self.get_parameter('mock').value)
        if os.environ.get('ACSR_MOCK', '0') == '1':
            self.mock = True
        self.model = None
        if HAS_YOLO and not self.mock:
            try:
                # yolov8n.pt auto-downloads on first run; fallback to mock if offline
                self.model = YOLO(self.model_name + '.pt' if not self.model_name.endswith('.pt') else self.model_name)
                self.get_logger().info(f'YOLO loaded: {self.model_name} (HAS_YOLO)')
            except Exception as e:
                self.get_logger().warn(f'YOLO load failed -> mock mode: {e}')
                self.model = None
        self.pub_level = self.create_publisher(Int32, '/threat/level', 10)
        self.pub_tracks = self.create_publisher(String, '/threat/tracks', 10)
        self.pub_heartbeat = self.create_publisher(String, '/threat/heartbeat', 10)
        topic = self.get_parameter('input_topic').value
        self.sub = self.create_subscription(Image, topic, self.on_image, 10)
        self.timer = self.create_timer(1.0, self.on_heartbeat)
        self.frame_count = 0
        self.last_level = 0
        self.get_logger().info(f'ThreatNode ready conf={self.conf_thresh} model={self.model_name} mock={self.mock} has_yolo={HAS_YOLO} topic={topic}')

    def on_image(self, msg: Image):
        self.frame_count += 1
        detections = []
        if self.model is not None and not self.mock:
            try:
                # Lazy cv_bridge import — may not be installed headless
                try:
                    from cv_bridge import CvBridge
                    import cv2
                    bridge = CvBridge()
                    cv_im = bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
                    results = self.model(cv_im, verbose=False, conf=self.conf_thresh)
                    for r in results:
                        for box in r.boxes:
                            cls_id = int(box.cls.item())
                            conf = float(box.conf.item())
                            xywh = box.xywhn[0].tolist() if hasattr(box, 'xywhn') else [0,0,0,0]
                            detections.append({'cls': cls_id, 'conf': conf, 'bbox': xywh})
                except Exception as e:
                    self.get_logger().warn(f'cv_bridge/YOLO infer failed: {e}')
            except Exception as e:
                self.get_logger().warn(f'YOLO infer error: {e}')
        # Parse + classify (mock still exercises logic)
        parsed = parse_yolo_output(detections)
        result = classify_threat(parsed, conf_thresh=self.conf_thresh)
        self.last_level = result['level']
        self.pub_level.publish(Int32(data=result['level']))
        self.pub_tracks.publish(String(data=json.dumps(result)))
        self.get_logger().debug(f'frame {self.frame_count} level={result["level"]} dom={result["dominant_class"]}')

    def on_heartbeat(self):
        self.pub_heartbeat.publish(String(data=json.dumps({'frame_count': self.frame_count, 'last_level': self.last_level, 'ts': time.time(), 'mock': self.mock})))


def main():
    rclpy.init()
    n = ThreatNode()
    try:
        rclpy.spin(n)
    except KeyboardInterrupt:
        pass
    n.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
