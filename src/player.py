import pygame
from block import Block, BlockType

class Player():
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.selection = None
        self.block_selected = None
        self.blocks = []
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
        self.mousepos = self.get_mouse_pos()

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
                self.selection = None
                newblock = Block(self.mousepos.x, self.mousepos.y, self.size, self.color, BlockType.SOLID)
                if newblock in self.blocks:
                    self.blocks.remove(newblock)

            # debug 
            # print('block selected: {}'.format(self.block_selected))
            # print('blocks: {}'.format(self.blocks))
            # print('selection: {}'.format(self.selection))
            print('blocks count: ' + str(len(self.blocks)))
        
        if event.type == pygame.KEYDOWN:
            # clear blocks  
            if event.key == pygame.K_c:
                self.blocks.clear()
            # run 
            if event.key == pygame.K_r:
                self.running = not self.running

    def update(self, display_width, display_height):
        # move blocks
        if self.running and self.moving:
            for block in self.blocks:
                other_blocks = [other for other in self.blocks if other is not block]
                block.move(other_blocks, display_width, display_height)
                '''if block.type == BlockType.ARROWRIGHT:
                    if block.check_right(other_blocks, display_width):
                        block.moveright()
                elif block.type == BlockType.ARROWDOWN:
                    if block.check_down(other_blocks, display_height):
                        block.movedown()
                elif block.type == BlockType.ARROWLEFT:
                    if block.check_left(other_blocks, 0):
                        block.moveleft()
                elif block.type == BlockType.ARROWUP:
                    if block.check_up(other_blocks, 0):
                        block.moveup()'''

    def get_mouse_pos(self):
        return pygame.Vector2([(x // self.size) * self.size for x in pygame.mouse.get_pos()])