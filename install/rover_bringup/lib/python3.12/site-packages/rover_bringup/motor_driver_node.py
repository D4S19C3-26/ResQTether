#!/usr/bin/env python3
"""
motor_driver_node.py
--------------------
ROS 2 motor controller for 6-wheel rover chassis on Raspberry Pi 5.
Uses lgpio pin factory for Raspberry Pi 5.
"""

import os
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

# Force lgpio on Raspberry Pi 5
os.environ["GPIOZERO_PIN_FACTORY"] = "lgpio"

try:
    from gpiozero import OutputDevice
    HAS_GPIO = True
except Exception as e:
    HAS_GPIO = False


class MotorDriverNode(Node):
    def __init__(self):
        super().__init__('motor_driver_node')

        self.declare_parameter('in1_pin', 17)
        self.declare_parameter('in2_pin', 18)
        self.declare_parameter('in3_pin', 27)
        self.declare_parameter('in4_pin', 22)
        self.declare_parameter('watchdog_timeout_sec', 1.0)

        in1_pin = self.get_parameter('in1_pin').value
        in2_pin = self.get_parameter('in2_pin').value
        in3_pin = self.get_parameter('in3_pin').value
        in4_pin = self.get_parameter('in4_pin').value
        self.timeout = self.get_parameter('watchdog_timeout_sec').value

        self.current_state = "STOP"
        self.last_cmd_time = time.monotonic()

        self.get_logger().info(
            f"Initializing 6-Wheel Motor Driver on GPIO:\n"
            f"  Left Motors : IN1=GPIO{in1_pin}, IN2=GPIO{in2_pin}\n"
            f"  Right Motors: IN3=GPIO{in3_pin}, IN4=GPIO{in4_pin}"
        )

        if HAS_GPIO:
            try:
                self.in1 = OutputDevice(in1_pin)
                self.in2 = OutputDevice(in2_pin)
                self.in3 = OutputDevice(in3_pin)
                self.in4 = OutputDevice(in4_pin)
                self.stop_motors()
                self.get_logger().info("✅ GPIOZero (lgpio) initialized successfully!")
            except Exception as e:
                self.get_logger().error(f"❌ Failed to initialize GPIO: {e}")
                self.in1 = self.in2 = self.in3 = self.in4 = None
        else:
            self.get_logger().warn("gpiozero not available.")
            self.in1 = self.in2 = self.in3 = self.in4 = None

        # Subscriber
        self.sub_cmd_vel = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        # Safety Watchdog Timer (checks at 10Hz)
        self.watchdog_timer = self.create_timer(0.1, self.watchdog_callback)

    def set_outputs(self, in1_val: bool, in2_val: bool, in3_val: bool, in4_val: bool):
        if not HAS_GPIO or self.in1 is None:
            return
        
        if in1_val: self.in1.on()
        else: self.in1.off()

        if in2_val: self.in2.on()
        else: self.in2.off()

        if in3_val: self.in3.on()
        else: self.in3.off()

        if in4_val: self.in4.on()
        else: self.in4.off()

    def forward(self):
        if self.current_state != "FORWARD":
            self.get_logger().info("🚗 FORWARD (IN1=1, IN2=0, IN3=1, IN4=0)")
            self.current_state = "FORWARD"
        self.set_outputs(True, False, True, False)

    def backward(self):
        if self.current_state != "BACKWARD":
            self.get_logger().info("🚗 BACKWARD (IN1=0, IN2=1, IN3=0, IN4=1)")
            self.current_state = "BACKWARD"
        self.set_outputs(False, True, False, True)

    def turn_left(self):
        if self.current_state != "LEFT":
            self.get_logger().info("🔄 SPIN LEFT (IN1=0, IN2=1, IN3=1, IN4=0)")
            self.current_state = "LEFT"
        self.set_outputs(False, True, True, False)

    def turn_right(self):
        if self.current_state != "RIGHT":
            self.get_logger().info("🔄 SPIN RIGHT (IN1=1, IN2=0, IN3=0, IN4=1)")
            self.current_state = "RIGHT"
        self.set_outputs(True, False, False, True)

    def stop_motors(self):
        if self.current_state != "STOP":
            self.get_logger().info("🛑 STOP (All 0)")
            self.current_state = "STOP"
        self.set_outputs(False, False, False, False)

    def cmd_vel_callback(self, msg: Twist):
        self.last_cmd_time = time.monotonic()
        linear = msg.linear.x
        angular = msg.angular.z

        if linear > 0.1:
            self.forward()
        elif linear < -0.1:
            self.backward()
        elif angular > 0.1:
            self.turn_left()
        elif angular < -0.1:
            self.turn_right()
        else:
            self.stop_motors()

    def watchdog_callback(self):
        if time.monotonic() - self.last_cmd_time > self.timeout:
            if self.current_state != "STOP":
                self.stop_motors()

    def destroy_node(self):
        self.stop_motors()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = MotorDriverNode()
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
