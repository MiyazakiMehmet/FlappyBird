import time
import pygame

screen_width = 680
screen_height = 720

WIN = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 60

#shifting
ground_scroll = 0
scroll_speed = 4

#upload image
bg = pygame.image.load("bg_night.png")
ground = pygame.image.load("ground.png")
bg = pygame.transform.scale(bg, (screen_width,screen_height - 100))
ground = pygame.transform.scale(ground, (screen_width + 40, 100))
