#!/usr/bin/env python3
"""
dashboard_node.py
-----------------
Unified Mission Control Dashboard Server for ResQTether.
Aggregates and serves:
1. Live 30 FPS Human Detection Video Stream (/stream.mjpg)
2. Live 2D LiDAR Scan Points & Signal Strength Heatmap Overlay (Canvas Radar)
3. Dynamic Rolling RSSI Graph Telemetry
4. Rescue Event Alerts & Victim Discoveries Log
5. On-screen & WASD Keyboard Teleop Controls (/cmd_vel)
"""

import os
import math
import time
import json
import threading
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from ament_index_python.packages import get_package_share_directory

from sensor_msgs.msg import CompressedImage, LaserScan
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32, String, Float32
from visualization_msgs.msg import MarkerArray
from resqtether_interfaces.msg import LoraStatus, VictimAlert


# Shared Global State
STATE_LOCK = threading.Lock()
LATEST_JPEG = None
LATEST_RSSI = -55.0
LATEST_SNR = 0.0
VICTIM_COUNT = 0
MISSION_STATE = "STANDBY"
ALERTS_LOG = []
LATEST_SCAN_PTS = []
LATEST_HEATMAP_CELLS = []
ROBOT_POSE = {'x': 0.0, 'y': 0.0, 'yaw': 0.0}
CMD_VEL_PUB = None


class UnifiedDashboardHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # 1. Main Dashboard HTML
        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            try:
                pkg_dir = get_package_share_directory('resqtether_dashboard')
                html_path = os.path.join(pkg_dir, 'www', 'index.html')
                if not os.path.exists(html_path):
                    # Fallback to local src path
                    html_path = os.path.join(os.path.dirname(__file__), 'www', 'index.html')
                with open(html_path, 'rb') as f:
                    self.wfile.write(f.read())
            except Exception as e:
                self.wfile.write(f"<h3>Error loading dashboard: {e}</h3>".encode('utf-8'))

        # 2. Live MJPEG Video Stream
        elif path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()

            while True:
                with STATE_LOCK:
                    jpg = LATEST_JPEG

                if jpg is not None:
                    try:
                        self.wfile.write(b'--frame\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', str(len(jpg)))
                        self.end_headers()
                        self.wfile.write(jpg)
                        self.wfile.write(b'\r\n')
                    except (BrokenPipeError, ConnectionResetError):
                        break
                time.sleep(0.033)  # ~30 FPS

        # 3. Live Telemetry Endpoint
        elif path == '/telemetry':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            with STATE_LOCK:
                data = {
                    'rssi': float(LATEST_RSSI),
                    'snr': float(LATEST_SNR),
                    'victims': int(VICTIM_COUNT),
                    'state': str(MISSION_STATE),
                    'scan': list(LATEST_SCAN_PTS),
                    'heatmap': list(LATEST_HEATMAP_CELLS),
                    'pose': dict(ROBOT_POSE),
                    'alerts': list(ALERTS_LOG)
                }
            self.wfile.write(json.dumps(data).encode('utf-8'))

        # 4. Teleop Velocity Endpoint
        elif path == '/teleop':
            params = parse_qs(parsed.query)
            vx = float(params.get('vx', [0.0])[0])
            wz = float(params.get('wz', [0.0])[0])

            if CMD_VEL_PUB:
                msg = Twist()
                msg.linear.x = vx
                msg.angular.z = wz
                CMD_VEL_PUB.publish(msg)

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")

        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress HTTP access logging to keep console clean


class CentralDashboardNode(Node):
    def __init__(self):
        super().__init__('central_dashboard_node')
        global CMD_VEL_PUB

        self.declare_parameter('port', 8090)
        self.http_port = int(self.get_parameter('port').value)

        CMD_VEL_PUB = self.create_publisher(Twist, '/cmd_vel', 10)

        # QoS Settings
        qos_best_effort = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5
        )

        # Subscriptions
        self.sub_img = self.create_subscription(
            CompressedImage,
            '/human_detect/image_annotated/compressed',
            self.image_cb,
            qos_best_effort
        )

        self.sub_scan = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_cb,
            qos_best_effort
        )

        self.sub_lora = self.create_subscription(
            LoraStatus,
            '/lora/rssi',
            self.lora_cb,
            10
        )

        self.sub_float_rssi = self.create_subscription(
            Float32,
            '/signal/rssi_measured',
            self.float_rssi_cb,
            10
        )

        self.sub_count = self.create_subscription(
            Int32,
            '/human_detect/count',
            self.count_cb,
            10
        )

        self.sub_state = self.create_subscription(
            String,
            '/rescue/mission_state',
            self.state_cb,
            10
        )

        self.sub_alert = self.create_subscription(
            VictimAlert,
            '/rescue/victim_alert',
            self.alert_cb,
            10
        )

        self.sub_markers = self.create_subscription(
            MarkerArray,
            '/signal_map',
            self.marker_cb,
            10
        )

        self.get_logger().info(f"Central Mission Dashboard node initialized! Web port: {self.http_port}")

    def image_cb(self, msg: CompressedImage):
        global LATEST_JPEG
        with STATE_LOCK:
            LATEST_JPEG = bytes(msg.data)

    def scan_cb(self, msg: LaserScan):
        global LATEST_SCAN_PTS
        # Convert range & angle into 2D (x, y) points relative to robot (downsampled for fast browser rendering)
        pts = []
        angle = msg.angle_min
        step = max(1, len(msg.ranges) // 120)  # ~120 sample points is ideal for 60fps canvas

        for i in range(0, len(msg.ranges), step):
            r = msg.ranges[i]
            cur_angle = msg.angle_min + i * msg.angle_increment
            if not math.isnan(r) and not math.isinf(r) and msg.range_min < r < msg.range_max:
                x = r * math.cos(cur_angle)
                y = r * math.sin(cur_angle)
                pts.append({'x': round(x, 2), 'y': round(y, 2)})

        with STATE_LOCK:
            LATEST_SCAN_PTS = pts

    def lora_cb(self, msg: LoraStatus):
        global LATEST_RSSI, LATEST_SNR
        with STATE_LOCK:
            LATEST_RSSI = float(msg.rssi)
            LATEST_SNR = float(msg.snr)

    def float_rssi_cb(self, msg: Float32):
        global LATEST_RSSI
        with STATE_LOCK:
            LATEST_RSSI = float(msg.data)

    def count_cb(self, msg: Int32):
        global VICTIM_COUNT
        with STATE_LOCK:
            VICTIM_COUNT = max(VICTIM_COUNT, msg.data)

    def state_cb(self, msg: String):
        global MISSION_STATE
        with STATE_LOCK:
            MISSION_STATE = msg.data

    def alert_cb(self, msg: VictimAlert):
        global ALERTS_LOG
        t_str = time.strftime('%H:%M:%S')
        mode = "RELAY DELIVERED" if msg.deferred_relay else "DIRECT"
        text = f"[{t_str}] Victim at ({msg.victim_x:.2f}, {msg.victim_y:.2f}) | {mode} | RSSI: {msg.rssi_at_transmission:.1f} dBm"
        with STATE_LOCK:
            ALERTS_LOG.append(text)

    def marker_cb(self, msg: MarkerArray):
        global LATEST_HEATMAP_CELLS
        cells = []
        for m in msg.markers:
            # Estimate RSSI from marker color
            # Green (g=1.0) >= -60, Yellow >= -75, Red < -75
            rssi_est = -55.0
            if m.color.r > 0.8 and m.color.g < 0.2:
                rssi_est = -85.0
            elif m.color.r > 0.8 and m.color.g > 0.5:
                rssi_est = -70.0

            cells.append({
                'x': round(m.pose.position.x, 2),
                'y': round(m.pose.position.y, 2),
                'rssi': rssi_est,
                'size': round(m.scale.x, 2)
            })

        with STATE_LOCK:
            LATEST_HEATMAP_CELLS = cells


def main(args=None):
    rclpy.init(args=args)
    node = CentralDashboardNode()

    # Run ROS 2 executor in background thread
    ros_thread = threading.Thread(target=lambda: rclpy.spin(node), daemon=True)
    ros_thread.start()

    port = node.http_port
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, UnifiedDashboardHTTPHandler)

    print("\n" + "=" * 65)
    print("  🚀 ResQTether Central Mission Control Dashboard Active!")
    print(f"  💻 Laptop Browser:  http://localhost:{port}")
    print(f"  📱 Mobile / Remote:  http://10.219.174.40:{port}")
    print("=" * 65 + "\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
