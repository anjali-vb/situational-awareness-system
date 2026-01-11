from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    """
    Immutable position in 2D space (e.g., longitude/latitude or Cartesian).
    """
    x: float
    y: float
