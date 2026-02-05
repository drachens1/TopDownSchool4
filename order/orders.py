from abc import ABC, abstractmethod
import math

FOLLOW_TYPE = 0
GO_TO_TYPE = 1
STAND_STILL_TYPE = 2
FACE_TYPE = 3

class Order(ABC):
    def __init__(self, target_troop_id: int):
        self.target_troop_id = target_troop_id
        self.finished = False  # common lifecycle flag

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
    def __init__(self, target_troop_id: int, x: float, y: float):
        super().__init__(target_troop_id)
        self.target_pos = (x, y)

    def tick(self, map, troop_manager):
        troop = troop_manager.troops[self.target_troop_id]

        if troop.move_towards(self.target_pos, dt):
            self.finished = True

    def render(self, WIN, camera):
        pass

class StandStill(Order):
    def tick(self, map, troop_manager):
        troop = troop_manager.troops[self.target_troop_id]
        troop.stop()

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
        troop.angle = math.atan2(dy, dx)

        self.finished = True

    def render(self, WIN, camera):
        pass
