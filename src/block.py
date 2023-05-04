import pygame

from enum import IntEnum

class BlockType(IntEnum):
    SOLID = 0
    HOLLOW = 4
    ARROWUP = 5
    ARROWDOWN = 6
    ARROWLEFT = 7
    ARROWRIGHT = 8

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

        return self.x == other.x and self.y == other.y and self.size == other.size

    def draw(self, display):
        if self.type == BlockType.SOLID:
            pygame.draw.rect(display, self.color, pygame.Rect(self.x, self.y, self.size, self.size), 0)
        elif self.type == BlockType.HOLLOW:
            pygame.draw.rect(display, self.color, pygame.Rect(self.x, self.y, self.size, self.size), 4)
        elif self.type == BlockType.ARROWDOWN:
            pygame.draw.polygon(display, self.color, [self.get_topleft(), self.get_topright(), self.get_midbot()], 0)
        elif self.type == BlockType.ARROWLEFT:
            pygame.draw.polygon(display, self.color, [self.get_midleft(), self.get_topright(), self.get_botright()], 0)
        elif self.type == BlockType.ARROWRIGHT:
            pygame.draw.polygon(display, self.color, [self.get_topleft(), self.get_midright(), self.get_botleft()], 0)
        elif self.type == BlockType.ARROWUP:
            pygame.draw.polygon(display, self.color, [self.get_midtop(), self.get_botleft(), self.get_botright()], 0)
    
    def get_topleft(self):
        return [self.x, self.y]
    
    def get_topright(self):
        return [self.x + self.size, self.y]
    
    def get_botleft(self):
        return [self.x, self.y + self.size]
    
    def get_botright(self):
        return [self.x + self.size, self.y + self.size]
    
    def get_midtop(self):
        return [self.x + (self.size / 2), self.y]
    
    def get_midbot(self):
        return [self.x + (self.size / 2), self.y + self.size]
    
    def get_midright(self):
        return [self.x + self.size, self.y + (self.size / 2)]

    def get_midleft(self):
        return [self.x, self.y + (self.size / 2)]