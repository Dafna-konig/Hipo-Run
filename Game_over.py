import math
import random
import pygame

# Cache fonts globally 
_fonts = {}


def get_font(size):
    if size not in _fonts:
        _fonts[size] = pygame.font.Font("Assets/PressStart2P-Regular.ttf", size)
    return _fonts[size]


def choose_mini_hippos(mini_hippos, mini_names, eggs_collected, unlocked_ids=None):
    """
    Selects mini hippos based on eggs collected.
    Prioritizes undiscovered mini hippos so players expand their collection!
    Returns list of dicts: {'id': id, 'image': img, 'name': name, 'is_new': bool}
    """
    if unlocked_ids is None:
        unlocked_ids = set()

    total_available = len(mini_hippos)
    all_indices = list(range(1, total_available + 1))

    # Separate into locked and already unlocked
    locked_ids = [i for i in all_indices if i not in unlocked_ids]
    unlocked_list = [i for i in all_indices if i in unlocked_ids]

    random.shuffle(locked_ids)
    random.shuffle(unlocked_list)

    # Pick up to eggs_collected, giving priority to locked
    selected_ids = []
    # Up to 24 unique
    needed = min(eggs_collected, total_available)
    # Take from locked first
    from_locked = locked_ids[:needed]
    selected_ids.extend(from_locked)
    # Fill remaining from already unlocked
    if len(selected_ids) < needed:
        selected_ids.extend(unlocked_list[:(needed - len(selected_ids))])

    # If player collected MORE than total_available, duplicate randomly
    while len(selected_ids) < eggs_collected:
        selected_ids.append(random.choice(all_indices))

    # Build result
    results = []
    seen_in_run = set()
    for mini_id in selected_ids:
        idx = mini_id - 1
        is_new = (mini_id not in unlocked_ids) and (mini_id not in seen_in_run)
        seen_in_run.add(mini_id)
        results.append({
            "id": mini_id,
            "image": mini_hippos[idx],
            "name": mini_names[idx],
            "is_new": is_new
        })

    return results


def draw_game_over(screen, game_font, player_score, high_score, is_new_record, selected_minis, unlocked_count=0):
    # Background
    screen.fill((208, 245, 244))

    title_f = get_font(36)
    sub_f = get_font(16)
    name_f = get_font(9)
    new_badge_f = get_font(7)
    hint_f = get_font(12)
    btn_f = get_font(12)

    # GAME OVER Title with shadow
    t_shadow = title_f.render("GAME OVER", True, (130, 185, 185))
    screen.blit(t_shadow, t_shadow.get_rect(center=(642, 112)))
    text = title_f.render("GAME OVER", True, (20, 45, 45))
    screen.blit(text, text.get_rect(center=(640, 110)))

    # New Record Banner
    now_ticks = pygame.time.get_ticks()
    if is_new_record and player_score > 0:
        pulse = 0.5 + 0.5 * math.sin(now_ticks * 0.008)
        gold_color = (int(255 - 40 * pulse), int(195 + 40 * pulse), 30)
        rec_text = sub_f.render("★ ¡NUEVO RECORD! ★", True, gold_color)
        screen.blit(rec_text, rec_text.get_rect(center=(640, 155)))
        score_y = 190
    else:
        score_y = 165

    # Scores display
    score_line = f"Puntaje: {int(player_score)}   |   Record: {int(high_score)}"
    score_surf = sub_f.render(score_line, True, (40, 70, 70))
    screen.blit(score_surf, score_surf.get_rect(center=(640, score_y)))

    # Eggs / Mini Hippos
    total = len(selected_minis)

    if total == 0:
        empty_text = hint_f.render("No atrapaste ningún huevo mágico esta vez.", True, (90, 130, 130))
        screen.blit(empty_text, empty_text.get_rect(center=(640, 310)))
        hint_text = hint_f.render("¡Atrápalos para rescatar mini hipos y agregarlos al álbum!", True, (90, 130, 130))
        screen.blit(hint_text, hint_text.get_rect(center=(640, 345)))
    else:
        eggs_header = hint_f.render(f"Rescataste {total} mini hipos esta partida:", True, (35, 75, 75))
        screen.blit(eggs_header, eggs_header.get_rect(center=(640, score_y + 36)))

        max_per_row = 8 if total > 10 else min(total, 6)
        spacing_x = 100
        spacing_y = 90
        base_grid_y = score_y + 100

        for i, item in enumerate(selected_minis):
            mini = item["image"]
            name = item["name"]
            is_new = item.get("is_new", False)

            row = i // max_per_row
            col = i % max_per_row
            items_in_row = min(max_per_row, total - row * max_per_row)
            start_x = 640 - (items_in_row - 1) * spacing_x / 2
            x = start_x + col * spacing_x
            y = base_grid_y + row * spacing_y

            # Gentle bobbing animation
            bob = math.sin(now_ticks * 0.005 + i * 0.4) * 3.0
            cur_y = y + bob

            # Draw mini hippo (scaled to 70x52)
            mini_scaled = pygame.transform.scale(mini, (70, 52))
            screen.blit(mini_scaled, mini_scaled.get_rect(center=(x, cur_y)))

            # If newly unlocked, draw vibrant pulsing badge above head
            if is_new:
                pulse_badge = 0.5 + 0.5 * math.sin(now_ticks * 0.01 + i)
                badge_col = (int(255 - 30 * pulse_badge), int(160 + 50 * pulse_badge), 30)
                badge_surf = new_badge_f.render("¡NUEVO!", True, badge_col)
                screen.blit(badge_surf, badge_surf.get_rect(center=(x, cur_y - 32)))

            # Name tag
            name_text = name_f.render(name, True, (30, 60, 60))
            screen.blit(name_text, name_text.get_rect(center=(x, cur_y + 34)))

    # Collection button
    col_btn_rect = pygame.Rect(450, 580, 380, 44)
    mouse_pos = pygame.mouse.get_pos()
    is_col_hover = col_btn_rect.collidepoint(mouse_pos)
    btn_bg = (113, 205, 205) if is_col_hover else (143, 223, 221)
    pygame.draw.rect(screen, btn_bg, col_btn_rect, border_radius=10)
    pygame.draw.rect(screen, (35, 75, 75), col_btn_rect, width=2, border_radius=10)
    col_btn_text = btn_f.render(f"VER ÁLBUM [C] ({unlocked_count}/24)", True, (35, 75, 75))
    screen.blit(col_btn_text, col_btn_text.get_rect(center=col_btn_rect.center))

    # Restart & Mute prompts at bottom
    pulse_alpha = int(180 + 75 * math.sin(now_ticks * 0.006))
    restart_surf = hint_f.render("Presiona [R] o [ESPACIO] para jugar de nuevo", True, (25, 55, 55))
    restart_surf.set_alpha(pulse_alpha)
    screen.blit(restart_surf, restart_surf.get_rect(center=(640, 650)))

    sub_hint = name_f.render("[M] Mutear sonido", True, (100, 135, 135))
    screen.blit(sub_hint, sub_hint.get_rect(center=(640, 680)))

    return col_btn_rect


def draw_start_screen(screen, title_font, otro_font, start_image, flor1, flor2, high_score=0, unlocked_count=0):
    screen.fill((208, 245, 244))

    # Gentle breathing/floating motion for title image
    now_ticks = pygame.time.get_ticks()
    float_offset = math.sin(now_ticks * 0.004) * 5.0

    # Title shadow & text
    title_text = title_font.render("HIPO RUN", True, (25, 65, 65))
    title_shadow = title_font.render("HIPO RUN", True, (135, 195, 195))
    screen.blit(title_shadow, title_shadow.get_rect(center=(643, 133)))
    screen.blit(title_text, title_text.get_rect(center=(640, 130)))

    # Start character image with gentle float
    img_rect = start_image.get_rect(center=(640, 290 + float_offset))
    screen.blit(start_image, img_rect)

    # Flowers decoration
    screen.blit(flor1, (280, 120))
    screen.blit(flor2, (355, 105))
    screen.blit(flor2, (880, 120))
    screen.blit(flor1, (945, 95))

    # High score banner if exists
    if high_score > 0:
        hs_font = get_font(13)
        hs_surf = hs_font.render(f"★ RECORD: {int(high_score)} ★", True, (190, 130, 20))
        screen.blit(hs_surf, hs_surf.get_rect(center=(640, 420)))

    # Instructions
    inst_font = get_font(12)
    inst1 = inst_font.render("Esquiva las tortugas y murciélagos", True, (35, 75, 75))
    screen.blit(inst1, inst1.get_rect(center=(640, 452)))
    inst2 = inst_font.render("¡Atrapa huevos para coleccionar los 24 mini hipos!", True, (35, 75, 75))
    screen.blit(inst2, inst2.get_rect(center=(640, 478)))

    # Controls guide
    ctrl_font = get_font(10)
    ctrl_text = ctrl_font.render("[ESPACIO / W / ↑] Saltar   [S / ↓] Agacharse   [P] Pausa   [M] Mutear", True, (90, 130, 130))
    screen.blit(ctrl_text, ctrl_text.get_rect(center=(640, 514)))

    mouse_pos = pygame.mouse.get_pos()
    btn_font = get_font(16)

    # Two side-by-side action buttons: [ ¡JUGAR! ] and [ ALBUM (X/24) [C] ]
    play_btn = pygame.Rect(330, 560, 280, 58)
    col_btn = pygame.Rect(640, 560, 310, 58)

    # 1. Play Button
    is_play_hover = play_btn.collidepoint(mouse_pos)
    play_col = (113, 205, 205) if is_play_hover else (143, 223, 221)
    pygame.draw.rect(screen, play_col, play_btn, border_radius=14)
    pygame.draw.rect(screen, (35, 75, 75), play_btn, width=3, border_radius=14)
    play_text = btn_font.render("¡JUGAR!", True, (35, 75, 75))
    screen.blit(play_text, play_text.get_rect(center=play_btn.center))

    # 2. Collection Button
    is_col_hover = col_btn.collidepoint(mouse_pos)
    col_color = (255, 235, 140) if is_col_hover else (255, 245, 180)
    pygame.draw.rect(screen, col_color, col_btn, border_radius=14)
    pygame.draw.rect(screen, (160, 120, 20), col_btn, width=3, border_radius=14)
    col_text = btn_font.render(f"ÁLBUM ({unlocked_count}/24)", True, (130, 95, 15))
    screen.blit(col_text, col_text.get_rect(center=(col_btn.centerx, col_btn.centery - 6)))
    key_hint = get_font(9).render("Presiona [C]", True, (150, 115, 30))
    screen.blit(key_hint, key_hint.get_rect(center=(col_btn.centerx, col_btn.centery + 15)))

    return play_btn, col_btn


def draw_pause_screen(screen):
    # Dark semi-transparent tint
    overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
    overlay.fill((15, 35, 35, 160))
    screen.blit(overlay, (0, 0))

    title_f = get_font(36)
    sub_f = get_font(15)
    hint_f = get_font(11)

    pause_title = title_f.render("PAUSA", True, (240, 255, 255))
    screen.blit(pause_title, pause_title.get_rect(center=(640, 300)))

    resume_text = sub_f.render("Presiona [P] o [ESC] para continuar", True, (200, 240, 240))
    screen.blit(resume_text, resume_text.get_rect(center=(640, 370)))

    mute_text = hint_f.render("[M] Silenciar / Activar sonido", True, (160, 205, 205))
    screen.blit(mute_text, mute_text.get_rect(center=(640, 420)))
