import math
from motion import relative_position, relative_velocity
from vessel import Vessel


def tcpa(own: Vessel, target: Vessel) -> float | None:
    """
    Compute Time to Closest Point of Approach (TCPA).

    Args:
        own: Own vessel
        target: Target vessel

    Returns:
        TCPA in hours, or None if relative velocity is zero
    """
    dx, dy = relative_position(own, target)
    dvx, dvy = relative_velocity(own, target)

    v_squared = dvx * dvx + dvy * dvy

    if v_squared == 0.0:
        return None

    t = - (dx * dvx + dy * dvy) / v_squared
    return t


#To calculate the CPA
def cpa_distance(own: Vessel, target: Vessel) -> float | None:
    """
    Compute distance at Closest Point of Approach (CPA).

    Args:
        own: Own vessel
        target: Target vessel

    Returns:
        CPA distance in nautical miles
    """
    dx, dy = relative_position(own, target)
    dvx, dvy = relative_velocity(own, target)

    t = tcpa(own, target)

    # No relative motion → distance never changes
    if t is None:
        return math.hypot(dx, dy)

    # Relative position at CPA
    cx = dx + dvx * t
    cy = dy + dvy * t

    return math.hypot(cx, cy)
