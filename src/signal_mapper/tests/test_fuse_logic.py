"""
test_fuse_logic.py
------------------
Pure pytest unit tests for the SLAM pose + LoRa RSSI fusion logic.
Tests coordinate discretization, cell running averages, and CSV logging.
"""

import math
import os
import sys
import tempfile
import pytest

# Ensure signal_mapper is importable when running pytest standalone
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from signal_mapper.fuse_core import SignalMapAggregator


def test_world_to_cell_discretization():
    agg = SignalMapAggregator(cell_size=0.25, csv_path=tempfile.mktemp())
    
    # Positive quadrant
    cx, cy = agg.world_to_cell(0.1, 0.2)
    assert (cx, cy) == (0, 0)
    
    cx, cy = agg.world_to_cell(0.26, 0.51)
    assert (cx, cy) == (1, 2)
    
    # Negative quadrant
    cx, cy = agg.world_to_cell(-0.1, -0.2)
    assert (cx, cy) == (-1, -1)

    cx, cy = agg.world_to_cell(-0.3, -0.6)
    assert (cx, cy) == (-2, -3)


def test_single_cell_rssi_averaging():
    temp_csv = tempfile.mktemp(suffix=".csv")
    agg = SignalMapAggregator(cell_size=0.25, csv_path=temp_csv)

    # Add 3 readings within the same cell (0, 0) [x: 0.0 to 0.24, y: 0.0 to 0.24]
    agg.add_reading(x=0.05, y=0.05, rssi=-40.0, snr=10.0, sender_id="base", timestamp=1.0)
    agg.add_reading(x=0.10, y=0.15, rssi=-50.0, snr=8.0, sender_id="base", timestamp=2.0)
    agg.add_reading(x=0.20, y=0.20, rssi=-60.0, snr=6.0, sender_id="base", timestamp=3.0)

    # Average should be (-40 + -50 + -60) / 3 = -50.0 dBm
    avg = agg.get_cell_average(0, 0)
    assert pytest.approx(avg, 0.01) == -50.0


def test_multiple_cells_and_averages():
    temp_csv = tempfile.mktemp(suffix=".csv")
    agg = SignalMapAggregator(cell_size=0.5, csv_path=temp_csv)

    # Cell (2, 2) -> (x: 1.0 to 1.5, y: 1.0 to 1.5)
    agg.add_reading(x=1.1, y=1.1, rssi=-45.0, snr=9.0, sender_id="b1", timestamp=10.0)
    agg.add_reading(x=1.2, y=1.2, rssi=-55.0, snr=7.0, sender_id="b1", timestamp=11.0)

    # Cell (-2, 0) -> (x: -1.0 to -0.5, y: 0.0 to 0.5)
    agg.add_reading(x=-0.8, y=0.2, rssi=-80.0, snr=-2.0, sender_id="b1", timestamp=12.0)

    all_avgs = agg.get_all_cell_averages()
    assert len(all_avgs) == 2
    assert pytest.approx(all_avgs[(2, 2)], 0.01) == -50.0
    assert pytest.approx(all_avgs[(-2, 0)], 0.01) == -80.0


def test_csv_file_persistence():
    temp_csv = tempfile.mktemp(suffix=".csv")
    agg = SignalMapAggregator(cell_size=0.25, csv_path=temp_csv)

    agg.add_reading(x=1.5, y=-2.5, rssi=-68.4, snr=4.2, sender_id="beacon_01", timestamp=100.123)

    assert os.path.exists(temp_csv)
    with open(temp_csv, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 2  # Header + 1 data row
    assert "timestamp,x,y,rssi,snr,sender_id" in lines[0]
    assert "100.123,1.5000,-2.5000,-68.40,4.20,beacon_01" in lines[1]
