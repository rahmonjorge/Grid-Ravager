import pygame

from input import *


# pygame setup
pygame.init()
pygame.display.set_caption("Grid Ravager")
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
dt = 0

# mygame setup
BLOCK_SIZE = 20
MOVE_DISTANCE = 20
PLAYER_COLOR = "red"
GRID_COLOR = "black"

player_pos = pygame.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

grid_pos = player_pos / 20

def main():
    running = True
    blocks = []
    while running:
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # user input
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key in (pygame.K_UP, pygame.K_w):
                    player_pos.y -= MOVE_DISTANCE
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    player_pos.x -= MOVE_DISTANCE
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    player_pos.y += MOVE_DISTANCE
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    player_pos.x += MOVE_DISTANCE
                if event.key == pygame.K_SPACE:
                    if player_pos not in blocks: 
                        blocks.append(pygame.Vector2(player_pos))

        # update game logic
        grid_pos = player_pos / 20

        # debug log

        # fill the screen with a color to wipe away anything from last frame
        SCREEN.fill("white")

        # draw grid
        drawGrid()
        drawBlocks(blocks)

        # draw player
        player_rect = pygame.Rect(
            player_pos.x, player_pos.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, PLAYER_COLOR, player_rect, 2)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = CLOCK.tick(60) / 1000

    pygame.quit()

def drawGrid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, GRID_COLOR, rect, 1)

def drawBlocks(blocks):
    for block in blocks:
        rect = pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, PLAYER_COLOR, rect, 0)


# calling main
main()
