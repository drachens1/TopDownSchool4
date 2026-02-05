
SCALE = 20

def map_cell(x: int, y: int, width: int) -> int:
    return y * width + x

def screen_to_map_coords(x: int, y: int, camera) -> int:
    return (
        int((x // camera.zoom + camera.x) // SCALE),
        int((y // camera.zoom + camera.y) // SCALE),
    )

def screen_to_cell(x: int, y: int, width: int, camera) -> int:
    mx, my = screen_to_map_coords(x, y, camera)
    return map_cell(mx, my, width)

def cell_to_map(cell: int, width: int):
    x = cell % width
    y = cell // width
    return x * SCALE, y * SCALE

