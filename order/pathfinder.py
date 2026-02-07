from heapq import heappush, heappop

from grid_helper import EMPTY

def heuristic(a: int, b: int, width: int) -> int:
    ax, ay = a % width, a // width
    bx, by = b % width, b // width
    return abs(ax - bx) + abs(ay - by)

def find_path(terrain, start_cell: int, end_cell: int) -> list[int]:
    if start_cell == end_cell:
        return []

    open_set = []
    heappush(open_set, (0, start_cell))

    came_from: dict[int, int] = {}
    g_score = {start_cell: 0}

    while open_set:
        _, current = heappop(open_set)

        if current == end_cell:
            break

        for neighbor in terrain.neighbors(current):
            if terrain.cells[neighbor] != EMPTY:
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, 1_000_000):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, end_cell, terrain.width)
                heappush(open_set, (f, neighbor))

    if end_cell not in came_from:
        return []

    path = []
    cur = end_cell
    while cur != start_cell:
        path.append(cur)
        cur = came_from[cur]

    path.reverse()
    return path
