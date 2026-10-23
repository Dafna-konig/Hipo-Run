import pygame
import sys
import random
from Classes import Hipo, Tortuga, Bat

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Hipo Run")

# Variables
game_font = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 24)
game_speed = 3
player_score = 0
game_over = False
obstacle_cooldown = 5000
ground = pygame.image.load("Assets/Pasto.png").convert_alpha()
ground = pygame.transform.scale(ground, (1700, 90))
ground_x = 0

# Personaje y grupos de obstáculos
hipo = Hipo(110, 365)
tortugas = pygame.sprite.Group()
bats = pygame.sprite.Group()
last_spawn_time = pygame.time.get_ticks()
spawn_cooldown = 1800

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hipo.jump()

            if event.key == pygame.K_DOWN:
                hipo.set_ducking(True)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                hipo.set_ducking(False)

    current_time = pygame.time.get_ticks()

    if current_time - last_spawn_time >= spawn_cooldown:

        # Elegir aleatoriamente el tipo de obstáculo
        if random.choice(["tortuga", "bat"]) == "tortuga":
            tortugas.add(Tortuga(1330, 397))
        else:
            bats.add(Bat())

        last_spawn_time = current_time
        spawn_cooldown = random.randint(1800, 2800)

    # Mover el pasto
    ground_x -= game_speed
    if ground_x <= -1700:
        ground_x = 0

    screen.fill((208, 245, 244))
    screen.blit(ground, (ground_x, 390))
    screen.blit(ground, (ground_x + 1700, 390))

    # Actualizar y dibujar obstáculos
    tortugas.update()
    bats.update()

    tortugas.draw(screen)
    bats.draw(screen)

    # Actualizar y dibujar a Hipo
    hipo.update()
    hipo.draw(screen)

    pygame.display.flip()
    clock.tick(60)
