
SCALE = 20

EMPTY = 0
BUILDING = 1

def map_cell(x: int, y: int, width: int) -> int:
    return y * width + x

def screen_to_map_coords(x: int, y: int, camera) -> (int, int):
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

def cell_to_xy(cell: int, width: int):
    return cell % width, cell // width

def xy_to_cell(x: int, y: int, width: int):
    return y * width + x

def is_screen_pos_on_map(sx: int, sy: int, width: int, height: int, camera) -> bool:
    wx = (sx / camera.zoom) + camera.x
    wy = (sy / camera.zoom) + camera.y

    return 0 <= wx // SCALE < width and 0 <= wy // SCALE < height
