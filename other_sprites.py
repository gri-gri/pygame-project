import pygame
from helping_functions import load_image

TILE_WIDTH = TILE_HEIGHT = 50
    
class Tile(pygame.sprite.Sprite):
    
    def __init__(self, pos, image_filename, color_key, *groups):
        super().__init__(*groups)
        self.image = load_image(image_filename, color_key=color_key)
        self.rect = self.image.get_rect().move(TILE_WIDTH*pos[0], TILE_HEIGHT*pos[1])
        self.mask = pygame.mask.from_surface(self.image)


class Platform(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'platform.png', -2, *groups)