"""
fuse_core.py
------------
Pure Python core math and data structures for spatial RSSI grid binning,
running average computation, and live CSV persistence.
Independent of ROS 2 runtime for pure logic unit testing.
"""

import csv
import math
import os
from typing import Dict, List, Tuple


class SignalMapAggregator:
    def __init__(self, cell_size: float = 0.25, csv_path: str = "signal_map.csv"):
        """
        Args:
            cell_size: Dimension of each grid cell in metres (default 0.25m).
            csv_path:  Filepath for continuous live logging.
        """
        self.cell_size = float(cell_size)
        self.csv_path = csv_path

        # Stores list of all RSSI readings falling into each cell: {(cell_x, cell_y): [rssi1, rssi2, ...]}
        self.grid_cells: Dict[Tuple[int, int], List[float]] = {}
        self.readings: List[dict] = []

        self._init_csv()

    def _init_csv(self):
        """Initializes the CSV header if file does not exist or is empty."""
        if not os.path.exists(self.csv_path) or os.path.getsize(self.csv_path) == 0:
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'x', 'y', 'rssi', 'snr', 'sender_id'])

    def world_to_cell(self, x: float, y: float) -> Tuple[int, int]:
        """Maps continuous world coordinates (x, y) into integer discrete grid cell indices."""
        cx = math.floor(float(x) / self.cell_size)
        cy = math.floor(float(y) / self.cell_size)
        return int(cx), int(cy)

    def cell_to_world(self, cx: int, cy: int) -> Tuple[float, float]:
        """Returns the world-coordinate center (x, y) of a given cell index."""
        wx = (cx + 0.5) * self.cell_size
        wy = (cy + 0.5) * self.cell_size
        return float(wx), float(wy)

    def add_reading(self, x: float, y: float, rssi: float, snr: float, sender_id: str, timestamp: float):
        """
        Logs a new pose + RSSI observation, updates cell running statistics,
        and immediately appends to CSV disk file.
        """
        record = {
            'timestamp': float(timestamp),
            'x': float(x),
            'y': float(y),
            'rssi': float(rssi),
            'snr': float(snr),
            'sender_id': str(sender_id)
        }
        self.readings.append(record)

        cell = self.world_to_cell(x, y)
        if cell not in self.grid_cells:
            self.grid_cells[cell] = []
        self.grid_cells[cell].append(float(rssi))

        # Append live to CSV file with flush to guarantee persistence
        with open(self.csv_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                f"{timestamp:.3f}",
                f"{x:.4f}",
                f"{y:.4f}",
                f"{rssi:.2f}",
                f"{snr:.2f}",
                str(sender_id)
            ])
            f.flush()

    def get_cell_average(self, cx: int, cy: int) -> float:
        """Returns the average RSSI for a specific cell, or NaN if no readings exist."""
        vals = self.grid_cells.get((cx, cy), [])
        if not vals:
            return float('nan')
        return sum(vals) / len(vals)

    def get_all_cell_averages(self) -> Dict[Tuple[int, int], float]:
        """Returns a dictionary mapping all visited (cx, cy) cells to their average RSSI."""
        return {cell: sum(vals) / len(vals) for cell, vals in self.grid_cells.items()}
