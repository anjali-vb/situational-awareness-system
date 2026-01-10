import math
from dataclasses import dataclass


#Reduces boilerplate code (no need to manually write __init__)
@dataclass
class Vessel:
    """
    Represents a vessel with position, speed, and heading.
    """
    vessel_id: str
    x: float  # Longitude or X position
    y: float  # Latitude or Y position
    speed_knots: float
    heading_deg: float  # 0° = North, 90° = East

    def velocity_vector(self) -> tuple[float, float]:
        """
        Calculate velocity vector (vx, vy) in nautical miles per hour.

        Returns:
            (vx, vy): Velocity components
        """
        heading_rad = math.radians(self.heading_deg)

        # Maritime convention:
        # 0° = North (+Y), 90° = East (+X)
        vx = self.speed_knots * math.sin(heading_rad)
        vy = self.speed_knots * math.cos(heading_rad)

        return vx, vy
