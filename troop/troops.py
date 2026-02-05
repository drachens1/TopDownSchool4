import pygame.draw

from order.orders import Order

FRIENDLY = (0, 0, 255)
ENEMY = (255,0,0)

MAX_HP = 100

class Troop:
    x: int
    y: int
    r: int
    cell: int
    angle: int
    see_dist: int
    friendly: bool
    active: bool
    hp: int
    current_order: int

    def __init__(self, x: int, y: int, r: int, cell: int, angle: int, see_dist: int, friendly: bool):
        self.x=x
        self.y=y
        self.r=r
        self.cell = cell
        self.angle=angle
        self.see_dist=see_dist
        self.friendly=friendly
        self.active = False
        self.current_order = -1

    def set_active(self, active: bool):
        self.active = active

    # def command(self):
    #     print("")

    def render(self, WIN, camera):
        if self.friendly:
            if self.active:
                colour = (255,255,255)
            else:
                colour = FRIENDLY
        else:
            colour = ENEMY
        pygame.draw.ellipse(WIN, colour, camera.apply_on_rect(self.x, self.y, self.r, self.r))


