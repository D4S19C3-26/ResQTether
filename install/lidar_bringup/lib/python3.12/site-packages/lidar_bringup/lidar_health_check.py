#!/usr/bin/env python3
"""
lidar_health_check.py
---------------------
Sanity-check & diagnostic tool for 360° LiDAR hardware / simulation.

Subscribes to /scan (sensor_msgs/msg/LaserScan) and monitors:
- Publishing frequency (Hz)
- Min and Max measured range values
- Total and valid points count
- Warns with high priority if topic is silent for > 2.0 seconds.
"""

import math
import time
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class LidarHealthCheck(Node):
    def __init__(self):
        super().__init__('lidar_health_check')

        self.declare_parameter('scan_topic', '/scan')
        scan_topic = self.get_parameter('scan_topic').get_parameter_value().string_value

        self.subscription = self.create_subscription(
            LaserScan,
            scan_topic,
            self.scan_callback,
            10
        )

        self.msg_count = 0
        self.last_msg_time = None
        self.last_calc_time = time.time()
        self.latest_min_range = 0.0
        self.latest_max_range = 0.0
        self.latest_valid_pts = 0
        self.latest_total_pts = 0

        # Run health evaluation loop at 1 Hz
        self.timer = self.create_timer(1.0, self.health_timer_callback)

        self.get_logger().info(f"LiDAR Health Check initialized. Listening to: {scan_topic}")

    def scan_callback(self, msg: LaserScan):
        now = time.time()
        self.last_msg_time = now
        self.msg_count += 1

        valid_ranges = [
            r for r in msg.ranges
            if not math.isnan(r) and not math.isinf(r) and msg.range_min <= r <= msg.range_max
        ]
        self.latest_total_pts = len(msg.ranges)
        self.latest_valid_pts = len(valid_ranges)

        if valid_ranges:
            self.latest_min_range = min(valid_ranges)
            self.latest_max_range = max(valid_ranges)
        else:
            self.latest_min_range = 0.0
            self.latest_max_range = 0.0

    def health_timer_callback(self):
        now = time.time()

        if self.last_msg_time is None:
            self.get_logger().warn("Waiting for first /scan message... No LiDAR data received yet.")
            return

        silence_duration = now - self.last_msg_time
        if silence_duration > 2.0:
            self.get_logger().error(
                f"⚠️  [ALERT] /scan topic SILENT for {silence_duration:.1f}s! "
                f"Check USB connection, permissions (/dev/ttyUSB0), or power."
            )
            return

        elapsed = now - self.last_calc_time
        rate = self.msg_count / elapsed if elapsed > 0 else 0.0
        self.msg_count = 0
        self.last_calc_time = now

        self.get_logger().info(
            f"✅ [LiDAR HEALTHY] Rate: {rate:5.1f} Hz | "
            f"Valid Points: {self.latest_valid_pts}/{self.latest_total_pts} | "
            f"Range: [{self.latest_min_range:.2f} m - {self.latest_max_range:.2f} m]"
        )


def main(args=None):
    rclpy.init(args=args)
    node = LidarHealthCheck()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
