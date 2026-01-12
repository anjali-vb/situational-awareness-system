import unittest
from vessel import Vessel
from position import Position


class TestVesselChangeHeading(unittest.TestCase):

    def setUp(self):
        self.vessel = Vessel(
            vessel_id="V1",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0,
        )

    def test_change_heading_simple(self):
        """
        Heading should update directly
        """
        self.vessel.change_heading(90.0)
        self.assertEqual(self.vessel.heading_deg, 90.0)

    def test_heading_wrap_above_360(self):
        """
        Heading should wrap correctly above 360
        """
        self.vessel.change_heading(450.0)
        self.assertEqual(self.vessel.heading_deg, 90.0)

    def test_heading_wrap_negative(self):
        """
        Negative heading should wrap correctly
        """
        self.vessel.change_heading(-90.0)
        self.assertEqual(self.vessel.heading_deg, 270.0)

    def test_heading_does_not_move_vessel(self):
        """
        Changing heading should not change position
        """
        self.vessel.change_heading(180.0)

        self.assertEqual(self.vessel.position.x, 0.0)
        self.assertEqual(self.vessel.position.y, 0.0)

    def test_velocity_changes_after_heading_change(self):
        """
        Velocity vector should reflect new heading
        """
        self.vessel.change_heading(90.0)
        vx, vy = self.vessel.velocity_vector()

        self.assertAlmostEqual(vx, 10.0, places=6)
        self.assertAlmostEqual(vy, 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
