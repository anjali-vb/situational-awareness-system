import unittest
from vessel import Vessel
from position import Position
from motion import relative_position


class TestRelativePosition(unittest.TestCase):

    def test_target_northeast_of_own(self):
        """
        Target at (3, 4), own at (0, 0)
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=0.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(3.0, 4.0),
            speed_knots=0.0,
            heading_deg=0.0
        )

        dx, dy = relative_position(own, target)

        self.assertEqual(dx, 3.0)
        self.assertEqual(dy, 4.0)

    def test_target_southwest_of_own(self):
        """
        Target at (-2, -5), own at (1, 1)
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(1.0, 1.0),
            speed_knots=0.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(-2.0, -5.0),
            speed_knots=0.0,
            heading_deg=0.0
        )

        dx, dy = relative_position(own, target)

        self.assertEqual(dx, -3.0)
        self.assertEqual(dy, -6.0)

    def test_same_position(self):
        """
        Target and own at the same position
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(5.0, -3.0),
            speed_knots=0.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(5.0, -3.0),
            speed_knots=0.0,
            heading_deg=0.0
        )

        dx, dy = relative_position(own, target)

        self.assertEqual(dx, 0.0)
        self.assertEqual(dy, 0.0)


if __name__ == "__main__":
    unittest.main()
