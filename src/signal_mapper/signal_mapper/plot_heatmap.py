#!/usr/bin/env python3
"""
plot_heatmap.py
---------------
Offline analysis and visualization tool.
Reads signal_map.csv and creates a color-coded RSSI signal heatmap.
If a saved SLAM map (map.yaml + map.pgm) exists, overlays the heatmap
directly on top of the floorplan image in the correct coordinate frame.
"""

import os
import sys
import yaml
import numpy as np
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from PIL import Image


def load_slam_map():
    """Finds and loads saved SLAM map metadata and image if available."""
    candidates = [
        ('test_map.yaml', 'test_map.pgm'),
        ('map.yaml', 'map.pgm'),
        ('room_map.yaml', 'room_map.pgm'),
    ]

    for yaml_file, pgm_file in candidates:
        if os.path.exists(yaml_file) and os.path.exists(pgm_file):
            print(f"🗺️  Found SLAM map floorplan: {yaml_file} and {pgm_file}")
            with open(yaml_file, 'r') as f:
                map_meta = yaml.safe_load(f)

            res = map_meta.get('resolution', 0.05)
            origin = map_meta.get('origin', [0.0, 0.0, 0.0])
            ox, oy = origin[0], origin[1]

            img = Image.open(pgm_file)
            img_arr = np.array(img)
            height, width = img_arr.shape

            extent = [ox, ox + width * res, oy, oy + height * res]
            return img_arr, extent

    print("ℹ️  No saved SLAM map found in current directory. Generating heatmap without floorplan background.")
    return None, None


def main():
    csv_file = "signal_map.csv"
    if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
        print(f"❌ Error: '{csv_file}' not found or empty! Run fuse_node first to log readings.")
        sys.exit(1)

    xs, ys, rssis = [], [], []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                xs.append(float(row['x']))
                ys.append(float(row['y']))
                rssis.append(float(row['rssi']))
            except (ValueError, KeyError):
                continue

    if len(xs) == 0:
        print(f"❌ Error: '{csv_file}' contains no valid data rows.")
        sys.exit(1)

    xs = np.array(xs)
    ys = np.array(ys)
    rssis = np.array(rssis)

    print(f"📊 Loaded {len(xs)} signal readings from '{csv_file}'.")
    print(f"   RSSI Range: [{rssis.min():.1f} dBm, {rssis.max():.1f} dBm]")
    print(f"   Position Bounds: X=[{xs.min():.2f}, {xs.max():.2f}], Y=[{ys.min():.2f}, {ys.max():.2f}]")

    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)

    # 1. Overlay SLAM Map Floorplan if present
    map_img, extent = load_slam_map()
    if map_img is not None:
        ax.imshow(
            map_img,
            cmap='gray',
            origin='lower',
            extent=extent,
            alpha=0.65
        )

    # 2. Plot RSSI Scatter Heatmap
    # Normalize between -90 dBm (weak) and -40 dBm (strong)
    norm = Normalize(vmin=-90.0, vmax=-40.0)
    scatter = ax.scatter(
        xs,
        ys,
        c=rssis,
        cmap='RdYlGn',  # Red (weak) -> Yellow -> Green (strong)
        norm=norm,
        s=90,
        edgecolors='black',
        linewidth=0.6,
        alpha=0.9,
        label='WiFi RSSI Observations'
    )

    # Add path line connecting observations
    ax.plot(xs, ys, color='blue', linestyle='--', linewidth=0.8, alpha=0.5, label='Robot Trajectory')

    # Start and End points
    ax.scatter(xs[0], ys[0], color='cyan', marker='^', s=150, zorder=5, label='Start')
    ax.scatter(xs[-1], ys[-1], color='magenta', marker='v', s=150, zorder=5, label='Latest')

    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('LoRa Signal Strength (RSSI in dBm)', rotation=270, labelpad=18, fontsize=11, fontweight='bold')

    ax.set_title('ResQTether: SLAM Floorplan & LoRa Signal Quality Heatmap', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Map X Position (meters)', fontsize=11)
    ax.set_ylabel('Map Y Position (meters)', fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.set_aspect('equal', adjustable='datalim')

    output_png = "signal_heatmap.png"
    plt.tight_layout()
    plt.savefig(output_png, bbox_inches='tight')
    print(f"✅ Saved high-resolution heatmap to '{output_png}'!")

    try:
        plt.show()
    except Exception:
        pass


if __name__ == '__main__':
    main()
