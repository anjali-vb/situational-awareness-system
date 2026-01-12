import unittest
from world import World
from vessel import Vessel
from position import Position


class TestWorldUpdateCourseSplit(unittest.TestCase):

    def setUp(self):
        self.own = Vessel("OWN", Position(0, 0), 10, 0)

        self.t1 = Vessel("T1", Position(1, 1), 5, 90)
        self.t2 = Vessel("T1", Position(2, 2), 6, 180)
        self.t3 = Vessel("T2", Position(3, 3), 7, 270)

        self.world = World(self.own, [self.t1, self.t2, self.t3])

    # ----------------------------
    # Own vessel
    # ----------------------------
    def test_update_own_heading(self):
        self.world.update_own_heading(180)
        self.assertEqual(self.own.heading_deg, 180)

    def test_update_own_speed(self):
        self.world.update_own_speed(15)
        self.assertEqual(self.own.speed_knots, 15)

    # ----------------------------
    # Target vessels
    # ----------------------------
    def test_update_target_heading(self):
        updated = self.world.update_target_heading("T1", 45)

        self.assertEqual(updated, 2)
        self.assertEqual(self.t1.heading_deg, 45)
        self.assertEqual(self.t2.heading_deg, 45)

    def test_update_target_speed(self):
        updated = self.world.update_target_speed("T1", 9)

        self.assertEqual(updated, 2)
        self.assertEqual(self.t1.speed_knots, 9)
        self.assertEqual(self.t2.speed_knots, 9)

    def test_update_target_heading_single(self):
        updated = self.world.update_target_heading("T2", 0)

        self.assertEqual(updated, 1)
        self.assertEqual(self.t3.heading_deg, 0)

    def test_update_target_speed_not_found(self):
        updated = self.world.update_target_speed("NOPE", 5)
        self.assertEqual(updated, 0)


if __name__ == "__main__":
    unittest.main()
