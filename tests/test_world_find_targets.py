import unittest
from world import World
from vessel import Vessel
from position import Position


class TestWorldFindTargets(unittest.TestCase):

    def setUp(self):
        self.own = Vessel("OWN", Position(0, 0), 10, 0)

        self.t1 = Vessel("T1", Position(1, 1), 5, 90)
        self.t2 = Vessel("T1", Position(2, 2), 6, 180)
        self.t3 = Vessel("T2", Position(3, 3), 7, 270)

        self.world = World(self.own, [self.t1, self.t2, self.t3])

    def test_find_targets_by_id_multiple(self):
        matches = self.world.find_targets_by_id("T1")

        self.assertEqual(len(matches), 2)
        self.assertIn(self.t1, matches)
        self.assertIn(self.t2, matches)

    def test_find_targets_by_id_single(self):
        matches = self.world.find_targets_by_id("T2")

        self.assertEqual(matches, [self.t3])

    def test_find_targets_by_id_none(self):
        matches = self.world.find_targets_by_id("NOPE")

        self.assertEqual(matches, [])

    def test_remove_target_removes_all_matches(self):
        removed = self.world.remove_target("T1")

        self.assertEqual(removed, 2)
        self.assertEqual(len(self.world.targets), 1)
        self.assertEqual(self.world.targets[0].vessel_id, "T2")


if __name__ == "__main__":
    unittest.main()
