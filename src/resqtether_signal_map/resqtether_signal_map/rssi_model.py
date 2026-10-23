import math

def predicted_rssi(distance_m, walls_crossed, tx_ref=-30, n=2.5, wall_penalty=8):
    """
    Predict RSSI using log-distance path loss with wall attenuation.
    RSSI = tx_ref - 10*n*log10(max(distance_m, 1)) - wall_penalty*walls_crossed
    """
    distance = max(distance_m, 1.0)
    return tx_ref - 10 * n * math.log10(distance) - wall_penalty * walls_crossed

def walls_crossed(grid, r1, c1, r2, c2):
    """
    Walks a line between (r1, c1) and (r2, c2) on a 2D grid using Bresenham's algorithm.
    Counts the number of occupied/wall cells (value > 50) passed through.
    """
    walls = 0
    r, c = r1, c1
    dr = abs(r2 - r1)
    dc = abs(c2 - c1)
    sr = 1 if r1 < r2 else -1
    sc = 1 if c1 < c2 else -1
    err = dr - dc

    while True:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            # Typical ROS occupancy grid where > 50 is occupied, 100 is solid wall
            if grid[r][c] > 50:
                walls += 1
                
        if r == r2 and c == c2:
            break
            
        e2 = 2 * err
        if e2 > -dc:
            err -= dc
            r += sr
        if e2 < dr:
            err += dr
            c += sc
            
    return walls
