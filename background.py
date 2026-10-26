import math
import random
import pygame


class Cloud:
    def __init__(self, x=None):
        self.scale = random.uniform(0.7, 1.4)
        w = int(140 * self.scale)
        h = int(55 * self.scale)
        self.surf = pygame.Surface((w, h), pygame.SRCALPHA)
        color = (255, 255, 255, random.randint(180, 220))
        # Overlapping rounded puffs
        pygame.draw.circle(self.surf, color, (int(w * 0.28), int(h * 0.55)), int(h * 0.35))
        pygame.draw.circle(self.surf, color, (int(w * 0.50), int(h * 0.42)), int(h * 0.44))
        pygame.draw.circle(self.surf, color, (int(w * 0.72), int(h * 0.55)), int(h * 0.35))
        pygame.draw.rect(
            self.surf,
            color,
            (int(w * 0.18), int(h * 0.48), int(w * 0.64), int(h * 0.38)),
            border_radius=int(h * 0.18)
        )

        self.x = float(x if x is not None else random.randint(0, 1280))
        self.y = float(random.randint(40, 180))
        self.drift_speed = random.uniform(0.35, 0.85)

    def update(self, game_speed):
        self.x -= self.drift_speed + game_speed * 0.05
        if self.x < -self.surf.get_width():
            self.x = 1280 + random.randint(20, 150)
            self.y = float(random.randint(40, 180))

    def draw(self, screen):
        screen.blit(self.surf, (int(self.x), int(self.y)))


class GroundDash:
    """Subtle speed dashes underneath the ground line to show forward motion."""
    def __init__(self, x, span_w):
        self.x = float(x)
        self.span_w = span_w
        self._randomize()

    def _randomize(self):
        self.offset_y = random.randint(12, 60)
        self.length = random.randint(6, 16)
        self.color = random.choice([
            (168, 224, 208),
            (180, 232, 218),
            (155, 216, 200)
        ])

    def update(self, speed):
        self.x -= speed
        if self.x < -30:
            self.x += self.span_w
            self._randomize()

    def draw(self, screen, ground_y):
        y = ground_y + self.offset_y
        pygame.draw.line(screen, self.color, (int(self.x), y), (int(self.x + self.length), y), 2)


class BackgroundManager:
    """
    Manages clean two-tone background with a clear ground separating line.
    No grass blades/briznas. Entities (Hipo & Tortuga) are aligned at ground_y = 442.
    """

    def __init__(self, screen_width=1280, screen_height=720):
        self.width = screen_width
        self.height = screen_height
        self.ground_y = 418  # Exact baseline matching Tortuga & Hipo visible feet

        # 1. Sky gradient (renders above ground line)
        self.sky_surf = pygame.Surface((self.width, self.ground_y))
        top_color = (175, 226, 242)
        bottom_color = (218, 248, 246)
        for y in range(self.ground_y):
            ratio = y / float(self.ground_y)
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            pygame.draw.line(self.sky_surf, (r, g, b), (0, y), (self.width, y))

        # 2. Clouds
        self.clouds = [
            Cloud(x=random.randint(0, 1280)) for _ in range(5)
        ]

        # 3. Seamless distant hills (meet cleanly at ground line)
        self.hills_w = 1600
        self.hills_h = 130
        self.hills_surf = pygame.Surface((self.hills_w, self.hills_h), pygame.SRCALPHA)
        pts = [(0, self.hills_h)]
        for x in range(self.hills_w + 1):
            y_curve = 55 + 24 * math.sin(2 * math.pi * x / 800.0) + 12 * math.sin(2 * math.pi * x / 400.0)
            pts.append((x, int(y_curve)))
        pts.append((self.hills_w, self.hills_h))
        pygame.draw.polygon(self.hills_surf, (168, 224, 214), pts)
        self.hills_x = 0.0

        # 4. Ground dashes for smooth speed sensation
        self.ground_span = 1400
        self.dashes = [
            GroundDash(random.randint(0, self.ground_span), self.ground_span)
            for _ in range(30)
        ]

        # 5. Ground color palette
        self.ground_color = (148, 210, 192)      # Soft pastel meadow sage
        self.line_color = (92, 170, 150)          # Clean dividing line
        self.line_highlight = (185, 235, 222)     # 1px top highlight

    def update(self, game_speed):
        # Update clouds
        for c in self.clouds:
            c.update(game_speed)

        # Update distant hills (speed * 0.18)
        self.hills_x -= game_speed * 0.18
        if self.hills_x <= -self.hills_w:
            self.hills_x += self.hills_w

        # Update ground dashes
        for dash in self.dashes:
            dash.update(game_speed)

    def draw_sky_and_distance(self, screen):
        # 1. Sky above ground
        screen.blit(self.sky_surf, (0, 0))

        # 2. Clouds
        for c in self.clouds:
            c.draw(screen)

        # 3. Distant hills (sit right behind ground line)
        hills_y = self.ground_y - 127
        screen.blit(self.hills_surf, (int(self.hills_x), hills_y))
        screen.blit(self.hills_surf, (int(self.hills_x + self.hills_w), hills_y))

    def draw_foreground(self, screen):
        # 4. Solid ground area from ground_y downwards
        pygame.draw.rect(
            screen,
            self.ground_color,
            (0, self.ground_y, self.width, self.height - self.ground_y)
        )

        # 5. Speed dashes underneath the ground line
        for dash in self.dashes:
            dash.draw(screen, self.ground_y)

        # 6. Clean, crisp dividing ground line
        pygame.draw.line(screen, self.line_color, (0, self.ground_y), (self.width, self.ground_y), 3)
        pygame.draw.line(screen, self.line_highlight, (0, self.ground_y - 1), (self.width, self.ground_y - 1), 1)

    def reset(self):
        self.hills_x = 0.0
        for dash in self.dashes:
            dash.x = random.randint(0, self.ground_span)
            dash._randomize()
