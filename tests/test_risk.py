import unittest
from vessel import Vessel
from position import Position
from risk import classify_risk, RiskLevel


class TestRiskClassification(unittest.TestCase):

    def test_danger_case(self):
        """
        Head-on collision → DANGER
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.0, 5.0),
            speed_knots=10.0,
            heading_deg=180.0
        )

        risk = classify_risk(own, target)

        self.assertEqual(risk, RiskLevel.DANGER)

    def test_warning_case(self):
        """
        Close but not immediate collision → WARNING
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(1.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )

        risk = classify_risk(own, target)

        self.assertEqual(risk, RiskLevel.WARNING)

    def test_safe_parallel_motion(self):
        """
        Parallel vessels → SAFE
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=8.0,
            heading_deg=90.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(5.0, 0.0),
            speed_knots=8.0,
            heading_deg=90.0
        )

        risk = classify_risk(own, target)

        self.assertEqual(risk, RiskLevel.SAFE)

    def test_opening_target(self):
        """
        Target moving away → SAFE
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=5.0,
            heading_deg=0.0
        )
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.0, 2.0),
            speed_knots=10.0,
            heading_deg=0.0
        )

        risk = classify_risk(own, target)

        self.assertEqual(risk, RiskLevel.SAFE)


if __name__ == "__main__":
    unittest.main()
