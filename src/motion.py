from vessel import Vessel

#Calculating relative position
def relative_position(own: Vessel, target: Vessel) -> tuple[float, float]:
    """
    Compute relative position of target vessel with respect to own vessel.

    Args:
        own: Own vessel
        target: Target vessel

    Returns:
        (dx, dy): Relative position vector (target - own)
    """
    dx = target.position.x - own.position.x
    dy = target.position.y - own.position.y

    return dx, dy


#Calculating the relative velocity

def relative_velocity(own: Vessel, target: Vessel) -> tuple[float, float]:
    """
    Compute relative velocity of target vessel with respect to own vessel.

    Args:
        own: Own vessel
        target: Target vessel

    Returns:
        (dvx, dvy): Relative velocity vector (target - own)
    """
    own_vx, own_vy = own.velocity_vector()
    tgt_vx, tgt_vy = target.velocity_vector()

    dvx = tgt_vx - own_vx
    dvy = tgt_vy - own_vy

    return dvx, dvy