#!/usr/bin/env python3
"""
lora_serial_node.py
-------------------
High-reliability ROS 2 driver for LoRa transceivers (LilyGO LoRa32 / SX1276 / Reyax)
connected via USB Serial (/dev/ttyUSB0, /dev/ttyUSB1) or hardware UART.

Features:
- Auto-detection of /dev/ttyUSB* ports if target port is unavailable.
- Multi-format parsing:
    1) Standard CSV:      "base_station,-72.5,9.2" or "-72.5,9.2"
    2) Reyax AT command:  +RCV=<addr>,<len>,<data>,<RSSI>,<SNR>
    3) Key-Value string:  "RSSI: -75 dBm, SNR: 8 dB, FROM: beacon_01"
- Publishes to:
    * /lora/rssi (resqtether_interfaces/msg/LoraStatus)
    * /signal/rssi_measured (std_msgs/msg/Float32)
- Reconnects automatically if USB is unplugged and replugged.
"""

import glob
import os
import re
import time
import serial
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from resqtether_interfaces.msg import LoraStatus


class LoraSerialNode(Node):
    def __init__(self):
        super().__init__('lora_serial_node')

        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('timeout_sec', 0.5)
        self.declare_parameter('default_sender_id', 'base_station')

        self.target_port = self.get_parameter('port').get_parameter_value().string_value
        self.baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value
        self.timeout = self.get_parameter('timeout_sec').get_parameter_value().double_value
        self.default_sender_id = self.get_parameter('default_sender_id').get_parameter_value().string_value

        # Dual publishers for full pipeline compatibility
        self.status_pub = self.create_publisher(LoraStatus, '/lora/rssi', 10)
        self.float_pub = self.create_publisher(Float32, '/signal/rssi_measured', 10)

        self.serial_conn = None
        self.active_port = None
        self.packet_count = 0

        self.get_logger().info(
            f"📡 LoRa Driver initializing on target '{self.target_port}' ({self.baudrate} baud)..."
        )

        # 50 Hz non-blocking read timer
        self.timer = self.create_timer(0.02, self.read_serial_loop)

    def _resolve_port(self):
        """Resolves port, checking target_port first, then scanning /dev/ttyUSB*."""
        if os.path.exists(self.target_port):
            return self.target_port

        # Scan available USB serial devices
        candidates = sorted(glob.glob('/dev/ttyUSB*') + glob.glob('/dev/ttyACM*'))
        if candidates:
            return candidates[0]

        return self.target_port

    def connect_serial(self):
        """Attempts to open or reopen serial port."""
        if self.serial_conn and self.serial_conn.is_open:
            return True

        port_to_try = self._resolve_port()
        if not os.path.exists(port_to_try):
            self.get_logger().warn(
                f"Waiting for LoRa device... No port at '{port_to_try}'. "
                f"(Make sure LilyGO LoRa32 is plugged into USB).",
                throttle_duration_sec=3.0
            )
            return False

        try:
            self.serial_conn = serial.Serial(
                port=port_to_try,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            self.active_port = port_to_try
            self.get_logger().info(f"✅ Connected to LoRa module on {self.active_port} at {self.baudrate} baud!")
            return True
        except serial.SerialException as e:
            self.get_logger().warn(
                f"Cannot open {port_to_try}: {e}. Retrying in 2s...",
                throttle_duration_sec=2.0
            )
            self.serial_conn = None
            return False

    def parse_packet(self, raw_line: str):
        """
        Parses incoming serial string into (sender_id, rssi, snr).
        """
        line = raw_line.strip()
        if not line:
            return None

        # 1. AT / Reyax format: +RCV=<addr>,<len>,<data>,<RSSI>,<SNR>
        if line.startswith('+RCV='):
            parts = line[5:].split(',')
            if len(parts) >= 5:
                try:
                    return f"node_{parts[0]}", float(parts[3]), float(parts[4])
                except ValueError:
                    pass

        # 2. CSV format: "sender_id,rssi,snr" or "rssi,snr"
        csv_parts = [p.strip() for p in line.split(',')]
        if len(csv_parts) == 3:
            try:
                return csv_parts[0], float(csv_parts[1]), float(csv_parts[2])
            except ValueError:
                pass
        elif len(csv_parts) == 2:
            try:
                return self.default_sender_id, float(csv_parts[0]), float(csv_parts[1])
            except ValueError:
                pass

        # 3. Regex search for RSSI and SNR
        rssi_match = re.search(r'RSSI[:=]?\s*([-\d\.]+)', line, re.IGNORECASE)
        snr_match = re.search(r'SNR[:=]?\s*([-\d\.]+)', line, re.IGNORECASE)
        if rssi_match:
            try:
                rssi = float(rssi_match.group(1))
                snr = float(snr_match.group(1)) if snr_match else 0.0
                sender_match = re.search(r'(?:FROM|ID|SENDER)[:=]?\s*(\w+)', line, re.IGNORECASE)
                sender = sender_match.group(1) if sender_match else self.default_sender_id
                return sender, rssi, snr
            except ValueError:
                pass

        return None

    def read_serial_loop(self):
        if not self.connect_serial():
            return

        try:
            while self.serial_conn and self.serial_conn.in_waiting > 0:
                raw_bytes = self.serial_conn.readline()
                try:
                    line = raw_bytes.decode('utf-8', errors='ignore').strip()
                except Exception:
                    continue

                if not line:
                    continue

                parsed = self.parse_packet(line)
                if parsed is not None:
                    sender, rssi, snr = parsed
                    self.packet_count += 1

                    # Publish LoraStatus msg
                    now = self.get_clock().now().to_msg()
                    msg = LoraStatus()
                    msg.stamp = now
                    msg.sender_id = sender
                    msg.rssi = float(rssi)
                    msg.snr = float(snr)
                    self.status_pub.publish(msg)

                    # Publish Float32 msg
                    f_msg = Float32()
                    f_msg.data = float(rssi)
                    self.float_pub.publish(f_msg)

                    self.get_logger().info(
                        f"📡 [LORA #{self.packet_count}] Sender: {msg.sender_id} | "
                        f"RSSI: {msg.rssi:.1f} dBm | SNR: {msg.snr:.1f} dB"
                    )
                else:
                    self.get_logger().debug(f"Raw line: '{line}'")

        except (serial.SerialException, OSError) as e:
            self.get_logger().error(f"LoRa serial communication error: {e}. Reconnecting...")
            if self.serial_conn:
                try:
                    self.serial_conn.close()
                except Exception:
                    pass
                self.serial_conn = None


def main(args=None):
    rclpy.init(args=args)
    node = LoraSerialNode()
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
