from typing import Any

from grid_helper import screen_to_cell

class TroopsManager:
    troops: list[Any]
    troop_id_map: list[int]
    active_troop_id: int

    def __init__(self, width: int, height: int, troops: list[Any]):
        self.troops = []
        self.troop_id_map = []
        self.active_troop_id = -1

        for i in range(0, width * height):
            self.troop_id_map.append(-1)

        for troop, cell in troops:
            id = len(self.troops)
            self.troops.append(troop)
            self.troop_id_map[cell] = id

    def on_left_click(self, x: int, y: int, width: int, camera):
        cell = screen_to_cell(x, y, width, camera)
        if cell == -1 or cell >= len(self.troop_id_map):
            self.clear_selection()
            return

        troop_id = self.troop_at(cell)
        if troop_id == -1:
            self.clear_selection()
            return

        self.select_troop(troop_id)

    def move_troop(self, troop_id: int, from_cell: int, to_cell: int):
        self.troop_id_map[from_cell] = -1
        self.troop_id_map[to_cell] = troop_id

    def troop_at(self, cell: int) -> int:
        tid = self.troop_id_map[cell]
        return tid

    def select_troop(self, troop_id: int):
        self.clear_selection()
        troop = self.troops[troop_id]
        if troop.friendly:
            self.active_troop_id = troop_id
            troop.set_active(True)

    def clear_selection(self):
        if self.active_troop_id != -1:
            self.troops[self.active_troop_id].set_active(False)
        self.active_troop_id = -1

    def render(self, WIN, camera):
        for troop in self.troops:
            troop.render(WIN, camera)
