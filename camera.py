import pygame

class Camera:
    x: int
    y: int
    zoom: float

    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.zoom = 1.

    def add_x(self, v: int):
        self.x+=v

    def add_y(self, v: int):
        self.y+=v

    def add_zoom(self, v: float):
        self.zoom+=v
        if self.zoom <= 0 :
            self.zoom = 0.5

    def x(self):
        return self.x

    def y(self):
        return self.y

    def zoom(self):
        return self.zoom

    def apply_on_rect(self, x, y, w, h):
        sx = (x - self.x) * self.zoom
        sy = (y - self.y) * self.zoom
        sw = w * self.zoom
        sh = h * self.zoom
        return pygame.Rect(sx, sy, sw, sh)

    def apply_on_surface(self, surface: pygame.Surface) -> pygame.Surface:
        scaled = pygame.transform.scale(
            surface,
            (
                int(surface.get_width() * self.zoom),
                int(surface.get_height() * self.zoom),
            ),
        )

        offset_x = int(-self.x * self.zoom)
        offset_y = int(-self.y * self.zoom)

        return scaled, (offset_x, offset_y)

    def has_clicked(self, mouse_x, mouse_y, x, y, w, h):
        sx = (x - self.x) * self.zoom
        sy = (y - self.y) * self.zoom
        sw = w * self.zoom
        sh = h * self.zoom
        return sx < mouse_x < sx + sw and sy < mouse_y < sy + sh

