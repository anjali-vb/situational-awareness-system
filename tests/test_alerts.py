import unittest
from vessel import Vessel
from position import Position
from alert import generate_alerts
from risk import RiskLevel


class TestGenerateAlerts(unittest.TestCase):

    def setUp(self):
        self.own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0,
        )

    def test_multiple_targets_filter_safe(self):
        """
        Only non-SAFE alerts should be returned by default
        """
        targets = [
            Vessel(
                vessel_id="TGT1",
                position=Position(0.0, 5.0),
                speed_knots=10.0,
                heading_deg=180.0,  # DANGER
            ),
            Vessel(
                vessel_id="TGT2",
                position=Position(5.0, 0.0),
                speed_knots=10.0,
                heading_deg=0.0,  # SAFE (parallel)
            ),
        ]

        alerts = generate_alerts(self.own, targets)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0].target_id, "TGT1")
        self.assertEqual(alerts[0].risk_level, RiskLevel.DANGER)

    def test_include_safe_alerts(self):
        """
        SAFE alerts should be included when requested
        """
        targets = [
            Vessel(
                vessel_id="TGT1",
                position=Position(0.0, 5.0),
                speed_knots=10.0,
                heading_deg=180.0,
            ),
            Vessel(
                vessel_id="TGT2",
                position=Position(5.0, 0.0),
                speed_knots=10.0,
                heading_deg=0.0,
            ),
        ]

        alerts = generate_alerts(self.own, targets, include_safe=True)

        self.assertEqual(len(alerts), 2)
        risk_levels = {a.risk_level for a in alerts}

        self.assertIn(RiskLevel.DANGER, risk_levels)
        self.assertIn(RiskLevel.SAFE, risk_levels)

    def test_no_targets(self):
        """
        Empty target list should return empty alert list
        """
        alerts = generate_alerts(self.own, [])

        self.assertEqual(alerts, [])


if __name__ == "__main__":
    unittest.main()
