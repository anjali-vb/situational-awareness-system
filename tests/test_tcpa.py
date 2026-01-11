import unittest
from vessel import Vessel
from position import Position
from cpa import tcpa


class TestTCPA(unittest.TestCase):

    def test_head_on_approach(self):
        """
        Head-on vessels closing at 20 knots, 10 nm apart
        → TCPA = 0.5 hours
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.0, 10.0),
            speed_knots=10.0,
            heading_deg=180.0
        )

        t = tcpa(own, target)

        self.assertAlmostEqual(t, 0.5, places=6)

    def test_overtaking(self):
        """
        Own faster than target, same heading
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=12.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.0, 6.0),
            speed_knots=8.0,
            heading_deg=0.0
        )

        t = tcpa(own, target)

        self.assertAlmostEqual(t, 1.5, places=6)

    def test_opening_targets(self):
        """
        Target moving away → TCPA negative
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=5.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.0, 10.0),
            speed_knots=8.0,
            heading_deg=0.0
        )

        t = tcpa(own, target)

        self.assertLess(t, 0.0)

    def test_zero_relative_velocity(self):
        """
        Same speed and heading → no CPA in time
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

        t = tcpa(own, target)

        self.assertIsNone(t)


if __name__ == "__main__":
    unittest.main()
