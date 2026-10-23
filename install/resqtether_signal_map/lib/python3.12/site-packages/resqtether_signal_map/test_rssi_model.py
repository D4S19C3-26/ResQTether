import math
import unittest
from rssi_model import predicted_rssi, walls_crossed

class TestRSSIModel(unittest.TestCase):
    def test_rssi_decreases_with_distance(self):
        rssi_close = predicted_rssi(distance_m=2.0, walls_crossed=0)
        rssi_far = predicted_rssi(distance_m=10.0, walls_crossed=0)
        self.assertLess(rssi_far, rssi_close)
        
    def test_rssi_decreases_with_walls(self):
        rssi_no_walls = predicted_rssi(distance_m=5.0, walls_crossed=0)
        rssi_with_walls = predicted_rssi(distance_m=5.0, walls_crossed=2)
        self.assertLess(rssi_with_walls, rssi_no_walls)
        
    def test_output_is_finite_float(self):
        rssi = predicted_rssi(distance_m=0.0, walls_crossed=0) # max(d, 1) handles 0
        self.assertTrue(math.isfinite(rssi))
        self.assertIsInstance(rssi, float)
        
    def test_walls_crossed_no_walls(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.assertEqual(walls_crossed(grid, 0, 0, 2, 2), 0)
        
    def test_walls_crossed_with_walls(self):
        grid = [
            [0,   0, 0],
            [100, 100, 100],
            [0,   0, 0]
        ]
        self.assertEqual(walls_crossed(grid, 0, 1, 2, 1), 1)

if __name__ == '__main__':
    unittest.main()
