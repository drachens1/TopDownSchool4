
N, NE, E, SE, S, SW, W, NW = range(8)

DIR_VECTORS = {
    N:  (0, -1),
    NE: (1, -1),
    E:  (1, 0),
    SE: (1, 1),
    S:  (0, 1),
    SW: (-1, 1),
    W:  (-1, 0),
    NW: (-1, -1),
}

def _transform_octant(cx, cy, dx, dy, octant):
    if octant == 0: return cx + dx, cy + dy
    if octant == 1: return cx + dy, cy + dx
    if octant == 2: return cx - dy, cy + dx
    if octant == 3: return cx - dx, cy + dy
    if octant == 4: return cx - dx, cy - dy
    if octant == 5: return cx - dy, cy - dx
    if octant == 6: return cx + dy, cy - dx
    if octant == 7: return cx + dx, cy - dy
    return None

VECTOR_TO_DIR = {v: k for k, v in DIR_VECTORS.items()}

def delta_to_dir(dx: int, dy: int) -> int | None:
    dx = max(-1, min(1, dx))
    dy = max(-1, min(1, dy))
    return VECTOR_TO_DIR.get((dx, dy))
