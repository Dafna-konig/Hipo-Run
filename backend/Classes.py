import math
import random
import pygame


class Hipo(pygame.sprite.Sprite):
    GROUND_BOTTOM = 456  # Visible feet land on ground_y = 418
    _running_sprites = None
    _ducking_sprites = None

    @classmethod
    def load_assets(cls):
        if cls._running_sprites is None:
            cls._running_sprites = [
                pygame.transform.scale(pygame.image.load("Assets/Hipo_1.png").convert_alpha(), (150, 200)),
                pygame.transform.scale(pygame.image.load("Assets/Hipo_2.png").convert_alpha(), (150, 200)),
                pygame.transform.scale(pygame.image.load("Assets/Hipo_1.png").convert_alpha(), (150, 200)),
                pygame.transform.scale(pygame.image.load("Assets/Hipo_3.png").convert_alpha(), (150, 200)),
            ]
            cls._ducking_sprites = [
                pygame.transform.scale(pygame.image.load("Assets/Hipo_duck_1.png").convert_alpha(), (150, 150)),
                pygame.transform.scale(pygame.image.load("Assets/Hipo_duck_2.png").convert_alpha(), (150, 150)),
                pygame.transform.scale(pygame.image.load("Assets/Hipo_duck_1.png").convert_alpha(), (150, 150)),
                pygame.transform.scale(pygame.image.load("Assets/Hipo_duck_3.png").convert_alpha(), (150, 150)),
            ]

    def __init__(self, x=120, y=356):
        super().__init__()
        Hipo.load_assets()
        self.running_sprites = Hipo._running_sprites
        self.ducking_sprites = Hipo._ducking_sprites

        self.current_image = 0.0
        self.image = self.running_sprites[0]
        self.rect = self.image.get_rect(center=(x, y))
        self.rect.bottom = self.GROUND_BOTTOM

        # Physics
        self.gravity = 0.5
        self.jump_speed = -14.0
        self.velocity_y = 0.0
        self.is_jumping = False
        self.ducking = False

        # Input buffering & game feel
        self.jump_buffer = 0  # Frames to remember jump press before landing
        self.just_landed = False

    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_speed
            self.is_jumping = True
            self.jump_buffer = 0
            return True
        else:
            # Buffer the jump press if close to the ground
            self.jump_buffer = 10
            return False

    def cut_jump(self):
        """Variable jump height: releasing jump cuts upward velocity."""
        if self.is_jumping and self.velocity_y < -4.0:
            self.velocity_y *= 0.5

    def set_ducking(self, ducking):
        if self.ducking == ducking:
            return
        bottom = self.rect.bottom
        centerx = self.rect.centerx
        self.ducking = ducking

        if self.ducking:
            self.image = self.ducking_sprites[0]
        else:
            self.image = self.running_sprites[0]

        self.rect = self.image.get_rect(midbottom=(centerx, bottom))

    def update(self):
        self.just_landed = False

        # Decrement jump buffer
        if self.jump_buffer > 0:
            self.jump_buffer -= 1

        # Fast fall if holding duck while in the air
        effective_gravity = self.gravity * 1.8 if (self.is_jumping and self.ducking) else self.gravity

        # Jumping physics
        if self.is_jumping:
            self.velocity_y += effective_gravity
            self.rect.y += round(self.velocity_y)

            # Ground collision check
            if self.rect.bottom >= self.GROUND_BOTTOM:
                self.rect.bottom = self.GROUND_BOTTOM
                self.velocity_y = 0.0
                self.is_jumping = False
                self.just_landed = True

                # Consume buffered jump immediately upon landing
                if self.jump_buffer > 0:
                    self.jump()

        self.animate()

    def animate(self):
        midbottom = self.rect.midbottom
        if self.is_jumping:
            self.image = self.running_sprites[0]
        elif self.ducking:
            self.current_image += 0.12
            if self.current_image >= len(self.ducking_sprites):
                self.current_image = 0.0
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.current_image += 0.12
            if self.current_image >= len(self.running_sprites):
                self.current_image = 0.0
            self.image = self.running_sprites[int(self.current_image)]
        self.rect = self.image.get_rect(midbottom=midbottom)

    def get_hitbox(self):
        if self.ducking:
            box = self.rect.inflate(-65, -70)
            box.bottom = self.rect.bottom - 8
        else:
            box = self.rect.inflate(-75, -80)
            box.bottom = self.rect.bottom - 10
        return box

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Tortuga(pygame.sprite.Sprite):
    _sprites = None

    @classmethod
    def load_assets(cls):
        if cls._sprites is None:
            cls._sprites = [
                pygame.transform.scale(pygame.image.load(f"Assets/Tortuga_{i}.png").convert_alpha(), (150, 90))
                for i in range(1, 7)
            ]

    def __init__(self, x=1330, y=397):
        # Height 90, center 397 -> bottom 442 (walks exactly on ground_y = 442)
        super().__init__()
        Tortuga.load_assets()
        self.image = random.choice(Tortuga._sprites)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, game_speed):
        self.speed = 2.0 + game_speed
        self.rect.x -= int(self.speed)
        if self.rect.right < -50:
            self.kill()

    def get_hitbox(self):
        box = self.rect.inflate(-50, -25)
        box.bottom = self.rect.bottom - 4
        return box


class Bat(pygame.sprite.Sprite):
    _sprites = None

    @classmethod
    def load_assets(cls):
        if cls._sprites is None:
            cls._sprites = [
                pygame.transform.scale(pygame.image.load(f"Assets/{filename}").convert_alpha(), (120, 105))
                for filename in ["Bat_1.png", "Bat_2.png"]
            ]

    def __init__(self):
        super().__init__()
        Bat.load_assets()
        self.sprites = Bat._sprites
        self.current_image = 0.0
        self.animation_speed = 0.12
        self.speed = 3.0

        y = random.choice([310, 211])
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(1300, y))

    def update(self, game_speed):
        self.rect.x -= int(self.speed + game_speed)
        self.animate()
        if self.rect.right < -50:
            self.kill()

    def animate(self):
        self.current_image += self.animation_speed
        if self.current_image >= len(self.sprites):
            self.current_image = 0.0
        self.image = self.sprites[int(self.current_image)]

    def get_hitbox(self):
        return self.rect.inflate(-35, -30)


class Huevo(pygame.sprite.Sprite):
    _sprites = None

    @classmethod
    def load_assets(cls):
        if cls._sprites is None:
            cls._sprites = {
                1: [
                    pygame.transform.scale(pygame.image.load(f"Assets/Huevo_1{l}.png").convert_alpha(), (110, 80))
                    for l in ["a", "b"]
                ],
                2: [
                    pygame.transform.scale(pygame.image.load(f"Assets/Huevo_2{l}.png").convert_alpha(), (110, 80))
                    for l in ["a", "b"]
                ]
            }

    def __init__(self, x=1330, y=397):
        # Height 80, center 397 -> visible bottom lands on ground_y = 418
        super().__init__()
        Huevo.load_assets()
        self.color = random.choice([1, 2])
        self.sprites = Huevo._sprites[self.color]
        self.current_image = 0.0
        self.animation_speed = 0.1
        self.image = self.sprites[0]
        self.base_y = float(y)
        self.spawn_tick = pygame.time.get_ticks()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, game_speed):
        self.rect.x -= int(game_speed)
        # Gentle floating oscillation
        elapsed = (pygame.time.get_ticks() - self.spawn_tick) * 0.005
        self.rect.centery = int(self.base_y + math.sin(elapsed) * 4.0)

        self.animate()
        if self.rect.right < -50:
            self.kill()

    def animate(self):
        self.current_image += self.animation_speed
        if self.current_image >= len(self.sprites):
            self.current_image = 0.0
        self.image = self.sprites[int(self.current_image)]
