import pygame
pygame.init()
pygame.font.init()

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)

WIDTH = 600
HEIGHT = 700
TOOLBAR_HEIGHT = HEIGHT - WIDTH

COLUMNS = 50
ROWS = 50

PIXEL_SIZE = WIDTH // ROWS
BG_COLOR = WHITE

FPS = 240

clock = pygame.time.Clock()

def get_font(size):
    return pygame.font.SysFont("comicsans",size)