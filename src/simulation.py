from world import World


class Simulation:
    """
    Controls simulation execution (start / pause).
    """

    def __init__(self, world: World):
        self.world = world
        self.running = False
        self.speed_multiplier = 1.0  # real-time by default

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


    def set_speed(self, multiplier: float) -> None:
        """
        Set simulation speed multiplier.
        """
        if multiplier <= 0:
            raise ValueError("Speed multiplier must be positive")
        self.speed_multiplier = multiplier

    def step(self, dt_hours: float) -> None:
        """
        Advance simulation if running, applying speed multiplier.
        """
        if not self.running:
            return

        effective_dt = dt_hours * self.speed_multiplier
        self.world.step(effective_dt)