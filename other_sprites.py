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

class Checkpoint_Tile(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, 'flag.png', -2, *groups)
        self.pos = pos
        self.image =  pygame.transform.scale(load_image('flag.png', color_key=-1), (46, 200))
        self.name = 'not_checked'
        
    def collided(self, ifcollided):
        if ifcollided:
            self.image = pygame.transform.scale(load_image('flag_appear.png', color_key=-1), (80, 300))
            self.name = 'checked'
            self.rect.y -= 100
            self.rect.x -= 30

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, image_filename, color_key, group):
        super().__init__(group)
        self.image_name = image_filename
        self.image = load_image(self.image_name, color_key=color_key)
        self.rect = self.image.get_rect().move(TILE_WIDTH*pos[0], TILE_HEIGHT*pos[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.damaged = False
        self.damaged_time = 0
        self.health = 0
        self.speed_x = 0
        self.speed_y = 0
        self.S_x, self.S_y = 0, 0
        self.word = False        
    
    def move(self):
        pass
    
    def react(self, filename):
        if self.damaged:
            self.damaged_time += 1
            if self.damaged_time > 15:
                self.image = load_image(filename, -1)
                self.damaged_time = 0
                self.damaged = False
                
    def change_direction(self):
        self.image = pygame.transform.flip(self.image, True, False)     
    
    def bullet_touch(self, damage):
        pass
        ''''''    
        

class Snail(Enemy):
    def __init__(self, pos, group):
        super().__init__(pos, 'snail.png', -1, group)
        self.health = 2
        self.speed_x = 1      
    
    def move(self):
        self.react(self.image_name)
        if self.word:
            self.rect.x += self.speed_x
            self.S_x += 1
        else:
            self.rect.x -= self.speed_x
            self.S_x -= 1
        
        if self.S_x <= -400:
            self.word = True            
            self.S_x = 0
            self.change_direction()
            
        elif self.S_x >= 400:
            self.word = False
            self.S_x = 0        
            self.change_direction()
            
    def bullet_touch(self, damage):
        if self.health != 1:
            print(self.health, damage)
            self.health -= damage
            self.damaged = True
            self.image = load_image('snail_damaged.png', -1)
        else:
            super().kill()        
        

class Robot(Enemy):
    def __init__(self, pos, group):
        super().__init__(pos, 'robot.png', -1, group)
        self.image_name = 'robot.png'
        self.image = load_image(self.image_name, color_key=-1)
        print(self.image)
        self.rect = self.image.get_rect().move(TILE_WIDTH*pos[0], TILE_HEIGHT*pos[1])
        self.mask = pygame.mask.from_surface(self.image)        
        self.speed_y = 7
        
    def react(self):
        self.damaged_time += 1
        if self.damaged_time > 15:            
            super().kill() 
            
    def move(self):
        if self.damaged:
            self.react()
        if not self.damaged:
            if self.word:
                self.rect.y += self.speed_y
                self.S_y += 1
            else:
                self.rect.y -= self.speed_y
                self.S_y -= 1
            
            if self.S_y <= -50:
                self.word = True            
                self.S_y = 0
                
            elif self.S_y >= 50:
                self.word = False
                self.S_y = 0        
            
    def bullet_touch(self, damage):
        self.damaged = True
        self.image = load_image('robot_damaged.png', -1)
        
        
class Bullet_for_enemy(pygame.sprite.Sprite):	
    GRAVITY = 0.5	
    def __init__(self, pos, coef, *groups):
        self.flag_to_diff = 'enemy'
        super().__init__(*groups)	
        self.image = pygame.transform.scale(load_image('bullet.png', color_key=-2), (10, 10))	
        self.rect = self.image.get_rect().move(pos[0], pos[1])	
        self.mask = pygame.mask.from_surface(self.image)	
        self.x_velocity = 10 * coef
        self.damage = 1

    def update(self, enemies_group, platform_group, width):	
        self.rect.move_ip(self.x_velocity, Bullet_for_enemy.GRAVITY)	
        flag = False	
        for enemy in enemies_group:	
            if pygame.sprite.collide_mask(self, enemy):	
                enemy.bullet_touch(self.damage)	
                flag = True	
        if flag or pygame.sprite.spritecollideany(self,	
                                                  platform_group,	
                                                  collided=pygame.sprite.collide_mask):
            super().kill()
        '''elif self.rect.x <= 0 or self.rect.x + self.rect.w >= width:	
            super().kill()'''
    
    
    class Maslina_for_player(pygame.sprite.Sprite):	
        GRAVITY = 0.5	
        def __init__(self, pos, coef, *groups):	
            self.flag_to_diff = 'player'
            super().__init__(*groups)	
            self.image = pygame.transform.scale(load_image('bullet.png', color_key=-2), (10, 10))	
            self.rect = self.image.get_rect().move(pos[0], pos[1])	
            self.mask = pygame.mask.from_surface(self.image)	
            self.x_velocity = 10 * coef
            self.damage = 1

        def update(self, player, platform_group, width):	
            self.rect.move_ip(self.x_velocity, Maslina_for_player.GRAVITY)		
            if pygame.sprite.collide_mask(self, player):	
                player.kill()		
            if pygame.sprite.spritecollideany(self,
                                              platform_group,
                                              collided=pygame.sprite.collide_mask) \
               or self.rect.x <= 0 or self.rect.x + self.rect.w >= width:	
                    super().kill()
            