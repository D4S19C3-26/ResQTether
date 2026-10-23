#!/usr/bin/env python3
"""
walk_controller.py
------------------
Enables signal heatmap mapping WITHOUT a physical LiDAR.

Publishes `map -> base_link` TF transforms:
1. Automatically drives/walks in a trajectory (if auto_walk is true), OR
2. Allows manual control via RViz '2D Pose Estimate' clicks or keyboard.
"""

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, PoseWithCovarianceStamped
from tf2_ros import TransformBroadcaster


class WalkControllerNode(Node):
    def __init__(self):
        super().__init__('walk_controller')

        self.declare_parameter('auto_walk', True)
        self.declare_parameter('speed_mps', 0.3)
        self.declare_parameter('radius_m', 2.0)

        self.auto_walk = self.get_parameter('auto_walk').value
        self.speed = self.get_parameter('speed_mps').value
        self.radius = self.get_parameter('radius_m').value

        self.tf_broadcaster = TransformBroadcaster(self)

        # Current position
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.angle = 0.0

        # Subscribe to RViz "2D Pose Estimate" so you can click anywhere in RViz to move!
        self.sub_pose = self.create_subscription(
            PoseWithCovarianceStamped,
            '/initialpose',
            self.pose_callback,
            10
        )

        # 10Hz TF broadcast timer
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.get_logger().info(
            "🚶 Walk Controller Active (No LiDAR Needed!)\n"
            f"  Mode: {'Auto Spiral/Circle Walk' if self.auto_walk else 'Manual RViz Click'}\n"
            "  Click '2D Pose Estimate' in RViz to set position instantly!"
        )

    def pose_callback(self, msg: PoseWithCovarianceStamped):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y
        self.auto_walk = False
        self.get_logger().info(f"📍 Set robot location to: ({self.x:.2f}, {self.y:.2f})")

    def timer_callback(self):
        now = self.get_clock().now()

        if self.auto_walk:
            # Gradually expand radius and walk outward to map the room
            self.angle += (self.speed / max(self.radius, 0.5)) * 0.1
            r = min(self.radius, 0.2 + 0.05 * self.angle)
            self.x = r * math.cos(self.angle)
            self.y = r * math.sin(self.angle)
            self.yaw = self.angle + math.pi / 2.0

        t = TransformStamped()
        t.header.stamp = now.to_msg()
        t.header.frame_id = 'map'
        t.child_frame_id = 'base_link'

        t.transform.translation.x = float(self.x)
        t.transform.translation.y = float(self.y)
        t.transform.translation.z = 0.0

        # Quaternion from yaw
        t.transform.rotation.z = math.sin(self.yaw / 2.0)
        t.transform.rotation.w = math.cos(self.yaw / 2.0)

        self.tf_broadcaster.sendTransform(t)


def main(args=None):
    rclpy.init(args=args)
    node = WalkControllerNode()
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
