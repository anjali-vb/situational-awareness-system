from enum import Enum
from vessel import Vessel
from cpa import cpa_distance, tcpa


class RiskLevel(Enum):
    SAFE = "SAFE"
    WARNING = "WARNING"
    DANGER = "DANGER"


DANGER_CPA_NM = 0.5
WARNING_CPA_NM = 1.5


def classify_risk(own: Vessel, target: Vessel) -> RiskLevel:
    """
    Classify collision risk based on CPA distance and TCPA.

    Args:
        own: Own vessel
        target: Target vessel

    Returns:
        RiskLevel
    """
    cpa = cpa_distance(own, target)
    t = tcpa(own, target)

    # No CPA or closest approach already passed
    if cpa is None or (t is not None and t < 0):
        return RiskLevel.SAFE

    if cpa <= DANGER_CPA_NM:
        return RiskLevel.DANGER

    if cpa <= WARNING_CPA_NM:
        return RiskLevel.WARNING

    return RiskLevel.SAFE