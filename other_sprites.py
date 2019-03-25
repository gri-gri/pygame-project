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
        
class Fire(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'fire.png', -2, *groups) 


class Snail(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'snail.png', -1, *groups)
        self.speed_x = 1
        self.speed_y = 0
        self.S_x, self.S_y = 0, 0
        self.word = False
    
    def move(self):
        if self.word:
            self.rect.x += self.speed_x
            self.S_x += 1
        else:
            self.rect.x -= self.speed_x
            self.S_x -= 1
            
        self.rect.y += self.speed_y
        self.S_y += self.speed_y
        
        if self.S_x <= -400:
            self.word = True            
            self.S_x = 0
            self.change_direction()
            
        elif self.S_x >= 400:
            self.word = False
            self.S_x = 0        
            self.change_direction()
            
    def change_direction(self):
        self.image = pygame.transform.flip(self.image, True, False)     
    
    def bullet_touch(self):
        super().kill()

class Bullet(pygame.sprite.Sprite):	
    GRAVITY = 0.5	

    def __init__(self, pos, coef, *groups):	
        super().__init__(*groups)	
        self.image = pygame.transform.scale(load_image('bullet.png', color_key=-2), (10, 10))	
        self.rect = self.image.get_rect().move(pos[0], pos[1])	
        self.mask = pygame.mask.from_surface(self.image)	
        self.x_velocity = 10 * coef	

    def update(self, enemies_group, platform_group):	
        self.rect.move_ip(self.x_velocity, Bullet.GRAVITY)	
        flag = False	
        for enemy in enemies_group:	
            if pygame.sprite.collide_mask(self, enemy):	
                enemy.bullet_touch()	
                flag = True	
        if flag or pygame.sprite.spritecollideany(self,	
                                                  platform_group,	
                                                  collided=pygame.sprite.collide_mask):	
            super().kill()