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

#Chequear colisiones
def check_collisions():
    hipo_hitbox = hipo.rect.inflate(-70, -100)
    for tortuga in tortugas:
        tortuga_hitbox = tortuga.rect.inflate(-50, -20)
        if hipo_hitbox.colliderect(tortuga_hitbox):
            return True
    for bat in bats:
        bat_hitbox = bat.rect.inflate(-30, -20)
        if hipo_hitbox.colliderect(bat_hitbox):
            return True
    return False

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

    ##### TEMPORAL: DIBUJAR RECTÁNGULOS DE COLISIÓN #####
    # Rectángulo de Hipo en rojo
    hipo_hitbox = hipo.rect.inflate(-70, -100)
    pygame.draw.rect(screen, (255, 0, 0), hipo_hitbox, 2)
    for tortuga in tortugas:
        tortuga_hitbox = tortuga.rect.inflate(-50, -20)
        pygame.draw.rect(screen, (0, 0, 255), tortuga_hitbox, 2)
    # Rectángulos de los murciélagos en verde
    for bat in bats:
        bat_hitbox = bat.rect.inflate(-30, -20)
        pygame.draw.rect(screen, (0, 255, 0), bat_hitbox, 2)
    ####################################################

    if check_collisions():
        game_over = True
        
    if game_over:
        text = game_font.render("GAME OVER", True, (0, 0, 0))
        text_rect = text.get_rect(center=(640, 300))

        screen.fill((208, 245, 244))
        screen.blit(text, text_rect)
        final_score_text = game_font.render(f"Final Score: {int(player_score)}", True, (0, 0, 0))
        final_score_rect = final_score_text.get_rect(center=(640, 350))
        screen.blit(final_score_text, final_score_rect)

        pygame.display.flip()
        clock.tick(60)
        continue

    else:
        player_score += 0.1
        score_text = game_font.render(f"Score: {int(player_score)}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))   
        game_speed += 0.0025


    pygame.display.flip()
    clock.tick(60)
