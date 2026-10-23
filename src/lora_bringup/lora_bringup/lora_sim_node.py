#!/usr/bin/env python3
"""
lora_sim_node.py
----------------
Simulates incoming LoRa beacon packets from a fixed base station.
Publishes on /lora/rssi (resqtether_interfaces/msg/LoraStatus) at 1 Hz
with smoothly varying RSSI and SNR values to simulate moving away/near the source.
"""

import math
import random
import time
import rclpy
from rclpy.node import Node
from resqtether_interfaces.msg import LoraStatus


class LoraSimNode(Node):
    def __init__(self):
        super().__init__('lora_sim_node')

        self.declare_parameter('publish_rate_hz', 1.0)
        self.declare_parameter('sender_id', 'base_station_01')
        self.declare_parameter('base_rssi', -65.0)  # Center RSSI in dBm
        self.declare_parameter('amplitude', 25.0)   # Swing between -40 dBm and -90 dBm
        self.declare_parameter('period_sec', 60.0)  # Full cycle time in seconds

        rate_hz = self.get_parameter('publish_rate_hz').get_parameter_value().double_value
        self.sender_id = self.get_parameter('sender_id').get_parameter_value().string_value
        self.base_rssi = self.get_parameter('base_rssi').get_parameter_value().double_value
        self.amplitude = self.get_parameter('amplitude').get_parameter_value().double_value
        self.period_sec = self.get_parameter('period_sec').get_parameter_value().double_value

        self.publisher_ = self.create_publisher(LoraStatus, '/lora/rssi', 10)
        self.timer = self.create_timer(1.0 / rate_hz, self.publish_telemetry)

        self.start_time = time.time()
        self.get_logger().info(
            f"LoRa Simulator active. Publishing synthetic beacons on /lora/rssi at {rate_hz} Hz "
            f"(Sender ID: '{self.sender_id}')"
        )

    def publish_telemetry(self):
        elapsed = time.time() - self.start_time

        # Smooth sinusoidal variation (simulating motion towards and away from transmitter)
        phase = (2.0 * math.pi * elapsed) / self.period_sec
        clean_rssi = self.base_rssi + self.amplitude * math.sin(phase)

        # Add Gaussian radio noise (±1.5 dB)
        noisy_rssi = clean_rssi + random.gauss(0.0, 1.5)

        # Correlated SNR: strong signal -> positive SNR, weak signal -> negative SNR
        # Maps RSSI [-100, -40] to SNR approx [-12.0, +10.0]
        norm = (noisy_rssi + 100.0) / 60.0
        snr = -12.0 + norm * 22.0 + random.gauss(0.0, 0.8)

        msg = LoraStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.sender_id = self.sender_id
        msg.rssi = float(noisy_rssi)
        msg.snr = float(snr)

        self.publisher_.publish(msg)
        self.get_logger().info(
            f"📡 [SIM BEACON] Sender: {msg.sender_id} | RSSI: {msg.rssi:6.1f} dBm | SNR: {msg.snr:5.1f} dB"
        )


def main(args=None):
    rclpy.init(args=args)
    node = LoraSimNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
