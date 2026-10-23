#!/usr/bin/env python3
"""
fake_lidar_node.py
------------------
Simulates a 360-degree 2D LiDAR in a rectangular room (10m x 6m)
publishing standard sensor_msgs/LaserScan at 5Hz without requiring hardware or Gazebo.
"""

import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class FakeLidarNode(Node):
    def __init__(self):
        super().__init__('fake_lidar_node')

        self.declare_parameter('frame_id', 'laser_link')
        self.declare_parameter('rate_hz', 5.0)
        self.declare_parameter('room_width', 10.0)   # x-axis: -5m to +5m
        self.declare_parameter('room_height', 6.0)   # y-axis: -3m to +3m

        self.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        rate_hz = self.get_parameter('rate_hz').get_parameter_value().double_value
        self.room_w = self.get_parameter('room_width').get_parameter_value().double_value
        self.room_h = self.get_parameter('room_height').get_parameter_value().double_value

        self.pub = self.create_publisher(LaserScan, '/scan', 10)
        self.timer = self.create_timer(1.0 / rate_hz, self.publish_scan)

        self.samples = 360
        self.angle_min = -math.pi
        self.angle_max = math.pi
        self.angle_increment = (2 * math.pi) / self.samples

        self.get_logger().info(
            f"Fake LiDAR publishing 360° scan of {self.room_w}m x {self.room_h}m room "
            f"on /scan at {rate_hz} Hz (frame: '{self.frame_id}')"
        )

    def publish_scan(self):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.frame_id

        msg.angle_min = self.angle_min
        msg.angle_max = self.angle_max
        msg.angle_increment = self.angle_increment
        msg.time_increment = 0.0
        msg.scan_time = 0.2
        msg.range_min = 0.1
        msg.range_max = 20.0

        half_w = self.room_w / 2.0
        half_h = self.room_h / 2.0

        ranges = []
        for i in range(self.samples):
            theta = self.angle_min + i * self.angle_increment
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)

            d_candidates = []
            if abs(cos_t) > 1e-6:
                d_x = half_w / abs(cos_t)
                d_candidates.append(d_x)
            if abs(sin_t) > 1e-6:
                d_y = half_h / abs(sin_t)
                d_candidates.append(d_y)

            dist = min(d_candidates) if d_candidates else msg.range_max
            ranges.append(float(dist))

        msg.ranges = ranges
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FakeLidarNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
