import pygame

class Object():
    def __init__(self, name, x, y, texture = None, offset = 0, sound = None):
        self.name = name
        self.x = x
        self.y = y
        self.texture = texture
        self.offset = offset
        self.sound = sound

    def __eq__(self, other): 
        if not isinstance(other, Object):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.name == other.name

    def __str__(self):
        return '({x},{y}): {type}'.format(x=self.x, y=self.y, type=self.texture)
    
    def draw(self, display):
        display.blit(self.texture, (self.x + self.offset, self.y + self.offset))

    def play_sound(self):
        pygame.mixer.Sound.play(self.sound)