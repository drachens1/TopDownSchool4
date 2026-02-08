from abc import ABC, abstractmethod
import math

import pygame.draw

from directions import delta_to_dir
from grid_helper import SCALE, map_cell
from map.terrain_map import TerrainMap
from order.pathfinder import find_path

FOLLOW_TYPE = 0
GO_TO_TYPE = 1
STAND_STILL_TYPE = 2
FACE_TYPE = 3

class Order(ABC):
    def __init__(self, target_troop_id: int):
        self.target_troop_id = target_troop_id
        self.finished = False
        self.tick_num = 0

    def order_tick(self, map, troop_manager):
        self.tick_num += 1
        if self.tick_num > 20:
            self.tick(map, troop_manager)
            self.tick_num = 0

    @abstractmethod
    def tick(self, map, troop_manager) -> None:
        pass

    @abstractmethod
    def render(self, WIN, camera) -> None:
        pass

class Follow(Order):
    def __init__(self, target_troop_id: int, follow_troop_id: int):
        super().__init__(target_troop_id)
        self.follow_troop_id = follow_troop_id

    def tick(self, map, troop_manager):
        troop = troop_manager.troops[self.target_troop_id]
        target = troop_manager.troops[self.follow_troop_id]

        troop.move_towards(target.position)

    def render(self, WIN, camera):
        pass

class GoTo(Order):
    def __init__(self, target_troop_id: int, x: int, y: int, troop_manager, map):
        super().__init__(target_troop_id)
        self.target_pos = (x, y)
        troop = troop_manager.troops[self.target_troop_id]
        end = map_cell(self.target_pos[0], self.target_pos[1], map.width)
        self.path = find_path(map, troop.cell, end)

    def tick(self, map: TerrainMap, troop_manager):
        troop = troop_manager.troops[self.target_troop_id]

        if not self.path:
            self.finished = True
            return
        start = troop.cell

        next_cell = self.path[0]

        sx, sy = troop_manager.cell_to_xy(start)
        nx, ny = troop_manager.cell_to_xy(next_cell)

        dx = nx - sx
        dy = ny - sy
        new_dir = delta_to_dir(dx, dy)
        if new_dir is not None:
            troop.angle = new_dir

        if troop_manager.move_troop(self.target_troop_id, start, self.path[0]):
            self.path.pop(0)

        if len(self.path) == 0:
            self.finished = True

    def render(self, WIN, camera):
        pygame.draw.rect(WIN, (255, 255, 255), camera.apply_on_rect(self.target_pos[0]*SCALE,
                                                                    self.target_pos[1]*SCALE, SCALE, SCALE))

class StandStill(Order):
    def tick(self, map, troop_manager):
        pass

    def render(self, WIN, camera):
        pass

class Face(Order):
    def __init__(self, target_troop_id: int, x: float, y: float):
        super().__init__(target_troop_id)
        self.target = (x, y)

    def tick(self, map, troop_manager):
        troop = troop_manager.troops[self.target_troop_id]

        dx = self.target[0] - troop.x
        dy = self.target[1] - troop.y

        angle = math.atan2(dy, dx)

        octant = int(round(angle / (math.pi / 4))) % 8

        troop.angle = (octant + 2) % 8

        self.finished = True

    def render(self, WIN, camera):
        pass
