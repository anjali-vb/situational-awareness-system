import unittest
from vessel import Vessel
from position import Position
from motion import relative_velocity


class TestRelativeVelocity(unittest.TestCase):

    def test_same_velocity(self):
        """
        Same speed and heading → zero relative velocity
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=90.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(5.0, 5.0),
            speed_knots=10.0,
            heading_deg=90.0
        )

        dvx, dvy = relative_velocity(own, target)

        self.assertAlmostEqual(dvx, 0.0, places=6)
        self.assertAlmostEqual(dvy, 0.0, places=6)

    def test_target_faster_same_heading(self):
        """
        Target faster than own on same heading
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=8.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.0, 10.0),
            speed_knots=12.0,
            heading_deg=0.0
        )

        dvx, dvy = relative_velocity(own, target)

        self.assertAlmostEqual(dvx, 0.0, places=6)
        self.assertAlmostEqual(dvy, 4.0, places=6)

    def test_opposite_headings(self):
        """
        Own north, target south
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=5.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.0, 20.0),
            speed_knots=5.0,
            heading_deg=180.0
        )

        dvx, dvy = relative_velocity(own, target)

        self.assertAlmostEqual(dvx, 0.0, places=6)
        self.assertAlmostEqual(dvy, -10.0, places=6)

    def test_perpendicular_motion(self):
        """
        Own east, target north
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=6.0,
            heading_deg=90.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(5.0, 5.0),
            speed_knots=6.0,
            heading_deg=0.0
        )

        dvx, dvy = relative_velocity(own, target)

        self.assertAlmostEqual(dvx, -6.0, places=6)
        self.assertAlmostEqual(dvy, 6.0, places=6)


if __name__ == "__main__":
    unittest.main()
