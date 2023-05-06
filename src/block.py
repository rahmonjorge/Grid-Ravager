import pygame

from enum import IntEnum

class BlockType(IntEnum):
    SOLID = 0
    HOLLOW = 1
    ARROWUP = 2
    ARROWDOWN = 3
    ARROWLEFT = 4
    ARROWRIGHT = 5

class Block():
    def __init__(self, x, y, size, color = 'pink', type = BlockType.SOLID):
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

    def __str__(self):
        return '({x},{y}): {type}'.format(x=self.x, y=self.y, type=self.type.name)

    def move(self, blocks, display_width, display_height):
        if self.type == BlockType.ARROWRIGHT:
            if self.check_right(blocks, display_width):
                self.moveright()
        elif self.type == BlockType.ARROWDOWN:
            if self.check_down(blocks, display_height):
                self.movedown()
        elif self.type == BlockType.ARROWLEFT:
            if self.check_left(blocks, 0):
                self.moveleft()
        elif self.type == BlockType.ARROWUP:
            if self.check_up(blocks, 0):
                self.moveup()

    def check_right(self, blocks, boundary):
        intent = self.x + self.size

        collision = [other for other in blocks if intent == other.x and self.y == other.y]

        return intent < boundary and not collision
    
    def check_up(self, blocks, boundary):
        intent = self.y - self.size

        collision = [other for other in blocks if self.x == other.x and intent == other.y]

        return intent >= boundary and not collision
    
    def check_down(self, blocks, boundary):
        intent = self.y + self.size

        collision = [other for other in blocks if self.x == other.x and intent == other.y]

        return intent < boundary and not collision
    
    def check_left(self, blocks, boundary):
        intent = self.x - self.size

        collision = [other for other in blocks if intent == other.x and self.y == other.y]
        
        return intent >= boundary and not collision

    def moveright(self):
        self.x += self.size

    def moveup(self):
        self.y -= self.size

    def movedown(self):
        self.y += self.size

    def moveleft(self):
        self.x -= self.size

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