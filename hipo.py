import pygame
import sys
import random
from Classes import Hipo

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Hipo Run")

#Variables
game_font = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 24)
game_speed = 3
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

ground = pygame.image.load("Assets/Pasto.png").convert_alpha()
ground = pygame.transform.scale(ground, (2100, 80))
ground_x = 0

hipo = Hipo(110, 375)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hipo.jump()

    ground_x -= game_speed
    if ground_x <= -2100:
        ground_x = 0

    screen.fill((255, 255, 255))
    screen.blit(ground, (ground_x, 360))
    screen.blit(ground, (ground_x + 2100, 360))

    # Update 
    hipo.update()
    hipo.draw(screen)

    pygame.display.flip()
    clock.tick(60)