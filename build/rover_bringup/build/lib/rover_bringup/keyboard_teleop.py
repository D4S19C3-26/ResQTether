#!/usr/bin/env python3
"""
keyboard_teleop.py
------------------
Continuous smooth WASD keyboard teleoperation for the ResQTether rover.
Publishes velocity commands at 10Hz so the robot cruises smoothly.

Controls:
  [W]     : Drive Forward (keeps driving until Space/Stop)
  [S]     : Drive Backward
  [A]     : Spin Left
  [D]     : Spin Right
  [SPACE] : Immediate Stop
  [Q]     : Quit Teleop
"""

import sys
import time
import termios
import tty
import select
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

BANNER = """
======================================================
  🤖 ResQTether Rover Smooth WASD Teleoperation
======================================================
  Controls:
    [W]     : Cruise FORWARD
    [S]     : Cruise BACKWARD
    [A]     : Spin LEFT
    [D]     : Spin RIGHT
    [SPACE] : Immediate STOP
    [Q]     : Quit Teleop
======================================================
"""


def get_key(settings, timeout=0.05):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


class KeyboardTeleopNode(Node):
    def __init__(self):
        super().__init__('keyboard_teleop_node')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.linear_x = 0.0
        self.angular_z = 0.0
        self.speed = 1.0

        # Continuous 10Hz publisher timer for smooth cruising
        self.timer = self.create_timer(0.1, self.publish_velocity)

    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = float(self.linear_x)
        msg.angular.z = float(self.angular_z)
        self.pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardTeleopNode()
    settings = termios.tcgetattr(sys.stdin)
    print(BANNER)

    last_press_time = 0.0

    try:
        while rclpy.ok():
            key = get_key(settings, timeout=0.05)

            if key in ['w', 'W']:
                node.linear_x = node.speed
                node.angular_z = 0.0
                last_press_time = time.time()
                print("\r🚗 MOVING FORWARD                           ", end='', flush=True)
            elif key in ['s', 'S']:
                node.linear_x = -node.speed
                node.angular_z = 0.0
                last_press_time = time.time()
                print("\r🚗 MOVING BACKWARD                          ", end='', flush=True)
            elif key in ['a', 'A']:
                node.linear_x = 0.0
                node.angular_z = node.speed
                last_press_time = time.time()
                print("\r🔄 SPINNING LEFT                            ", end='', flush=True)
            elif key in ['d', 'D']:
                node.linear_x = 0.0
                node.angular_z = -node.speed
                last_press_time = time.time()
                print("\r🔄 SPINNING RIGHT                           ", end='', flush=True)
            elif key == ' ':
                node.linear_x = 0.0
                node.angular_z = 0.0
                last_press_time = 0.0
                print("\r🛑 STOPPED                                  ", end='', flush=True)
            elif key in ['q', 'Q', '\x03']:
                print("\n\nExiting Teleoperation...")
                break
            else:
                # Momentary auto-stop: stop if no key pressed for 0.35s
                if (node.linear_x != 0.0 or node.angular_z != 0.0) and (time.time() - last_press_time > 0.35):
                    node.linear_x = 0.0
                    node.angular_z = 0.0
                    print("\r🛑 STOPPED                                  ", end='', flush=True)

            rclpy.spin_once(node, timeout_sec=0.01)

    except Exception as e:
        print(f"\nError: {e}")
    finally:
        node.linear_x = 0.0
        node.angular_z = 0.0
        node.publish_velocity()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
