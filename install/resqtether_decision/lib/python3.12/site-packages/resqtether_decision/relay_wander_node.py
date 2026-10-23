#!/usr/bin/env python3
"""
relay_wander_node.py
--------------------
Autonomous Signal-Aware Search & Rescue Navigation Node.

Behavior:
1. WANDERING: Explores the area using LiDAR reactive obstacle avoidance.
2. HUMAN DETECTION: When camera detects a victim (/human_detect/count > 0):
   - Samples robot's SLAM pose (x, y).
   - If LoRa RSSI >= -70 dBm (Good link): Immediately sends VictimAlert to laptop.
   - If LoRa RSSI < -70 dBm (Dead zone): Buffers victim alert, retreats to nearest
     known strong signal position, transmits alert as soon as link restores,
     then resumes exploration!
"""

import math
import time
from typing import List, Tuple, Optional

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration
import tf2_ros

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32, String
from resqtether_interfaces.msg import LoraStatus, VictimAlert


# Mission States
STATE_WANDER = "WANDERING_EXPLORATION"
STATE_EVALUATE_VICTIM = "EVALUATING_VICTIM"
STATE_RETREAT_TO_SIGNAL = "RETREATING_TO_SIGNAL"


class SignalAwareRelayNode(Node):
    def __init__(self):
        super().__init__('signal_aware_relay_node')

        # Parameters
        self.declare_parameter('signal_threshold_dbm', -70.0)
        self.declare_parameter('recovery_threshold_dbm', -67.0)
        self.declare_parameter('cruise_speed', 0.22)
        self.declare_parameter('turn_speed', 0.5)
        self.declare_parameter('obstacle_dist_m', 0.55)
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('base_frame', 'base_link')

        self.signal_thresh = float(self.get_parameter('signal_threshold_dbm').value)
        self.recovery_thresh = float(self.get_parameter('recovery_threshold_dbm').value)
        self.cruise_speed = float(self.get_parameter('cruise_speed').value)
        self.turn_speed = float(self.get_parameter('turn_speed').value)
        self.obstacle_dist = float(self.get_parameter('obstacle_dist_m').value)
        self.map_frame = str(self.get_parameter('map_frame').value)
        self.base_frame = str(self.get_parameter('base_frame').value)

        # State Variables
        self.state = STATE_WANDER
        self.latest_rssi = -60.0  # Default initial value
        self.latest_rssi_time = time.monotonic()
        self.human_detected = False
        self.human_cooldown = 0.0

        # Memory of strong signal locations [(x, y, rssi)]
        self.signal_oases: List[Tuple[float, float, float]] = [(0.0, 0.0, -50.0)]
        self.buffered_victim: Optional[dict] = None
        self.target_oasis: Tuple[float, float] = (0.0, 0.0)

        # Laser Scan Sectors
        self.dist_front = 5.0
        self.dist_left = 5.0
        self.dist_right = 5.0

        # TF Listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Publishers
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.alert_pub = self.create_publisher(VictimAlert, '/rescue/victim_alert', 10)
        self.state_pub = self.create_publisher(String, '/rescue/mission_state', 10)

        # Subscribers
        self.sub_scan = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.sub_lora = self.create_subscription(LoraStatus, '/lora/rssi', self.lora_callback, 10)
        self.sub_human = self.create_subscription(Int32, '/human_detect/count', self.human_callback, 10)

        # Control Loop Timer (10 Hz)
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info(
            f"🤖 Signal-Aware Relay Decision Node Initialized!\n"
            f"   Signal Threshold: {self.signal_thresh:.1f} dBm | Recovery: {self.recovery_thresh:.1f} dBm\n"
            f"   Wandering with LiDAR obstacle avoidance..."
        )

    def lora_callback(self, msg: LoraStatus):
        self.latest_rssi = float(msg.rssi)
        self.latest_rssi_time = time.monotonic()

        # If signal is strong, remember this spot as an oasis
        if self.latest_rssi >= self.recovery_thresh:
            pose = self.get_current_pose()
            if pose is not None:
                x, y, _ = pose
                # Add if far enough from existing oases
                if not any(math.hypot(x - ox, y - oy) < 1.0 for ox, oy, _ in self.signal_oases):
                    self.signal_oases.append((x, y, self.latest_rssi))

    def human_callback(self, msg: Int32):
        if msg.data > 0 and (time.monotonic() - self.human_cooldown) > 8.0:
            self.human_detected = True
            self.human_cooldown = time.monotonic()
            self.get_logger().info(f"👀 Human detection trigger received! Count = {msg.data}")

    def scan_callback(self, msg: LaserScan):
        # Break 360 scan into Front, Left, Right sectors
        num_rays = len(msg.ranges)
        if num_rays == 0:
            return

        def clean_range(r):
            if math.isnan(r) or math.isinf(r) or r < msg.range_min:
                return msg.range_max
            return r

        # Assuming index 0 is front or standard LiDAR layout
        half = num_rays // 2
        deg30 = int(num_rays * (30.0 / 360.0))
        deg75 = int(num_rays * (75.0 / 360.0))

        # Front sector (-30 to +30 deg)
        front_ranges = [clean_range(r) for r in msg.ranges[-deg30:] + msg.ranges[:deg30]]
        left_ranges = [clean_range(r) for r in msg.ranges[deg30:deg75]]
        right_ranges = [clean_range(r) for r in msg.ranges[-deg75:-deg30]]

        self.dist_front = min(front_ranges) if front_ranges else 5.0
        self.dist_left = min(left_ranges) if left_ranges else 5.0
        self.dist_right = min(right_ranges) if right_ranges else 5.0

    def get_current_pose(self) -> Optional[Tuple[float, float, float]]:
        """Returns (x, y, yaw) in map frame via TF lookup."""
        try:
            t = self.tf_buffer.lookup_transform(
                self.map_frame,
                self.base_frame,
                Time(),
                timeout=Duration(seconds=0.05)
            )
            x = t.transform.translation.x
            y = t.transform.translation.y
            qz = t.transform.rotation.z
            qw = t.transform.rotation.w
            yaw = 2.0 * math.atan2(qz, qw)
            return x, y, yaw
        except Exception:
            return 0.0, 0.0, 0.0  # Fallback to origin if SLAM starting up

    def control_loop(self):
        pose = self.get_current_pose()
        x, y, yaw = pose if pose else (0.0, 0.0, 0.0)

        # -------------------------------------------------------------
        # STATE: WANDERING EXPLORATION
        # -------------------------------------------------------------
        if self.state == STATE_WANDER:
            # Check if human spotted
            if self.human_detected:
                self.human_detected = False
                self.state = STATE_EVALUATE_VICTIM
                self.stop_robot()
                return

            # Reactive obstacle avoidance
            cmd = Twist()
            if self.dist_front < self.obstacle_dist:
                # Obstacle ahead — turn towards more open side
                cmd.linear.x = 0.0
                cmd.angular.z = self.turn_speed if self.dist_left > self.dist_right else -self.turn_speed
            elif self.dist_left < (self.obstacle_dist * 0.7):
                cmd.linear.x = self.cruise_speed * 0.7
                cmd.angular.z = -self.turn_speed * 0.6
            elif self.dist_right < (self.obstacle_dist * 0.7):
                cmd.linear.x = self.cruise_speed * 0.7
                cmd.angular.z = self.turn_speed * 0.6
            else:
                cmd.linear.x = self.cruise_speed
                cmd.angular.z = 0.0

            self.cmd_pub.publish(cmd)

        # -------------------------------------------------------------
        # STATE: EVALUATING VICTIM
        # -------------------------------------------------------------
        elif self.state == STATE_EVALUATE_VICTIM:
            self.stop_robot()
            signal_age = time.monotonic() - self.latest_rssi_time
            is_dead_zone = (self.latest_rssi < self.signal_thresh) or (signal_age > 4.0)

            if not is_dead_zone:
                # DIRECT TRANSMISSION
                self.get_logger().info(
                    f"✅ DIRECT LINK: LoRa RSSI is strong ({self.latest_rssi:.1f} dBm >= {self.signal_thresh:.1f} dBm). "
                    f"Transmitting victim alert directly from ({x:.2f}, {y:.2f})!"
                )
                self.publish_alert(x, y, self.latest_rssi, self.latest_rssi, deferred=False, delay_sec=0.0)
                self.state = STATE_WANDER
            else:
                # DEAD ZONE -> STORE & RETREAT
                self.get_logger().warn(
                    f"⚠️ DEAD ZONE DETECTED: RSSI is {self.latest_rssi:.1f} dBm (< {self.signal_thresh:.1f} dBm)! "
                    f"Buffering victim location at ({x:.2f}, {y:.2f}). Retreating to signal oasis..."
                )
                self.buffered_victim = {
                    'x': x,
                    'y': y,
                    'rssi_at_spot': self.latest_rssi,
                    'time_found': time.monotonic()
                }

                # Find closest strong signal oasis
                best_oasis = (0.0, 0.0)
                best_dist = float('inf')
                for ox, oy, _ in self.signal_oases:
                    d = math.hypot(x - ox, y - oy)
                    if d < best_dist:
                        best_dist = d
                        best_oasis = (ox, oy)

                self.target_oasis = best_oasis
                self.get_logger().info(f"🎯 Set retreat target oasis: ({best_oasis[0]:.2f}, {best_oasis[1]:.2f})")
                self.state = STATE_RETREAT_TO_SIGNAL

        # -------------------------------------------------------------
        # STATE: RETREAT TO SIGNAL OASIS
        # -------------------------------------------------------------
        elif self.state == STATE_RETREAT_TO_SIGNAL:
            # Check if signal has restored
            if self.latest_rssi >= self.recovery_thresh:
                elapsed = time.monotonic() - self.buffered_victim['time_found']
                self.get_logger().info(
                    f"🎉 SIGNAL RESTORED! Current RSSI = {self.latest_rssi:.1f} dBm (>= {self.recovery_thresh:.1f} dBm).\n"
                    f"   Transmitting DEFERRED VICTIM ALERT after {elapsed:.1f}s relay flight!"
                )
                self.publish_alert(
                    self.buffered_victim['x'],
                    self.buffered_victim['y'],
                    self.buffered_victim['rssi_at_spot'],
                    self.latest_rssi,
                    deferred=True,
                    delay_sec=elapsed
                )
                self.buffered_victim = None
                self.state = STATE_WANDER
                return

            # Drive towards target oasis while avoiding obstacles
            tx, ty = self.target_oasis
            dx = tx - x
            dy = ty - y
            target_heading = math.atan2(dy, dx)
            heading_err = target_heading - yaw

            # Normalize angle to [-pi, pi]
            heading_err = (heading_err + math.pi) % (2.0 * math.pi) - math.pi

            cmd = Twist()
            if self.dist_front < self.obstacle_dist:
                cmd.linear.x = 0.0
                cmd.angular.z = self.turn_speed if self.dist_left > self.dist_right else -self.turn_speed
            elif abs(heading_err) > 0.4:
                cmd.linear.x = self.cruise_speed * 0.4
                cmd.angular.z = self.turn_speed if heading_err > 0 else -self.turn_speed
            else:
                cmd.linear.x = self.cruise_speed
                cmd.angular.z = heading_err * 0.5

            self.cmd_pub.publish(cmd)

        # Broadcast State
        msg_state = String()
        msg_state.data = f"{self.state} | RSSI: {self.latest_rssi:.1f} dBm"
        self.state_pub.publish(msg_state)

    def publish_alert(self, vx: float, vy: float, r_detect: float, r_tx: float, deferred: bool, delay_sec: float):
        alert = VictimAlert()
        alert.stamp = self.get_clock().now().to_msg()
        alert.victim_x = float(vx)
        alert.victim_y = float(vy)
        alert.rssi_at_detection = float(r_detect)
        alert.rssi_at_transmission = float(r_tx)
        alert.deferred_relay = bool(deferred)
        alert.delay_seconds = float(delay_sec)
        alert.notes = (
            f"Relay delivery: signal restored at {r_tx:.1f} dBm" if deferred 
            else f"Direct transmission at {r_detect:.1f} dBm"
        )
        self.alert_pub.publish(alert)

    def stop_robot(self):
        cmd = Twist()
        self.cmd_pub.publish(cmd)

    def destroy_node(self):
        self.stop_robot()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = SignalAwareRelayNode()
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
