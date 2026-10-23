#!/usr/bin/env python3
"""
bridge_node.py
--------------
High-performance ROS 2 to ESP32 Motor Serial Bridge.
Subscribes to /cmd_vel and streams formatted velocity strings to the ESP32 motor controller.
Features auto-port detection and auto-reconnection.
"""

import os
import glob
import time
import serial

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class Esp32MotorBridgeNode(Node):
    def __init__(self):
        super().__init__('esp32_motor_bridge_node')

        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('rate_hz', 20.0)

        self.target_port = str(self.get_parameter('port').value)
        self.baudrate = int(self.get_parameter('baudrate').value)
        self.rate_hz = float(self.get_parameter('rate_hz').value)

        self.ser = None
        self.linear_x = 0.0
        self.angular_z = 0.0
        self.last_cmd_time = 0.0
        self.timeout_sec = 0.5

        # Subscribe to standard velocity topic
        self.sub_cmd_vel = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Connection check & transmission timer
        self.timer = self.create_timer(1.0 / self.rate_hz, self.transmit_loop)
        self.get_logger().info(f"ESP32 Motor Bridge started. Target port: {self.target_port} ({self.baudrate} baud)")

    def _find_port(self):
        """Auto-detects USB serial device if default port is missing."""
        if os.path.exists(self.target_port):
            return self.target_port
        candidates = glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*')
        if candidates:
            return candidates[0]
        return None

    def connect_serial(self):
        port = self._find_port()
        if not port:
            self.get_logger().warn("Waiting for ESP32 USB serial connection...", throttle_duration_sec=3.0)
            return False

        try:
            self.ser = serial.Serial()
            self.ser.port = port
            self.ser.baudrate = self.baudrate
            self.ser.timeout = 0.1
            self.ser.dtr = False
            self.ser.rts = False
            self.ser.open()
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            time.sleep(0.5)
            self.get_logger().info(f"✅ Connected to ESP32 on {port} at {self.baudrate} baud!")
            return True
        except Exception as e:
            self.get_logger().error(f"Failed to connect to {port}: {e}", throttle_duration_sec=3.0)
            self.ser = None
            return False

    def cmd_vel_callback(self, msg: Twist):
        self.linear_x = msg.linear.x
        self.angular_z = msg.angular.z
        self.last_cmd_time = time.time()

    def transmit_loop(self):
        if self.ser is None or not self.ser.is_open:
            self.connect_serial()
            return

        # Watchdog: Stop motors if no new /cmd_vel received within timeout_sec
        if time.time() - self.last_cmd_time > self.timeout_sec:
            self.linear_x = 0.0
            self.angular_z = 0.0

        cmd_str = f"V,{self.linear_x:.2f},{self.angular_z:.2f}\n"
        try:
            # Discard any serial spam from ESP32 to prevent PC buffer overflow
            if self.ser.in_waiting > 128:
                self.ser.reset_input_buffer()
            self.ser.write(cmd_str.encode('ascii'))
            self.ser.flush()
        except (serial.SerialException, OSError) as e:
            self.get_logger().warn(f"Serial connection lost: {e}. Reconnecting...", throttle_duration_sec=2.0)
            try:
                self.ser.close()
            except Exception:
                pass
            self.ser = None

    def destroy_node(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(b"V,0.0,0.0\n")
                self.ser.close()
            except Exception:
                pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = Esp32MotorBridgeNode()
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
