import pygame
import random

# CLASE HIPO

class Hipo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []
        self.x = x
        self.y = y

        self.running_sprites.append(pygame.transform.scale(pygame.image.load("Assets/Hipo_1.png"), (150, 200)))
        self.running_sprites.append(pygame.transform.scale(pygame.image.load("Assets/Hipo_2.png"), (150, 200)))
        self.running_sprites.append(pygame.transform.scale(pygame.image.load("Assets/Hipo_1.png"), (150, 200)))
        self.running_sprites.append(pygame.transform.scale(pygame.image.load("Assets/Hipo_3.png"), (150, 200)))


        self.ducking_sprites.append(pygame.transform.scale(pygame.image.load("Assets/Hipo_Duck_1.png"), (150, 150)))
        self.ducking_sprites.append(pygame.transform.scale(pygame.image.load("Assets/Hipo_Duck_2.png"), (150, 150)))
        self.ducking_sprites.append(pygame.transform.scale(pygame.image.load("Assets/Hipo_Duck_1.png"), (150, 150)))
        self.ducking_sprites.append(pygame.transform.scale(pygame.image.load("Assets/Hipo_Duck_3.png"), (150, 150)))

        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.velocity = 40
        self.gravity = 0.5
        self.jump_speed = -14
        self.velocity_y = 0
        self.is_jumping = False
        self.ducking = False


    def jump(self):
        if not self.is_jumping:
            self.velocity_y = self.jump_speed
            self.is_jumping = True

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

        self.rect = self.image.get_rect(
            midbottom=(centerx, bottom))
        self.x = self.rect.centerx
        self.y = self.rect.centery


    def update(self):
        # Actualizar el salto
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.rect.y += round(self.velocity_y)

            # Comprobar si Hipo tocó el suelo
            if self.rect.bottom >= 460:
                self.rect.bottom = 460
                self.velocity_y = 0
                self.is_jumping = False
        self.animate()

    def animate(self):
        if self.is_jumping:
            self.image = self.running_sprites[0]  # Imagen de salto
       
        elif self.ducking:
            self.current_image += 0.1
            if self.current_image >= len(self.ducking_sprites):
                self.current_image = 0
            self.image = self.ducking_sprites[int(self.current_image)]
       
        else:
            self.current_image += 0.1  # Cambia la velocidad de animación
            if self.current_image >= len(self.running_sprites):
                self.current_image = 0
            self.image = self.running_sprites[int(self.current_image)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)




class Tortuga(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprites = []

        for i in range(1, 7):
            image = pygame.image.load(f"Assets/Tortuga_{i}.png").convert_alpha()
            image = pygame.transform.scale(image, (150, 90))
            self.sprites.append(image)

        # Elegir una variante aleatoria
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, game_speed):
        self.speed = 2 + game_speed 
        # Mover la tortuga hacia la izquierda
        self.rect.x -= self.speed
        # Eliminarla cuando salga de la pantalla
        if self.rect.right < 0:
            self.kill()
        


class Bat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []

        for filename in ["Bat_1.png", "Bat_2.png"]:
            image = pygame.image.load(f"Assets/{filename}").convert_alpha()
            image = pygame.transform.scale(image, (120, 105))
            self.sprites.append(image)

        self.current_image = 0
        self.animation_speed = 0.1
        self.speed = 3

        y = random.choice([310, 211])
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(1300, y))

    def update(self, game_speed):
        # Mover y animar el murciélago
        self.rect.x -= self.speed + game_speed
        self.animate()
        # Eliminarlo al salir de la pantalla
        if self.rect.right < 0:
            self.kill()

    def animate(self):
        self.current_image += self.animation_speed
        if self.current_image >= len(self.sprites):
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]



class Huevo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Elegir aleatoriamente uno de los dos colores
        color = random.choice([1, 2])
        self.sprites = []
        for letra in ["a", "b"]:
            filename = f"Assets/Huevo_{color}{letra}.png"
            image = pygame.image.load(filename).convert_alpha()
            image = pygame.transform.scale(image, (150, 90))
            self.sprites.append(image)

        self.current_image = 0
        self.animation_speed = 0.1
        self.speed = 3
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, game_speed):
        self.rect.x -= game_speed
        # Animar el huevo
        self.animate()
        # Eliminarlo cuando salga de la pantalla
        if self.rect.right < 0:
            self.kill()

    def animate(self):
        self.current_image += self.animation_speed
        if self.current_image >= len(self.sprites):
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]
