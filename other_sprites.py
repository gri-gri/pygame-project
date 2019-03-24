import pygame
from helping_functions import load_image

TILE_WIDTH = TILE_HEIGHT = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image_filename, color_key, *groups):
        super().__init__(*groups)
        self.image = load_image(image_filename, color_key=color_key)
        self.rect = self.image.get_rect().move(TILE_WIDTH*pos[0], TILE_HEIGHT*pos[1])
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, pos):
        self.rect.topleft = (TILE_WIDTH * pos[0], TILE_HEIGHT * pos[1])

    def kill(self):
        super().kill()

    def add(self, *groups):
        super().add(*groups)

    def groups(self):
        return super().groups()

class Platform(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'platform.png', -2, *groups)


class Stairs(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'stairs.png', -2, *groups)
    
class Fire(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'fire.png', -2, *groups)
