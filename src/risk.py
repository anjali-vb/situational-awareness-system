from enum import Enum
from vessel import Vessel
from cpa import cpa_distance, tcpa


class RiskLevel(Enum):
    SAFE = "SAFE"
    WARNING = "WARNING"
    DANGER = "DANGER"


DANGER_CPA_NM = 0.5
WARNING_CPA_NM = 1.5
DANGER_TCPA_HOURS = 0.5   # 30 minutes
WARNING_TCPA_HOURS = 1.0  # 60 minutes


def classify_risk(own: Vessel, target: Vessel) -> RiskLevel:
    """
    Classify collision risk based on CPA distance and TCPA.

    Risk is determined by both how close vessels will get (CPA)
    and how soon that will happen (TCPA):
    - DANGER: CPA <= 0.5 nm AND TCPA <= 30 minutes
    - WARNING: CPA <= 1.5 nm AND TCPA <= 60 minutes
    - SAFE: Otherwise (large CPA, far in future, or already passed)

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

    # If TCPA is None (no relative motion), use current distance
    if t is None:
        if cpa <= DANGER_CPA_NM:
            return RiskLevel.DANGER
        if cpa <= WARNING_CPA_NM:
            return RiskLevel.WARNING
        return RiskLevel.SAFE

    # Check DANGER: close approach happening soon
    if cpa <= DANGER_CPA_NM and t <= DANGER_TCPA_HOURS:
        return RiskLevel.DANGER

    # Check WARNING: somewhat close approach within the hour
    if cpa <= WARNING_CPA_NM and t <= WARNING_TCPA_HOURS:
        return RiskLevel.WARNING

    return RiskLevel.SAFE