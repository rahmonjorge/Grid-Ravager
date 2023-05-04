import pygame

from enum import IntEnum

class BlockType(IntEnum):
    SOLID = 0
    HOLLOW = 2

class Block():
    def __init__(self, x, y, size, color, type):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.type = type
        self.rect = (x, y, size, size)

    def __eq__(self, other): 
        if not isinstance(other, Block):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.size == other.size and self.type == other.type

    def draw(self, display):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(display, self.color, rect, self.type)
