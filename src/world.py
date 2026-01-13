from typing import Any, Dict, List
from vessel import Vessel
from alert import alert_text, generate_alert, generate_alerts, sort_alerts


class World:
    """
    Simulation world containing own vessel and target vessels.
    """

    def __init__(self, own: Vessel, targets: List[Vessel]):
        self.own = own
        self.targets = list(targets)

    
    # Simulation
    
    def step(self, dt_hours: float) -> None:
        self.own.step(dt_hours)
        for target in self.targets:
            target.step(dt_hours)

    
    # Target management
    
    def add_target(self, target: Vessel) -> None:
        self.targets.append(target)

    def find_targets_by_id(self, vessel_id: str) -> List[Vessel]:
        return [t for t in self.targets if t.vessel_id == vessel_id]

    def remove_target(self, vessel_id: str) -> int:
        matches = self.find_targets_by_id(vessel_id)
        self.targets = [t for t in self.targets if t.vessel_id != vessel_id]
        return len(matches)

   
    # Own vessel course control
    
    def update_own_heading(self, heading_deg: float) -> None:
        """
        Update own vessel heading.
        """
        self.own.change_heading(heading_deg)

    def update_own_speed(self, speed_knots: float) -> None:
        """
        Update own vessel speed.
        """
        self.own.change_speed(speed_knots)

    
    # Target vessel course control
    
    def update_target_heading(self, vessel_id: str, heading_deg: float) -> int:
        """
        Update heading for all targets matching vessel_id.

        Returns:
            Number of targets updated
        """
        targets = self.find_targets_by_id(vessel_id)
        for t in targets:
            t.change_heading(heading_deg)
        return len(targets)

    def update_target_speed(self, vessel_id: str, speed_knots: float) -> int:
        """
        Update speed for all targets matching vessel_id.

        Returns:
            Number of targets updated
        """
        targets = self.find_targets_by_id(vessel_id)
        for t in targets:
            t.change_speed(speed_knots)
        return len(targets)

   
    # Snapshot
    
    def snapshot(self) -> Dict[str, Any]:
        alerts = sort_alerts(
            generate_alerts(self.own, self.targets, include_safe=False)
        )

        return {
            "own": self._own_snapshot(),
            "targets": [self._target_snapshot(t) for t in self.targets],
            "alerts": [self._alert_snapshot(a) for a in alerts],
        }

    
    # Snapshot helpers
    
    def _own_snapshot(self) -> Dict[str, Any]:
        return {
            "id": self.own.vessel_id,
            "position": self._position_snapshot(self.own),
            "speed_knots": self.own.speed_knots,
            "heading_deg": self.own.heading_deg,
        }

    def _target_snapshot(self, target: Vessel) -> Dict[str, Any]:
        alert = generate_alert(self.own, target)
        return {
            "id": target.vessel_id,
            "position": self._position_snapshot(target),
            "speed_knots": target.speed_knots,
            "heading_deg": target.heading_deg,
            "alert": self._alert_detail_snapshot(alert),
        }

    def _position_snapshot(self, vessel: Vessel) -> Dict[str, float]:
        return {"x": vessel.position.x, "y": vessel.position.y}

    def _alert_snapshot(self, alert) -> Dict[str, Any]:
        return {
            "target_id": alert.target_id,
            "risk": alert.risk_level.value,
            "cpa_nm": alert.cpa_nm,
            "tcpa_hours": alert.tcpa_hours,
        }

    def _alert_detail_snapshot(self, alert) -> Dict[str, Any]:
        return {
            "risk": alert.risk_level.value,
            "cpa_nm": alert.cpa_nm,
            "tcpa_hours": alert.tcpa_hours,
            "text": alert_text(alert),
        }
