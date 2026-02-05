import pygame.draw

BUTTON_TEXT_COLOUR = (255, 255, 255)
BUTTON_COLOUR = (60, 60, 60)
BUTTON_HOVER_COLOUR = (80, 80, 80)
BUTTON_CLICK_COLOUR = (100, 100, 100)
BUTTON_ACTIVE_COLOUR = (120, 120, 120)

class Button:
    text: str
    x: int
    y: int
    width: int
    height: int
    hover: bool
    clicked: bool
    active: bool

    def __init__(self, text: str, x: int, y: int, width: int, height: int):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hover = False
        self.clicked = False
        self.active = False

    def set_clicked(self, clicked: bool):
        self.clicked = clicked

    def set_hover(self, hover: bool):
        self.hover = hover

    def set_active(self, active: bool):
        self.active = active

    def on_hover(self, mouse_x: int, mouse_y: int) -> bool:
        return self.x < mouse_x < self.x + self.width and self.y < mouse_y < self.y + self.height

    def render(self, WIN, font):
        if self.clicked:
            colour = BUTTON_CLICK_COLOUR
        elif self.hover:
            colour = BUTTON_HOVER_COLOUR
        elif self.active:
            colour = BUTTON_ACTIVE_COLOUR
        else:
            colour = BUTTON_COLOUR
        pygame.draw.rect(WIN, colour, pygame.Rect(self.x, self.y, self.width, self.height))
        text = font.render(self.text, True, BUTTON_TEXT_COLOUR)
        WIN.blit(text, (self.x, self.y))