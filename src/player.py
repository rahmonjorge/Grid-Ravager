import pygame
from block import Block, BlockType

class Player():
    def __init__(self, size, color):

        # attributes
        self.size = size
        self.color = color
        self.blocks = []

        # assets
        self.sound1 = None
        self.sound2 = None

        # states
        self.selection = None
        self.block_selected = None
        self.mousepos = None
        self.moving = False
        self.running = False

    def draw_blocks(self, display):
        for block in self.blocks:
            block.draw(display)
    
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
        

        if event.type == pygame.MOUSEBUTTONDOWN:

            # select block
            self.selection = self.mousepos

            # add/toggle block
            if event.button == 1:
                newblock = Block(self.mousepos.x, self.mousepos.y, self.size, self.color, BlockType.SOLID)
                if newblock not in self.blocks:
                    self.blocks.append(newblock)
                else:
                    index = self.blocks.index(newblock)
                    type = self.blocks[index].type
                    if type == BlockType.SOLID:
                        self.blocks[index].type = BlockType.ARROWUP
                    elif type == BlockType.ARROWUP:
                        self.blocks[index].type = BlockType.ARROWRIGHT
                    elif type == BlockType.ARROWRIGHT:
                        self.blocks[index].type = BlockType.ARROWDOWN
                    elif type == BlockType.ARROWDOWN:
                        self.blocks[index].type = BlockType.ARROWLEFT
                    elif type == BlockType.ARROWLEFT:
                        self.blocks[index].type = BlockType.HOLLOW
                    else:
                        self.blocks[index].type = BlockType.SOLID
                
            # remove block
            if event.button == 3:
                pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound1))

                self.selection = None

                check = Block(self.mousepos.x, self.mousepos.y, self.size, self.color)
                if check in self.blocks:
                    self.blocks.remove(check)
                

            
        
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                pygame.mixer.Sound.play(pygame.mixer.Sound(self.sound2))

        if event.type == pygame.KEYDOWN:
            # clear blocks  
            if event.key == pygame.K_c:
                self.blocks.clear()
            # run 
            if event.key == pygame.K_r:
                self.running = not self.running

    def update(self, display_width, display_height):
        self.mousepos = self.get_mouse_pos()

        # move blocks
        if self.running and self.moving:
            for block in self.blocks:
                other_blocks = [other for other in self.blocks if other is not block]
                block.move(other_blocks, display_width, display_height)

        # debug 
        # print('block selected: {}'.format(self.block_selected))
        # print('blocks: {}'.format(self.blocks))
        # print('selection: {}'.format(self.selection))
        

    def get_mouse_pos(self):
        return pygame.Vector2([(p // self.size) * self.size for p in pygame.mouse.get_pos()])