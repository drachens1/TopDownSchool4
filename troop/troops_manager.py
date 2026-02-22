from typing import Any
import pygame

from directions import _transform_octant, DIR_VECTORS
from grid_helper import screen_to_cell, SCALE
from troop.combat import Combat
from troop.troops import Troop

class TroopsManager:
    troops: list[Troop]
    visible: list[bool]
    troop_visible: list[bool]
    troop_id_map: list[int]
    combats: list[Combat]
    active_troop_id: int
    width: int
    height: int
    fog: pygame.Surface

    def __init__(self, width: int, height: int, troops: list[Any]):
        self.width = width
        self.height = height

        self.troops: list[Troop] = []
        self.combats: list[Combat] = []
        self.troop_id_map = [-1] * (width * height)

        self.active_troop_id = -1

        self.visible = [False] * (width * height)
        self.troop_visible = [False] * (self.width * self.height)

        self.fog = pygame.Surface(
            (width * SCALE, height * SCALE),
            pygame.SRCALPHA
        )

        for troop, cell in troops:
            tid = len(self.troops)
            self.troops.append(troop)
            self.troop_id_map[cell] = tid

    def move_troop(self, troop_id: int, from_cell: int, to_cell: int) -> bool:
        if self.troop_id_map[to_cell] != -1:
            return False
        troop = self.troops[troop_id]
        troop.cell = to_cell
        self.troop_id_map[from_cell] = -1
        self.troop_id_map[to_cell] = troop_id
        return True

    def troop_at(self, cell: int) -> int:
        tid = self.troop_id_map[cell]
        return tid

    def cell_to_xy(self, cell: int):
        return cell % self.width, cell // self.width

    def xy_to_cell(self, x: int, y: int):
        return y * self.width + x

    def on_left_click(self, x: int, y: int, width: int, camera):
        cell = screen_to_cell(x, y, width, camera)
        if cell < 0 or cell >= len(self.troop_id_map):
            self.clear_selection()
            return

        tid = self.troop_id_map[cell]
        if tid == -1:
            self.clear_selection()
            return

        self.select_troop(tid)

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

    def update_visibility(self, terrain, order_manager):
        self.visible = [False] * (self.width * self.height)

        for tid, troop in enumerate(self.troops):
            if troop.hp <= 0: continue

            if troop.friendly:
                self.troop_visible = [False] * (self.width * self.height)
                cx, cy = self.cell_to_xy(troop.cell)
                self._compute_fov(cx, cy, troop.see_dist, terrain)
                self._apply_facing_filter(tid, cx, cy, troop.angle)
                self.visible[troop.cell] = True

                for i, vis in enumerate(self.troop_visible):
                    if vis: self.visible[i] = True

            else:
                self.troop_visible = [False] * (self.width * self.height)
                cx, cy = self.cell_to_xy(troop.cell)
                self._compute_fov(cx, cy, troop.see_dist, terrain)
                self._apply_facing_filter(tid, cx, cy, troop.angle)

    def _compute_fov(self, cx, cy, radius, terrain):
        for octant in range(8):
            self._cast_light(cx, cy, 1, 1.0, 0.0, radius, octant, terrain)

    def _cast_light(self, cx, cy, row, start, end, radius, octant, terrain):
        if start < end:
            return

        radius_sq = radius * radius

        for i in range(row, radius + 1):
            dx = -i - 1
            dy = -i
            blocked = False
            new_start = start

            while dx <= 0:
                dx += 1
                x, y = _transform_octant(cx, cy, dx, dy, octant)
                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)

                if start < r_slope:
                    continue
                if end > l_slope:
                    break

                if 0 <= x < self.width and 0 <= y < self.height:
                    cell = self.xy_to_cell(x, y)
                    if dx*dx + dy*dy <= radius_sq:
                        self.troop_visible[cell] = True

                    if blocked:
                        if terrain.blocks_vision(cell):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if terrain.blocks_vision(cell) and i < radius:
                            blocked = True
                            self._cast_light(
                                cx, cy, i + 1, start, l_slope,
                                radius, octant, terrain
                            )
                            new_start = r_slope
            if blocked:
                break

    def _apply_facing_filter(self, viewer_id, cx, cy, angle):
        viewer = self.troops[viewer_id]
        dx, dy = DIR_VECTORS[angle]

        for cell, vis in enumerate(self.troop_visible):
            if not vis: continue

            tx, ty = self.cell_to_xy(cell)
            if (tx - cx) * dx + (ty - cy) * dy <= 0:
                self.troop_visible[cell] = False
                continue

            target_id = self.troop_id_map[cell]
            if target_id != -1 and target_id != viewer_id:
                target = self.troops[target_id]
                if target.friendly != viewer.friendly:
                    self.start_combat(viewer_id, target_id)

    def start_combat(self, t1_id, t2_id):
        existing_combat = None
        for c in self.combats:
            if t1_id in c.participants or t2_id in c.participants:
                existing_combat = c
                break

        if existing_combat:
            existing_combat.add_participant(t1_id)
            existing_combat.add_participant(t2_id)
        else:
            self.combats.append(Combat(t1_id, t2_id))

    def resolve_combat(self, order_manager):
        for combat in self.combats[:]:
            combat.tick(self, order_manager)
            if combat.finished:
                self.combats.remove(combat)

    def render(self, WIN, camera, order_manager):
        num = 0
        for troop in self.troops:
            if troop.friendly:
                num+=1
            if self.visible[troop.cell]:
                troop.render(WIN, camera, self.width)

        self.resolve_combat(order_manager)

        self.fog.fill((50, 50, 50, 200))
        for cell, vis in enumerate(self.visible):
            if vis:
                x, y = self.cell_to_xy(cell)
                self.fog.fill((0, 0, 0, 0), pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE))

        fog_scaled, fog_pos = camera.apply_on_surface(self.fog)
        WIN.blit(fog_scaled, fog_pos)
