from grid_helper import SCALE
from map.buildings_manager import BuildingsManager
from map.terrain_map import TerrainMap
from order.order_manager import OrderManager
from troop.troops_manager import TroopsManager

class CentralManager:
    building_manager: BuildingsManager
    troops_manager: TroopsManager
    order_manager: OrderManager
    terrain_map: TerrainMap

    def __init__(self, building_manager: BuildingsManager, troops_manager: TroopsManager,
                 order_manager: OrderManager, terrain_map: TerrainMap):
        self.building_manager = building_manager
        self.troops_manager = troops_manager
        self.order_manager = order_manager
        self.terrain_map = terrain_map

    def has_active_troop(self) -> bool:
        return self.troops_manager.active_troop_id != -1

    def on_click(self, x: int, y: int, camera):
        self.troops_manager.on_left_click(x, y, self.terrain_map.width, camera)

    def render(self, WIN, camera, mx, my):
        self.order_manager.tick(self.terrain_map, self.troops_manager, mx, my, camera)

        self.terrain_map.render(WIN, camera)
        self.troops_manager.update_visibility(self.terrain_map)
        self.troops_manager.render(WIN, camera)
        self.building_manager.render(WIN, camera)
        self.order_manager.render(WIN, camera)

