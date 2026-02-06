import pygame

from grid_helper import SCALE, map_cell, BUILDING


class TerrainMap:
    cells: list[int]
    width: int
    height: int

    def __init__(self, cells: list[int], width: int, height: int):
        self.cells = cells
        self.width = width
        self.height = height

    def neighbors(self, cell: int) -> list[int]:
        x = cell % self.width
        y = cell // self.width
        out = []

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                out.append(map_cell(nx, ny, self.width))
        return out

    def blocks_vision(self, cell: int) -> bool:
        return self.cells[cell] == BUILDING

    def render(self, WIN, camera):
        pygame.draw.rect(WIN,(85, 175, 30),camera.apply_on_rect(0,0,self.width * SCALE,self.height * SCALE))
