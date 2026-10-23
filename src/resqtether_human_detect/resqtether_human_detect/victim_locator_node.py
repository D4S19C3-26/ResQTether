#!/usr/bin/env python3
"""
victim_locator_node.py
----------------------
Calculates exact real-world (X, Y) coordinates of detected victims by fusing:
1. Camera detections (/human_detect/count)
2. LiDAR distance (/scan)
3. SLAM robot pose via TF (map -> base_link)

Publishes:
- /victim_markers (visualization_msgs/MarkerArray) -> Bright Red 3D pins in RViz
- /rescue/victim_location (geometry_msgs/PointStamped)
- Logs to 'victims_found.csv'
"""

import os
import csv
import math
import time
from typing import Optional, Tuple

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration
import tf2_ros

from std_msgs.msg import Int32, Float32
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped
from visualization_msgs.msg import Marker, MarkerArray


class VictimLocatorNode(Node):
    def __init__(self):
        super().__init__('victim_locator_node')

        self.declare_parameter('min_cooldown_sec', 5.0)
        self.declare_parameter('clustering_dist', 1.5)  # Don't duplicate victim within 1.5m
        self.declare_parameter('log_file', 'victims_found.csv')

        self.cooldown_sec = float(self.get_parameter('min_cooldown_sec').value)
        self.clustering_dist = float(self.get_parameter('clustering_dist').value)
        self.log_file = str(self.get_parameter('log_file').value)

        # State
        self.last_detection_time = 0.0
        self.detected_victims = []  # List of (id, x, y, timestamp, rssi)
        self.victim_id_counter = 1
        self.latest_rssi = -70.0
        self.front_lidar_dist = 1.5  # Default estimated distance (meters)

        # TF2 Setup
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Publishers
        self.marker_pub = self.create_publisher(MarkerArray, '/victim_markers', 10)
        self.point_pub = self.create_publisher(PointStamped, '/rescue/victim_location', 10)

        # Subscribers
        self.sub_human = self.create_subscription(
            Int32, '/human_detect/count', self.human_callback, 10
        )
        self.sub_scan = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )
        self.sub_rssi = self.create_subscription(
            Float32, '/signal/rssi_measured', self.rssi_callback, 10
        )

        self._init_csv()
        self.get_logger().info("🎯 Victim Locator Node Active! Listening for human detections...")

    def _init_csv(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['victim_id', 'timestamp', 'victim_x', 'victim_y', 'robot_x', 'robot_y', 'rssi_dbm'])

    def rssi_callback(self, msg: Float32):
        self.latest_rssi = float(msg.data)

    def scan_callback(self, msg: LaserScan):
        """Measures obstacle distance directly in front (-20 to +20 degrees)."""
        num_rays = len(msg.ranges)
        if num_rays == 0:
            return

        deg20 = max(1, int(num_rays * (20.0 / 360.0)))
        front_ranges = [r for r in (msg.ranges[-deg20:] + msg.ranges[:deg20])
                        if not math.isnan(r) and not math.isinf(r) and r >= msg.range_min]

        if front_ranges:
            front_ranges.sort()
            idx = int(len(front_ranges) * 0.2)
            self.front_lidar_dist = min(max(front_ranges[idx], 0.3), 6.0)

    def get_robot_pose(self) -> Optional[Tuple[float, float, float]]:
        """Lookup robot base_link in map coordinate frame."""
        try:
            t = self.tf_buffer.lookup_transform(
                'map', 'base_link', Time(), timeout=Duration(seconds=0.08)
            )
            rx = t.transform.translation.x
            ry = t.transform.translation.y
            qz = t.transform.rotation.z
            qw = t.transform.rotation.w
            yaw = 2.0 * math.atan2(qz, qw)
            return rx, ry, yaw
        except Exception:
            return None

    def human_callback(self, msg: Int32):
        if msg.data <= 0:
            return

        now = time.time()
        if (now - self.last_detection_time) < self.cooldown_sec:
            return

        robot_pose = self.get_robot_pose()
        if robot_pose is None:
            self.get_logger().warn("⚠️ Human detected, but SLAM 'map' pose not ready yet!")
            return

        rx, ry, yaw = robot_pose

        dist = self.front_lidar_dist
        vx = rx + dist * math.cos(yaw)
        vy = ry + dist * math.sin(yaw)

        for _, ex, ey, _, _ in self.detected_victims:
            if math.hypot(vx - ex, vy - ey) < self.clustering_dist:
                return

        self.last_detection_time = now
        v_id = self.victim_id_counter
        self.victim_id_counter += 1
        time_str = time.strftime('%H:%M:%S', time.localtime(now))

        self.detected_victims.append((v_id, vx, vy, time_str, self.latest_rssi))

        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([v_id, time_str, f"{vx:.2f}", f"{vy:.2f}", f"{rx:.2f}", f"{ry:.2f}", f"{self.latest_rssi:.1f}"])

        self.get_logger().info(
            f"\n"
            f"🚨 ==========================================================\n"
            f"   VICTIM #{v_id} CONFIRMED BY SENSOR FUSION!\n"
            f"   Location:  X = {vx:.2f} m,  Y = {vy:.2f} m (in SLAM Map)\n"
            f"   Distance:  {dist:.2f} m from Rover\n"
            f"   Signal:    {self.latest_rssi:.1f} dBm | Time: {time_str}\n"
            f"   Logged to: {self.log_file}\n"
            f"============================================================"
        )

        pt_msg = PointStamped()
        pt_msg.header.stamp = self.get_clock().now().to_msg()
        pt_msg.header.frame_id = 'map'
        pt_msg.point.x = vx
        pt_msg.point.y = vy
        pt_msg.point.z = 0.5
        self.point_pub.publish(pt_msg)

        self.publish_markers()

    def publish_markers(self):
        """Publishes 3D Red Cylinders and Floating Text Labels for all victims in RViz."""
        marker_array = MarkerArray()

        for v_id, vx, vy, t_str, _ in self.detected_victims:
            marker = Marker()
            marker.header.frame_id = 'map'
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = 'victims'
            marker.id = v_id * 2
            marker.type = Marker.CYLINDER
            marker.action = Marker.ADD
            marker.pose.position.x = vx
            marker.pose.position.y = vy
            marker.pose.position.z = 0.4
            marker.scale.x = 0.45
            marker.scale.y = 0.45
            marker.scale.z = 0.8
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 0.85
            marker_array.markers.append(marker)

            text_marker = Marker()
            text_marker.header.frame_id = 'map'
            text_marker.header.stamp = self.get_clock().now().to_msg()
            text_marker.ns = 'victims_text'
            text_marker.id = v_id * 2 + 1
            text_marker.type = Marker.TEXT_VIEW_FACING
            text_marker.action = Marker.ADD
            text_marker.pose.position.x = vx
            text_marker.pose.position.y = vy
            text_marker.pose.position.z = 1.0
            text_marker.scale.z = 0.35
            text_marker.color.r = 1.0
            text_marker.color.g = 1.0
            text_marker.color.b = 1.0
            text_marker.color.a = 1.0
            text_marker.text = f"VICTIM #{v_id} ({vx:.1f}, {vy:.1f})"
            marker_array.markers.append(text_marker)

        self.marker_pub.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    node = VictimLocatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
