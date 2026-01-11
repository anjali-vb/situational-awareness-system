import unittest
from world import World
from vessel import Vessel
from position import Position
from risk import RiskLevel


class TestWorldSnapshotWithAlerts(unittest.TestCase):

    def setUp(self):
        self.own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0,
        )

        self.target = Vessel(
            vessel_id="TGT1",
            position=Position(0.0, 5.0),
            speed_knots=10.0,
            heading_deg=180.0,
        )

        self.world = World(self.own, [self.target])

    def test_snapshot_contains_alert_block(self):
        """
        Snapshot should include CPA/TCPA/risk for each target
        """
        snap = self.world.snapshot()
        print(snap)

        tgt = snap["targets"][0]

        self.assertIn("alert", tgt)
        self.assertIn("risk", tgt["alert"])
        self.assertIn("cpa_nm", tgt["alert"])
        self.assertIn("tcpa_hours", tgt["alert"])

    def test_danger_risk_in_snapshot(self):
        """
        Head-on target should be classified as DANGER
        """
        snap = self.world.snapshot()

        alert = snap["targets"][0]["alert"]

        self.assertEqual(alert["risk"], RiskLevel.DANGER.value)
        self.assertAlmostEqual(alert["cpa_nm"], 0.0, places=6)
        self.assertGreater(alert["tcpa_hours"], 0)

    def test_snapshot_does_not_mutate_world(self):
        """
        Snapshot modifications must not affect world state
        """
        snap = self.world.snapshot()
        snap["targets"][0]["alert"]["risk"] = "SAFE"

        # World recomputes alert fresh
        snap2 = self.world.snapshot()
        self.assertEqual(
            snap2["targets"][0]["alert"]["risk"],
            RiskLevel.DANGER.value
        )


if __name__ == "__main__":
    unittest.main()
