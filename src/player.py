import pygame

class Player():
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.rect = (x, y, size, size)
        self.blocks = []

    def getPos(self):
        return pygame.Vector2(self.x, self.y)

    def draw(self, display):
        for block in self.blocks:
            rect = pygame.Rect(block.x, block.y, self.size, self.size)
            pygame.draw.rect(display, self.color, rect, 0)

        pygame.draw.rect(display, "green", self.rect, 2)

    def controls(self, event):
        # move
        if event.key in (pygame.K_UP, pygame.K_w):
            self.y -= self.size
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.x -= self.size
        if event.key in (pygame.K_DOWN, pygame.K_s):
            self.y += self.size
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.x += self.size

        # edit
        if event.key == pygame.K_SPACE:
            if self.getPos() not in self.blocks: 
                print((self.x,self.y))
                self.blocks.append(pygame.Vector2(self.x, self.y))
        if event.key == pygame.K_c:
            self.blocks.clear()

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.size, self.size)