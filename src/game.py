import pygame
from network import Network
from player import Player

# consts
DISPLAY_WIDTH = 500
DISPLAY_HEIGHT = 500
BLOCK_SIZE = 20

# pygame setup
pygame.init()
pygame.display.set_caption('Grid Ravager')
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
CLOCK = pygame.time.Clock()
dt = 0
speed = 0.5

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


    second = 0
    while running:

        if gamemode == 'multi':
            other_players = net.send(player)
        else:
            other_players = None

        # poll for events
        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            player.controls(event)

        # draw everything
        draw_everything(player, other_players)

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
        pygame.display.set_caption(caption)

        # update player
        player.update(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    pygame.quit()

def draw_everything(player, other_players = None):

    # fill the screen with a color to wipe away anything from last frame
    DISPLAY.fill('white')

    drawGrid()

    if other_players is not None:
        for other in other_players:
            other.draw_blocks(DISPLAY)
            # other.draw_selection(DISPLAY, other.color)
            other.draw_cursor(DISPLAY, other.color)
    if player is not None:
        player.draw_blocks(DISPLAY)
        # player.draw_selection(DISPLAY, 'green')
        player.draw_cursor(DISPLAY, 'green')

    # draw cursor

    # flip() the display to put your work on screen
    pygame.display.flip()

def drawGrid():
    for x in range(0, DISPLAY_WIDTH, BLOCK_SIZE):
        for y in range(0, DISPLAY_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(DISPLAY, 'black', rect, 1)

# calling main
main()