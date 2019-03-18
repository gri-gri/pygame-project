from other_sprites import Tile
import pygame

PLAYER_IMAGE_FILENAME = 'player.png'
PLAYER_MOVEMENT_SPEED = 1 / 6
JUMP_POWER = 10
GRAVITY = 0.3
climbing_speed = 5


class Player(Tile):
    def __init__(self, pos, *groups):
        super().__init__(pos, PLAYER_IMAGE_FILENAME, -2, *groups)
        self.x_velocity = 0
        self.y_velocity = 0
        self.falling_speed = GRAVITY
        self.onGround = False
        self.hor_collision = False
        self.jump_sec = 0

    def update(self, left, right, up, down, hold, group_of_platforms):
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
        
        '''if hold:
            self.y_velocity = 0'''
            
        if up:
            #if not hold:
            if self.onGround:
                self.y_velocity -= JUMP_POWER
                self.jump_sec = 0
            '''else:
                self.y_velocity = -climbing_speed'''
                 
        if not self.onGround:
            self.jump_sec += 1
            self.y_velocity += self.falling_speed
            self.falling_speed = GRAVITY * self.jump_sec / 6
        
        '''if down and hold:
            self.y_velocity = climbing_speed'''      
            
        self.onGround = False
        self.rect.y += self.y_velocity
        self.collide(0, self.y_velocity, group_of_platforms)

    def collide(self, x_velocity, y_velocity, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if x_velocity > 0:
                    self.rect.right = p.rect.left
                    self.hor_collision = True
                if x_velocity < 0:
                    self.rect.left = p.rect.right
                    self.hor_collision = True
                if y_velocity > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.y_velocity = 0
                if y_velocity < 0:
                    self.rect.top = p.rect.bottom
                    self.y_velocity = 0
            else:
                self.hor_collision = False
