import pygame
from network import Network
from player import Player

# consts
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

# pygame setup
pygame.init()
pygame.display.set_caption("Grid Ravager")
DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
CLOCK = pygame.time.Clock()
dt = 0

# mygame setup
BLOCK_SIZE = 20
MOVE_DISTANCE = 20
GREEN = "green"
RED = "red"
BLACK = "black"
WHITE = "white"

def main():

    running = True
    net = Network() # creates a new network object
    player = net.get_player() # gets the player from the server

    while running:

        other_players = net.send(player)

        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.controls(event)
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        draw_everything(player, other_players)

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = CLOCK.tick(60) / 1000

    pygame.quit()

def draw_everything(player, players):

    # fill the screen with a color to wipe away anything from last frame
    DISPLAY.fill(WHITE)

    drawGrid()
    player.draw(DISPLAY)

    for other_player in players:
        other_player.draw(DISPLAY)

    # flip() the display to put your work on screen
    pygame.display.flip()


def drawGrid():
    for x in range(0, DISPLAY_WIDTH, BLOCK_SIZE):
        for y in range(0, DISPLAY_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(DISPLAY, BLACK, rect, 1)


# calling main
main()
