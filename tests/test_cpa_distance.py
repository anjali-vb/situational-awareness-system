import unittest
from vessel import Vessel
from position import Position
from cpa import cpa_distance


class TestCPADistance(unittest.TestCase):

    def test_head_on_collision(self):
        """
        Head-on vessels should have CPA distance = 0
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

        d = cpa_distance(own, target)

        self.assertAlmostEqual(d, 0.0, places=6)

    def test_parallel_tracks(self):
        """
        Parallel vessels maintain constant separation
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(3.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )

        d = cpa_distance(own, target)

        self.assertAlmostEqual(d, 3.0, places=6)

    def test_crossing_situation(self):
        """
        Crossing paths at right angles
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=90.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(10.0, -10.0),
            speed_knots=10.0,
            heading_deg=0.0
        )

        d = cpa_distance(own, target)

        self.assertAlmostEqual(d, 0.0, places=6)

    def test_zero_relative_velocity(self):
      """
      Same speed and heading → CPA equals current separation
      """
      own = Vessel(
          vessel_id="OWN",
          position=Position(0.0, 0.0),
          speed_knots=8.0,
          heading_deg=45.0
      )
      target = Vessel(
          vessel_id="TGT",
          position=Position(5.0, 5.0),
          speed_knots=8.0,
          heading_deg=45.0
      )

      d = cpa_distance(own, target)

      self.assertAlmostEqual(d, 7.0710678, places=6)



if __name__ == "__main__":
    unittest.main()
