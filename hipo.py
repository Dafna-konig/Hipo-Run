import pygame
import sys
import random
from Classes import Hipo, Tortuga, Bat, Huevo
from Game_over import draw_game_over, choose_mini_hippos

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Hipo Run")

# Variables
game_font = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 24)
game_speed = 3
player_score = 0
game_over = False
ground = pygame.image.load("Assets/Pasto.png").convert_alpha()
ground = pygame.transform.scale(ground, (1700, 90))
ground_x = 0
eggs_collected = 0

egg_icon = pygame.image.load("Assets/Huevo_1a.png").convert_alpha()
egg_icon = pygame.transform.scale(egg_icon, (130, 90))

# Personaje y grupos de obstáculos
hipo = Hipo(110, 365)
tortugas = pygame.sprite.Group()
bats = pygame.sprite.Group()
huevos = pygame.sprite.Group()
last_spawn_time = pygame.time.get_ticks()
spawn_cooldown = 1800
next_egg_spawn = pygame.time.get_ticks() + random.randint(5000, 9000)

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

# Cargar mini Hippos
mini_hippos = []
for i in range(1, 25):
    image = pygame.image.load(f"Assets/minis/mini_{i}.png").convert_alpha()
    image = pygame.transform.scale(image, (80, 60))
    mini_hippos.append(image)
mini_names = ["Sylvia", "Mora", "Bigotes", "Cunky", "Platón", "Gambito", "Roberto", "Oscar", "Chicho", "Focaccia", "Carlos", "Soya", 
              "Ángel", "Abed", "Hummus", "Pelusa", "Espresso", "Flan", "Coco", "Fuji", "Alvi", "Penco", "Samurai", "Arya"]
selected_minis = []

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

    if game_over:
        draw_game_over(screen, game_font, player_score, selected_minis)
        pygame.display.flip()
        clock.tick(60)
        continue

    current_time = pygame.time.get_ticks()

    if current_time - last_spawn_time >= spawn_cooldown:
        # Elegir aleatoriamente el tipo de obstáculo
        if random.choice(["tortuga", "tortuga", "bat"]) == "tortuga":
            tortugas.add(Tortuga(1330, 397))
        else:
            bats.add(Bat())

        last_spawn_time = current_time

    if current_time >= next_egg_spawn:
        huevos.add(Huevo(1330, 397))
        next_egg_spawn = current_time + random.randint(6000, 9000)

    # Mover el pasto
    ground_x -= game_speed
    if ground_x <= -1700:
        ground_x = 0

    screen.fill((208, 245, 244))
    screen.blit(ground, (ground_x, 390))
    screen.blit(ground, (ground_x + 1700, 390))


    # Actualizar y dibujar obstáculos
    tortugas.update(game_speed)
    bats.update(game_speed)
    huevos.update(game_speed)

    collected_eggs = pygame.sprite.spritecollide(hipo, huevos, dokill=True)
    for huevo in collected_eggs:
        eggs_collected += 1

    tortugas.draw(screen)
    bats.draw(screen)
    huevos.draw(screen)

    # Actualizar y dibujar a Hipo
    hipo.update()
    hipo.draw(screen)

    if check_collisions():
        game_over = True
        selected_minis = choose_mini_hippos(mini_hippos, mini_names, eggs_collected)
        draw_game_over(screen, game_font, player_score, selected_minis)

    else:
        player_score += 0.1 + len(collected_eggs) * 10
        score_text = game_font.render(f"Score: {int(player_score)}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))  
        screen.blit(egg_icon, (0, 20)) 
        eggs_text = game_font.render(f" : {eggs_collected}", True, (0, 0, 0))
        screen.blit(eggs_text, (89, 50))
        game_speed += 0.0025
        spawn_cooldown = max(800, random.randint(1500, 3000) - int(player_score * 2))


    pygame.display.flip()
    clock.tick(60)
