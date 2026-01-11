import unittest
from vessel import Vessel
from position import Position


class TestVesselStep(unittest.TestCase):

    def test_zero_time_step(self):
        """
        Zero dt should not change position
        """
        vessel = Vessel(
            vessel_id="E",
            position=Position(3.0, -2.0),
            speed_knots=12.0,
            heading_deg=270.0
        )

        vessel.step(0.0)

        self.assertEqual(vessel.position, Position(3.0, -2.0))


    def test_step_north(self):
        """
        10 knots north for 1 hour → move 10 nm north
        """
        vessel = Vessel(
            vessel_id="A",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )

        vessel.step(1.0)

        self.assertAlmostEqual(vessel.position.x, 0.0, places=6)
        self.assertAlmostEqual(vessel.position.y, 10.0, places=6)

    def test_step_east_half_hour(self):
        """
        8 knots east for 0.5 hours → move 4 nm east
        """
        vessel = Vessel(
            vessel_id="B",
            position=Position(1.0, 1.0),
            speed_knots=8.0,
            heading_deg=90.0
        )

        vessel.step(0.5)

        self.assertAlmostEqual(vessel.position.x, 5.0, places=6)
        self.assertAlmostEqual(vessel.position.y, 1.0, places=6)

    def test_step_south(self):
        """
        6 knots south for 2 hours → move 12 nm south
        """
        vessel = Vessel(
            vessel_id="C",
            position=Position(0.0, 0.0),
            speed_knots=6.0,
            heading_deg=180.0
        )

        vessel.step(2.0)

        self.assertAlmostEqual(vessel.position.x, 0.0, places=6)
        self.assertAlmostEqual(vessel.position.y, -12.0, places=6)

    def test_step_diagonal(self):
        """
        10 knots at 45° for 1 hour → move equally in x and y
        """
        vessel = Vessel(
            vessel_id="D",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=45.0
        )

        vessel.step(1.0)

        self.assertAlmostEqual(vessel.position.x, 7.0710678, places=6)
        self.assertAlmostEqual(vessel.position.y, 7.0710678, places=6)


if __name__ == "__main__":
    unittest.main()
