from typing import List
from vessel import Vessel


class World:
    """
    Simulation world containing own vessel and target vessels.
    """

    def __init__(self, own: Vessel, targets: List[Vessel]):
        self.own = own
        self.targets = list(targets)

    def step(self, dt_hours: float) -> None:
        """
        Advance simulation by dt_hours.
        """
        self.own.step(dt_hours)

        for target in self.targets:
            target.step(dt_hours)
    