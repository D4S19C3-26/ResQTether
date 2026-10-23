#!/usr/bin/env python3
"""
fuse_node.py
------------
ROS 2 node that fuses incoming WiFi / LoRa RSSI telemetry with the robot's current SLAM pose.

Subscriptions:
  /lora/rssi (resqtether_interfaces/msg/LoraStatus)
  /tf, /tf_static (via tf2_ros buffer)

Publishes:
  /signal_map (visualization_msgs/msg/MarkerArray)
"""

import time
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration
import tf2_ros

from resqtether_interfaces.msg import LoraStatus
from visualization_msgs.msg import Marker, MarkerArray
from nav_msgs.msg import OccupancyGrid, MapMetaData
from geometry_msgs.msg import Pose, Point, Quaternion
from std_msgs.msg import ColorRGBA
from builtin_interfaces.msg import Duration as MsgDuration

from signal_mapper.fuse_core import SignalMapAggregator


class SignalFuseNode(Node):
    def __init__(self):
        super().__init__('signal_fuse_node')

        self.declare_parameter('cell_size', 0.25)
        self.declare_parameter('csv_path', 'signal_map.csv')
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('base_frame', 'base_link')
        self.declare_parameter('publish_interval_sec', 1.0)

        self.cell_size = self.get_parameter('cell_size').get_parameter_value().double_value
        self.csv_path = self.get_parameter('csv_path').get_parameter_value().string_value
        self.map_frame = self.get_parameter('map_frame').get_parameter_value().string_value
        self.base_frame = self.get_parameter('base_frame').get_parameter_value().string_value
        publish_interval = self.get_parameter('publish_interval_sec').get_parameter_value().double_value

        # Initialize core math & CSV persistence
        self.aggregator = SignalMapAggregator(cell_size=self.cell_size, csv_path=self.csv_path)

        # TF2 Buffer and Listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Subscriber
        self.sub_lora = self.create_subscription(
            LoraStatus,
            '/lora/rssi',
            self.lora_callback,
            10
        )

        # Publishers for live RViz heatmap
        self.pub_signal_map = self.create_publisher(MarkerArray, '/signal_map', 10)
        self.pub_signal_overlay = self.create_publisher(OccupancyGrid, '/signal_map_overlay', 10)

        # Periodic timer for map republication
        self.timer = self.create_timer(publish_interval, self.publish_signal_grid)

        self.get_logger().info(
            f"Signal Fuse Node active. Cell size: {self.cell_size}m | "
            f"Logging to: '{self.csv_path}' | TF: {self.map_frame} -> {self.base_frame}"
        )

    def lora_callback(self, msg: LoraStatus):
        x, y = 0.0, 0.0
        pose_found = False

        # Attempt 1: Lookup transform in map frame
        try:
            transform = self.tf_buffer.lookup_transform(
                self.map_frame,
                self.base_frame,
                Time(),
                timeout=Duration(seconds=0.1)
            )
            x = transform.transform.translation.x
            y = transform.transform.translation.y
            pose_found = True
        except Exception:
            # Attempt 2: Fallback to odom frame if map not yet built
            try:
                transform = self.tf_buffer.lookup_transform(
                    'odom',
                    self.base_frame,
                    Time(),
                    timeout=Duration(seconds=0.1)
                )
                x = transform.transform.translation.x
                y = transform.transform.translation.y
                pose_found = True
            except Exception:
                # Standalone fallback: Log at origin (0,0) if SLAM/TF not running yet
                x, y = 0.0, 0.0
                pose_found = True
                self.get_logger().info(
                    f"TF '{self.map_frame}' not active yet — logging at default (0,0) | RSSI: {msg.rssi:.1f} dBm",
                    throttle_duration_sec=3.0
                )

        if not pose_found:
            return

        ts_float = msg.stamp.sec + msg.stamp.nanosec * 1e-9
        self.aggregator.add_reading(
            x=x,
            y=y,
            rssi=msg.rssi,
            snr=msg.snr,
            sender_id=msg.sender_id,
            timestamp=ts_float
        )

        self.get_logger().info(
            f"Fused [{msg.sender_id}] at ({x:.2f}, {y:.2f}) -> RSSI: {msg.rssi:.1f} dBm"
        )

    def _rssi_to_color(self, rssi: float) -> ColorRGBA:
        c = ColorRGBA()
        c.a = 0.8
        if rssi >= -60.0:
            c.r, c.g, c.b = 0.0, 1.0, 0.0   # Green: Strong signal
        elif rssi >= -75.0:
            c.r, c.g, c.b = 1.0, 0.65, 0.0  # Amber: Marginal
        else:
            c.r, c.g, c.b = 1.0, 0.0, 0.0   # Red: Weak / Blocked
        return c

    def publish_signal_grid(self):
        cell_averages = self.aggregator.get_all_cell_averages()
        if not cell_averages:
            return

        now = self.get_clock().now().to_msg()

        # 1. Publish 3D MarkerArray (colored cubes in RViz)
        marker_array = MarkerArray()
        for idx, ((cx, cy), avg_rssi) in enumerate(cell_averages.items()):
            wx, wy = self.aggregator.cell_to_world(cx, cy)

            m = Marker()
            m.header.frame_id = self.map_frame
            m.header.stamp = now
            m.ns = 'signal_strength_grid'
            m.id = idx
            m.type = Marker.CUBE
            m.action = Marker.ADD

            m.pose.position.x = wx
            m.pose.position.y = wy
            m.pose.position.z = 0.08
            m.pose.orientation.w = 1.0

            m.scale.x = self.cell_size * 0.95
            m.scale.y = self.cell_size * 0.95
            m.scale.z = 0.1

            m.color = self._rssi_to_color(avg_rssi)
            m.lifetime = MsgDuration(sec=0, nanosec=0)

            marker_array.markers.append(m)

        self.pub_signal_map.publish(marker_array)

        # 2. Publish 2D OccupancyGrid (Overlay directly on top of LiDAR /map)
        try:
            min_cx = min(cx for cx, cy in cell_averages.keys())
            max_cx = max(cx for cx, cy in cell_averages.keys())
            min_cy = min(cy for cx, cy in cell_averages.keys())
            max_cy = max(cy for cx, cy in cell_averages.keys())

            width = max_cx - min_cx + 1
            height = max_cy - min_cy + 1

            grid_msg = OccupancyGrid()
            grid_msg.header.frame_id = self.map_frame
            grid_msg.header.stamp = now
            grid_msg.info.resolution = float(self.cell_size)
            grid_msg.info.width = int(width)
            grid_msg.info.height = int(height)

            origin_x, origin_y = self.aggregator.cell_to_world(min_cx, min_cy)
            grid_msg.info.origin.position.x = origin_x - (self.cell_size / 2.0)
            grid_msg.info.origin.position.y = origin_y - (self.cell_size / 2.0)
            grid_msg.info.origin.position.z = 0.02
            grid_msg.info.origin.orientation.w = 1.0

            # Default -1 = unknown / transparent
            data = [-1] * (width * height)

            for (cx, cy), avg_rssi in cell_averages.items():
                gx = cx - min_cx
                gy = cy - min_cy
                idx_1d = gy * width + gx

                # Normalize -90 dBm (weak, cost=10) to -40 dBm (strong, cost=100)
                norm_val = int(max(1.0, min(100.0, ((avg_rssi - (-90.0)) / 50.0) * 100.0)))
                data[idx_1d] = norm_val

            grid_msg.data = data
            self.pub_signal_overlay.publish(grid_msg)
        except Exception as e:
            self.get_logger().warn(f"Failed to publish OccupancyGrid overlay: {e}", throttle_duration_sec=5.0)


def main(args=None):
    rclpy.init(args=args)
    node = SignalFuseNode()
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
