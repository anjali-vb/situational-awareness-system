import math
from dataclasses import dataclass
from position import Position


@dataclass
class Vessel:
    """
    Represents a vessel with position, speed, and heading.
    """
    vessel_id: str
    position : Position
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

    def step(self, dt_hours: float) -> None:
         """
        Advance vessel position by dt_hours.

        Args:
            dt_hours: Time step in hours
        """
         vx, vy = self.velocity_vector()
         self.position = Position(
            x=self.position.x + vx * dt_hours,
            y=self.position.y + vy * dt_hours
        )
        
        #To change thde direction of the vessel
    def change_heading(self, new_heading_deg: float) -> None:
        """
        Change vessel heading.

        Args:
            new_heading_deg: New heading in degrees (will be normalized)
        """
        self.heading_deg = new_heading_deg % 360.0



        #To change the speed of the vessel
    def change_speed(self, new_speed_knots: float) -> None:
        """
        Change vessel speed.

        Args:
            new_speed_knots: New speed in knots (must be >= 0)
        """
        if new_speed_knots < 0:
            raise ValueError("Speed must be non-negative")

        self.speed_knots = new_speed_knots
        


