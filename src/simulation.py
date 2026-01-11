from world import World


class Simulation:
    """
    Controls simulation execution (start / pause).
    """

    def __init__(self, world: World):
        self.world = world
        self.running = False

    def start(self) -> None:
        """
        Start the simulation.
        """
        self.running = True

    def pause(self) -> None:
        """
        Pause the simulation.
        """
        self.running = False

    def step(self, dt_hours: float) -> None:
        """
        Advance simulation if running.
        """
        if not self.running:
            return

        self.world.step(dt_hours)
       