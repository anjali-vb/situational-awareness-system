import unittest
from alert import Alert, alert_text
from risk import RiskLevel


class TestAlertText(unittest.TestCase):

    def test_danger_alert_text(self):
        """
        Closing danger case
        """
        alert = Alert(
            target_id="TGT1",
            risk_level=RiskLevel.DANGER,
            cpa_nm=0.3,
            tcpa_hours=0.2,  # 12 minutes
        )

        text = alert_text(alert)

        self.assertEqual(text, "CPA 0.3 nm in 12 min – DANGER")

    def test_warning_alert_text(self):
        """
        Warning case with longer TCPA
        """
        alert = Alert(
            target_id="TGT2",
            risk_level=RiskLevel.WARNING,
            cpa_nm=1.2,
            tcpa_hours=0.5,  # 30 minutes
        )

        text = alert_text(alert)

        self.assertEqual(text, "CPA 1.2 nm in 30 min – WARNING")

    def test_parallel_motion_text(self):
        """
        CPA exists but TCPA is undefined
        """
        alert = Alert(
            target_id="TGT3",
            risk_level=RiskLevel.SAFE,
            cpa_nm=5.0,
            tcpa_hours=None,
        )

        text = alert_text(alert)

        self.assertEqual(text, "CPA 5.0 nm – SAFE")

    def test_opening_target_text(self):
        """
        TCPA negative → opening situation
        """
        alert = Alert(
            target_id="TGT4",
            risk_level=RiskLevel.SAFE,
            cpa_nm=2.5,
            tcpa_hours=-0.3,
        )

        text = alert_text(alert)

        self.assertEqual(text, "Opening, CPA 2.5 nm – SAFE")

    def test_no_cpa_text(self):
        """
        CPA undefined
        """
        alert = Alert(
            target_id="TGT5",
            risk_level=RiskLevel.SAFE,
            cpa_nm=None,
            tcpa_hours=None,
        )

        text = alert_text(alert)

        self.assertEqual(text, "No collision risk – SAFE")


if __name__ == "__main__":
    unittest.main()
