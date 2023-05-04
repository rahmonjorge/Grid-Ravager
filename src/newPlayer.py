import pygame
from block import Block, BlockType

class NewPlayer():
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.selection = None
        self.block_selected = None
        self.blocks = []
        self.mousepos = None

    def draw_blocks(self, display):
        for block in self.blocks:
            block.draw(display)
            # rect = pygame.Rect(block.x, block.y, self.size, self.size)
            # pygame.draw.rect(display, self.color, rect, 0)
    
    def draw_selection(self, display, color):
        if self.selection is None:
            return
        selection = pygame.Rect(self.selection.x, self.selection.y, self.size, self.size)
        pygame.draw.rect(display, color, selection, 2)

    def draw_cursor(self, display, color):
        if self.mousepos is None:
            return
        cursor = pygame.Rect(self.mousepos.x, self.mousepos.y, self.size, self.size)
        pygame.draw.rect(display, color, cursor, 2)

    def controls(self, event):
        
        self.mousepos = self.get_mouse_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:

            # select block
            self.selection = self.mousepos

            if event.button == 1:
                # move block
                if self.mousepos in self.blocks:
                    self.block_selected = pygame.Vector2(self.mousepos.x, self.mousepos.y)
                elif self.block_selected in self.blocks:
                    self.blocks.remove(self.block_selected)
                    self.blocks.append(self.mousepos)
                    print('appending mouse pos: {}'.format(self.mousepos))

            # add/remove block
            if event.button == 3:
                self.selection = None
                newblock = Block(self.mousepos.x, self.mousepos.y, self.size, self.color, BlockType.SOLID)
                # if self.mousepos not in self.blocks:
                if newblock not in self.blocks:
                    self.blocks.append(newblock)
                    # self.blocks.append(self.mousepos)
                else:
                    self.blocks.remove(newblock)
                    # self.blocks.remove(self.mousepos)
            # print('block selected: {}'.format(self.block_selected))
            # print('blocks: {}'.format(self.blocks))
            # print('selection: {}'.format(self.selection))
            print('blocks count: ' + str(len(self.blocks)))
        
        # clear blocks
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.blocks.clear()

    def get_mouse_pos(self):
        return pygame.Vector2([(x // self.size) * self.size for x in pygame.mouse.get_pos()])