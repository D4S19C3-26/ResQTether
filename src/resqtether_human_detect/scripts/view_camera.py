#!/usr/bin/env python3
"""
view_camera.py
--------------
Reliable live camera viewer for ResQTether base station (Laptop).
Subscribes exclusively to CompressedImage (/human_detect/image_annotated/compressed)
for smooth 30 FPS over WiFi with low latency and zero packet drop.
"""

import os
os.environ["QT_QPA_PLATFORM"] = "xcb"  # Bypass Wayland Qt issues

import time
import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int32


class CameraStreamViewer(Node):
    def __init__(self):
        super().__init__('camera_stream_viewer')

        self.latest_frame = None
        self.human_count = 0
        self.frame_count = 0
        self.last_frame_time = 0
        self.fps = 0.0

        qos_best_effort = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5
        )

        qos_reliable = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Subscribe exclusively to high-speed JPEG stream
        self.sub_comp = self.create_subscription(
            CompressedImage,
            '/human_detect/image_annotated/compressed',
            self._compressed_cb,
            qos_best_effort
        )

        # Subscribe to detection count
        self.sub_count = self.create_subscription(
            Int32,
            '/human_detect/count',
            self._count_cb,
            qos_reliable
        )

        self.get_logger().info("ResQTether High-Speed Camera Viewer initialized.")
        self.get_logger().info("Subscribed to /human_detect/image_annotated/compressed")

    def _compressed_cb(self, msg: CompressedImage):
        try:
            np_arr = np.frombuffer(msg.data, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is not None:
                now = time.time()
                self.frame_count += 1
                if self.last_frame_time > 0:
                    dt = now - self.last_frame_time
                    if dt > 0:
                        instant_fps = 1.0 / dt
                        self.fps = 0.85 * self.fps + 0.15 * instant_fps if self.fps > 0 else instant_fps

                self.last_frame_time = now
                self.latest_frame = frame
        except Exception as e:
            self.get_logger().warn(f"Decode error: {e}")

    def _count_cb(self, msg: Int32):
        self.human_count = msg.data

    def render(self):
        if self.latest_frame is not None:
            display = self.latest_frame.copy()
            h, w = display.shape[:2]
            status_text = f"ResQTether Live Feed | {w}x{h} | {self.fps:.1f} FPS"
            cv2.putText(display, status_text, (10, h - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.imshow("ResQTether Camera Viewer", display)
        else:
            placeholder = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(placeholder, "Connecting to Jetson stream...", (50, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)
            cv2.imshow("ResQTether Camera Viewer", placeholder)

        key = cv2.waitKey(1) & 0xFF
        return key != ord('q')


def main(args=None):
    rclpy.init(args=args)
    viewer = CameraStreamViewer()

    try:
        while rclpy.ok():
            rclpy.spin_once(viewer, timeout_sec=0.005)
            if not viewer.render():
                break
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        viewer.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
