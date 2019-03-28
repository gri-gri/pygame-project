from other_sprites import TILE_HEIGHT, TILE_WIDTH
import pygame
from helping_functions import load_image
from other_sprites import Bullet
from pygame_project_1 import SCREEN_WIDTH, SCREEN_HEIGHT

PLAYER_IMAGE_FILENAME = 'player.png'
PLAYER_MOVEMENT_SPEED = 1 / 6
JUMP_POWER = 10
GRAVITY = 0.3
climbing_speed = 5
pygame.init()
pygame.display.set_mode((1, 1))
running_left_image = load_image(PLAYER_IMAGE_FILENAME, color_key=-1)
running_right_image = pygame.transform.flip(running_left_image, True, False)
pygame.quit()

class Player(pygame.sprite.Sprite):
    running_left_image = running_left_image
    running_right_image = running_right_image

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = Player.running_right_image
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos[0], TILE_HEIGHT * pos[1])
        self.mask = pygame.mask.from_surface(self.image)
        self.x_velocity = 0
        self.y_velocity = 0
        self.falling_speed = GRAVITY
        self.onGround = False
        self.stair_coll = False
        self.jump_sec = 0
        self.stay_not_alive = 0
        self.tr_r, self.tr_l, self.tr_up, self.tr_down = 0, 0, 0, 0

    def update(self, left, right, up, player_group, group_of_platforms, bullet_group,
               enemies_group_cont, checkpoint, check_group):
        print(self.rect)
        if self.stay_not_alive > 30:
            print(checkpoint.rect)
            self.stay_not_alive -= 1
            self.x_velocity = 0
            self.y_velocity = 0
            return checkpoint
        if self.stay_not_alive > 1:
            super().kill() 
            self.move(checkpoint)
            self.stay_not_alive -= 1
            return checkpoint
        elif self.stay_not_alive == 1:
            super().add(self.groups)
            self.x_velocity = 0
            self.y_velocity = 0
            self.stay_not_alive -= 1
            return checkpoint
        if left:
            if not self.onGround:
                if self.x_velocity < 6:
                    self.x_velocity += PLAYER_MOVEMENT_SPEED
            else:
                if self.x_velocity < 10:
                    self.x_velocity += PLAYER_MOVEMENT_SPEED 
        if right:
            if not self.onGround:
                if self.x_velocity > -6:
                    self.x_velocity -= PLAYER_MOVEMENT_SPEED              
            else:
                if self.x_velocity > -10:
                    self.x_velocity -= PLAYER_MOVEMENT_SPEED
                    
        if not (left or right):
            self.x_velocity = 0
        self.rect.x += self.x_velocity
        self.collide(self.x_velocity, 0, group_of_platforms)
        if self.collide_enemies(enemies_group_cont):
            self.stay_not_alive = 40
        checkpoint = self.collide_checkpoint(check_group, checkpoint)

        if up:
            if self.onGround:
                self.y_velocity -= JUMP_POWER
                self.jump_sec = 0
                 
        if not self.onGround:
            self.jump_sec += 1
            self.y_velocity += self.falling_speed
            self.falling_speed = GRAVITY * self.jump_sec / 6           
            
        self.onGround = False
        self.rect.y += self.y_velocity
        
        self.collide(0, self.y_velocity, group_of_platforms)
        if self.x_velocity > 0:
            self.image = Player.running_right_image
        elif self.x_velocity < 0:
            self.image = Player.running_left_image
        return checkpoint

    def collide(self, x_velocity, y_velocity, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if x_velocity > 0:
                    self.rect.right = p.rect.left              
                if x_velocity < 0:
                    self.rect.left = p.rect.right   
                if y_velocity > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.y_velocity = 0
                if y_velocity < 0:
                    self.rect.top = p.rect.bottom
                    self.y_velocity = 0          

    def collide_enemies(self, enemies_group_cont):
        for enemies in enemies_group_cont:
            if pygame.sprite.spritecollideany(self, enemies,
                                              collided=pygame.sprite.collide_mask):
                return True
        return False
    
    def collide_checkpoint(self, check_group, checkpoint):
        for save in check_group:
            if pygame.sprite.collide_rect(self, save) and save.name != 'checked':
                save.collided()
                checkpoint = save
        return checkpoint

    def groups(self):
        return super().groups()

    def shoot(self, bullet_group, all_sprites):
        if self.image == Player.running_right_image:
            blt = Bullet(self.rect.midright, 1, bullet_group)
            all_sprites.add(blt, layer=3)
        else:
            blt = Bullet(self.rect.midleft, -1, bullet_group)
            all_sprites.add(blt, layer=3)

    def move(self, spawnpoint):
        self.rect.center = spawnpoint.rect.center
        print('moved player rect {}'.format(self.rect))
        # self.rect.topleft = (self.rect.topleft[0] % SCREEN_WIDTH, 
        #               self.rect.topleft[1] % SCREEN_HEIGHT) 
