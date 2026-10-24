import pygame
import random

def choose_mini_hippos(mini_hippos, mini_names, eggs_collected):
    minis_with_names = list(zip(mini_hippos, mini_names))
    random.shuffle(minis_with_names)
    selected = []
    # Primero, elegir hasta 24 minis sin repetir
    selected.extend(minis_with_names[:eggs_collected])
    # Si hay más de 24 huevos, repetir colores aleatoriamente
    while len(selected) < eggs_collected:
        selected.append(random.choice(minis_with_names))
    return selected

def draw_game_over(screen, game_font, player_score, selected_minis):
    screen.fill((208, 245, 244))
    text = game_font.render("GAME OVER", True, (0, 0, 0))
    text_rect = text.get_rect(center=(640, 250))
    screen.blit(text, text_rect)

    # Puntaje final
    final_score_text = game_font.render(f"Final Score: {int(player_score)}", True, (0, 0, 0))
    final_score_rect = final_score_text.get_rect(center=(640, 300))
    screen.blit(final_score_text, final_score_rect)

    # Dibujar un mini Hipo por cada huevo recolectado
    spacing = 90
    max_per_row = 10
    total = len(selected_minis)
    name_font = pygame.font.Font("Assets/PressStart2P-Regular.ttf", 10)

    for i, (mini, name) in enumerate(selected_minis):
        row = i // max_per_row
        col = i % max_per_row
        items_in_row = min(max_per_row, total - row * max_per_row)
        start_x = 640 - (items_in_row - 1) * spacing / 2
        x = start_x + col * spacing
        y = 420 + row * 100
        screen.blit(mini, mini.get_rect(center=(x, y)))
        name_text = name_font.render(name, True, (0, 0, 0))
        name_rect = name_text.get_rect(center=(x, y + 43))
        screen.blit(name_text, name_rect)

