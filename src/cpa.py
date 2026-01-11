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
