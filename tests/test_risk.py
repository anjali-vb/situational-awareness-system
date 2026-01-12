import unittest
from vessel import Vessel
from position import Position
from risk import classify_risk, RiskLevel, DANGER_TCPA_HOURS, WARNING_TCPA_HOURS


class TestRiskClassification(unittest.TestCase):

    def test_danger_head_on_collision(self):
        """
        Head-on collision within 30 minutes → DANGER
        CPA ≈ 0 nm, TCPA = 5nm / 20kts = 0.25 hours (15 min)
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

    def test_danger_close_cpa_but_far_tcpa_is_safe(self):
        """
        Close CPA but TCPA > 30 minutes → SAFE (not immediate threat)
        CPA ≈ 0 nm, but far away so TCPA > 0.5 hours
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=5.0,
            heading_deg=0.0
        )
        # Target 20nm away, closing at 10 knots → TCPA = 2 hours
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.0, 20.0),
            speed_knots=5.0,
            heading_deg=180.0
        )

        risk = classify_risk(own, target)

        # CPA is very close but TCPA > 30 min, so not DANGER
        # But TCPA (2 hours) > 1 hour, so not WARNING either
        self.assertEqual(risk, RiskLevel.SAFE)

    def test_warning_close_cpa_within_hour(self):
        """
        CPA within warning threshold and TCPA within 1 hour → WARNING
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )
        # Target 1nm to the side, parallel course
        # CPA = 1nm (within WARNING_CPA_NM), TCPA = 0 (parallel)
        target = Vessel(
            vessel_id="TGT",
            position=Position(1.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )

        risk = classify_risk(own, target)

        self.assertEqual(risk, RiskLevel.WARNING)

    def test_warning_moderate_cpa_soon(self):
        """
        Moderate CPA (1nm) happening within 1 hour → WARNING
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=90.0  # heading east
        )
        # Target approaching from the side, will pass about 1nm ahead
        target = Vessel(
            vessel_id="TGT",
            position=Position(5.0, 1.0),
            speed_knots=10.0,
            heading_deg=270.0  # heading west
        )

        risk = classify_risk(own, target)

        self.assertEqual(risk, RiskLevel.WARNING)

    def test_safe_parallel_motion_far_apart(self):
        """
        Parallel vessels far apart → SAFE
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

    def test_safe_opening_target(self):
        """
        Target moving away (TCPA < 0) → SAFE
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

    def test_safe_large_cpa(self):
        """
        Large CPA even if TCPA is soon → SAFE
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )
        # Target 5nm to the side, parallel course - CPA = 5nm
        target = Vessel(
            vessel_id="TGT",
            position=Position(5.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )

        risk = classify_risk(own, target)

        self.assertEqual(risk, RiskLevel.SAFE)

    def test_danger_threshold_boundary(self):
        """
        At DANGER thresholds → DANGER
        CPA ≈ 0.4nm (within 0.5nm), TCPA ≈ 0.45 hours (within 0.5 hours)
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )
        # Target offset 0.4nm, head-on at distance where TCPA < 0.5 hours
        # At closing speed of 20 knots, need distance < 10nm
        # Using 9nm gives TCPA = 0.45 hours
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.4, 9.0),
            speed_knots=10.0,
            heading_deg=180.0
        )

        risk = classify_risk(own, target)

        self.assertEqual(risk, RiskLevel.DANGER)

    def test_warning_when_cpa_danger_but_tcpa_warning(self):
        """
        CPA in DANGER range but TCPA only in WARNING range → WARNING
        CPA < 0.5nm, 0.5 < TCPA <= 1.0 hours
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0
        )
        # Head-on collision but 15nm away
        # TCPA = 15nm / 20kts = 0.75 hours (45 min)
        target = Vessel(
            vessel_id="TGT",
            position=Position(0.0, 15.0),
            speed_knots=10.0,
            heading_deg=180.0
        )

        risk = classify_risk(own, target)

        # CPA ≈ 0 (DANGER range), but TCPA = 0.75 hours (> 0.5, so not DANGER)
        # Since CPA < 1.5 and TCPA < 1.0, it's WARNING
        self.assertEqual(risk, RiskLevel.WARNING)


if __name__ == "__main__":
    unittest.main()
