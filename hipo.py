import math
import os
import random
import sys
import pygame

from backend.Classes import Bat, Hipo, Huevo, Tortuga
from backend.audio import AudioManager
from backend.high_score import get_unlocked_minis, load_high_score, save_high_score, unlock_minis
from frontend.Game_over import choose_mini_hippos, draw_game_over, draw_pause_screen, draw_start_screen
from frontend.background import BackgroundManager
from frontend.collection import (
    draw_collection_screen,
    get_current_page,
    next_page,
    prev_page,
    set_current_page,
)
from frontend.particles import ParticleManager

# Inicializar Pygame & Mixer
pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hipo Run")
clock = pygame.time.Clock()

# Superficie para efecto screen-shake
game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# Audio, Récords y Colección de Mini Hipos
audio = AudioManager()
high_score, max_eggs = load_high_score()
unlocked_minis = get_unlocked_minis()

# Partículas y Fondo
particles = ParticleManager()
bg_manager = BackgroundManager(SCREEN_WIDTH, SCREEN_HEIGHT)

# Fuentes
title_font = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 46)
game_font = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 20)
hud_font = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 16)
small_font = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 12)
particles.set_font(small_font)

# HUD Assets
hud_egg_icon = pygame.image.load("Assets/Huevo_1a.png").convert_alpha()
hud_egg_icon = pygame.transform.scale(hud_egg_icon, (115, 75))

# Assets Pantalla de Inicio
start_image = pygame.image.load("Assets/Hipo_1.png").convert_alpha()
start_image = pygame.transform.scale(start_image, (280, 240))
flower1 = pygame.image.load("Assets/Flor1.png").convert_alpha()
flower2 = pygame.image.load("Assets/Flor2.png").convert_alpha()
flower1 = pygame.transform.scale(flower1, (55, 55))
flower2 = pygame.transform.scale(flower2, (42, 42))

# Cargar los 24 Mini Hipos una sola vez
mini_hippos = []
for i in range(1, 49):
    img = pygame.image.load(f"Assets/Minis/mini_{i}.png").convert_alpha()
    mini_hippos.append(img)

mini_names = [
    "Sylvia", "Mora", "Bigotes", "Cunky", "Platón", "Gambito", "Roberto", "Óscar",  #8
    "Chicho", "Focaccia", "Carlos", "Soya", "Ángel", "Abed", "Magnolia", "Pelusa",  #16
    "Espresso", "Flan", "Coco", "Fuji", "Alvi", "Penco", "Samurai", "Arya", #24
    "Fuchsia", "Mario Hugo", "Frodo", "Lolita", "Jote", "Magnus", "Hummus", "Canelo", #32
    "Tulipa", "Jesús G", "Hoppy", "Ubwuzu", "Kalita", "Troy", "Pablo", "Mangual",  #40
    "Kiko", "Liguria", "Alex", "Cotona", "Krtek", "Amor", "Maní", "Dino"
]

# Estados del juego
STATE_START = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAME_OVER = 3
STATE_COLLECTION = 4

state = STATE_START
previous_state = STATE_START

game_speed = 3.2
player_score = 0.0
eggs_collected = 0
is_new_record = False
screen_shake = 0
show_debug_hitboxes = False

# Entidades (Hipo y obstáculos alineados en ground_y = 418)
hipo = Hipo(120, 356)
tortugas = pygame.sprite.Group()
bats = pygame.sprite.Group()
huevos = pygame.sprite.Group()

last_spawn_time = 0
spawn_cooldown = 1800
next_egg_spawn = 0
selected_minis = []
run_dust_timer = 0


def reset_game():
    global hipo, tortugas, bats, huevos
    global game_speed, player_score, eggs_collected
    global state, is_new_record, selected_minis
    global last_spawn_time, spawn_cooldown, next_egg_spawn
    global screen_shake, run_dust_timer

    hipo = Hipo(120, 356)
    tortugas.empty()
    bats.empty()
    huevos.empty()
    particles.clear()
    bg_manager.reset()

    game_speed = 3.2
    player_score = 0.0
    eggs_collected = 0
    is_new_record = False
    screen_shake = 0
    run_dust_timer = 0
    selected_minis = []

    current_time = pygame.time.get_ticks()
    last_spawn_time = current_time
    spawn_cooldown = random.randint(1400, 2200)
    next_egg_spawn = current_time + random.randint(7500, 10000)
    state = STATE_PLAYING


def check_collisions():
    hipo_box = hipo.get_hitbox()
    for tortuga in tortugas:
        if hipo_box.colliderect(tortuga.get_hitbox()):
            return True, (tortuga.rect.centerx, tortuga.rect.centery)
    for bat in bats:
        if hipo_box.colliderect(bat.get_hitbox()):
            return True, (bat.rect.centerx, bat.rect.centery)
    return False, None


def main():
    global state, previous_state, player_score, game_speed, eggs_collected, is_new_record
    global screen_shake, show_debug_hitboxes, last_spawn_time, spawn_cooldown
    global next_egg_spawn, selected_minis, run_dust_timer, high_score, unlocked_minis

    play_btn = pygame.Rect(330, 560, 280, 58)
    col_btn = pygame.Rect(640, 560, 310, 58)
    col_btn_rect = pygame.Rect(450, 580, 380, 44)
    col_buttons = {
        "back": pygame.Rect(500, 615, 280, 46),
        "prev": pygame.Rect(260, 552, 90, 38),
        "next": pygame.Rect(910, 552, 90, 38),
        "page1": pygame.Rect(370, 552, 250, 38),
        "page2": pygame.Rect(640, 552, 250, 38),
    }

    while True:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mutear / Activar sonido (M)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                audio.toggle_mute()

            # Ver hitboxes de depuración (F3 o H)
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_F3 or event.key == pygame.K_h):
                show_debug_hitboxes = not show_debug_hitboxes

            # --- ESTADO INICIO ---
            if state == STATE_START:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        audio.play("click")
                        reset_game()
                    elif event.key == pygame.K_c:
                        audio.play("click")
                        previous_state = STATE_START
                        set_current_page(0)
                        state = STATE_COLLECTION

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_btn.collidepoint(event.pos):
                        audio.play("click")
                        reset_game()
                    elif col_btn.collidepoint(event.pos):
                        audio.play("click")
                        previous_state = STATE_START
                        set_current_page(0)
                        state = STATE_COLLECTION

            # --- ESTADO JUGANDO ---
            elif state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        if not hipo.is_jumping:
                            audio.play("jump")
                        hipo.jump()
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        audio.play("duck")
                        hipo.set_ducking(True)
                    elif event.key in (pygame.K_p, pygame.K_ESCAPE):
                        state = STATE_PAUSED
                        audio.play("click")

                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                        hipo.cut_jump()
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        hipo.set_ducking(False)

            # --- ESTADO PAUSA ---
            elif state == STATE_PAUSED:
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_ESCAPE):
                    state = STATE_PLAYING
                    audio.play("click")

            # --- ESTADO GAME OVER ---
            elif state == STATE_GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_r, pygame.K_SPACE, pygame.K_RETURN):
                        audio.play("click")
                        reset_game()
                    elif event.key == pygame.K_c:
                        audio.play("click")
                        previous_state = STATE_GAME_OVER
                        set_current_page(0)
                        state = STATE_COLLECTION

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if col_btn_rect.collidepoint(event.pos):
                        audio.play("click")
                        previous_state = STATE_GAME_OVER
                        set_current_page(0)
                        state = STATE_COLLECTION
                    else:
                        audio.play("click")
                        reset_game()

            # --- ESTADO COLECCIÓN / ÁLBUM ---
            elif state == STATE_COLLECTION:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_ESCAPE, pygame.K_c, pygame.K_SPACE, pygame.K_RETURN):
                        audio.play("click")
                        state = previous_state
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        audio.play("click")
                        prev_page()
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        audio.play("click")
                        next_page()
                    elif event.key in (pygame.K_1, pygame.K_KP1):
                        audio.play("click")
                        set_current_page(0)
                    elif event.key in (pygame.K_2, pygame.K_KP2):
                        audio.play("click")
                        set_current_page(1)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if col_buttons.get("back") and col_buttons["back"].collidepoint(event.pos):
                        audio.play("click")
                        state = previous_state
                    elif col_buttons.get("prev") and col_buttons["prev"].collidepoint(event.pos):
                        audio.play("click")
                        prev_page()
                    elif col_buttons.get("next") and col_buttons["next"].collidepoint(event.pos):
                        audio.play("click")
                        next_page()
                    elif col_buttons.get("page1") and col_buttons["page1"].collidepoint(event.pos):
                        audio.play("click")
                        set_current_page(0)
                    elif col_buttons.get("page2") and col_buttons["page2"].collidepoint(event.pos):
                        audio.play("click")
                        set_current_page(1)

        # ================= RENDERIZADO Y ACTUALIZACIÓN =================

        if state == STATE_START:
            play_btn, col_btn = draw_start_screen(
                game_surface, title_font, small_font, start_image, flower1, flower2,
                high_score, len(unlocked_minis)
            )

        elif state == STATE_PAUSED:
            draw_pause_screen(game_surface)

        elif state == STATE_GAME_OVER:
            col_btn_rect = draw_game_over(
                game_surface, game_font, player_score, high_score, is_new_record,
                selected_minis, len(unlocked_minis)
            )

        elif state == STATE_COLLECTION:
            col_buttons = draw_collection_screen(game_surface, unlocked_minis, mini_hippos, mini_names)

        elif state == STATE_PLAYING:
            # 1. Generación de obstáculos
            if current_time - last_spawn_time >= spawn_cooldown:
                if player_score > 40 and random.random() < 0.35:
                    bats.add(Bat())
                else:
                    tortugas.add(Tortuga(1330, 397))

                last_spawn_time = current_time
                min_cooldown = max(850, 1500 - int(player_score * 3.0))
                spawn_cooldown = random.randint(min_cooldown, min_cooldown + 400)

            # 2. Generación de huevos mágicos (3 alturas: suelo 397, salto medio 305, salto alto 220)
            if current_time >= next_egg_spawn:
                has_near_obstacle = any(t.rect.x > 1100 for t in tortugas)
                if not has_near_obstacle:
                    egg_y = random.choice([397, 305, 220])
                    huevos.add(Huevo(1330, egg_y))
                    next_egg_spawn = current_time + random.randint(5500, 8500)
                else:
                    next_egg_spawn = current_time + 500

            # 3. Actualizar fondo
            bg_manager.update(game_speed)

            # 4. Dibujar cielo, nubes y colinas
            bg_manager.draw_sky_and_distance(game_surface)

            # 5. Dibujar suelo y línea divisoria (ground_y = 418)
            bg_manager.draw_foreground(game_surface)

            # 6. Actualizar entidades
            tortugas.update(game_speed)
            bats.update(game_speed)
            huevos.update(game_speed)
            hipo.update()

            # 7. Partículas de polvo al correr y aterrizar
            if hipo.just_landed:
                particles.add_landing_dust(hipo.rect.centerx, 418)
            elif not hipo.is_jumping and not hipo.ducking:
                run_dust_timer += 1
                if run_dust_timer >= 5:
                    run_dust_timer = 0
                    particles.add_run_dust(hipo.rect.left + 25, 418)

            # 8. Recolección de huevos mágicos
            hipo_box = hipo.get_hitbox()
            for egg in list(huevos):
                if hipo_box.colliderect(egg.rect):
                    eggs_collected += 1
                    player_score += 10.0
                    audio.play("egg")
                    particles.add_egg_sparkles(egg.rect.centerx, egg.rect.centery)
                    particles.add_floating_text("+10", egg.rect.centerx, egg.rect.centery)
                    egg.kill()

            # 9. Actualizar y dibujar partículas
            particles.update()
            particles.draw(game_surface)

            # 10. Dibujar entidades
            tortugas.draw(game_surface)
            bats.draw(game_surface)
            huevos.draw(game_surface)
            hipo.draw(game_surface)

            # 11. Hitboxes de depuración
            if show_debug_hitboxes:
                pygame.draw.rect(game_surface, (0, 255, 0), hipo.get_hitbox(), 2)
                for t in tortugas:
                    pygame.draw.rect(game_surface, (255, 0, 0), t.get_hitbox(), 2)
                for b in bats:
                    pygame.draw.rect(game_surface, (255, 0, 255), b.get_hitbox(), 2)
                for e in huevos:
                    pygame.draw.rect(game_surface, (255, 255, 0), e.rect, 2)

            # 12. Chequear colisiones con obstáculos
            collided, col_pos = check_collisions()
            if collided:
                state = STATE_GAME_OVER
                screen_shake = 16
                if col_pos:
                    particles.add_impact(col_pos[0], col_pos[1])

                # Elegir mini hipos 
                selected_minis = choose_mini_hippos(
                    mini_hippos, mini_names, eggs_collected, unlocked_minis
                )
                # Guardar los mini hipos desbloqueados permanentemente
                rescued_ids = [m["id"] for m in selected_minis]
                newly_found, unlocked_minis = unlock_minis(rescued_ids)

                high_score, is_new_record = save_high_score(player_score, eggs_collected)

                if is_new_record or newly_found:
                    audio.play("record")
                else:
                    audio.play("game_over")

            else:
                # Avanzar puntaje y velocidad
                player_score += 0.1
                game_speed += 0.0018

                # --- HUD ---
                score_text = hud_font.render(f"Score: {int(player_score):05d}", True, (25, 55, 55))
                game_surface.blit(score_text, (20, 18))

                effective_hi = max(high_score, int(player_score))
                hi_text = hud_font.render(f"Record: {effective_hi:05d}", True, (110, 135, 135))
                game_surface.blit(hi_text, (280, 18))

                game_surface.blit(hud_egg_icon, (14, 25))
                eggs_text = hud_font.render(f": {eggs_collected}", True, (25, 55, 55))
                game_surface.blit(eggs_text, (100, 55))

                if audio.muted:
                    mute_indicator = small_font.render("MUTED (M)", True, (180, 80, 80))
                    game_surface.blit(mute_indicator, (SCREEN_WIDTH - 120, 18))

        # ================= SCREEN SHAKE Y BLIT FINAL =================
        if screen_shake > 0:
            shake_x = random.randint(-screen_shake, screen_shake)
            shake_y = random.randint(-screen_shake, screen_shake)
            screen_shake -= 1
        else:
            shake_x, shake_y = 0, 0

        screen.fill((0, 0, 0))
        screen.blit(game_surface, (shake_x, shake_y))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
