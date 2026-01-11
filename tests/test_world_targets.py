import unittest
from world import World
from vessel import Vessel
from position import Position


class TestWorldTargets(unittest.TestCase):

    def setUp(self):
        self.own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0,
        )

        self.world = World(self.own, [])

    def test_add_target(self):
        """
        Target should be added to the world
        """
        target = Vessel(
            vessel_id="TGT1",
            position=Position(5.0, 5.0),
            speed_knots=5.0,
            heading_deg=180.0,
        )

        self.world.add_target(target)

        self.assertEqual(len(self.world.targets), 1)
        self.assertEqual(self.world.targets[0].vessel_id, "TGT1")

    def test_remove_existing_target(self):
        """
        Existing target should be removed by ID
        """
        target = Vessel(
            vessel_id="TGT1",
            position=Position(5.0, 5.0),
            speed_knots=5.0,
            heading_deg=180.0,
        )

        self.world.add_target(target)
        removed = self.world.remove_target("TGT1")

        self.assertTrue(removed)
        self.assertEqual(len(self.world.targets), 0)

    def test_remove_nonexistent_target(self):
        """
        Removing unknown target should return False
        """
        removed = self.world.remove_target("UNKNOWN")

        self.assertFalse(removed)

   
if __name__ == "__main__":
    unittest.main()
