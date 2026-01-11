import unittest
from simulation import Simulation
from world import World
from vessel import Vessel
from position import Position


class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.own = Vessel(                 #testing framework runs this setup before very test 
            vessel_id="OWN",
            position=Position(0.0, 0.0),
            speed_knots=10.0,
            heading_deg=0.0,
        )

        self.world = World(self.own, [])   #includes all vessel targets ...
        self.sim = Simulation(self.world)   #time start stop

    def test_initially_paused(self):
        """
        Simulation should start paused.
        """
        self.sim.step(1.0)
        self.assertEqual(self.own.position, Position(0.0, 0.0))

    def test_start_simulation(self):
        """
        Simulation should advance when started.
        """
        self.sim.start()
        self.sim.step(1.0)

        self.assertAlmostEqual(self.own.position.y, 10.0, places=6)

    def test_pause_simulation(self):
        """
        Simulation should stop advancing when paused.
        """
        self.sim.start()
        self.sim.step(1.0)

        # Pause and attempt another step
        self.sim.pause()
        self.sim.step(1.0)

        # Position should not change further
        self.assertAlmostEqual(self.own.position.y, 10.0, places=6)

    def test_multiple_steps(self):
        """
        Multiple steps accumulate correctly when running.
        """
        self.sim.start()
        self.sim.step(0.5)
        self.sim.step(0.5)

        self.assertAlmostEqual(self.own.position.y, 10.0, places=6)


if __name__ == "__main__":
    unittest.main()
