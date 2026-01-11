import unittest
from simulation import Simulation
from world import World
from vessel import Vessel
from position import Position


class TestSimulationSpeed(unittest.TestCase):

    def setUp(self):
        self.own = Vessel(
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0,
        )
        self.world = World(self.own, [])
        self.sim = Simulation(self.world)

    def test_default_speed_is_real_time(self):
        """
        Default speed multiplier should be 1.0
        """
        self.sim.start()
        self.sim.step(1.0)

        self.assertAlmostEqual(self.own.position.y, 10.0, places=6)

    def test_double_speed(self):
        """
        Speed multiplier of 2.0 should double motion
        """
        self.sim.set_speed(2.0)
        self.sim.start()
        self.sim.step(1.0)

        self.assertAlmostEqual(self.own.position.y, 20.0, places=6)

    def test_half_speed(self):
        """
        Speed multiplier of 0.5 should halve motion
        """
        self.sim.set_speed(0.5)
        self.sim.start()
        self.sim.step(1.0)

        self.assertAlmostEqual(self.own.position.y, 5.0, places=6)

    def test_speed_change_during_run(self):
        """
        Changing speed mid-simulation should take effect immediately
        """
        self.sim.start()
        self.sim.step(1.0)  # normal speed → 10 nm

        self.sim.set_speed(2.0)
        self.sim.step(0.5)  # double speed → 10 nm

        self.assertAlmostEqual(self.own.position.y, 20.0, places=6)

    def test_invalid_speed(self):
        """
        Non-positive speed multipliers should raise error
        """
        with self.assertRaises(ValueError):
            self.sim.set_speed(0)

        with self.assertRaises(ValueError):
            self.sim.set_speed(-1.0)


if __name__ == "__main__":
    unittest.main()
