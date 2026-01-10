import unittest
from vessel import Vessel




class TestVessel(unittest.TestCase):

    def test_velocity_north(self):
        vessel = Vessel(
            vessel_id="A",
            x=0.0,
            y=0.0,
            speed_knots=10.0,
            heading_deg=0.0
        )
        vx, vy = vessel.velocity_vector()
        self.assertAlmostEqual(vx, 0.0, places=6)
        self.assertAlmostEqual(vy, 10.0, places=6)

    def test_velocity_east(self):
        vessel = Vessel(
            vessel_id="B",
            x=0.0,
            y=0.0,
            speed_knots=5.0,
            heading_deg=90.0
        )
        vx, vy = vessel.velocity_vector()
        self.assertAlmostEqual(vx, 5.0, places=6)
        self.assertAlmostEqual(vy, 0.0, places=6)

    def test_velocity_south(self):
        vessel = Vessel(
            vessel_id="C",
            x=0.0,
            y=0.0,
            speed_knots=12.0,
            heading_deg=180.0
        )
        vx, vy = vessel.velocity_vector()
        self.assertAlmostEqual(vx, 0.0, places=6)
        self.assertAlmostEqual(vy, -12.0, places=6)

    def test_velocity_west(self):
        vessel = Vessel(
            vessel_id="D",
            x=0.0,
            y=0.0,
            speed_knots=7.0,
            heading_deg=270.0
        )
        vx, vy = vessel.velocity_vector()
        self.assertAlmostEqual(vx, -7.0, places=6)
        self.assertAlmostEqual(vy, 0.0, places=6)

    def test_velocity_diagonal(self):
        vessel = Vessel(
            vessel_id="E",
            x=0.0,
            y=0.0,
            speed_knots=10.0,
            heading_deg=45.0
        )
        vx, vy = vessel.velocity_vector()
        self.assertAlmostEqual(vx, 7.0710678, places=6)
        self.assertAlmostEqual(vy, 7.0710678, places=6)


if __name__ == "__main__":
    unittest.main()
