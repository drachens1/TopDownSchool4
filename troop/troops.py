import pygame.draw

from grid_helper import cell_to_xy, SCALE

FRIENDLY = (0, 0, 255)
ENEMY = (255, 0, 0)
MAX_HP = 100

class Troop:
    def __init__(self, r: int, cell: int, angle: int, see_dist: int, friendly: bool):
        self.r = r
        self.cell = cell
        self.angle = angle
        self.see_dist = see_dist
        self.friendly = friendly
        self.active = False
        self.hp = MAX_HP
        self.current_order = -1

    def set_active(self, active: bool):
        self.active = active

    def take_damage(self, amount, order_manager):
        self.hp -= amount
        if self.current_order != -1 and order_manager:
            order_manager.remove_order(self.current_order)
            self.current_order = -1

        if self.hp < 0: self.hp = 0

    def render(self, WIN, camera, width: int):
        if self.hp <= 0: return

        x, y = cell_to_xy(self.cell, width)
        rect = camera.apply_on_rect(x * SCALE, y * SCALE, self.r, self.r)

        color = (255, 255, 255) if self.active else (FRIENDLY if self.friendly else ENEMY)
        pygame.draw.ellipse(WIN, color, rect)

        if self.hp < 100:
            bar_w = self.r
            bar_h = 4
            bg_rect = camera.apply_on_rect(x * SCALE, (y * SCALE) - 8, bar_w, bar_h)
            pygame.draw.rect(WIN, (50, 0, 0), bg_rect)
            current_w = int(bar_w * (self.hp / 100))
            fg_rect = camera.apply_on_rect(x * SCALE, (y * SCALE) - 8, current_w, bar_h)
            pygame.draw.rect(WIN, (0, 255, 0), fg_rect)