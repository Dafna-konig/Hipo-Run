import math
import random
import pygame


class DustParticle:
    def __init__(self, x, y, vx=None, vy=None, max_life=16):
        self.x = float(x)
        self.y = float(y)
        self.vx = vx if vx is not None else random.uniform(-3.5, -1.0)
        self.vy = vy if vy is not None else random.uniform(-1.2, 0.4)
        self.life = max_life
        self.max_life = max_life
        self.base_size = random.uniform(3.0, 6.0)
        self.color = random.choice([
            (210, 235, 230),
            (190, 220, 215),
            (230, 245, 240)
        ])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.94
        self.vy *= 0.94
        self.life -= 1
        return self.life > 0

    def draw(self, screen):
        progress = self.life / self.max_life
        size = max(1, int(self.base_size * progress))
        alpha = int(210 * progress)
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (size, size), size)
        screen.blit(s, (int(self.x - size), int(self.y - size)))


class SparkleParticle:
    COLORS = [
        (255, 225, 80),   # Bright gold
        (255, 120, 190),  # Bright pink
        (80, 235, 255),   # Cyan
        (255, 255, 255),  # White
        (160, 255, 120),  # Lime
    ]

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2.5, 6.5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(18, 30)
        self.max_life = self.life
        self.size = random.uniform(3.0, 5.5)
        self.color = random.choice(self.COLORS)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08  # slight gravity
        self.vx *= 0.93
        self.vy *= 0.93
        self.life -= 1
        return self.life > 0

    def draw(self, screen):
        progress = self.life / self.max_life
        sz = max(1, int(self.size * progress))
        alpha = int(255 * progress)
        s = pygame.Surface((sz * 4, sz * 4), pygame.SRCALPHA)
        cx, cy = sz * 2, sz * 2
        # Draw little diamond sparkle
        pts = [
            (cx, cy - sz * 1.5),
            (cx + sz * 0.8, cy),
            (cx, cy + sz * 1.5),
            (cx - sz * 0.8, cy)
        ]
        pygame.draw.polygon(s, (*self.color, alpha), pts)
        screen.blit(s, (int(self.x - cx), int(self.y - cy)))


class FloatingText:
    def __init__(self, text, x, y, font, color=(255, 225, 50), max_life=42):
        self.text = text
        self.x = float(x)
        self.y = float(y)
        self.font = font
        self.color = color
        self.vy = -1.8
        self.life = max_life
        self.max_life = max_life

        # Pre-render text with black outline for high contrast
        text_surf = self.font.render(text, True, color)
        outline_surf = self.font.render(text, True, (20, 40, 40))
        w, h = text_surf.get_size()
        self.surf = pygame.Surface((w + 4, h + 4), pygame.SRCALPHA)
        # Outline offsets
        for ox in (-2, 0, 2):
            for oy in (-2, 0, 2):
                if ox != 0 or oy != 0:
                    self.surf.blit(outline_surf, (ox + 2, oy + 2))
        self.surf.blit(text_surf, (2, 2))

    def update(self):
        self.y += self.vy
        self.vy *= 0.96
        self.life -= 1
        return self.life > 0

    def draw(self, screen):
        progress = self.life / self.max_life
        alpha = int(255 * (progress ** 0.8))
        s = self.surf.copy()
        s.set_alpha(alpha)
        screen.blit(s, (int(self.x - s.get_width() / 2), int(self.y - s.get_height() / 2)))


class ImpactShockwave:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.radius = 10.0
        self.max_radius = 65.0
        self.life = 18
        self.max_life = 18

    def update(self):
        progress = 1.0 - (self.life / self.max_life)
        self.radius = 10.0 + (self.max_radius - 10.0) * progress
        self.life -= 1
        return self.life > 0

    def draw(self, screen):
        progress = self.life / self.max_life
        alpha = int(220 * progress)
        width = max(1, int(4 * progress))
        r = int(self.radius)
        s = pygame.Surface((r * 2 + 8, r * 2 + 8), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 80, 80, alpha), (r + 4, r + 4), r, width=width)
        screen.blit(s, (int(self.x - r - 4), int(self.y - r - 4)))


class ParticleManager:
    def __init__(self):
        self.particles = []
        self.floating_texts = []
        self.shockwaves = []
        self.font = None

    def set_font(self, font):
        self.font = font

    def add_run_dust(self, x, y):
        self.particles.append(DustParticle(x, y, vx=random.uniform(-4.0, -1.5), vy=random.uniform(-0.8, 0.4)))

    def add_landing_dust(self, x, y):
        for _ in range(8):
            vx = random.choice([-1, 1]) * random.uniform(2.0, 5.0)
            vy = random.uniform(-1.5, 0.2)
            self.particles.append(DustParticle(x, y, vx=vx, vy=vy, max_life=22))

    def add_egg_sparkles(self, x, y):
        for _ in range(16):
            self.particles.append(SparkleParticle(x, y))

    def add_floating_text(self, text, x, y, color=(255, 225, 50)):
        if self.font:
            self.floating_texts.append(FloatingText(text, x, y, self.font, color=color))

    def add_impact(self, x, y):
        self.shockwaves.append(ImpactShockwave(x, y))
        for _ in range(14):
            self.particles.append(DustParticle(
                x, y,
                vx=random.uniform(-6.0, 6.0),
                vy=random.uniform(-6.0, 2.0),
                max_life=24
            ))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]
        self.floating_texts = [ft for ft in self.floating_texts if ft.update()]
        self.shockwaves = [sw for sw in self.shockwaves if sw.update()]

    def draw(self, screen):
        for p in self.particles:
            p.draw(screen)
        for sw in self.shockwaves:
            sw.draw(screen)
        for ft in self.floating_texts:
            ft.draw(screen)

    def clear(self):
        self.particles.clear()
        self.floating_texts.clear()
        self.shockwaves.clear()
