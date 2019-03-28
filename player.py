from other_sprites import TILE_HEIGHT, TILE_WIDTH
import pygame
from helping_functions import load_image
from other_sprites import Bullet_for_enemy
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
        self.spawnpoint = pos
        self.tr_r, self.tr_l, self.tr_up, self.tr_down = 0, 0, 0, 0

    def update(self, left, right, up, group_of_platforms, bullet_group,
               enemies_group_cont, spawnpoint, check_group, camera):
        if self.stay_not_alive > 30:
            self.stay_not_alive -= 1
            return None
        if self.stay_not_alive > 1:
            super().kill() 
            self.x_velocity = 0
            self.y_velocity = 0
            self.move(self.spawnpoint, camera.update_group, camera)
            self.stay_not_alive -= 1
            return None
        elif self.stay_not_alive == 1:
            super().add(self.groups)
            self.stay_not_alive -= 1
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
            self.kill()
        self.collide_checkpoint(check_group)

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
    
    def kill(self):
        self.stay_not_alive = 40

    def collide_enemies(self, enemies_group_cont):
        for enemies in enemies_group_cont:
            if pygame.sprite.spritecollideany(self, enemies,
                                              collided=pygame.sprite.collide_mask):
                return True
        return False
    
    def collide_checkpoint(self, check_group):
        for save in check_group:
            if pygame.sprite.collide_rect(self, save) and save.name != 'checked':
                save.collided(True)
                self.spawnpoint = (int(save.pos[0]), int(save.pos[1]))
                print(self.spawnpoint)

    def groups(self):
        return super().groups()

    def shoot(self, bullet_group, all_sprites):
        if self.image == Player.running_right_image:
            blt = Bullet_for_enemy(self.rect.midright, 1, bullet_group)
            all_sprites.add(blt, layer=2)
        else:
            blt = Bullet_for_enemy(self.rect.midleft, -1, bullet_group)
            all_sprites.add(blt, layer=2)

    def move(self, pos, update_groups, camera):
        print(self.tr_r, self.tr_l, self.tr_up, self.tr_down)
        
        self.rect.topleft = (TILE_WIDTH*pos[0], TILE_HEIGHT*pos[1])
        if self.rect.topleft[0] > SCREEN_WIDTH:
            for i in range(self.rect.topleft[0] // SCREEN_WIDTH):
                for i in update_groups:
                    for obj in i:
                        camera.special_apply(obj, True, False, False, False)
        if self.rect.topleft[1] > SCREEN_HEIGHT:
            for i in range(self.rect.topleft[1] // SCREEN_HEIGHT):
                for i in groups_to_update_with_camera:
                    for obj in i:
                        camera.special_apply(obj, False, False, True, False)
        self.rect.topleft = (self.rect.topleft[0] % SCREEN_WIDTH, 
                             self.rect.topleft[1] % SCREEN_HEIGHT)
        
        for i in range(self.tr_r):
            for i in update_groups:
                for obj in i:
                    camera.special_apply(obj, False, True, False, False)  
        for i in range(self.tr_l):
            for i in update_groups:
                for obj in i:
                    camera.special_apply(obj, True, False, False, False)
        for i in range(self.tr_up):
            for i in update_groups:
                for obj in i:
                    camera.special_apply(obj, False, False, False, True)
        for i in range(self.tr_down):
            for i in update_groups:
                for obj in i:
                    camera.special_apply(obj, False, False, True, False)        
        self.tr_r, self.tr_l, self.tr_up, self.tr_down = 0, 0, 0, 0