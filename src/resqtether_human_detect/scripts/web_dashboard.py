#!/usr/bin/env python3
"""
web_dashboard.py
----------------
Lightweight Web Video & Rescue Dashboard for ResQTether.
Streams live annotated human detection video and telemetry directly to any browser.
Zero external pip dependencies (built on standard library http.server).
"""

import io
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int32, Float32
from resqtether_interfaces.msg import LoraStatus, VictimAlert

# Shared thread-safe telemetry
LATEST_JPEG = None
LATEST_RSSI = -55.0
LATEST_COUNT = 0
ALERT_LOG = []
LOCK = threading.Lock()

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ResQTether Live Mission Dashboard</title>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: #0f111a;
      color: #fff;
      margin: 0;
      padding: 15px;
      text-align: center;
    }
    h1 {
      color: #00d2ff;
      margin-bottom: 5px;
      font-size: 22px;
    }
    .metrics {
      display: flex;
      justify-content: center;
      gap: 15px;
      margin: 15px auto;
      max-width: 680px;
    }
    .card {
      background: #1c1f2e;
      border: 1px solid #2d3247;
      border-radius: 10px;
      padding: 10px 18px;
      flex: 1;
    }
    .card h3 {
      margin: 0 0 5px 0;
      font-size: 13px;
      color: #8892b0;
      text-transform: uppercase;
    }
    .card .val {
      font-size: 22px;
      font-weight: bold;
      color: #00e676;
    }
    .video-container {
      background: #000;
      border: 2px solid #00d2ff;
      border-radius: 12px;
      overflow: hidden;
      display: inline-block;
      max-width: 100%;
      box-shadow: 0 8px 24px rgba(0, 210, 255, 0.2);
    }
    img {
      display: block;
      width: 100%;
      max-width: 640px;
      height: auto;
    }
    .alerts {
      margin: 20px auto;
      max-width: 680px;
      text-align: left;
      background: #1c1f2e;
      border-radius: 10px;
      padding: 12px 18px;
    }
    .alerts h3 { margin: 0 0 8px 0; color: #ff5252; font-size: 15px; }
    .alert-item {
      font-size: 13px;
      padding: 5px 0;
      border-bottom: 1px solid #282c3f;
      color: #ffd166;
    }
  </style>
</head>
<body>
  <h1>📡 ResQTether: Live Rescue & Human Detection</h1>

  <div class="metrics">
    <div class="card">
      <h3>WiFi Signal</h3>
      <div class="val" id="rssi">-- dBm</div>
    </div>
    <div class="card">
      <h3>Victims In View</h3>
      <div class="val" id="count" style="color: #ff5252;">0</div>
    </div>
    <div class="card">
      <h3>Mission Link</h3>
      <div class="val" id="link" style="color: #00e676;">ONLINE</div>
    </div>
  </div>

  <div class="video-container">
    <img src="/stream.mjpg" alt="Live Camera Stream">
  </div>

  <div class="alerts">
    <h3>🚨 Emergency Rescue Log</h3>
    <div id="alert-list">Waiting for victim detections...</div>
  </div>

  <script>
    setInterval(() => {
      fetch('/status')
        .then(r => r.json())
        .then(data => {
          document.getElementById('rssi').innerText = data.rssi.toFixed(1) + ' dBm';
          document.getElementById('count').innerText = data.count;
          
          let alertHtml = '';
          if (data.alerts && data.alerts.length > 0) {
            data.alerts.slice(-4).reverse().forEach(a => {
              alertHtml += '<div class="alert-item">📍 ' + a + '</div>';
            });
            document.getElementById('alert-list').innerHTML = alertHtml;
          }
        })
        .catch(() => {});
    }, 1000);
  </script>
</body>
</html>
"""


class DashboardHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global LATEST_JPEG, LATEST_RSSI, LATEST_COUNT, ALERT_LOG

        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))

        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            with LOCK:
                json_str = f'{{"rssi": {LATEST_RSSI}, "count": {LATEST_COUNT}, "alerts": {list(ALERT_LOG)}}}'
            self.wfile.write(json_str.encode('utf-8'))

        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()

            while True:
                with LOCK:
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
                time.sleep(0.04)  # ~25 FPS stream
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # Suppress HTTP access logging to keep terminal clean


class WebDashboardNode(Node):
    def __init__(self):
        super().__init__('web_dashboard_node')

        qos_best_effort = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=5
        )

        self.sub_img = self.create_subscription(
            CompressedImage,
            '/human_detect/image_annotated/compressed',
            self.img_callback,
            qos_best_effort
        )

        self.sub_count = self.create_subscription(
            Int32,
            '/human_detect/count',
            self.count_callback,
            10
        )

        self.sub_rssi = self.create_subscription(
            LoraStatus,
            '/lora/rssi',
            self.rssi_callback,
            10
        )

        self.sub_alert = self.create_subscription(
            VictimAlert,
            '/rescue/victim_alert',
            self.alert_callback,
            10
        )

        self.get_logger().info("Web Dashboard Node Subscriptions active!")

    def img_callback(self, msg: CompressedImage):
        global LATEST_JPEG
        with LOCK:
            LATEST_JPEG = bytes(msg.data)

    def count_callback(self, msg: Int32):
        global LATEST_COUNT
        with LOCK:
            LATEST_COUNT = msg.data

    def rssi_callback(self, msg: LoraStatus):
        global LATEST_RSSI
        with LOCK:
            LATEST_RSSI = float(msg.rssi)

    def alert_callback(self, msg: VictimAlert):
        global ALERT_LOG
        t_str = time.strftime('%H:%M:%S')
        text = f"[{t_str}] Victim at ({msg.victim_x:.2f}, {msg.victim_y:.2f}) | {msg.notes}"
        with LOCK:
            ALERT_LOG.append(text)


def main(args=None):
    rclpy.init(args=args)
    ros_node = WebDashboardNode()

    # Start ROS 2 executor in background
    ros_thread = threading.Thread(target=lambda: rclpy.spin(ros_node), daemon=True)
    ros_thread.start()

    # Start Web Server on port 5000
    server_address = ('0.0.0.0', 5000)
    httpd = HTTPServer(server_address, DashboardHTTPHandler)

    print("\n" + "=" * 58)
    print("  🌐 ResQTether Web Mission Dashboard Live!")
    print("  💻 On your Laptop:  http://localhost:5000")
    print("  📱 On your Phone:   http://10.219.174.40:5000")
    print("=" * 58 + "\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        ros_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
