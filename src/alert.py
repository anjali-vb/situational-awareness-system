from dataclasses import dataclass
from functools import cmp_to_key
from typing import Iterable, List
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

def generate_alerts(
    own: Vessel,
    targets: Iterable[Vessel],
    include_safe: bool = False,
) -> List[Alert]:
    """
    Generate collision alerts for multiple target vessels.

    Args:
        own: Own vessel
        targets: Iterable of target vessels
        include_safe: Whether to include SAFE alerts

    Returns:
        List of Alert objects
    """
    alerts: List[Alert] = []

    for target in targets:
        alert = generate_alert(own, target)

        if include_safe or alert.risk_level != RiskLevel.SAFE:
            alerts.append(alert)

    return alerts

def alert_text(alert: Alert) -> str:
    if alert.cpa_nm is None:
        return f"No collision risk – {alert.risk_level.value}"

    if alert.tcpa_hours is None:
        return f"CPA {alert.cpa_nm:.1f} nm – {alert.risk_level.value}"

    if alert.tcpa_hours < 0:
        return f"Opening, CPA {alert.cpa_nm:.1f} nm – {alert.risk_level.value}"

    tcpa_minutes = int(round(alert.tcpa_hours * 60))
    return (
         f"CPA {alert.cpa_nm:.1f} nm "
        f"in {tcpa_minutes} min – {alert.risk_level.value}"
    )
def sort_alerts(alerts: List[Alert]) -> List[Alert]:
    """
    Sort alerts using a traditional comparator:
    1. Risk level (DANGER > WARNING > SAFE)
    2. CPA distance (smaller is higher priority)
    """

    risk_priority = {
        RiskLevel.DANGER: 0,
        RiskLevel.WARNING: 1,
        RiskLevel.SAFE: 2,
    }

    def compare(a: Alert, b: Alert) -> int:
        # 1. Compare risk level
        rp_diff = (
            risk_priority[a.risk_level]
            - risk_priority[b.risk_level]
        )
        if rp_diff != 0:
            return rp_diff

        # 2. Compare CPA distance
        if a.cpa_nm is None and b.cpa_nm is None:
            return 0
        if a.cpa_nm is None:
            return 1
        if b.cpa_nm is None:
            return -1

        # Traditional comparison idiom
        return (a.cpa_nm > b.cpa_nm) - (a.cpa_nm < b.cpa_nm)

    return sorted(alerts, key=cmp_to_key(compare))

    