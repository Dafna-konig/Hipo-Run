import math
import pygame

_fonts = {}
_cached_silhouettes = None
_cached_colored = None


def get_font(size):
    if size not in _fonts:
        _fonts[size] = pygame.font.Font("Assets/PressStart2P-Regular.ttf", size)
    return _fonts[size]


def _init_caches(mini_hippos):
    global _cached_silhouettes, _cached_colored
    if _cached_silhouettes is None:
        _cached_silhouettes = []
        _cached_colored = []
        for img in mini_hippos:
            scaled = pygame.transform.scale(img, (64, 48))
            _cached_colored.append(scaled)
            mask = pygame.mask.from_surface(scaled)
            sil = mask.to_surface(setcolor=(60, 105, 105, 170), unsetcolor=(0, 0, 0, 0))
            _cached_silhouettes.append(sil)


def draw_collection_screen(screen, unlocked_ids, mini_hippos, mini_names):
    _init_caches(mini_hippos)
    screen.fill((208, 245, 244))

    title_f = get_font(26)
    sub_f = get_font(13)
    card_f = get_font(9)
    num_f = get_font(8)
    btn_f = get_font(14)
    hint_f = get_font(10)

    now_ticks = pygame.time.get_ticks()
    unlocked_count = len(unlocked_ids)
    total_count = len(mini_hippos)

    # 1. Header Title
    title_shadow = title_f.render("ALBUM DE MINI HIPOS", True, (135, 195, 195))
    screen.blit(title_shadow, title_shadow.get_rect(center=(642, 42)))
    title_text = title_f.render("ALBUM DE MINI HIPOS", True, (25, 65, 65))
    screen.blit(title_text, title_text.get_rect(center=(640, 40)))

    # 2. Progress text & bar
    pct = int((unlocked_count / total_count) * 100)
    prog_line = f"Coleccion: {unlocked_count} / {total_count} ({pct}%)"
    prog_text = sub_f.render(prog_line, True, (40, 80, 80))
    screen.blit(prog_text, prog_text.get_rect(center=(640, 75)))

    # Progress bar
    bar_w = 320
    bar_h = 12
    bar_x = 640 - bar_w // 2
    bar_y = 92
    pygame.draw.rect(screen, (165, 215, 210), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
    fill_w = int(bar_w * (unlocked_count / total_count))
    if fill_w > 0:
        bar_color = (255, 215, 60) if unlocked_count == total_count else (65, 185, 165)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_w, bar_h), border_radius=6)
    pygame.draw.rect(screen, (35, 75, 75), (bar_x, bar_y, bar_w, bar_h), width=2, border_radius=6)

    # 3. All 24 Cards in 6 cols x 4 rows
    total_cols = 6
    spacing_x = 180
    spacing_y = 110
    base_x = 190
    base_y = 175

    for i in range(total_count):
        mini_id = i + 1  # 1-based index
        col = i % total_cols
        row = i // total_cols
        cx = base_x + col * spacing_x
        cy = base_y + row * spacing_y

        is_unlocked = mini_id in unlocked_ids
        card_rect = pygame.Rect(cx - 80, cy - 48, 160, 96)

        # Card Background
        if is_unlocked:
            card_bg = (235, 252, 250)
            border_color = (75, 175, 165)
            border_w = 2
        else:
            card_bg = (175, 220, 215)
            border_color = (130, 180, 175)
            border_w = 1

        pygame.draw.rect(screen, card_bg, card_rect, border_radius=10)
        pygame.draw.rect(screen, border_color, card_rect, width=border_w, border_radius=10)

        # Slot ID Badge top-left
        id_surf = num_f.render(f"#{mini_id:02d}", True, (100, 145, 140))
        screen.blit(id_surf, (card_rect.left + 8, card_rect.top + 6))

        # Mini Hippo image
        if is_unlocked:
            bob = math.sin(now_ticks * 0.005 + i * 0.5) * 2.5
            img = _cached_colored[i]
            img_rect = img.get_rect(center=(cx, cy - 6 + bob))
            screen.blit(img, img_rect)

            # Name tag
            name_text = mini_names[i]
            name_surf = card_f.render(name_text, True, (25, 60, 60))
            screen.blit(name_surf, name_surf.get_rect(center=(cx, cy + 32)))
        else:
            # Silhouette
            sil = _cached_silhouettes[i]
            sil_rect = sil.get_rect(center=(cx, cy - 6))
            screen.blit(sil, sil_rect)

            # Mystery name tag
            lock_surf = card_f.render("???", True, (110, 150, 145))
            screen.blit(lock_surf, lock_surf.get_rect(center=(cx, cy + 32)))

    # 4. Return Button at bottom
    btn_rect = pygame.Rect(490, 620, 300, 48)
    mouse_pos = pygame.mouse.get_pos()
    is_hover = btn_rect.collidepoint(mouse_pos)

    btn_color = (113, 205, 205) if is_hover else (143, 223, 221)
    pygame.draw.rect(screen, btn_color, btn_rect, border_radius=12)
    pygame.draw.rect(screen, (35, 75, 75), btn_rect, width=3, border_radius=12)

    btn_surf = btn_f.render("VOLVER", True, (35, 75, 75))
    screen.blit(btn_surf, btn_surf.get_rect(center=btn_rect.center))

    # Helper text
    hint_surf = hint_f.render("[ESC / C / ESPACIO] o Clic para volver", True, (90, 135, 135))
    screen.blit(hint_surf, hint_surf.get_rect(center=(640, 685)))

    return btn_rect
