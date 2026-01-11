import unittest
from world import World
from vessel import Vessel
from position import Position


class TestWorld(unittest.TestCase):

    def test_world_step_updates_all_vessels(self):
        """
        All vessels should move when world steps forward
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0,
        )

        target1 = Vessel(
            vessel_id="TGT1",
            position=Position(0.0, 10.0),
            speed_knots=5.0,
            heading_deg=180.0,
        )

        target2 = Vessel(
            vessel_id="TGT2",
            position=Position(5.0, 0.0),
            speed_knots=10.0,
            heading_deg=90.0,
        )

        world = World(own, [target1, target2])

        world.step(1.0)  # 1 hour

        # Own vessel moves north by 10 nm
        self.assertAlmostEqual(world.own.position.y, 10.0, places=6)

        # Target1 moves south by 5 nm
        self.assertAlmostEqual(world.targets[0].position.y, 5.0, places=6)

        # Target2 moves east by 10 nm
        self.assertAlmostEqual(world.targets[1].position.x, 15.0, places=6)

    def test_zero_time_step(self):
        """
        Zero dt should not change positions
        """
        own = Vessel(
            vessel_id="OWN",
            position=Position(1.0, 1.0),
            speed_knots=10.0,
            heading_deg=0.0,
        )

        world = World(own, [])

        world.step(0.0)

        self.assertEqual(world.own.position, Position(1.0, 1.0))


if __name__ == "__main__":
    unittest.main()
