from dataclasses import dataclass
from risk import RiskLevel, classify_risk
from cpa import cpa_distance, tcpa
from vessel import Vessel


@dataclass(frozen=True)
class Alert:
    """
    Represents a collision alert for a target vessel.
    """
    target_id: str
    risk_level: RiskLevel
    cpa_nm: float | None
    tcpa_hours: float | None


def generate_alert(own: Vessel, target: Vessel) -> Alert:
    """
    Generate a collision alert for a target vessel.

    Args:
        own: Own vessel
        target: Target vessel

    Returns:
        Alert
    """
    return Alert(
        target_id=target.vessel_id,
        risk_level=classify_risk(own, target),
        cpa_nm=cpa_distance(own, target),
        tcpa_hours=tcpa(own, target)
    )