import unittest
from vessel import Vessel
from position import Position
from alert import generate_alert
from risk import RiskLevel


class TestAlert(unittest.TestCase):

    def test_danger_alert(self):
        """
        Head-on collision should produce a DANGER alert
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT1",
            position=Position(0.0, 5.0),
            speed_knots=10.0,
            heading_deg=180.0
        )

        alert = generate_alert(own, target)

        self.assertEqual(alert.target_id, "TGT1")
        self.assertEqual(alert.risk_level, RiskLevel.DANGER)
        self.assertAlmostEqual(alert.cpa_nm, 0.0, places=6)
        self.assertGreater(alert.tcpa_hours, 0)

    def test_safe_parallel_motion(self):
        """
        Parallel vessels should produce SAFE alert
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=8.0,
            heading_deg=90.0
        )
        target = Vessel(
            vessel_id="TGT2",
            position=Position(5.0, 0.0),
            speed_knots=8.0,
            heading_deg=90.0
        )

        alert = generate_alert(own, target)

        self.assertEqual(alert.risk_level, RiskLevel.SAFE)
        self.assertAlmostEqual(alert.cpa_nm, 5.0, places=6)
        self.assertIsNone(alert.tcpa_hours)


if __name__ == "__main__":
    unittest.main()
