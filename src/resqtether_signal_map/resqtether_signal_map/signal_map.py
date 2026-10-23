import math
try:
    from .rssi_model import predicted_rssi, walls_crossed
except ImportError:
    from rssi_model import predicted_rssi, walls_crossed

class SignalQualityMap:
    def __init__(self, grid, resolution=1.0, origin_x=0.0, origin_y=0.0):
        """
        grid: 2D array-like (list of lists or numpy array)
        resolution: meters per cell
        origin_x, origin_y: coordinates of the grid origin (r=0, c=0) in meters
        """
        self.grid = grid
        self.resolution = resolution
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.measurements = [] # List of (pose, rssi_value)
        
    def _pose_to_grid(self, x, y):
        c = int((x - self.origin_x) / self.resolution)
        r = int((y - self.origin_y) / self.resolution)
        return r, c
        
    def _grid_to_pose(self, r, c):
        x = self.origin_x + (c + 0.5) * self.resolution
        y = self.origin_y + (r + 0.5) * self.resolution
        return x, y
        
    def log_measurement(self, pose, rssi_value):
        """pose is an (x, y) tuple."""
        self.measurements.append((pose, rssi_value))
        
    def predict(self, pose, base_pose):
        """Predict RSSI at pose given the base station pose."""
        x1, y1 = pose
        x2, y2 = base_pose
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        r1, c1 = self._pose_to_grid(x1, y1)
        r2, c2 = self._pose_to_grid(x2, y2)
        
        walls = walls_crossed(self.grid, r1, c1, r2, c2)
        
        return predicted_rssi(distance, walls)
        
    def get_map_overlay(self, base_pose):
        """
        Returns a 2D array of predicted RSSI values across the whole grid.
        base_pose is (x, y) tuple.
        """
        if not self.grid or not self.grid[0]:
            return []
            
        rows = len(self.grid)
        cols = len(self.grid[0])
        overlay = []
        
        for r in range(rows):
            row_overlay = []
            for c in range(cols):
                pose = self._grid_to_pose(r, c)
                rssi = self.predict(pose, base_pose)
                row_overlay.append(rssi)
            overlay.append(row_overlay)
            
        return overlay

if __name__ == "__main__":
    # Standalone test printing a heatmap
    # A small 5x5 grid with a vertical wall down the middle (c=2)
    grid = [
        [0, 0, 100, 0, 0],
        [0, 0, 100, 0, 0],
        [0, 0, 100, 0, 0],
        [0, 0, 100, 0, 0],
        [0, 0,   0, 0, 0] # gap in the wall
    ]
    sq_map = SignalQualityMap(grid, resolution=1.0)
    base = sq_map._grid_to_pose(2, 0) # Base station on the left side
    overlay = sq_map.get_map_overlay(base)
    
    print("Predicted RSSI Heatmap (Base at r=2, c=0):")
    print("Wall is at c=2 (values are much lower on the right side of the wall)")
    print("-" * 50)
    for r in range(len(overlay)):
        row_str = " ".join(f"{val:6.1f}" for val in overlay[r])
        print(row_str)
