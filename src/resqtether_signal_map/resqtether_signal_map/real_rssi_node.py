#!/usr/bin/env python3
"""
real_rssi_node.py
-----------------
WiFi RSSI monitoring node for ResQTether.

Reads live WiFi signal strength (dBm) between the mobile robot (Raspberry Pi 5)
and the base station (laptop hotspot fixed at map origin (0,0)).

Publishers:
  /signal/rssi_measured (std_msgs/msg/Float32)
  /lora/rssi            (resqtether_interfaces/msg/LoraStatus) - for fuse_node / heatmap

Query Strategy (Ubuntu 24.04):
  1. `iw dev <iface> link` -> direct kernel signal dBm (fastest, most accurate, no sudo)
  2. `/proc/net/wireless`  -> direct kernel proc read fallback
  3. `nmcli dev wifi`      -> NetworkManager percentage-to-dBm fallback
"""

import os
import re
import subprocess
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

try:
    from resqtether_interfaces.msg import LoraStatus
    HAS_LORA_MSG = True
except ImportError:
    HAS_LORA_MSG = False


class WifiRssiNode(Node):
    def __init__(self):
        super().__init__('wifi_rssi_node')

        # Parameters
        self.declare_parameter('interface', 'wlan0')
        self.declare_parameter('rate_hz', 1.0)
        self.declare_parameter('topic_float', '/signal/rssi_measured')
        self.declare_parameter('topic_status', '/lora/rssi')
        self.declare_parameter('base_station_id', 'laptop_base')

        self.iface = self.get_parameter('interface').value
        rate_hz = float(self.get_parameter('rate_hz').value)
        topic_float = self.get_parameter('topic_float').value
        topic_status = self.get_parameter('topic_status').value
        self.base_id = self.get_parameter('base_station_id').value

        # Auto-detect interface if default not found
        self.iface = self._detect_wireless_interface(self.iface)

        # Publishers
        self.pub_float = self.create_publisher(Float32, topic_float, 10)
        if HAS_LORA_MSG:
            self.pub_status = self.create_publisher(LoraStatus, topic_status, 10)
        else:
            self.pub_status = None

        # Timer loop (default 1.0 Hz)
        timer_period = 1.0 / max(rate_hz, 0.1)
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.miss_count = 0
        self.get_logger().info(
            f"WiFi RSSI Node active | Interface: '{self.iface}' | Rate: {rate_hz}Hz\n"
            f"Publishing to: '{topic_float}'" +
            (f" and '{topic_status}'" if HAS_LORA_MSG else "")
        )

    def _detect_wireless_interface(self, preferred: str) -> str:
        """Find the active wireless interface name."""
        if os.path.exists(f"/sys/class/net/{preferred}"):
            return preferred
        
        try:
            for iface in os.listdir('/sys/class/net'):
                if os.path.exists(f"/sys/class/net/{iface}/wireless") or iface.startswith('w'):
                    self.get_logger().info(f"Auto-selected wireless interface: '{iface}'")
                    return iface
        except Exception:
            pass
        return preferred

    def get_wifi_rssi(self) -> float | None:
        """
        Query WiFi RSSI in dBm using the most reliable Ubuntu 24.04 method available.
        Returns RSSI as float (e.g. -45.0) or None if disconnected/failed.
        """
        # Method 1: `iw dev <iface> link` (Most accurate direct dBm, ~3ms, no sudo)
        try:
            res = subprocess.run(
                ['iw', 'dev', self.iface, 'link'],
                capture_output=True,
                text=True,
                timeout=0.5
            )
            if res.returncode == 0 and 'Not connected' not in res.stdout:
                match = re.search(r'signal:\s*(-?\d+)\s*dBm', res.stdout)
                if match:
                    return float(match.group(1))
        except Exception:
            pass

        # Method 2: `/proc/net/wireless` (Direct kernel proc read)
        try:
            if os.path.exists('/proc/net/wireless'):
                with open('/proc/net/wireless', 'r') as f:
                    content = f.read()
                match = re.search(rf'{self.iface}:\s*\d+\s+[\d\.]+\s+(-?\d+)', content)
                if match:
                    rssi_val = float(match.group(1))
                    return rssi_val if rssi_val < 0 else (rssi_val / 2.0 - 100.0)
        except Exception:
            pass

        # Method 3: `nmcli -t -f IN-USE,SIGNAL dev wifi` (NetworkManager percentage fallback)
        try:
            res = subprocess.run(
                ['nmcli', '-t', '-f', 'IN-USE,SIGNAL', 'dev', 'wifi'],
                capture_output=True,
                text=True,
                timeout=0.8
            )
            if res.returncode == 0:
                for line in res.stdout.strip().splitlines():
                    if line.startswith('*:'):
                        signal_pct = float(line.split(':')[1])
                        return (signal_pct / 2.0) - 100.0
        except Exception:
            pass

        return None

    def timer_callback(self):
        rssi = self.get_wifi_rssi()

        if rssi is None:
            self.miss_count += 1
            self.get_logger().warn(
                f"WiFi RSSI read failed or disconnected on '{self.iface}' "
                f"(miss count: {self.miss_count}). Is the robot connected to hotspot?",
                throttle_duration_sec=5.0
            )
            return

        self.miss_count = 0
        now = self.get_clock().now().to_msg()

        # 1. Publish Float32
        msg_float = Float32()
        msg_float.data = float(rssi)
        self.pub_float.publish(msg_float)

        # 2. Publish LoraStatus for signal_mapper fuse_node
        if self.pub_status:
            msg_status = LoraStatus()
            msg_status.stamp = now
            msg_status.rssi = float(rssi)
            msg_status.snr = 20.0  # nominal WiFi SNR
            msg_status.sender_id = self.base_id
            self.pub_status.publish(msg_status)

        self.get_logger().info(
            f"WiFi RSSI [{self.iface}]: {rssi:.1f} dBm -> Base: '{self.base_id}'"
        )


def main(args=None):
    rclpy.init(args=args)
    node = WifiRssiNode()
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
