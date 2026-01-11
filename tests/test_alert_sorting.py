import unittest
from alert import Alert, sort_alerts
from risk import RiskLevel


class TestAlertSorting(unittest.TestCase):

    def test_sort_by_risk_level(self):
        alerts = [
            Alert("T1", RiskLevel.SAFE, 5.0, None),
            Alert("T2", RiskLevel.DANGER, 1.0, 0.1),
            Alert("T3", RiskLevel.WARNING, 0.8, 0.2),
        ]

        sorted_alerts = sort_alerts(alerts)

        self.assertEqual(sorted_alerts[0].target_id, "T2")  # DANGER
        self.assertEqual(sorted_alerts[1].target_id, "T3")  # WARNING
        self.assertEqual(sorted_alerts[2].target_id, "T1")  # SAFE

    def test_sort_by_cpa_within_same_risk(self):
        alerts = [
            Alert("T1", RiskLevel.DANGER, 1.5, 0.3),
            Alert("T2", RiskLevel.DANGER, 0.4, 0.1),
            Alert("T3", RiskLevel.DANGER, 0.8, 0.2),
        ]

        sorted_alerts = sort_alerts(alerts)

        self.assertEqual(
            [a.target_id for a in sorted_alerts],
            ["T2", "T3", "T1"],
        )

    def test_none_cpa_goes_last(self):
        alerts = [
            Alert("T1", RiskLevel.WARNING, None, None),
            Alert("T2", RiskLevel.WARNING, 2.0, 0.5),
        ]

        sorted_alerts = sort_alerts(alerts)

        self.assertEqual(sorted_alerts[0].target_id, "T2")
        self.assertEqual(sorted_alerts[1].target_id, "T1")

    def test_empty_list(self):
        self.assertEqual(sort_alerts([]), [])


if __name__ == "__main__":
    unittest.main()
