import unittest
from vessel import Vessel
from position import Position


class TestVesselChangeSpeed(unittest.TestCase):

    def setUp(self):
        self.vessel = Vessel(
            vessel_id="V1",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0,
        )

    def test_change_speed_simple(self):
        """
        Speed should update directly
        """
        self.vessel.change_speed(15.0)
        self.assertEqual(self.vessel.speed_knots, 15.0)

    def test_speed_zero_allowed(self):
        """
        Vessel should be allowed to stop
        """
        self.vessel.change_speed(0.0)
        self.assertEqual(self.vessel.speed_knots, 0.0)

    def test_negative_speed_rejected(self):
        """
        Negative speeds must raise ValueError
        """
        with self.assertRaises(ValueError):
            self.vessel.change_speed(-5.0)

    def test_speed_change_does_not_move_vessel(self):
        """
        Changing speed should not change position
        """
        self.vessel.change_speed(5.0)

        self.assertEqual(self.vessel.position.x, 0.0)
        self.assertEqual(self.vessel.position.y, 0.0)

    def test_velocity_changes_after_speed_change(self):
        """
        Velocity vector should reflect new speed
        """
        self.vessel.change_speed(20.0)
        vx, vy = self.vessel.velocity_vector()

        self.assertAlmostEqual(vx, 0.0, places=6)
        self.assertAlmostEqual(vy, 20.0, places=6)


if __name__ == "__main__":
    unittest.main()
