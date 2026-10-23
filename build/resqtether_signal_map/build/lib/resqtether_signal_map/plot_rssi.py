#!/usr/bin/env python3
"""
plot_rssi.py
------------
Live real-time graphical RSSI telemetry monitor for ResQTether.
Visualizes:
1. Continuous dynamic RSSI signal strength (dBm) over time.
2. Signal health threshold zones (Strong / Marginal / Dead Zone).
3. Human detection events and Deferred Relay transmission triggers.
4. Real-time statistics banner.
"""

import os
import sys
import time
import collections
import threading

# Force X11 / XCB for smooth Qt/Matplotlib rendering on Ubuntu Wayland
os.environ["QT_QPA_PLATFORM"] = "xcb"

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Patch

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Int32
from resqtether_interfaces.msg import LoraStatus, VictimAlert


class RssiPlotterNode(Node):
    def __init__(self):
        super().__init__('rssi_plotter_node')

        self.declare_parameter('window_seconds', 60.0)
        self.window_sec = float(self.get_parameter('window_seconds').value)

        # Thread-safe ring buffers for plotting
        self.lock = threading.Lock()
        self.times = collections.deque(maxlen=1200)
        self.rssis = collections.deque(maxlen=1200)
        self.snrs = collections.deque(maxlen=1200)
        self.events = []  # List of (timestamp, event_type, label, value)

        self.start_time = time.monotonic()
        self.latest_rssi = float('nan')
        self.latest_snr = 0.0
        self.victim_count = 0
        self.relay_active = False

        # Subscriptions
        self.sub_lora = self.create_subscription(
            LoraStatus,
            '/lora/rssi',
            self.lora_callback,
            10
        )

        self.sub_float = self.create_subscription(
            Float32,
            '/signal/rssi_measured',
            self.float_callback,
            10
        )

        self.sub_victim = self.create_subscription(
            VictimAlert,
            '/rescue/victim_alert',
            self.victim_alert_callback,
            10
        )

        self.sub_count = self.create_subscription(
            Int32,
            '/human_detect/count',
            self.human_count_callback,
            10
        )

        self.get_logger().info("📈 RSSI Real-Time Graph Monitor Initialized!")

    def lora_callback(self, msg: LoraStatus):
        t = time.monotonic() - self.start_time
        with self.lock:
            self.times.append(t)
            self.rssis.append(float(msg.rssi))
            self.snrs.append(float(msg.snr))
            self.latest_rssi = float(msg.rssi)
            self.latest_snr = float(msg.snr)

    def float_callback(self, msg: Float32):
        # Fallback if lora node publishes raw float
        if not self.times or (time.monotonic() - self.start_time - self.times[-1]) > 0.4:
            t = time.monotonic() - self.start_time
            with self.lock:
                self.times.append(t)
                self.rssis.append(float(msg.data))
                self.snrs.append(0.0)
                self.latest_rssi = float(msg.data)

    def human_count_callback(self, msg: Int32):
        if msg.data > 0 and (not self.events or (time.monotonic() - self.start_time - self.events[-1][0]) > 4.0):
            t = time.monotonic() - self.start_time
            with self.lock:
                self.victim_count += msg.data
                self.events.append((t, 'DETECT', f"Human x{msg.data}", self.latest_rssi))

    def victim_alert_callback(self, msg: VictimAlert):
        t = time.monotonic() - self.start_time
        with self.lock:
            lbl = "RELAY DELIVERED" if msg.deferred_relay else "DIRECT ALERT"
            self.events.append((t, 'ALERT', lbl, msg.rssi_at_transmission))


def main(args=None):
    rclpy.init(args=args)
    node = RssiPlotterNode()

    # Spin ROS 2 in background thread
    ros_thread = threading.Thread(target=lambda: rclpy.spin(node), daemon=True)
    ros_thread.start()

    # Setup Matplotlib Figure
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    fig.canvas.manager.set_window_title('ResQTether - Live RSSI & Rescue Telemetry')

    # Lines
    line_rssi, = ax1.plot([], [], color='#00e5ff', linewidth=2.2, label='LoRa RSSI (dBm)')
    line_snr, = ax2.plot([], [], color='#76ff03', linewidth=1.5, label='LoRa SNR (dB)')

    # Shaded threshold zones on ax1
    ax1.axhspan(-65, 0, color='#00e676', alpha=0.15, label='Strong Signal (>= -65 dBm)')
    ax1.axhspan(-75, -65, color='#ffea00', alpha=0.15, label='Marginal (-75 to -65 dBm)')
    ax1.axhspan(-120, -75, color='#ff1744', alpha=0.20, label='Dead Zone (< -75 dBm: Relay Active)')
    ax1.axhline(-75, color='#ff5252', linestyle='--', linewidth=1.2)

    ax1.set_ylabel('Signal Strength (dBm)', fontsize=11, fontweight='bold', color='#ffffff')
    ax1.set_ylim(-110, -35)
    ax1.grid(True, linestyle=':', alpha=0.35, color='#888888')

    ax2.set_xlabel('Time (seconds)', fontsize=11, fontweight='bold', color='#ffffff')
    ax2.set_ylabel('SNR (dB)', fontsize=11, fontweight='bold', color='#ffffff')
    ax2.set_ylim(-15, 15)
    ax2.grid(True, linestyle=':', alpha=0.35, color='#888888')

    title_text = fig.suptitle('📡 ResQTether: Live LoRa RSSI & Autonomous Relay Monitor', fontsize=13, fontweight='bold', color='#00d2ff')
    event_artists = []

    def update(frame):
        nonlocal event_artists
        with node.lock:
            if not node.times:
                return line_rssi, line_snr

            t_list = list(node.times)
            r_list = list(node.rssis)
            s_list = list(node.snrs)
            events_list = list(node.events)
            cur_rssi = node.latest_rssi
            cur_snr = node.latest_snr
            v_count = node.victim_count

        now = t_list[-1]
        x_min = max(0.0, now - node.window_sec)
        x_max = max(node.window_sec, now + 2.0)

        line_rssi.set_data(t_list, r_list)
        line_snr.set_data(t_list, s_list)

        ax1.set_xlim(x_min, x_max)
        ax2.set_xlim(x_min, x_max)

        # Clear old event lines
        for art in event_artists:
            try: art.remove()
            except Exception: pass
        event_artists.clear()

        # Plot event markers
        for (et, kind, lbl, val) in events_list:
            if et >= x_min:
                color = '#ff1744' if kind == 'DETECT' else '#00e5ff'
                vl = ax1.axvline(et, color=color, linestyle=':', linewidth=1.8, alpha=0.85)
                ann = ax1.text(et + 0.3, -45 if kind == 'DETECT' else -52, f"🚨 {lbl}", color=color, fontsize=9, fontweight='bold', rotation=90)
                event_artists.extend([vl, ann])

        # Header status bar
        health = "🟢 STRONG" if cur_rssi >= -65.0 else ("🟡 MARGINAL" if cur_rssi >= -75.0 else "🔴 DEAD ZONE (RELAY)")
        title_text.set_text(
            f"📡 ResQTether RSSI Monitor  |  Current: {cur_rssi:.1f} dBm ({health})  |  SNR: {cur_snr:.1f} dB  |  Victims: {v_count}"
        )

        return line_rssi, line_snr

    ani = animation.FuncAnimation(fig, update, interval=200, blit=False, cache_frame_data=False)
    ax1.legend(loc='lower left', fontsize=9, facecolor='#1e1e24', edgecolor='none')

    plt.tight_layout()
    try:
        plt.show()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
