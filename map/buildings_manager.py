import pygame

BUILDING_COLOUR = (100,100,100)

class Building:
    x: int
    y: int
    w: int
    h: int

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def render(self, WIN, camera):
        pygame.draw.rect(WIN, BUILDING_COLOUR, camera.apply_on_rect(self.x,self.y,self.w,self.h))

class BuildingsManager:
    buildings: list[Building]

    def __init__(self, buildings: list[Building]):
        self.buildings = buildings

    def render(self, WIN, camera):
        for building in self.buildings:
            building.render(WIN, camera)