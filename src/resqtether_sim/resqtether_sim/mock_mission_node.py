#!/usr/bin/env python3
"""
mock_mission_node.py
--------------------
Complete hardware-free mission simulator for ResQTether:
1. Simulates robot movement driven by /cmd_vel.
2. Broadcasts TF: map -> base_link.
3. Publishes simulated 360-degree LiDAR /scan with room boundaries.
4. Simulates LoRa RSSI based on distance from base station (0,0) with wall attenuation.
   - Near (0,0): Strong signal (-45 to -60 dBm).
   - Distance > 3m: Radio Dead Zone (-76 to -92 dBm).
5. Injects a simulated human detection event at t = 12s so you can see the
   autonomous relay store-and-forward behavior in action!
"""

import math
import time
import random

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TransformStamped
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32, Float32
from tf2_ros import TransformBroadcaster
from resqtether_interfaces.msg import LoraStatus


class MockMissionSimulator(Node):
    def __init__(self):
        super().__init__('mock_mission_simulator')

        # Robot Pose in Map Frame
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.vx = 0.0
        self.wz = 0.0

        # Base Station location (Tether Anchor)
        self.base_x = 0.0
        self.base_y = 0.0

        # TF Broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Publishers
        self.scan_pub = self.create_publisher(LaserScan, '/scan', 10)
        self.lora_pub = self.create_publisher(LoraStatus, '/lora/rssi', 10)
        self.float_pub = self.create_publisher(Float32, '/signal/rssi_measured', 10)
        self.human_pub = self.create_publisher(Int32, '/human_detect/count', 10)

        # Subscriber
        self.sub_cmd = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)

        # Simulation Loop (20 Hz)
        self.start_time = time.monotonic()
        self.last_update = time.monotonic()
        self.victim_triggered = False

        self.timer = self.create_timer(0.05, self.sim_loop)
        self.get_logger().info("🧪 Mock Mission Simulator Active! (Simulating Robot, LiDAR, and LoRa RSSI)")

    def cmd_callback(self, msg: Twist):
        self.vx = msg.linear.x
        self.wz = msg.angular.z

    def sim_loop(self):
        now_mono = time.monotonic()
        dt = now_mono - self.last_update
        self.last_update = now_mono

        # 1. Integrate Kinematics
        self.yaw += self.wz * dt
        self.x += self.vx * math.cos(self.yaw) * dt
        self.y += self.vx * math.sin(self.yaw) * dt

        now_ros = self.get_clock().now().to_msg()

        # 2. Broadcast TF: map -> base_link
        t = TransformStamped()
        t.header.stamp = now_ros
        t.header.frame_id = 'map'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = float(self.x)
        t.transform.translation.y = float(self.y)
        t.transform.translation.z = 0.0
        t.transform.rotation.z = math.sin(self.yaw / 2.0)
        t.transform.rotation.w = math.cos(self.yaw / 2.0)
        self.tf_broadcaster.sendTransform(t)

        # 3. Simulate LoRa RSSI
        # Distance path loss from base station (0,0)
        dist = math.hypot(self.x - self.base_x, self.y - self.base_y)
        # Wall penalty if x > 2.5 (simulated concrete wall)
        wall_penalty = 18.0 if self.x > 2.5 else 0.0
        # Log-distance path loss
        base_rssi = -42.0 - (24.0 * math.log10(max(1.0, dist))) - wall_penalty
        noise = random.uniform(-1.5, 1.5)
        sim_rssi = float(base_rssi + noise)
        sim_snr = float(max(-10.0, min(12.0, (sim_rssi + 95.0) / 4.0)))

        lora_msg = LoraStatus()
        lora_msg.stamp = now_ros
        lora_msg.sender_id = 'base_station'
        lora_msg.rssi = sim_rssi
        lora_msg.snr = sim_snr
        self.lora_pub.publish(lora_msg)

        f_msg = Float32()
        f_msg.data = sim_rssi
        self.float_pub.publish(f_msg)

        # 4. Simulate LiDAR LaserScan (Box arena: -4 to +6m in X, -4 to +4m in Y)
        scan = LaserScan()
        scan.header.stamp = now_ros
        scan.header.frame_id = 'base_link'
        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = math.radians(2.0)
        scan.time_increment = 0.0
        scan.range_min = 0.15
        scan.range_max = 12.0

        ranges = []
        angles = [scan.angle_min + i * scan.angle_increment for i in range(180)]
        for a in angles:
            ray_yaw = self.yaw + a
            dx = math.cos(ray_yaw)
            dy = math.sin(ray_yaw)

            # Intersect with arena walls: X in [-3, 5], Y in [-3, 3]
            d_hit = 10.0
            if dx > 0: d_hit = min(d_hit, (5.0 - self.x) / dx)
            elif dx < 0: d_hit = min(d_hit, (-3.0 - self.x) / dx)

            if dy > 0: d_hit = min(d_hit, (3.0 - self.y) / dy)
            elif dy < 0: d_hit = min(d_hit, (-3.0 - self.y) / dy)

            # Simulated wall at x=2.5 with doorway at y in [-0.5, 0.5]
            if dx != 0:
                d_wall = (2.5 - self.x) / dx
                if d_wall > 0:
                    y_intersect = self.y + d_wall * dy
                    if abs(y_intersect) > 0.6:  # Doorway is +/- 0.6m
                        d_hit = min(d_hit, d_wall)

            ranges.append(float(max(0.15, min(12.0, d_hit + random.uniform(-0.02, 0.02)))))

        scan.ranges = ranges
        self.scan_pub.publish(scan)

        # 5. Trigger Victim Detection Event at t = 12s
        elapsed = now_mono - self.start_time
        if not self.victim_triggered and elapsed >= 12.0:
            self.victim_triggered = True
            h_msg = Int32()
            h_msg.data = 1
            self.human_pub.publish(h_msg)
            self.get_logger().info(
                f"🚨 [SIM] INJECTED HUMAN DETECTION AT t={elapsed:.1f}s | Robot at ({self.x:.2f}, {self.y:.2f}) | RSSI = {sim_rssi:.1f} dBm"
            )


def main(args=None):
    rclpy.init(args=args)
    node = MockMissionSimulator()
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
