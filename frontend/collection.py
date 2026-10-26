import math
import pygame

_fonts = {}
_cached_silhouettes = None
_cached_colored = None
_current_page = 0


def get_font(size):
    if size not in _fonts:
        _fonts[size] = pygame.font.Font("Assets/PressStart2P-Regular.ttf", size)
    return _fonts[size]


def get_current_page():
    return _current_page


def set_current_page(p):
    global _current_page
    _current_page = max(0, min(1, int(p)))


def next_page():
    global _current_page
    _current_page = 1 if _current_page == 0 else 0


def prev_page():
    global _current_page
    _current_page = 0 if _current_page == 1 else 1


def _init_caches(mini_hippos):
    global _cached_silhouettes, _cached_colored
    if _cached_silhouettes is None or len(_cached_colored) != len(mini_hippos):
        _cached_silhouettes = []
        _cached_colored = []
        for img in mini_hippos:
            scaled = pygame.transform.scale(img, (64, 48))
            _cached_colored.append(scaled)
            mask = pygame.mask.from_surface(scaled)
            sil = mask.to_surface(setcolor=(60, 105, 105, 170), unsetcolor=(0, 0, 0, 0))
            _cached_silhouettes.append(sil)


def draw_collection_screen(screen, unlocked_ids, mini_hippos, mini_names, page=None):
    global _current_page
    if page is not None:
        set_current_page(page)

    _init_caches(mini_hippos)
    screen.fill((208, 245, 244))

    title_f = get_font(26)
    sub_f = get_font(13)
    card_f = get_font(9)
    num_f = get_font(8)
    tab_f = get_font(10)
    btn_f = get_font(14)
    hint_f = get_font(10)

    now_ticks = pygame.time.get_ticks()
    unlocked_count = len(unlocked_ids)
    total_count = len(mini_hippos)
    items_per_page = 24

    # 1. Header Title
    title_shadow = title_f.render("Álbum de mini hipos", True, (135, 195, 195))
    screen.blit(title_shadow, title_shadow.get_rect(center=(642, 38)))
    title_text = title_f.render("Álbum de mini hipos", True, (25, 65, 65))
    screen.blit(title_text, title_text.get_rect(center=(640, 36)))

    # 2. Progress text & bar
    pct = int((unlocked_count / total_count) * 100) if total_count > 0 else 0
    prog_line = f"Colección: {unlocked_count} / {total_count} ({pct}%)"
    prog_text = sub_f.render(prog_line, True, (40, 80, 80))
    screen.blit(prog_text, prog_text.get_rect(center=(640, 68)))

    # Progress bar
    bar_w = 340
    bar_h = 12
    bar_x = 640 - bar_w // 2
    bar_y = 84
    pygame.draw.rect(screen, (165, 215, 210), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
    fill_w = int(bar_w * (unlocked_count / total_count)) if total_count > 0 else 0
    if fill_w > 0:
        bar_color = (255, 215, 60) if unlocked_count == total_count else (65, 185, 165)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_w, bar_h), border_radius=6)
    pygame.draw.rect(screen, (35, 75, 75), (bar_x, bar_y, bar_w, bar_h), width=2, border_radius=6)

    # 3. 24 Cards for the current page (6 cols x 4 rows)
    start_idx = _current_page * items_per_page

    total_cols = 6
    spacing_x = 180
    spacing_y = 98
    base_x = 190
    base_y = 158

    for slot in range(items_per_page):
        i = start_idx + slot
        if i >= total_count:
            break

        mini_id = i + 1  # 1-based index (1 to 48)
        col = slot % total_cols
        row = slot // total_cols
        cx = base_x + col * spacing_x
        cy = base_y + row * spacing_y

        is_unlocked = mini_id in unlocked_ids
        card_rect = pygame.Rect(cx - 80, cy - 44, 160, 88)

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
        screen.blit(id_surf, (card_rect.left + 8, card_rect.top + 5))

        # Mini Hippo image
        if is_unlocked:
            #bob = math.sin(now_ticks * 0.005 + slot * 0.5) * 2.5
            img = _cached_colored[i]
            #img_rect = img.get_rect(center=(cx, cy - 6 + bob))
            img_rect = img.get_rect(center=(cx, cy - 6))
            screen.blit(img, img_rect)

            # Name tag
            name_text = mini_names[i] if i < len(mini_names) else f"Hipo #{mini_id}"
            name_surf = card_f.render(name_text, True, (25, 60, 60))
            screen.blit(name_surf, name_surf.get_rect(center=(cx, cy + 30)))
        else:
            # Silhouette
            sil = _cached_silhouettes[i]
            sil_rect = sil.get_rect(center=(cx, cy - 6))
            screen.blit(sil, sil_rect)

            # Mystery name tag
            lock_surf = card_f.render("???", True, (110, 150, 145))
            screen.blit(lock_surf, lock_surf.get_rect(center=(cx, cy + 30)))

    # 4. Pagination Bar (Tabs & Arrows)
    mouse_pos = pygame.mouse.get_pos()

    # Page 1 Tab: #01 - #24
    p1_active = (_current_page == 0)
    p1_rect = pygame.Rect(370, 552, 250, 38)
    p1_hover = p1_rect.collidepoint(mouse_pos)
    if p1_active:
        p1_bg = (113, 205, 205) if p1_hover else (143, 223, 221)
        p1_border = (113, 205, 205)
        p1_txt_col = (35, 75, 75)
    else:
        p1_bg = (130, 210, 205) if p1_hover else (160, 220, 215)
        p1_border = (85, 155, 150)
        p1_txt_col = (45, 95, 90)
    pygame.draw.rect(screen, p1_bg, p1_rect, border_radius=8)
    pygame.draw.rect(screen, p1_border, p1_rect, width=2, border_radius=8)
    p1_txt = tab_f.render("Página 1", True, p1_txt_col)
    screen.blit(p1_txt, p1_txt.get_rect(center=p1_rect.center))

    # Page 2 Tab: #25 - #48
    p2_active = (_current_page == 1)
    p2_rect = pygame.Rect(640, 552, 250, 38)
    p2_hover = p2_rect.collidepoint(mouse_pos)
    if p2_active:
        p2_bg = (113, 205, 205) if p2_hover else (143, 223, 221)
        p2_border = (113, 205, 205)
        p2_txt_col = (35, 75, 75)
    else:
        p2_bg = (130, 210, 205) if p2_hover else (160, 220, 215)
        p2_border = (85, 155, 150)
        p2_txt_col = (45, 95, 90)
    pygame.draw.rect(screen, p2_bg, p2_rect, border_radius=8)
    pygame.draw.rect(screen, p2_border, p2_rect, width=2, border_radius=8)
    p2_txt = tab_f.render("Página 2", True, p2_txt_col)
    screen.blit(p2_txt, p2_txt.get_rect(center=p2_rect.center))

    # 5. Return Button at bottom
    btn_rect = pygame.Rect(500, 615, 280, 46)
    is_hover = btn_rect.collidepoint(mouse_pos)
    btn_color = (113, 205, 205) if is_hover else (143, 223, 221)
    pygame.draw.rect(screen, btn_color, btn_rect, border_radius=12)
    pygame.draw.rect(screen, (35, 75, 75), btn_rect, width=3, border_radius=12)
    btn_surf = btn_f.render("Volver", True, (35, 75, 75))
    screen.blit(btn_surf, btn_surf.get_rect(center=btn_rect.center))

    # 6. Helper text
    hint_surf = hint_f.render("[← / →] Cambiar página   |   [ESC / C / ESPACIO] Volver", True, (90, 135, 135))
    screen.blit(hint_surf, hint_surf.get_rect(center=(640, 685)))

    return {
        "back": btn_rect,
        "page1": p1_rect,
        "page2": p2_rect,
    }
