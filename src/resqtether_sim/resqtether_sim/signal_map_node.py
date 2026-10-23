#!/usr/bin/env python3
"""
signal_map_node.py
------------------
ROS 2 node that builds a live signal-quality map of the environment.

Subscriptions:
  /map           (nav_msgs/OccupancyGrid)  — live SLAM map
  /pose          (geometry_msgs/PoseStamped) — robot pose from SLAM Toolbox
  /clock         (rosgraph_msgs/Clock)     — sim time

Publishes:
  /signal_map    (visualization_msgs/MarkerArray)
      One cube marker per visited cell, coloured:
        GREEN  RSSI > -60 dBm   (good signal)
        AMBER  RSSI > -75 dBm   (marginal)
        RED    RSSI <= -75 dBm  (poor / dead zone)

The node also logs a wall-count breakdown every 2 seconds so you can
visually confirm the wall-penalty term is firing.
"""

import math
import random

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSReliabilityPolicy

from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA
from builtin_interfaces.msg import Duration

from resqtether_sim.rssi_model import predicted_rssi, walls_crossed, BASE_STATION_X, BASE_STATION_Y

# ── RSSI thresholds (dBm) ────────────────────────────────────────────────────
RSSI_GOOD   = -60.0   # >= good  → green
RSSI_MARGINAL = -75.0 # >= marginal → amber; below → red

# Gaussian noise std-dev added to simulate a real radio measurement
NOISE_STDDEV = 2.0    # dBm

# Marker lifetime — keep old readings visible for this many seconds
MARKER_LIFETIME_S = 0.0   # 0 = forever (cleared on new data only)

class SignalMapNode(Node):

    def __init__(self):
        super().__init__('signal_map_node')

        # Latest occupancy grid
        self._grid: OccupancyGrid | None = None

        # {(cell_col, cell_row): rssi_dBm}
        self._signal_map: dict[tuple[int, int], float] = {}

        self._marker_id_counter = 0
        self._last_log_time = self.get_clock().now()

        # ── QoS ──────────────────────────────────────────────────────────────
        map_qos = QoSProfile(
            depth=1,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            reliability=QoSReliabilityPolicy.RELIABLE,
        )
        pose_qos = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
        )

        # ── Subscribers ───────────────────────────────────────────────────────
        self.create_subscription(OccupancyGrid, '/map', self._map_cb, map_qos)
        self.create_subscription(PoseStamped,   '/pose', self._pose_cb, pose_qos)

        # ── Publisher ─────────────────────────────────────────────────────────
        self._marker_pub = self.create_publisher(
            MarkerArray, '/signal_map', 10)

        self.get_logger().info(
            f'SignalMapNode started. Base station at '
            f'({BASE_STATION_X}, {BASE_STATION_Y}). '
            f'Thresholds: good>{RSSI_GOOD} dBm, marginal>{RSSI_MARGINAL} dBm.'
        )

    # ── Callbacks ─────────────────────────────────────────────────────────────

    def _map_cb(self, msg: OccupancyGrid):
        self._grid = msg

    def _pose_cb(self, msg: PoseStamped):
        if self._grid is None:
            return  # no map yet

        rx = msg.pose.position.x
        ry = msg.pose.position.y

        grid = self._grid
        res   = grid.info.resolution
        ox    = grid.info.origin.position.x
        oy    = grid.info.origin.position.y
        w     = grid.info.width
        h     = grid.info.height
        data  = grid.data

        # ── Distance ─────────────────────────────────────────────────────────
        dist = math.sqrt((rx - BASE_STATION_X)**2 + (ry - BASE_STATION_Y)**2)

        # ── Wall penalty ──────────────────────────────────────────────────────
        wc = walls_crossed(
            data, w, h, res, ox, oy,
            rx, ry,
            BASE_STATION_X, BASE_STATION_Y
        )

        # ── RSSI (predicted + noise) ──────────────────────────────────────────
        rssi = predicted_rssi(dist, wc) + random.gauss(0.0, NOISE_STDDEV)

        # ── Record in map (best-of-N for each cell) ───────────────────────────
        cell_col = int((rx - ox) / res)
        cell_row = int((ry - oy) / res)
        key = (cell_col, cell_row)

        # Keep the latest reading (or average — latest is fine for visualisation)
        self._signal_map[key] = rssi

        # ── Periodic console log ──────────────────────────────────────────────
        now = self.get_clock().now()
        if (now - self._last_log_time).nanoseconds > 2_000_000_000:
            self._last_log_time = now
            self.get_logger().info(
                f'Robot ({rx:.2f}, {ry:.2f}) | '
                f'dist={dist:.2f} m | walls={wc} | '
                f'RSSI={rssi:.1f} dBm'
            )

        # ── Publish MarkerArray ───────────────────────────────────────────────
        self._publish_markers()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _rssi_to_color(self, rssi: float) -> ColorRGBA:
        c = ColorRGBA()
        c.a = 0.75
        if rssi >= RSSI_GOOD:
            c.r, c.g, c.b = 0.0, 1.0, 0.0   # green
        elif rssi >= RSSI_MARGINAL:
            c.r, c.g, c.b = 1.0, 0.65, 0.0  # amber
        else:
            c.r, c.g, c.b = 1.0, 0.0, 0.0   # red
        return c

    def _publish_markers(self):
        if self._grid is None or not self._signal_map:
            return

        res = self._grid.info.resolution
        ox  = self._grid.info.origin.position.x
        oy  = self._grid.info.origin.position.y

        marker_array = MarkerArray()

        # One marker per recorded cell
        for idx, ((col, row), rssi) in enumerate(self._signal_map.items()):
            m = Marker()
            m.header.frame_id = 'map'
            m.header.stamp = self.get_clock().now().to_msg()
            m.ns = 'signal_map'
            m.id = idx
            m.type = Marker.CUBE
            m.action = Marker.ADD

            # Centre of the cell in world frame
            m.pose.position.x = ox + (col + 0.5) * res
            m.pose.position.y = oy + (row + 0.5) * res
            m.pose.position.z = 0.05  # just above ground
            m.pose.orientation.w = 1.0

            m.scale.x = res * 0.9
            m.scale.y = res * 0.9
            m.scale.z = 0.1

            m.color = self._rssi_to_color(rssi)

            m.lifetime = Duration(sec=0, nanosec=0)  # keep forever

            marker_array.markers.append(m)

        self._marker_pub.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    node = SignalMapNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
