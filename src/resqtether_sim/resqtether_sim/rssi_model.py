import math

# Base station world coordinates — must match the world file
BASE_STATION_X = -4.5
BASE_STATION_Y = -4.5


def predicted_rssi(distance_m, walls_crossed_count, tx_ref=-30, n=2.5, wall_penalty=8):
    """
    Log-distance path-loss model with wall attenuation penalty.
    Ported from the validated HTML/JS interactive demo.

    RSSI = tx_ref - 10*n*log10(max(d, 1)) - wall_penalty * walls_crossed

    Args:
        distance_m:       Distance in metres (clamped to >= 1 m to avoid log(0)).
        walls_crossed_count: Number of occupied grid cells the LOS passes through.
        tx_ref:           Reference RSSI at 1 m (dBm). Default -30.
        n:                Path-loss exponent. Default 2.5.
        wall_penalty:     Per-wall attenuation in dB. Default 8.

    Returns:
        Predicted RSSI as a float (dBm).
    """
    distance = max(float(distance_m), 1.0)
    return tx_ref - 10.0 * n * math.log10(distance) - wall_penalty * walls_crossed_count


def walls_crossed(grid, width, height, resolution, origin_x, origin_y, x1, y1, x2, y2):
    """
    Raycast between two world-coordinate points on an OccupancyGrid,
    counting the number of occupied cells (value > 50) crossed.

    Uses Bresenham's line algorithm — same logic as the validated JS demo.

    Args:
        grid:       Flat list/array of occupancy values (row-major, 0–100, -1 unknown).
        width:      Grid width in cells.
        height:     Grid height in cells.
        resolution: Metres per cell.
        origin_x, origin_y: World coords of cell (0, 0).
        x1, y1:    Start point in world coordinates.
        x2, y2:    End point in world coordinates.

    Returns:
        Integer count of occupied cells crossed.
    """
    def world_to_cell(wx, wy):
        cx = int((wx - origin_x) / resolution)
        cy = int((wy - origin_y) / resolution)
        return cx, cy

    def cell_occupied(cx, cy):
        if cx < 0 or cx >= width or cy < 0 or cy >= height:
            return False
        val = grid[cy * width + cx]
        return val > 50  # Standard ROS occupancy threshold

    c1x, c1y = world_to_cell(x1, y1)
    c2x, c2y = world_to_cell(x2, y2)

    # Bresenham's line algorithm
    count = 0
    dx = abs(c2x - c1x)
    dy = abs(c2y - c1y)
    sx = 1 if c1x < c2x else -1
    sy = 1 if c1y < c2y else -1
    err = dx - dy
    cx, cy = c1x, c1y

    while True:
        if cell_occupied(cx, cy):
            count += 1
        if cx == c2x and cy == c2y:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            cx += sx
        if e2 < dx:
            err += dx
            cy += sy

    return count
