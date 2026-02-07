from central_manager import CentralManager
from directions import S, N
from grid_helper import SCALE, map_cell, EMPTY, BUILDING
from map.buildings_manager import Building, BuildingsManager
from map.terrain_map import TerrainMap
from order.order_manager import OrderManager
from troop.troops import Troop
from troop.troops_manager import TroopsManager


def load_central_manager(map_path: str) -> CentralManager:
    cells = []
    buildings = []
    troops = []

    with open(map_path) as f:
        lines = [line.rstrip("\n") for line in f]

    width, height = map(int, lines[0].split())

    assert len(lines[1:]) == height
    for row in lines[1:]:
        assert len(row) == width

    for y, row in enumerate(lines[1:]):
         for x, char in enumerate(row):
             if char == "x":
                 wx = x * SCALE
                 wy = y * SCALE
                 buildings.append(Building(wx, wy, SCALE, SCALE))
                 cells.append(BUILDING)
             elif char == "f":
                 cell = map_cell(x, y, width)
                 troops.append((Troop(SCALE, cell, N, 3, True), cell))
                 cells.append(EMPTY)
             elif char == "e":
                 cell = map_cell(x, y, width)
                 troops.append((Troop(SCALE, cell, S, 3, False), cell))
                 cells.append(EMPTY)
             else:
                 cells.append(EMPTY)

    troops_manager = TroopsManager(width, height, troops)
    buildings_manager = BuildingsManager(buildings)
    order_manager = OrderManager()
    terrain_map = TerrainMap(cells, width, height)
    return CentralManager(buildings_manager, troops_manager, order_manager, terrain_map)

