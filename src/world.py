from typing import Any, Dict, List
from alert import alert_text, generate_alert
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
    


    #adding and removing targets
    def add_target(self, target: Vessel) -> None:
        """
        Add a target vessel to the world.
        """
        self.targets.append(target)

    def remove_target(self, vessel_id: str) -> bool:
        """
        Remove a target vessel by ID.

        Returns:
            True if removed, False if not found
        """
        for i, target in enumerate(self.targets):
            if target.vessel_id == vessel_id:
                del self.targets[i]
                return True

        return False
    

    def snapshot(self) -> Dict[str, Any]:
        """
        Return a JSON-serializable snapshot including
        CPA, TCPA, risk, and human-readable alert text.
        """
        return {
            "own": self._own_snapshot(),
            "targets": [self._target_snapshot(t) for t in self.targets],
        }

    def _own_snapshot(self) -> Dict[str, Any]:
        return {
            "id": self.own.vessel_id,
            "position": {
                "x": self.own.position.x,
                "y": self.own.position.y,
            },
            "speed_knots": self.own.speed_knots,
            "heading_deg": self.own.heading_deg,
        }

    def _target_snapshot(self, target: Vessel) -> Dict[str, Any]:
        alert = generate_alert(self.own, target)

        return {
            "id": target.vessel_id,
            "position": {
                "x": target.position.x,
                "y": target.position.y,
            },
            "speed_knots": target.speed_knots,
            "heading_deg": target.heading_deg,
            "alert": {
                "risk": alert.risk_level.value,
                "cpa_nm": alert.cpa_nm,
                "tcpa_hours": alert.tcpa_hours,
                "text": alert_text(alert),
            },
        }