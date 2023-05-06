import pygame
from network import Network
from player import Player
from block import Block, BlockType
from object import Object
from random import randrange

# consts
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 240
BLOCK_SIZE = 20

GRID_WIDTH = DISPLAY_WIDTH // BLOCK_SIZE
GRID_HEIGHT = DISPLAY_HEIGHT // BLOCK_SIZE

COLOR_GRASS = (19,109,21)
COLOR_BLACK = (0,0,0)

# pygame setup
pygame.init()
pygame.display.set_caption('Grid Ravager')
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
CLOCK = pygame.time.Clock()
dt = 0
speed = 0.5
fps = 0

# assets
img_coin = pygame.image.load('assets/img/coin.png')
snd_coin = pygame.mixer.Sound('assets/audio/coin.wav')

# game
obj_count = 20

def main():
    caption = 'Grid Ravager'
    running = True
    net = Network() # creates a new network object
    player = net.get_player() # gets the player from the server

    # set gamemode
    if player is None:
        gamemode = 'single'
        player = Player(BLOCK_SIZE, 'red')
    else:
        gamemode = 'multi'
        caption += ': ' + str(player.color)

    print('Running in {}player mode'.format(gamemode))

    load_assets(player)

    terrain, objects = spawn_everything()

    second = 0
    while running:

        if gamemode == 'multi':
            other_players = net.send(player)
        else:
            other_players = None

        # update game logic
        player.update(DISPLAY_WIDTH,DISPLAY_HEIGHT)

        # poll for events
        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            # edit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # remove block
                    pygame.mixer.Sound.play(pygame.mixer.Sound(player.sound1))

                    block = Block(player.mousepos.x, player.mousepos.y, player.size, player.color)
                    if block in terrain:
                        terrain.remove(block)
                    # remove object
                    else:
                        check = Object('coin', player.mousepos.x, player.mousepos.y)
                        if check in objects:
                            index = objects.index(check)
                            objects[index].play_sound()
                            objects.remove(check)
            if event.type == pygame.MOUSEBUTTONUP:
                print('blocks count: ' + str(len(terrain)))
                if event.button == 1:
                    pygame.mixer.Sound.play(pygame.mixer.Sound(player.sound2))
            # player.controls(event)

        # draw everything
        draw_everything(terrain=terrain, objects=objects)

        # update clocks
        dt = CLOCK.tick(60) / 1000 # limits FPS to 60

        second += dt
        if second >= speed:
            player.moving = True
            second = 0
        else:
            player.moving = False
        
        # update window caption
        if gamemode == 'single':
            if player.running:
                caption = 'running'
            else:
                caption = 'paused'
        pygame.display.set_caption('CL: '+ str(len(objects)) + ' FPS: ' + str(CLOCK.get_fps()))

        # update player
        player.update(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    pygame.quit()

def draw_everything(terrain = None, objects = None, player = None, other_players = None):

    # fill the screen with a color to wipe away anything from last frame
    DISPLAY.fill('white')

    if objects:
        for obj in objects:
            obj.draw(DISPLAY)

    if terrain:
        for tile in terrain:
            tile.draw(DISPLAY)

    '''if other_players:
        for other in other_players:
            other.draw_blocks(DISPLAY)
            # other.draw_selection(DISPLAY, other.color)
            # other.draw_cursor(DISPLAY, other.color)
    if player:
        player.draw_blocks(DISPLAY)
        # player.draw_selection(DISPLAY, 'green')
        # player.draw_cursor(DISPLAY, 'green')'''

    drawGrid()
    # draw cursor

    # flip() the display to put your work on screen
    pygame.display.flip()

def spawn_everything():

    # spawn terrain
    terrain = [Block(x, y, BLOCK_SIZE, COLOR_GRASS, BlockType.SOLID) for x in range(0, DISPLAY_WIDTH, BLOCK_SIZE) for y in range(0, DISPLAY_WIDTH, BLOCK_SIZE)]

    # spawn coins
    objects = []
    for i in range(obj_count):
        rand_x = randrange(GRID_WIDTH) * BLOCK_SIZE
        rand_y = randrange(GRID_HEIGHT) * BLOCK_SIZE
        coin = Object('coin', rand_x, rand_y)
        coin.texture = img_coin
        coin.offset = 2
        coin.sound = snd_coin
        objects.append(coin)
    
    return terrain, objects

def drawGrid():
    for x in range(0, DISPLAY_WIDTH, BLOCK_SIZE):
        for y in range(0, DISPLAY_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(DISPLAY, COLOR_BLACK, rect, 1)

def load_assets(player):
    player.sound1 = 'assets/audio/click part 1.wav'
    player.sound2 = 'assets/audio/click part 2.wav'

# calling main
main()