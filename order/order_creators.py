from abc import ABC, abstractmethod
import math

import pygame.draw

from grid_helper import SCALE, map_cell, screen_to_map_coords, is_screen_pos_on_map
from order.orders import Order, GoTo
from order.pathfinder import find_path

class OrderCreator(ABC):
    def __init__(self, target_troop_id: int):
        self.target_troop_id = target_troop_id
        self.finished = False

    @abstractmethod
    def tick(self, mx, my, map, troop_manager, camera) -> None:
        pass

    @abstractmethod
    def render(self, WIN, camera) -> None:
        pass

    @abstractmethod
    def click(self, troop_manager, map) -> Order:
        pass

class FollowCreator(OrderCreator):
    def __init__(self, target_troop_id: int, follow_troop_id: int):
        super().__init__(target_troop_id)
        self.follow_troop_id = follow_troop_id

    def tick(self, mx, my, map, troop_manager, camera):
        troop = troop_manager.troops[self.target_troop_id]
        target = troop_manager.troops[self.follow_troop_id]

        troop.move_towards(target.position)

    def render(self, WIN, camera):
        pass

    def click(self, troop_manager, map) -> Order:
        pass

class GoToCreator(OrderCreator):
    def __init__(self, target_troop_id: int, x: int, y: int):
        super().__init__(target_troop_id)
        self.target_pos = (x, y)
        self.invalid = False

    def tick(self, mx, my, map, troop_manager, camera):
        x, y = screen_to_map_coords(mx, my, camera)
        self.target_pos = (x, y)

        if not is_screen_pos_on_map(mx, my, map.width, map.height, camera):
            self.invalid = True
            return

        cell = map_cell(x, y, map.width)
        self.invalid = map.blocks_vision(cell)

    def render(self, WIN, camera):
        if self.invalid:
            colour = (255, 0, 0)
        else:
            colour = (0, 255, 0)
        pygame.draw.rect(WIN, colour, camera.apply_on_rect(self.target_pos[0]*SCALE,
                                                                    self.target_pos[1]*SCALE, SCALE, SCALE))

    def click(self, troop_manager, map) -> Order:
        if self.invalid:
            return None
        return GoTo(self.target_troop_id, self.target_pos[0], self.target_pos[1], troop_manager, map)

class StandStillCreator(OrderCreator):
    def tick(self, mx, my, map, troop_manager, camera):
        troop = troop_manager.troops[self.target_troop_id]
        troop.stop()

    def render(self, WIN, camera):
        pass

    def click(self, troop_manager, map) -> Order:
        pass

class FaceCreator(OrderCreator):
    def __init__(self, target_troop_id: int, x: float, y: float):
        super().__init__(target_troop_id)
        self.target = (x, y)

    def tick(self, mx, my, map, troop_manager, camera):
        troop = troop_manager.troops[self.target_troop_id]

        dx = self.target[0] - troop.x
        dy = self.target[1] - troop.y
        troop.angle = math.atan2(dy, dx)

        self.finished = True

    def render(self, WIN, camera):
        pass

    def click(self, troop_manager, map) -> Order:
        pass
